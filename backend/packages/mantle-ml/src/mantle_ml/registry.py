"""Model registry: loads every artifact at startup and exposes one ``predict_*`` API used by the FastAPI service.

Import order matters (see ``mantle_ml/__init__``): lightgbm is imported before anything that pulls in torch.
Every response carries ``model``, ``version``, ``trained_on`` (data hash) and ``source``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import lightgbm  # noqa: F401  (must be imported before torch: two libomp copies otherwise crash)
import numpy as np

from . import common
from .models import m0_viscosity as m0
from .models import m1_thermal as m1
from .models import m2_forecast as m2
from .models import m3_dyno as m3
from .models import m4_risk as m4
from .models import m5_stroke as m5
from .models import m6_anomaly as m6
from .models import o1_srp as o1
from .models import o2_css as o2

ALL_IDS = ("M0", "M1", "M2", "M3", "M4", "M5", "M6", "O1", "O2", "O3")


class Registry:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.info: dict[str, dict] = {}
        self.loaded: list[str] = []
        self.missing: dict[str, str] = {}
        self.m0: Any = None
        self.m1: Any = None
        self.m2: Any = None
        self.m3: Any = None
        self.m4: Any = None
        self.m5: Any = None
        self.m6: Any = None
        self.o2: Any = None
        self.o3: Any = None
        self.plans: dict[str, dict] = {}

    # ------------------------------------------------------------ loading
    @classmethod
    def load(cls, root: Path | None = None, strict: bool = False, skip: tuple[str, ...] = ()) -> Registry:
        r = cls(Path(root) if root else common.models_dir())
        p = r.root / "registry.json"
        if p.exists():
            r.info = json.loads(p.read_text()).get("models", {})
        loaders = {
            "M0": r._load_m0, "M1": r._load_m1, "M2": r._load_m2, "M3": r._load_m3, "M4": r._load_m4, "M5": r._load_m5,
            "M6": r._load_m6, "O1": r._load_o1, "O2": r._load_o2, "O3": r._load_o3,
        }
        for mid, fn in loaders.items():
            if mid in skip:
                continue
            try:
                fn()
                r.loaded.append(mid)
            except Exception as e:                      # missing artifact / unreadable
                r.missing[mid] = f"{type(e).__name__}: {str(e)[:120]}"
                if strict:
                    raise
        return r

    def _d(self, mid: str) -> Path:
        return self.root / mid

    def _load_m0(self):
        self.m0 = m0.ViscosityModel.load(self._d("M0"))

    def _load_m1(self):
        self.m1 = m1.ThermalModel.load(self._d("M1"))

    def _load_m2(self):
        self.m2 = m2.ForecastModel.load(self._d("M2"), self.m1 or m1.ThermalModel.load(self._d("M1")), self.m0 or m0.ViscosityModel.load(self._d("M0")))

    def _load_m3(self):
        self.m3 = m3.DynoClassifier.load(self._d("M3"))

    def _load_m4(self):
        self.m4 = m4.RiskModel.load(self._d("M4"))

    def _load_m5(self):
        self.m5 = m5.StrokeEstimator.load(self._d("M5"))

    def _load_m6(self):
        if not (self._d("M6") / "ae_s3.onnx").exists():      # torch fallback only when no ONNX export exists
            import torch

            torch.set_num_threads(1)
        self.m6 = m6.AnomalyDetector.load(self._d("M6"))

    def _load_o1(self):
        from . import fasttwin

        fasttwin.tables()
        o1.rod_shape()
        if not (self._d("O1") / "meta.json").exists():
            raise FileNotFoundError("O1/meta.json")

    def _load_o2(self):
        if self.m2 is None:
            raise RuntimeError("O2 needs M2")
        self.o2 = o2.Planner(self.m2)
        pp = self._d("O2") / "plans.json"
        if pp.exists():
            self.plans = json.loads(pp.read_text())

    def _load_o3(self):
        import torch

        torch.set_num_threads(1)
        from .models import o3_rl

        self.o3 = o3_rl.RlPolicy.load(self._d("O3"))

    # ------------------------------------------------------------ metadata
    def models_loaded(self) -> int:
        return len(self.loaded)

    def describe(self) -> list[dict]:
        out = []
        for mid in ALL_IDS:
            i = self.info.get(mid, {})
            out.append({"id": mid, "loaded": mid in self.loaded, "version": i.get("version"), "trained_at": i.get("trained_at"),
                        "data_hash": i.get("data_hash"), "source": i.get("source"), "metrics": i.get("metrics", {}).get("primary"),
                        "error": self.missing.get(mid)})
        return out

    def _stamp(self, mid: str, res: dict) -> dict:
        i = self.info.get(mid, {})
        res.setdefault("model", mid)
        res.setdefault("version", i.get("version"))
        res["trained_on"] = i.get("data_hash")
        res.setdefault("source", i.get("source", "physics_synthetic"))
        return res

    # ------------------------------------------------------------ predict API
    def predict_viscosity(self, T, api: float = 18.0, asph: float = 9.2, **kw) -> dict:
        return self._stamp("M0", self.m0.predict(T, api, asph, **kw))

    def predict_thermal(self, steam_t: float, days, **kw) -> dict:
        return self._stamp("M1", self.m1.predict(steam_t, days, **kw))

    def predict_cycle(self, well: dict, steam_t: float, soak_d: float, spm: float, kd: float, cutoff_day: int, **kw) -> dict:
        return self._stamp("M2", self.m2.predict_daily(well, steam_t, soak_d, spm, kd, cutoff_day, **kw))

    def classify_card(self, pos, load, spm: float) -> dict:
        return self._stamp("M3", self.m3.classify(pos, load, spm))

    def estimate_stroke(self, pos, load, spm: float) -> dict:
        return self._stamp("M5", self.m5.estimate(pos, load, spm))

    def assess_risk(self, well: dict, steam: float, spm: float, kd: float, day_in_prod: float, cycle_no: int = 1,
                    days_since_workover: float = 90.0, history: dict | None = None) -> dict:
        cov = m4.cov_from_settings(well, steam, spm, kd, cycle_no, days_since_workover, history=history)
        return self._stamp("M4", self.m4.assess(cov, day_in_prod))

    def compare_risk(self, well: dict, steam: float, now: tuple[float, float], new: tuple[float, float], day_in_prod: float,
                     cycle_no: int = 1, days_since_workover: float = 90.0, history: dict | None = None) -> dict:
        """M4 with the well as it runs today (``now`` = spm, kd) versus at ``new`` settings. Only spm/kd-driven covariates
        change; the well and its history (corrosion, age, strokes so far, event record) are identical in both."""
        a = m4.cov_from_settings(well, steam, now[0], now[1], cycle_no, days_since_workover, history=history)
        b = m4.cov_from_settings(well, steam, new[0], new[1], cycle_no, days_since_workover, history_spm=now[0], history=history)
        return self._stamp("M4", self.m4.compare(a, b, day_in_prod))

    def score_telemetry(self, minutes: np.ndarray, **kw) -> dict:
        return self._stamp("M6", self.m6.score_series(minutes, **kw))

    def recommend_pump(self, steam: float, cycle_day: float, spm: float, kd: float, well: dict | None = None, **kw) -> dict:
        w = dict(well or {})
        rm = self.m4 if kw.pop("with_risk", False) else None
        if rm is not None and "rod_stress_factor" not in w:
            w.setdefault("rod_stress_factor", 1.3)
        return self._stamp("O1", o1.recommend(steam, cycle_day, spm, kd, w, risk_model=rm, **kw))

    def plan_next_cycle(self, well: dict, cycle_no: int = 1, budget_s: float = 5.0, refresh: bool = False, **kw) -> dict:
        """Cached plan (from training-time ``plans.json``) if present, else computed and cached in memory."""
        wid = well.get("well_id")
        if not refresh and wid in self.plans and "plan_curve" in self.plans[wid]:
            cached = dict(self.plans[wid])
            cached["cached"] = True
            return self._stamp("O2", cached)
        return self._stamp("O2", self.o2.plan(well, cycle_no, budget_s=budget_s, **kw))

    def rl_action(self, well: dict, cycle_no: int) -> dict:
        return self._stamp("O3", self.o3.act(well, cycle_no))


_REG: Registry | None = None


def get_registry(root: Path | None = None, reload: bool = False) -> Registry:
    global _REG
    if _REG is None or reload:
        _REG = Registry.load(root)
    return _REG


def predict_viscosity(*a, **k):
    return get_registry().predict_viscosity(*a, **k)


def predict_thermal(*a, **k):
    return get_registry().predict_thermal(*a, **k)


def predict_cycle(*a, **k):
    return get_registry().predict_cycle(*a, **k)


def classify_card(*a, **k):
    return get_registry().classify_card(*a, **k)


def estimate_stroke(*a, **k):
    return get_registry().estimate_stroke(*a, **k)


def assess_risk(*a, **k):
    return get_registry().assess_risk(*a, **k)


def score_telemetry(*a, **k):
    return get_registry().score_telemetry(*a, **k)


def recommend_pump(*a, **k):
    return get_registry().recommend_pump(*a, **k)


def plan_next_cycle(*a, **k):
    return get_registry().plan_next_cycle(*a, **k)


def rl_action(*a, **k):
    return get_registry().rl_action(*a, **k)


_ = Any
