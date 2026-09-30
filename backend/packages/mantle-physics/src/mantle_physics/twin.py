"""The ``WellSim`` digital twin: a faithful port of the browser simulator in ``app/js/sim.js``."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ._util import TAU, JsonMixin, clamp, fin, js_mod, smooth
from .constants import (
    CYCLE,
    CYCLE_DAYS,
    INJ_END,
    KVIS,
    MARGIN_REQ,
    MU_CAP_CP,
    PUMP_DEPTH,
    S_M,
    SOAK_END,
    SPM_MAX,
    SPM_MIN,
)
from .economics import (
    CycleCurves,
    coupling_dividend,
    cycle,
    days_to_cutoff,
    net_per_day,
    sor,
)
from .economics import co2_per_bbl as _co2_per_bbl
from .pump import Core, LoadModel, core, downhole_point, load_model, surface_point
from .reservoir import ProdBase, deposition, prod_base, t_fluid, t_geo
from .rig import rod_position
from .rods import KXP, SECT, TH_BOT, TH_TOP, KdTable, interp, kd_table, w_below
from .viscosity import viscosity_cp

__all__ = ["CYCLE", "WellSim", "viscosity_cp"]


@dataclass
class Alert(JsonMixin):
    level: str
    text: str


@dataclass
class Deltas(JsonMixin):
    oil: float
    float_margin: float
    energy: float

    _JSON_KEYS = {"float_margin": "float"}


@dataclass
class Recommendation(JsonMixin):
    title: str
    detail: str
    spm: float
    kd: float
    deltas: Deltas
    confidence: float


@dataclass
class CouplingDividend(JsonMixin):
    inr_per_cycle: float
    oil_pct: float


@dataclass
class Metrics(JsonMixin):
    phase: str
    cycle_day: float
    day_in_phase: float
    spm: float
    kd: float
    stroke: float
    sandface_t: float
    viscosity: float
    heated_radius: float
    thermal_battery: float
    days_to_cutoff: float
    oil_rate: float
    water_cut: float
    liquid_rate: float
    pump_displacement: float
    fillage: float
    pump_eff: float
    bottleneck: str
    pprl: float
    mprl: float
    float_margin: float
    spm_safe: float
    goodman: float
    torque_pct: float
    motor_kw: float
    kwh_per_bbl: float
    sor: float
    steam_tons: float
    cum_oil: float
    co2_per_bbl: float
    water_per_bbl: float
    net_per_day: float
    fluid_level: float
    submergence: float
    coupling_dividend: CouplingDividend
    recommendation: Recommendation
    alerts: list[Alert]


@dataclass
class State(JsonMixin):
    phase: str = "SOAK"
    theta: float = 0.0
    rod_pos: float = 0.0
    rod_vel: float = 0.0
    load: float = 0.0
    spm_actual: float = 0.0
    float_now: bool = False


@dataclass
class DynoCard(JsonMixin):
    surface: list[tuple[float, float]]
    downhole: list[tuple[float, float]]
    x_max: float
    f_min: float
    f_max: float
    cls: str
    cls_conf: float

    def to_json(self) -> dict:
        return {
            "surface": [{"x": x, "f": f} for x, f in self.surface],
            "downhole": [{"x": x, "f": f} for x, f in self.downhole],
            "xMax": self.x_max, "fMin": self.f_min, "fMax": self.f_max,
            "cls": self.cls, "clsConf": self.cls_conf,
        }


@dataclass
class Series(JsonMixin):
    day: list[float] = field(default_factory=list)
    T: list[float] = field(default_factory=list)
    mu: list[float] = field(default_factory=list)
    oil: list[float] = field(default_factory=list)
    oil_p10: list[float] = field(default_factory=list)
    oil_p90: list[float] = field(default_factory=list)
    spm_safe: list[float] = field(default_factory=list)
    float_margin: list[float] = field(default_factory=list)
    sor: list[float | None] = field(default_factory=list)


@dataclass
class Profile(JsonMixin):
    depth: list[float] = field(default_factory=list)
    t_fluid: list[float] = field(default_factory=list)
    t_formation: list[float] = field(default_factory=list)
    mu: list[float] = field(default_factory=list)
    pressure: list[float] = field(default_factory=list)
    rod_stress: list[float] = field(default_factory=list)
    deposition_top: float | None = None
    deposition_bot: float | None = None

    _JSON_KEYS = {"t_fluid": "Tfluid", "t_formation": "Tformation"}


class WellSim:
    """Cyclic-steam + rod-lift twin. API mirrors the JS class (snake_case)."""

    def __init__(self, spm: float = 5.4, cycle_day: float = 41, kd: float = 0.5, steam: float = 800):
        self._p = {
            "spm": clamp(fin(spm, 5.4), SPM_MIN, SPM_MAX),
            "day": clamp(fin(cycle_day, 41), 0, CYCLE_DAYS),
            "kd": clamp(fin(kd, 0.5), 0.4, 0.7),
            "steam": clamp(fin(steam, 800), 300, 1400),
        }
        prod = self._phase_of(self._p["day"]) == "PRODUCTION"
        self._theta = TH_BOT if prod else TH_TOP
        self._spm_act = self._p["spm"] if prod else 0.0
        self._cyc: CycleCurves | None = None
        self._cyc_key = ""
        self._m: Metrics | None = None
        self._dep: tuple[float | None, float | None] = (None, None)
        self._state = State(phase="SOAK", theta=self._theta)
        self._recompute()
        self._update_state(TAU * self._spm_act / 60 if self._spm_act > 0 else 0.0)

    @staticmethod
    def _phase_of(d: float) -> str:
        return "INJECTION" if d < INJ_END else "SOAK" if d < SOAK_END else "PRODUCTION"

    def set(self, spm: float | None = None, cycle_day: float | None = None,
            kd: float | None = None, steam: float | None = None) -> None:
        p = self._p
        if spm is not None:
            p["spm"] = clamp(fin(spm, p["spm"]), SPM_MIN, SPM_MAX)
        if cycle_day is not None:
            p["day"] = clamp(fin(cycle_day, p["day"]), 0, CYCLE_DAYS)
        if kd is not None:
            p["kd"] = clamp(fin(kd, p["kd"]), 0.4, 0.7)
        if steam is not None:
            p["steam"] = clamp(fin(steam, p["steam"]), 300, 1400)
        self._recompute()
        run = self._phase == "PRODUCTION"
        self._update_state(self._omega() if run else 0.0)

    def _omega(self) -> float:
        return TAU * self._spm_act / 60

    def _recompute(self) -> None:
        p = self._p
        self._phase = self._phase_of(p["day"])
        self._kt: KdTable = kd_table(p["kd"])
        self._b: ProdBase = prod_base(p["steam"], p["day"])
        self._c: Core = core(self._b, p["spm"], self._kt)
        self._lm: LoadModel = load_model(self._c, self._kt)
        self._m = None

    @property
    def theta(self) -> float:
        return self._theta

    @property
    def state(self) -> State:
        return self._state

    @property
    def params(self) -> dict[str, float]:
        return dict(self._p)

    def step(self, dt: float) -> None:
        dt = clamp(fin(dt, 0), 0, 0.25)
        run = self._phase == "PRODUCTION"
        kt = self._kt
        target = self._p["spm"] if run else 0.0
        self._spm_act += (target - self._spm_act) * (1 - math.exp(-dt / 0.7))
        omega = TAU * self._spm_act / 60
        if run:
            s = interp(kt.s, self._theta)
            self._theta = js_mod(self._theta + omega * s * dt, TAU)
        elif self._spm_act != 0 or abs(self._theta - TH_TOP) > 1e-9:
            # park with the horsehead at the top of stroke: creep forward, converging on TH_TOP
            d = js_mod(js_mod(TH_TOP - self._theta, TAU) + TAU, TAU)
            if d < 0.004 or d > TAU - 0.004:
                self._theta = TH_TOP
                self._spm_act = 0.0
                omega = 0.0
            else:
                omega = min(max(omega, 0.4), 2.5 * d + 0.02)
                self._theta = js_mod(self._theta + omega * dt, TAU)
                self._spm_act = omega * 60 / TAU
        self._update_state(omega)

    def _update_state(self, omega: float) -> None:
        st, kt, run = self._state, self._kt, self._phase == "PRODUCTION"
        st.phase = self._phase
        st.theta = self._theta
        st.rod_pos = clamp(rod_position(self._theta), 0, S_M)
        st.spm_actual = self._spm_act
        V = interp(kt.V, self._theta) if run else interp(KXP, self._theta)
        st.rod_vel = omega * V
        if omega > 1e-6 and (run or self._spm_act > 0):
            st.load = surface_point(self._lm, kt, self._theta, omega)[1]
            st.float_now = run and V < 0 and self._c.marginRaw < 0
        else:
            st.load = (self._c.Wrf + (self._c.Fo if run else 0)) / 1000
            st.float_now = False

    # ---- cycle-level values ----

    def _cycle(self) -> CycleCurves:
        p = self._p
        key = f"{p['spm']:.3f}|{p['kd']}|{math.floor(p['steam'] + 0.5)}"
        if self._cyc_key != key or self._cyc is None:
            self._cyc = cycle(p["steam"], p["spm"], p["kd"])
            self._cyc_key = key
        return self._cyc

    def metrics(self) -> Metrics:
        if self._m is not None:
            return self._m
        p, c, b, th, phase = self._p, self._c, self._b, self._b.th, self._phase
        cyc = self._cycle()
        prod = phase == "PRODUCTION"
        day = p["day"]
        i0 = min(CYCLE_DAYS - 1, math.floor(day))
        f = day - i0
        cum_oil = cyc.cum[i0] * (1 - f) + cyc.cum[i0 + 1] * f if prod else 0.0
        cum_water = cyc.cum_w[i0] * (1 - f) + cyc.cum_w[i0 + 1] * f if prod else 0.0
        steam_rate = p["steam"] / INJ_END
        steam_tons = steam_rate * day if phase == "INJECTION" else p["steam"]
        oil = c.oil if prod else 0.0
        liq = c.q if prod else 0.0
        sor_v = sor(p["steam"], cum_oil) if prod else 0.0
        kwh = c.motorKw * 24 if prod else 0.0
        kwh_bbl = kwh / max(oil, 0.5) if prod else 0.0
        co2 = _co2_per_bbl(p["steam"], cum_oil, kwh_bbl) if prod else 0.0
        water = max(0.0, p["steam"] - 0.85 * cum_water * 0.159) / max(cum_oil, 50) if prod else 0.0
        net = net_per_day(phase, p["steam"], oil, kwh)
        dcut = days_to_cutoff(cyc, p["steam"], day)

        dep = deposition(th.exc, b.Lr) if prod else (None, None)
        fillage = c.fill if prod else 0.0
        coupling = coupling_dividend(p["kd"])
        level = c.level
        submergence = max(0.0, PUMP_DEPTH - level)
        m = Metrics(
            phase=phase, cycle_day=day,
            day_in_phase=day if phase == "INJECTION" else day - INJ_END if phase == "SOAK" else day - SOAK_END,
            spm=p["spm"], kd=p["kd"], stroke=S_M,
            sandface_t=th.T, viscosity=b.muPump, heated_radius=th.rh, thermal_battery=th.battery,
            days_to_cutoff=dcut, oil_rate=oil, water_cut=c.wc if prod else 0.0, liquid_rate=liq,
            pump_displacement=c.PDg if prod else 0.0, fillage=fillage, pump_eff=c.pumpEff if prod else 0.0,
            bottleneck=c.bottleneck, pprl=c.pprl, mprl=c.mprl,
            float_margin=c.margin if prod else 1.0, spm_safe=c.spmSafe, goodman=c.goodman,
            torque_pct=c.torque if prod else 0.0, motor_kw=c.motorKw if prod else 0.0, kwh_per_bbl=kwh_bbl,
            sor=sor_v, steam_tons=steam_tons, cum_oil=cum_oil, co2_per_bbl=co2, water_per_bbl=water,
            net_per_day=net, fluid_level=level, submergence=submergence,
            coupling_dividend=CouplingDividend(coupling.inrPerCycle, coupling.oilPct),
            recommendation=Recommendation("", "", 0.0, 0.0, Deltas(0, 0, 0), 0.0),
            alerts=[],
        )
        m.recommendation = self._recommend(m, coupling, prod)
        m.alerts = self._alerts(m, dep, steam_rate, prod)
        self._m = m
        self._dep = dep
        return m

    def _recommend(self, m: Metrics, coupling, prod: bool) -> Recommendation:
        p, b = self._p, self._b

        def eval2(spm: float, kd: float) -> Core:
            return core(b, spm, kd_table(kd))

        def mk(title: str, detail: str, spm: float, kd: float, conf: float) -> Recommendation:
            c2, c0 = eval2(spm, kd), self._c
            e0 = c0.motorKw * 24 / max(c0.oil, 0.5)
            e1 = c2.motorKw * 24 / max(c2.oil, 0.5)
            return Recommendation(
                title, detail, spm, kd,
                Deltas(
                    oil=fin((c2.oil - c0.oil) / max(c0.oil, 0.5)),
                    float_margin=fin(c2.margin - c0.margin),
                    energy=fin((e1 - e0) / max(e0, 0.1)),
                ),
                conf,
            )

        if not prod:
            return Recommendation(
                "Hold: steaming" if m.phase == "INJECTION" else "Hold: soak",
                f"Pre-set production at {coupling.jointSpm:.1f} SPM (joint optimum with {_js_num(coupling.jointSteam)} t steam).",
                coupling.jointSpm, p["kd"], Deltas(0, 0, 0), 0.7,
            )
        if p["spm"] > 0.95 * m.spm_safe:
            spm2 = clamp(min(p["spm"], 0.9 * eval2(p["spm"], 0.62).spmSafe), 2, 9)
            return mk(
                "Slow down and shape the stroke",
                f"Rods are near float (margin {m.float_margin * 100:.0f}%). Run {spm2:.1f} SPM with kd 0.62 to restore margin.",
                spm2, 0.62, 0.84,
            )
        if m.fillage < 0.8:
            spm2 = clamp(p["spm"] * m.fillage / 0.92, 2, 9)
            return mk(
                "Match pump speed to inflow",
                f"Fillage {m.fillage * 100:.0f}%: the pump outruns the reservoir. Slow to {spm2:.1f} SPM to cut fluid pound and power.",
                spm2, p["kd"], 0.76,
            )
        return Recommendation("Hold settings", "Pump, rods and reservoir are balanced.", p["spm"], p["kd"], Deltas(0, 0, 0), 0.9)

    def _alerts(self, m: Metrics, dep, steam_rate: float, prod: bool) -> list[Alert]:
        a: list[Alert] = []
        if m.phase == "INJECTION":
            a.append(Alert("ok", f"Steam injection at {steam_rate:.0f} t/day; heated radius {m.heated_radius:.1f} m."))
        if m.phase == "SOAK":
            a.append(Alert("ok", f"Soak: heat equalising near the well ({m.sandface_t:.0f} C). Unit parked."))
        if prod:
            if m.float_margin < 0:
                a.append(Alert("crit", f"Rod float: margin {m.float_margin * 100:.0f}%. Rods lag on the downstroke; slow below {m.spm_safe:.1f} SPM."))
            elif m.float_margin < 0.2:
                a.append(Alert("warn", f"Float margin only {m.float_margin * 100:.0f}% (safe limit {m.spm_safe:.1f} SPM)."))
            if m.fillage < 0.7:
                a.append(Alert("warn", f"Pump fillage {m.fillage * 100:.0f}%: fluid pound risk."))
            if m.goodman > 1:
                a.append(Alert("crit", f"Goodman ratio {m.goodman:.2f}: rod fatigue limit exceeded."))
            elif m.goodman > 0.9:
                a.append(Alert("warn", f"Goodman ratio {m.goodman:.2f}: rods near fatigue limit."))
            if m.torque_pct > 1:
                a.append(Alert("crit", f"Gearbox torque {m.torque_pct * 100:.0f}% of rating."))
            if dep[1] is not None:
                a.append(Alert("warn", f"Asphaltene deposition band {dep[0]:.0f}-{dep[1]:.0f} m (fluid below 62 C)."))
            if m.days_to_cutoff <= 0:
                a.append(Alert("warn", "Past economic cut-off: plan the next steam cycle."))
        if not a or all(x.level == "ok" and prod for x in a):
            a.append(Alert("ok", "All operating limits nominal."))
        return a

    # ---- cards ----

    def dyno_card(self, n: int = 180) -> DynoCard:
        n = max(8, math.floor(n))
        c, kt, m, omega = self._c, self._kt, self._lm, TAU * self._p["spm"] / 60
        surface: list[tuple[float, float]] = []
        downhole: list[tuple[float, float]] = []
        f_min, f_max = math.inf, -math.inf
        for i in range(n):
            th = TH_BOT if i == n - 1 else TH_BOT + TAU * i / (n - 1)
            sx, sf, _up = surface_point(m, kt, th, omega)
            dx, df = downhole_point(m, kt, th)
            surface.append((sx, sf))
            downhole.append((dx, df))
            f_min = min(f_min, sf, df)
            f_max = max(f_max, sf, df)
        surface[n - 1] = surface[0]
        downhole[n - 1] = downhole[0]
        drag_frac = c.dDn / c.Wrf
        cls, conf = "NORMAL", clamp(0.6 + (c.margin - 0.4) * 0.5, 0.55, 0.95)
        if c.marginRaw < MARGIN_REQ:
            cls, conf = "ROD FLOAT RISK", clamp(0.65 + (MARGIN_REQ - c.marginRaw), 0.6, 0.98)
        elif c.fill < 0.8:
            cls, conf = "FLUID POUND", clamp(0.62 + (0.8 - c.fill) * 1.2, 0.6, 0.98)
        elif drag_frac > 0.35:
            cls, conf = "VISCOUS DRAG", clamp(0.6 + (drag_frac - 0.35), 0.6, 0.95)
        return DynoCard(surface, downhole, S_M, f_min, f_max, cls, conf)

    # ---- whole-cycle curves ----

    def series(self) -> Series:
        cyc = self._cycle()
        cum, steam = cyc.cum, self._p["steam"]
        out = Series()
        for d in range(CYCLE_DAYS + 1):
            t = max(0, d - SOAK_END)
            spread = 0.07 + 0.16 * min(1.0, t / 102)
            out.day.append(d)
            out.T.append(cyc.T[d])
            out.mu.append(cyc.mu[d])
            out.oil.append(cyc.oil[d])
            out.oil_p10.append(cyc.oil[d] * (1 + spread))
            out.oil_p90.append(cyc.oil[d] * (1 - spread))
            out.spm_safe.append(cyc.spm_safe[d])
            out.float_margin.append(cyc.margin[d])
            out.sor.append(sor(steam, cum[d]) if d > SOAK_END and cum[d] > 5 else None)
        return out

    # ---- depth tracks ----

    def profile(self) -> Profile:
        b, c, th = self._b, self._c, self._b.th
        prod = self._phase == "PRODUCTION"
        m = self.metrics()
        level = m.fluid_level
        out = Profile()
        bf = 1 - 0.128 * c.Gfl

        c_below: dict[int, float] = {}
        acc = 0.0
        z = 1060
        while z >= 0:
            tf = t_fluid(z + 5, th.exc, b.Lr)
            mu = min(viscosity_cp(tf), MU_CAP_CP) * KVIS / 1000
            sec = next((s for s in SECT if s.top <= z + 5 < s.bot), SECT[2])
            acc += TAU * mu * 10 / sec.lnr
            c_below[z] = acc
            z -= 10
        for z in range(0, 1251, 10):
            out.depth.append(z)
            tf = t_fluid(z, th.exc, b.Lr)
            out.t_fluid.append(tf)
            out.mu.append(viscosity_cp(tf))
            halo = smooth((z - 1055) / 25) * (1 - smooth((z - 1165) / 25))
            out.t_formation.append(t_geo(z) + 0.6 * th.exc * halo)
            out.pressure.append(3.0 if z < level else 3 + 0.0912 * (z - level))
            s_max = 0.0
            if z < PUMP_DEPTH:
                sec = next((s for s in SECT if s.top <= z < s.bot), SECT[2])
                wb = w_below(z)
                cb = c_below.get(math.floor(z / 10) * 10, 0)
                s_max = (wb * bf + c.Fo + wb * c.alpha + cb * c.vUp) / sec.A
            out.rod_stress.append(fin(s_max))
        if prod and self._dep:
            out.deposition_top, out.deposition_bot = self._dep
        return out


def _js_num(v: float) -> str:
    """JS template-literal formatting of a number (integers without a trailing .0)."""
    return str(int(v)) if float(v).is_integer() else repr(v)

