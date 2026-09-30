"""The service layer: one calibrated twin per well + records + models, all cached by scenario."""

from __future__ import annotations

import dataclasses
import json
import math
import threading
from datetime import date
from typing import Any

import numpy as np

from mantle_data.synth.s2_cycles import twin_day
from mantle_ml import registry as mlreg
from mantle_ml.models import m2_forecast as m2mod
from mantle_ml.models import m4_risk as m4mod
from mantle_ml.models import m5_stroke as m5mod
from mantle_physics import WellContext, WellSim, derive
from mantle_physics.constants import (
    CYCLE_DAYS,
    INJ_END,
    SOAK_END,
    SPM_MAX,
    SPM_MIN,
    TORQUE_RATING_INLB,
)
from mantle_physics.economics import co2_per_bbl, net_per_day, sor
from mantle_physics.hazard import N_RODS, ROD_LENGTH_M
from mantle_physics.twin import Metrics

from .settings import Settings
from .store import (
    Store,
    WellData,
    days_since_workover,
    maint_per_day,
    rod_sections,
    taper_at,
)
from .util import LRU, clean

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
UI_CLASS = {"rod_float": "ROD FLOAT RISK"}


def ui_class(c: str) -> str:
    return UI_CLASS.get(c, c.upper().replace("_", " "))


def fmt_date(d: date) -> str:
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def snake_plan_levers(d: dict) -> dict:
    return {("p_inj" if k == "pInj" else k): v for k, v in d.items()}


class Engine:
    def __init__(self, settings: Settings, store: Store, reg: mlreg.Registry):
        self.s, self.store, self.reg = settings, store, reg
        self.lock = threading.RLock()                      # the physics twin keeps per-instance scratch state
        self.cache = LRU(settings.cache_size)
        self._sims: dict[tuple, WellSim] = {}
        self._applied: dict[str, dict] = {}                # settings applied through POST /apply (per well)
        self.live_sessions: dict[str, set] = {}

    # ------------------------------------------------------------------ defaults and keys
    def defaults(self, wd: WellData) -> dict[str, float]:
        c = wd.current
        return {"day": float(wd.current_day), "spm": float(c["spm"]), "kd": float(c["kd"]), "steam": float(c["steam_t"])}

    @staticmethod
    def eff_steam(row: dict, steam: float) -> float:
        return float(np.clip(round(steam * float(row["steam_eff"])), 300, 1400))

    def _sim(self, row: dict, spm: float, kd: float, steam: float) -> WellSim:
        key = (round(spm, 3), round(kd, 3), int(self.eff_steam(row, steam)))
        if key not in self._sims:
            if len(self._sims) > 48:
                self._sims.pop(next(iter(self._sims)))
            self._sims[key] = WellSim(spm=spm, cycle_day=41, kd=kd, steam=key[2])
        return self._sims[key]

    def well_dict(self, wd: WellData) -> dict:
        return dict(wd.row)

    # ------------------------------------------------------------------ calibrated twin metrics
    def metrics(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> tuple[Metrics, Any]:
        row = wd.row
        with self.lock:
            sim = self._sim(row, spm, kd, steam)
            sim.set(cycle_day=day, spm=spm, kd=kd)
            m = dataclasses.replace(sim.metrics())
            m.recommendation = sim.metrics().recommendation
            state = dataclasses.replace(sim.state)
        k, v = float(row["pi_factor"]), float(row["visc_factor"])
        prod = m.phase == "PRODUCTION"
        if not (k == 1.0 and v == 1.0 and float(row["steam_eff"]) == 1.0
                and float(row["gearbox_rating_inlb"]) == TORQUE_RATING_INLB):
            m.oil_rate *= k
            m.liquid_rate *= k
            m.cum_oil *= k
            m.viscosity *= v
            if prod:
                m.fillage = min(0.98, m.fillage * k ** 0.6)
                m.pump_eff = float(np.clip(m.liquid_rate / max(m.pump_displacement, 1e-6), 0, 1))
                m.torque_pct *= TORQUE_RATING_INLB / float(row["gearbox_rating_inlb"])
            steam_rate = steam / INJ_END
            m.steam_tons = steam_rate * day if m.phase == "INJECTION" else steam
            m.sor = sor(steam, m.cum_oil) if prod else 0.0
            kwh = m.motor_kw * 24 if prod else 0.0
            m.kwh_per_bbl = kwh / max(m.oil_rate, 0.5) if prod else 0.0
            m.co2_per_bbl = co2_per_bbl(steam, m.cum_oil, m.kwh_per_bbl) if prod else 0.0
            m.net_per_day = net_per_day(m.phase, steam, m.oil_rate, kwh)
        return m, state

    # ------------------------------------------------------------------ models on the scenario
    def recommend(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> dict:
        def run() -> dict:
            r = self.reg.recommend_pump(steam, day, spm, kd, well=self.well_dict(wd))
            keep = ("title", "detail", "spm", "kd", "hz", "stroke", "deltas", "confidence", "feasible", "model", "version",
                    "trained_on", "source")
            return {k: r[k] for k in keep if k in r}
        return self.cache.get_or(("rec", wd.well_id, round(day, 2), round(spm, 3), round(kd, 3), int(steam)), run)

    def impacts(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> dict:
        """M5 on one stroke of the twin at these settings: fillage, impacts/day, impact velocity, impact point."""
        def run() -> dict:
            if day < SOAK_END:
                return {"impacts_day": 0.0, "impact_vel": 0.0, "fillage": 0.0, "impact": None, "pos": None, "load": None}
            es = self.eff_steam(wd.row, steam)
            with self.lock:
                st = m5mod.simulate_stroke(es, min(max(day, 19), 120), spm, kd)
            est = self.reg.estimate_stroke(st["pos"], st["load"], spm)
            k = float(wd.row["pi_factor"])
            if k != 1.0:      # per-well productivity changes fillage; apply the M5 impact laws to the scaled fillage
                fill = min(0.98, est["fillage"] * k ** 0.6)
                est = {**est, "fillage": fill, "impacts_day": float(m5mod.impacts_per_day(spm, fill)),
                       "impact_vel": float(m5mod.impact_velocity(spm, fill))}
            return {"impacts_day": est["impacts_day"], "impact_vel": est["impact_vel"], "fillage": est["fillage"],
                    "impact": est["impact"], "pos": st["pos"], "load": st["load"]}
        return self.cache.get_or(("imp", wd.well_id, round(day, 1), round(spm, 3), round(kd, 3), int(steam)), run)

    def risk(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> dict:
        def run() -> dict:
            on = wd.scenario_date(day)
            dip = max(day - SOAK_END, 0.5)
            return self.reg.assess_risk(self.well_dict(wd), steam, spm, kd, dip, wd.cycle_no, days_since_workover(wd, on))
        return self.cache.get_or(("risk", wd.well_id, round(day, 1), round(spm, 3), round(kd, 3), int(steam)), run)

    # ------------------------------------------------------------------ /state
    def context(self, wd: WellData, day: float) -> WellContext:
        s, row = self.s, wd.row
        done = wd.cycles[wd.cycles["complete"]]
        ooip = 7758.0 * s.drainage_area_acres * (float(row["net_pay_m"]) / 0.3048) * float(row["porosity"]) \
            * float(row["oil_saturation"]) / s.bo
        return WellContext(
            p_res_mpa=float(row["p_res_mpa"]), hold_down_kn=float(row["hold_down_kn"]),
            steam_inr_per_t=s.steam_inr_t, power_inr_per_kwh=s.power_inr_kwh, oil_inr_per_bbl=s.oil_inr_bbl,
            maint_inr_per_day=maint_per_day(wd, wd.scenario_date(day), s.maint_window_days),
            chem_inr_per_day=s.chem_inr_day, past_cum_oil_bbl=float(done["cum_oil_bbl"].sum()), ooip_bbl=ooip)

    def state(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> dict:
        def run() -> dict:
            m, st = self.metrics(wd, day, spm, kd, steam)
            rec = self.recommend(wd, day, spm, kd, steam)
            d = derive(m, st, self.context(wd, day))
            imp = self.impacts(wd, day, spm, kd, steam)
            impm = self.impacts(wd, day, rec["spm"], rec["kd"], steam)
            rk = self.risk(wd, day, spm, kd, steam)
            d["impactsDay"], d["impactVel"], d["impactsMantle"] = imp["impacts_day"], imp["impact_vel"], impm["impacts_day"]
            d["unseatRisk"] = rk["risk_30d_unseat"]
            return {
                "params": {"day": day, "spm": spm, "kd": kd, "steam": int(steam)},
                "metrics": m.to_json(), "recommendation": rec, "derived": d, "source": "physics_synthetic",
            }
        return self.cache.get_or(("state", wd.well_id, round(day, 2), round(spm, 3), round(kd, 3), int(steam)),
                                 lambda: clean(run()))

    # ------------------------------------------------------------------ /series
    def _scale(self, wd: WellData) -> float:
        """Per-well Bayesian scaling of M2 from (predicted, recorded) cumulative oil of the completed cycles."""
        def run() -> float:
            hist = []
            for c in self.store.past_cycles(wd.well_id):
                f = self.reg.predict_cycle(self.well_dict(wd), c["steam_t"], c["soak_days"], c["spm"], c["kd"],
                                           int(c["cutoff_day"]), cycle_no=int(c["cycle_no"]))
                hist.append((f["cum_oil"], float(c["cum_oil_bbl"])))
            return m2mod.well_scale(hist)
        return self.cache.get_or(("scale", wd.well_id), run)

    def series(self, wd: WellData, spm: float, kd: float, steam: float) -> dict:
        def run() -> dict:
            row = wd.row
            with self.lock:
                sim = self._sim(row, spm, kd, steam)
                sim.set(spm=spm, kd=kd)
                ser = sim.series().to_json()
            k, v = float(row["pi_factor"]), float(row["visc_factor"])
            cyc = wd.current
            f = self.reg.predict_cycle(self.well_dict(wd), steam, 4.0, spm, kd, CYCLE_DAYS,
                                       cycle_no=int(cyc["cycle_no"]), scale=self._scale(wd))
            hi = np.ones(CYCLE_DAYS + 1)
            lo = np.ones(CYCLE_DAYS + 1)
            idx = (f["day"] - SOAK_END).astype(int)
            ok = f["oil"] > 1e-9
            hi[idx[ok]] = f["oil_p90"][ok] / f["oil"][ok]          # oilfield convention: P10 = high case, P90 = low case
            lo[idx[ok]] = f["oil_p10"][ok] / f["oil"][ok]
            oil = np.array(ser["oil"]) * k
            ser["oil"] = oil.tolist()
            ser["oilP10"] = (oil * hi).tolist()
            ser["oilP90"] = (oil * lo).tolist()
            ser["mu"] = (np.array(ser["mu"]) * v).tolist()
            ser["past_cycles"] = self.past_cycle_curves(wd)
            ser["plan_curve"] = self.plan_curve(wd)
            ser.update(model="M2", version=f.get("version"), source="physics_synthetic", trained_on=f.get("trained_on"))
            return ser
        return self.cache.get_or(("series", wd.well_id, round(spm, 3), round(kd, 3), int(steam)), lambda: clean(run()))

    def past_cycle_curves(self, wd: WellData) -> list[dict]:
        ax = np.arange(CYCLE_DAYS + 1, dtype=float)
        out = []
        for c in self.store.past_cycles(wd.well_id):
            td = twin_day(c["day"], float(c["soak_days"]))
            oil = np.interp(ax, td, c["oil"], left=np.nan, right=np.nan)
            out.append({"n": int(c["cycle_no"]), "oil": oil.tolist(), "cum_oil": float(c["cum_oil_bbl"]),
                        "steam_t": float(c["steam_t"])})
        return out

    # ------------------------------------------------------------------ /plan
    def _plan_raw(self, wd: WellData) -> dict:
        def run() -> dict:
            return self.reg.plan_next_cycle(self.well_dict(wd), wd.cycle_no + 1, budget_s=2.0)
        return self.cache.get_or(("plan", wd.well_id), run)

    def plan(self, wd: WellData) -> dict:
        def run() -> dict:
            p = self._plan_raw(wd)
            rate = self.s.steam_rate_t_per_d

            def lv(d: dict) -> dict:
                o = snake_plan_levers(d)
                o["inj_days"] = round(float(d["steam"]) / rate, 2)
                return o
            return {
                "well_id": wd.well_id, "cycle": wd.cycle_no + 1, "practice": lv(p["practice"]), "mantle": lv(p["mantle"]),
                "ranges": snake_plan_levers(p["ranges"]), "pump": p["pump"], "oil_lift": p["oil_lift"], "sor": p["sor"],
                "inr_per_cycle": p["inr_per_cycle"], "joint_share": p["joint_share"], "p10_p90": p["p10_p90"],
                "steam_rate_t_per_d": rate, "model": "O2", "version": p.get("version"), "trained_on": p.get("trained_on"),
                "source": p.get("source", "physics_synthetic"),
            }
        return self.cache.get_or(("plan_ui", wd.well_id), lambda: clean(run()))

    def plan_curve(self, wd: WellData) -> dict | None:
        def run() -> dict:
            p = self._plan_raw(wd)
            mt, pump = p["mantle"], p["pump"]
            cut_actual = int(round(mt["cutoff"] + mt["soak"] - 4))
            f = self.reg.predict_cycle(self.well_dict(wd), mt["steam"], mt["soak"], pump["spm"], pump["kd"], cut_actual,
                                       cycle_no=wd.cycle_no + 1, p_inj=mt["pInj"], scale=self._scale(wd))
            return {"day": f["day"], "oil": f["oil"], "oil_p10": f["oil_p90"], "oil_p90": f["oil_p10"],
                    "cutoff": mt["cutoff"], "inj_days": mt["steam"] / self.s.steam_rate_t_per_d,
                    "model": "O2+M2"}
        return clean(self.cache.get_or(("plan_curve", wd.well_id), run))

    # ------------------------------------------------------------------ /profile /dyno
    def profile(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> dict:
        def run() -> dict:
            with self.lock:
                sim = self._sim(wd.row, spm, kd, steam)
                sim.set(cycle_day=day, spm=spm, kd=kd)
                pr = sim.profile().to_json()
            pr["mu"] = (np.array(pr["mu"]) * float(wd.row["visc_factor"])).tolist()
            pr["source"] = "physics_synthetic"
            return pr
        return self.cache.get_or(("profile", wd.well_id, round(day, 2), round(spm, 3), round(kd, 3), int(steam)),
                                 lambda: clean(run()))

    def dyno(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> dict:
        def run() -> dict:
            with self.lock:
                sim = self._sim(wd.row, spm, kd, steam)
                sim.set(cycle_day=day, spm=spm, kd=kd)
                card = sim.dyno_card(128)
            j = card.to_json()
            pos = np.array([p[0] for p in card.surface])
            load = np.array([p[1] for p in card.surface]) * 1000.0
            r = self.reg.classify_card(pos, load, spm)
            j["cls"], j["clsConf"] = ui_class(r["cls"]), r["conf"]
            j["cls_id"] = r["cls"]
            j["class_probs"] = r["probs"]
            imp = self.impacts(wd, day, spm, kd, steam)
            j["impact"] = None
            if imp["impact"] is not None and imp["impact"]["severity"] > 0.05 and imp["fillage"] < 0.85:
                i = imp["impact"]["index"]
                j["impact"] = {"x": float(imp["pos"][i]), "f": float(imp["load"][i]) / 1000.0,
                               "severity": imp["impact"]["severity"], "drop_kn": imp["impact"]["drop_kn"]}
            j.update(model="M3", version=r["version"], trained_on=r["trained_on"], source=r["source"])
            return j
        return self.cache.get_or(("dyno", wd.well_id, round(day, 2), round(spm, 3), round(kd, 3), int(steam)),
                                 lambda: clean(run()))

    # ------------------------------------------------------------------ /health (rod & pump)
    def health(self, wd: WellData, day: float, spm: float, kd: float, steam: float) -> dict:
        def run() -> dict:
            s, row = self.s, wd.row
            on = wd.scenario_date(day)
            secs = rod_sections(row)
            dip = max(day - SOAK_END, 0.5)
            rec = self.recommend(wd, day, spm, kd, steam)
            rk = self.risk(wd, day, spm, kd, steam)
            rkm = self.risk(wd, day, rec["spm"], rec["kd"], steam)
            dsw = days_since_workover(wd, on)
            cov = m4mod.cov_from_settings(self.well_dict(wd), steam, spm, kd, wd.cycle_no, dsw)
            with self.lock:
                fat = m4mod.rod_fatigue(cov, dip, steam=self.eff_steam(row, steam), day_twin=min(max(day, 19), 120))
            # recorded rod parts in the window ending at the scenario date
            f = wd.failures
            f = f[f["kind"] == "rod_part"] if not f.empty else f
            fails = []
            if not f.empty:
                dates = f["date"].map(lambda v: v.date() if hasattr(v, "date") else v)
                lo = _months_back(on, s.failure_window_months)
                for r, dt in zip(f.to_dict("records"), dates, strict=True):
                    if lo < dt <= on:
                        depth = float(r["depth_m"])
                        mode = str(r["mode"])
                        g = r.get("goodman")
                        cause = ("rod float: compressive buckling on the downstroke" if mode == "float-buckling"
                                 else "fatigue" + (f" at Goodman ratio {float(g):.2f}" if g == g and g is not None else ""))
                        fails.append({"rod": int(r["rod_index"]), "depth": round(depth), "size": taper_at(secs, depth),
                                      "mode": mode, "date": fmt_date(dt), "cause": cause, "cycle": int(r["cycle_no"])
                                      if r["cycle_no"] == r["cycle_no"] else None})
            failed = {x["rod"] for x in fails}
            rods = [{"index": i, "depth_m": round((i + 0.5) * ROD_LENGTH_M, 2), "taper": taper_at(secs, (i + 0.5) * ROD_LENGTH_M),
                     "fatigue": float(max(fat["goodman"][i], 0.0)), "failed": i in failed} for i in range(N_RODS)]
            # pump unseats, last 12 months
            end = on
            y, mo = end.year, end.month
            idx = [(y * 12 + mo - 1) - 11 + i for i in range(12)]
            months = [MONTHS[i % 12] for i in idx]
            events, details = [], []
            u = wd.unseats
            if not u.empty:
                wo = wd.workovers[wd.workovers["trigger"] == "pump_unseat"]
                jobs = dict(zip(wo["trigger_id"].astype(int), wo["job_type"], strict=True))
                lo = _months_back(on, s.unseat_window_months)
                for r in u.to_dict("records"):
                    dt = r["date"].date() if hasattr(r["date"], "date") else r["date"]
                    if lo < dt <= on:
                        mi = (dt.year * 12 + dt.month - 1) - idx[0]
                        events.append(mi)
                        act = str(jobs.get(int(r["unseat_id"]), "pump reseat"))
                        details.append({"month": MONTHS[dt.month - 1], "date": fmt_date(dt), "action": act,
                                        "downtime_h": round(float(r["downtime_h"]), 1)})
            imp = self.impacts(wd, day, spm, kd, steam)
            impm = self.impacts(wd, day, rec["spm"], rec["kd"], steam)
            ctx = self.context(wd, day)
            m, st = self.metrics(wd, day, spm, kd, steam)
            d = derive(m, st, ctx)
            return {
                "rods": rods, "failure_window_months": s.failure_window_months, "failures": fails,
                "unseats": {"months": months, "events": events, "hold_down_kn": float(row["hold_down_kn"]), "details": details},
                "mtbf_days": rk["mtbf_days"], "mtbf_mantle_days": rkm["mtbf_days"], "uplift_margin": d["upliftMargin"],
                "unseat_risk_30d": rk["risk_30d_unseat"], "rod_risk_30d": rk["risk_30d_rod"],
                "impacts_day": imp["impacts_day"], "impacts_mantle": impm["impacts_day"], "impact_vel": imp["impact_vel"],
                "top_rods": rk["top_rods"], "model": "M4", "version": rk.get("version"), "trained_on": rk.get("trained_on"),
                "source": "physics_synthetic",
            }
        return self.cache.get_or(("health", wd.well_id, round(day, 2), round(spm, 3), round(kd, 3), int(steam)),
                                 lambda: clean(run()))

    # ------------------------------------------------------------------ /wells
    def well_detail(self, wd: WellData) -> dict:
        def run() -> dict:
            row, s = wd.row, self.s
            mu = self.reg.predict_viscosity(float(row["t_res_c"]), float(row["api"]), float(row["asphaltene_wt_pct"]),
                                            walther_ab=(float(row["walther_A"]), float(row["walther_B"])))
            secs = rod_sections(row)
            return {
                "id": wd.well_id, "name": row["name"], "field": s.field_name, "reservoir": s.reservoir,
                "spud_date": str(row["spud_date"])[:10], "is_showcase": bool(row["is_showcase"]),
                "fluid": {"api": float(row["api"]), "asphaltene": float(row["asphaltene_wt_pct"]), "t_res": float(row["t_res_c"]),
                          "p_res": float(row["p_res_mpa"]), "dead_oil_cp": round(mu["mu_cp"], -2), "model": "M0"},
                "completion": {"depth_m": row["depth_m"], "perf_top_m": row["perf_top_m"], "perf_bot_m": row["perf_bot_m"],
                               "casing_od_in": row["casing_od_in"], "tubing_od_in": row["tubing_od_in"],
                               "pump_depth_m": row["pump_depth_m"], "plunger_in": row["pump_bore_in"],
                               "rod_taper": row["rod_taper"]},
                "unit": {"model": row["unit_class"], "gearbox_rating_inlb": row["gearbox_rating_inlb"],
                         "stroke_m": row["stroke_m"], "vfd_kw": row["vfd_kw"]},
                "rods": {"count": N_RODS, "length_m": ROD_LENGTH_M, "tapers": secs},
                "reservoir_props": {"net_pay_m": row["net_pay_m"], "porosity": row["porosity"], "perm_md": row["perm_md"],
                                    "oil_saturation": row["oil_saturation"]},
                "hold_down_kn": row["hold_down_kn"], "source": row["source"],
            }
        return clean(self.cache.get_or(("well", wd.well_id), run))

    def roster(self) -> list[dict]:
        out = []
        for wid in self.store.roster()["well_id"]:
            try:
                wd = self.store.well(wid)
            except KeyError:
                continue
            c = wd.current
            day = wd.current_day
            phase = "INJECTION" if day < INJ_END else "SOAK" if day < INJ_END + float(c["soak_days"]) else "PRODUCTION"
            out.append({"id": wid, "name": wd.row["name"], "cycle": wd.cycle_no, "cycle_day": day, "phase": phase,
                        "steam": float(c["steam_t"]), "spm": float(c["spm"]), "kd": float(c["kd"]),
                        "is_showcase": bool(wd.row["is_showcase"]), "source": wd.row["source"]})
        return out

    # ------------------------------------------------------------------ actions
    def apply(self, wd: WellData, spm: float, kd: float) -> dict:
        spm = float(np.clip(spm, SPM_MIN, SPM_MAX))
        kd = float(np.clip(kd, 0.4, 0.7))
        self._applied[wd.well_id] = {"spm": spm, "kd": kd}
        a = self.store.audit(wd.well_id, "apply_recommendation", {"spm": spm, "kd": kd})
        for sess in list(self.live_sessions.get(wd.well_id, ())):
            sess.retarget(spm=spm, kd=kd)
        return {"applied": True, "spm": spm, "kd": kd, **a}

    def schedule(self, wd: WellData, plan: dict) -> dict:
        a = self.store.audit(wd.well_id, "schedule_plan", {**plan, "cycle": wd.cycle_no + 1})
        return {"scheduled": True, "cycle": wd.cycle_no + 1, **a}

    def live_defaults(self, wd: WellData) -> dict:
        d = self.defaults(wd)
        d.update(self._applied.get(wd.well_id, {}))
        return d


def _months_back(d: date, months: int) -> date:
    y, m = divmod(d.year * 12 + d.month - 1 - months, 12)
    day = min(d.day, [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m])
    return date(y, m + 1, day)


_ = (json, math)
