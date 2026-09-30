"""O3 RL competitor: PPO (stable-baselines3) on a gymnasium env wrapping the tabulated physics twin.

Episode = one CSS cycle of one well: step 0 chooses (steam, soak, cut-off); steps 1-4 choose (spm, kd) for four
consecutive production blocks. Reward = block value (oil - energy - risk cost, INR/1e5) minus steam cost and constraint
penalties. All strategies (static practice, O1 only, O1+O2 plan, PPO) are scored by the same env physics on the
same held-out wells and cycle numbers. Trains in a few minutes on one CPU thread.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

from mantle_physics.constants import PRICE, SOAK_END
from mantle_physics.hazard import WEIBULL_K, pump_unseat_hazard, pump_uplift_kn, rod_damage_rate

from .. import common
from .. import fasttwin as ft
from . import m5_stroke, o1_srp

ID = "O3"
N_BLOCKS = 4
SCALE = 1e5
PEN = {"margin": 2.0e5, "fill": 1.0e5, "goodman": 2.0e5, "torque": 2.0e5}     # INR per unit violation (per block)
PRACTICE = {"steam": 800.0, "soak": 4.0, "cutoff": 120.0}
PRACTICE_PUMP = (5.4, 0.5)


def soak_factor(soak: float) -> float:
    return 1 + 0.015 * (min(soak, 7) - 4) - 0.012 * max(0.0, soak - 7)


def block_eval(well: dict, cyc: int, steam: float, soak: float, cutoff: float, d0: int, d1: int, spm, kd) -> dict[str, Any]:
    """Physics of production days d0..d1 (twin axis, inclusive). ``spm``/``kd`` arrays broadcast on leading axes."""
    w = {**o1_srp.DEFAULT_WELL, **well}
    b = ft.base_at(ft.eff_steam(steam, float(w["steam_eff"])))
    sl = slice(d0, d1 + 1)
    k = float(w["pi_factor"]) * float(w["decline_rate"]) ** (cyc - 1) * soak_factor(soak)
    f = {n: ft.base_field(b, n)[sl] for n in ("qIn", "wc", "c", "c500", "c800", "muPump")}
    spm, kd = np.asarray(spm, dtype=float), np.asarray(kd, dtype=float)
    S, K = spm[..., None], kd[..., None]
    r = ft.core(f["qIn"] * k, f["wc"], f["c"], f["c500"], f["c800"], S, K)
    oil = r["oil"].sum(-1)
    kw = r["kw"].sum(-1)
    imp = m5_stroke.impacts_per_day(S, r["fill"])
    ivel = m5_stroke.impact_velocity(S, r["fill"])
    n_days = d1 - d0 + 1
    T_total = max(cutoff - SOAK_END, 1.0)
    gm = r["goodman"].mean(-1)
    rate = rod_damage_rate(o1_srp.rod_shape() * gm[..., None] * float(w["rod_stress_factor"]), spm[..., None] * 1440, 0.0, imp.mean(-1)[..., None],
                           ivel.mean(-1)[..., None], float(w["corrosion_index"]))
    rod_fail = np.sum(1 - np.exp(-((rate * T_total) ** WEIBULL_K)), axis=-1) * n_days / T_total
    uplift = pump_uplift_kn(f["muPump"] * float(w["visc_factor"]), np.pi * 3.0255 * S / 60, r["fill"], ivel)
    unseat = (1 - np.exp(-pump_unseat_hazard(uplift, float(w["hold_down_kn"])).sum(-1)))
    risk = rod_fail * o1_srp.C_ROD + unseat * o1_srp.C_UNSEAT
    viol = {"margin": np.maximum(0, o1_srp.LIMITS["margin"] - r["margin_raw"].min(-1)), "fill": np.maximum(0, o1_srp.LIMITS["fill"] - r["fill"].mean(-1)),
            "goodman": np.maximum(0, r["goodman"].max(-1) - o1_srp.LIMITS["goodman"]), "torque": np.maximum(0, r["torque"].max(-1) - 1.0)}
    penalty = sum(PEN[k_] * v for k_, v in viol.items())
    value = oil * PRICE["oil"] - kw * 24 * PRICE["kwh"]
    return {"oil": oil, "kw": kw, "impacts": imp.mean(-1), "risk": risk, "penalty": penalty, "value": value, "net": value - risk - penalty,
            "feasible": sum(viol.values()) <= 0.02, "viol": viol}


def blocks(cutoff: float) -> list[tuple[int, int]]:
    edges = np.linspace(SOAK_END, int(cutoff), N_BLOCKS + 1).round().astype(int)
    return [(int(edges[i]) + (1 if i else 0), int(edges[i + 1])) for i in range(N_BLOCKS)]


class CssEnv(gym.Env):
    metadata: dict = {}

    def __init__(self, wells: list[dict], seed: int = 0, fixed_cycle: int | None = None):
        super().__init__()
        self.wells, self.rng, self.fixed_cycle = wells, np.random.default_rng(seed), fixed_cycle
        self.action_space = gym.spaces.Box(-1.0, 1.0, (5,), np.float32)
        self.observation_space = gym.spaces.Box(-5.0, 5.0, (16,), np.float32)
        self.well: dict = wells[0]
        self.cyc, self.stage, self.plan, self.last = 1, 0, dict(PRACTICE), (0.85, 0.5, 0.6, 0.0)

    def _obs(self) -> np.ndarray:
        w = self.well
        p = self.plan
        v = [w["pi_factor"] - 1, np.log(w["visc_factor"]) * 3, w["steam_eff"] - 1, w["decline_rate"] - 0.9, w["corrosion_index"] - 0.4,
             w["rod_stress_factor"] - 1.35, self.cyc / 6 - 1, self.stage / N_BLOCKS, (p["steam"] - 850) / 350, (p["soak"] - 6) / 4,
             (p["cutoff"] - 80) / 40, *list(self.last)]
        return np.clip(np.array(v[:16] + [0] * (16 - len(v)), dtype=np.float32), -5, 5)

    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.well = self.wells[int(self.rng.integers(len(self.wells)))]
        self.cyc = self.fixed_cycle or int(self.rng.integers(1, 9))
        self.stage, self.plan, self.last = 0, dict(PRACTICE), (0.85, 0.5, 0.6, 0.0)
        return self._obs(), {}

    @staticmethod
    def decode_plan(a) -> dict:
        return {"steam": float(500 + 700 * (a[0] + 1) / 2), "soak": float(round(2 + 8 * (a[1] + 1) / 2)),
                "cutoff": float(round(40 + 80 * (a[2] + 1) / 2))}

    @staticmethod
    def decode_pump(a) -> tuple[float, float]:
        return float(0.8 + 8.2 * (a[3] + 1) / 2), float(0.40 + 0.30 * (a[4] + 1) / 2)

    def step(self, action):
        a = np.clip(np.asarray(action, dtype=float), -1, 1)
        if self.stage == 0:
            self.plan = self.decode_plan(a)
            self.stage = 1
            r = -self.plan["steam"] * PRICE["steamT"] / SCALE
            self.info = {}
            return self._obs(), float(r), False, False, {}
        bl = blocks(self.plan["cutoff"])[self.stage - 1]
        spm, kd = self.decode_pump(a)
        e = block_eval(self.well, self.cyc, self.plan["steam"], self.plan["soak"], self.plan["cutoff"], bl[0], bl[1], np.array(spm), np.array(kd))
        self.last = (float(np.clip(1 - e["penalty"] / 3e5, -3, 1)), kd, spm / 9, float(e["oil"]) / 2000)
        self.stage += 1
        done = self.stage > N_BLOCKS
        return self._obs(), float(e["net"] / SCALE), done, False, {"oil": float(e["oil"]), "feasible": bool(e["feasible"])}


# ---------------------------------------------------------------- strategies (scored by the same physics)


def score_plan(well: dict, cyc: int, plan: dict, pump_fn) -> dict[str, float]:
    """Total net INR / oil / impacts / feasibility of a cycle: ``pump_fn(block_index, d0, d1)`` -> (spm, kd)."""
    tot = {"net": -plan["steam"] * PRICE["steamT"], "oil": 0.0, "impacts": 0.0, "feasible": 1.0, "risk": 0.0}
    for i, (d0, d1) in enumerate(blocks(plan["cutoff"])):
        spm, kd = pump_fn(i, d0, d1)
        e = block_eval(well, cyc, plan["steam"], plan["soak"], plan["cutoff"], d0, d1, np.array(spm), np.array(kd))
        tot["net"] += float(e["net"])
        tot["oil"] += float(e["oil"])
        tot["impacts"] += float(e["impacts"]) / N_BLOCKS
        tot["risk"] += float(e["risk"])
        tot["feasible"] *= float(e["feasible"])
    return tot


def o1_block_pump(well: dict, cyc: int, plan: dict):
    """O1's constrained optimum per block (grid over spm x kd on that block's days)."""
    S, K = np.meshgrid(o1_srp.SPM_GRID, o1_srp.KD_GRID, indexing="ij")

    def fn(i, d0, d1):
        e = block_eval(well, cyc, plan["steam"], plan["soak"], plan["cutoff"], d0, d1, S, K)
        j = np.unravel_index(int(np.argmax(e["net"])), S.shape)
        return float(S[j]), float(K[j])

    return fn


def evaluate_strategies(wells: list[dict], cycles: list[int], o2_plans: dict[str, dict] | None, policy=None) -> dict[str, dict]:
    rows: dict[str, list[dict]] = {"static": [], "o1_only": [], "o1_o2": [], "ppo": []}
    for w in wells:
        for cyc in cycles:
            rows["static"].append(score_plan(w, cyc, PRACTICE, lambda i, a, b: PRACTICE_PUMP))
            rows["o1_only"].append(score_plan(w, cyc, PRACTICE, o1_block_pump(w, cyc, PRACTICE)))
            if o2_plans and w["well_id"] in o2_plans:
                m = o2_plans[w["well_id"]]["mantle"]
                plan = {"steam": float(m["steam"]), "soak": float(m["soak"]), "cutoff": float(m["cutoff"])}
                rows["o1_o2"].append(score_plan(w, cyc, plan, o1_block_pump(w, cyc, plan)))
            if policy is not None:
                rows["ppo"].append(score_plan_policy(w, cyc, policy))
    out = {}
    for k, r in rows.items():
        if r:
            out[k] = {m: float(np.mean([x[m] for x in r])) for m in r[0]} | {"n": len(r)}
    return out


def score_plan_policy(well: dict, cyc: int, policy) -> dict[str, float]:
    env = CssEnv([well], fixed_cycle=cyc)
    obs, _ = env.reset(seed=0)
    tot = {"net": 0.0, "oil": 0.0, "impacts": 0.0, "feasible": 1.0, "risk": 0.0}
    done = False
    plan = None
    while not done:
        act, _ = policy.predict(obs, deterministic=True)
        if env.stage == 0:
            plan = env.decode_plan(act)
        stage = env.stage
        obs, r, done, _, info = env.step(act)
        tot["net"] += r * SCALE
        if stage > 0:
            tot["oil"] += info["oil"]
            tot["feasible"] *= float(info["feasible"])
            bl = blocks(env.plan["cutoff"])[stage - 1]
            spm, kd = env.decode_pump(act)
            e = block_eval(well, cyc, env.plan["steam"], env.plan["soak"], env.plan["cutoff"], bl[0], bl[1], np.array(spm), np.array(kd))
            tot["impacts"] += float(e["impacts"]) / N_BLOCKS
            tot["risk"] += float(e["risk"])
    del plan
    return tot


# ---------------------------------------------------------------- serving


class RlPolicy:
    def __init__(self, model, meta: dict):
        self.model, self.meta = model, meta

    @classmethod
    def load(cls, d: Path) -> RlPolicy:
        from stable_baselines3 import PPO

        return cls(PPO.load(str(Path(d) / "ppo.zip"), device="cpu"), json.loads((Path(d) / "meta.json").read_text()))

    def act(self, well: dict, cycle_no: int) -> dict:
        """Full-cycle plan the policy would execute: steam/soak/cut-off plus the pump setting for each of the 4 blocks."""
        env = CssEnv([well], fixed_cycle=cycle_no)
        obs, _ = env.reset(seed=0)
        a, _ = self.model.predict(obs, deterministic=True)
        plan = env.decode_plan(a)
        obs, *_ = env.step(a)
        pumps = []
        for _ in range(N_BLOCKS):
            a, _ = self.model.predict(obs, deterministic=True)
            pumps.append(env.decode_pump(a))
            obs, *_ = env.step(a)
        return {"plan": plan, "pump_by_block": [{"spm": s, "kd": k} for s, k in pumps], "model": ID, "version": self.meta["version"],
                "source": "physics_synthetic"}


def train(out_dir: Path, quick: bool = False) -> dict:
    import torch
    from stable_baselines3 import PPO
    from stable_baselines3.common.vec_env import DummyVecEnv

    torch.set_num_threads(1)
    from .. import data

    root = Path(out_dir)
    with common.timer() as tm:
        if quick:
            data.ensure_small_data()
        wl = data.wells().to_dict("records")
        rng = np.random.default_rng(0)
        idx = rng.permutation(len(wl))
        n_test = max(2, len(wl) // 5)
        test = [wl[i] for i in idx[:n_test]]
        train_w = [wl[i] for i in idx[n_test:]]
        steps = 2048 if quick else 160_000
        env = DummyVecEnv([lambda: CssEnv(train_w, seed=1)])
        ppo = PPO("MlpPolicy", env, n_steps=1024, batch_size=256, n_epochs=8, learning_rate=3e-4, gamma=0.995, gae_lambda=0.95,
                  ent_coef=0.003, policy_kwargs={"net_arch": [64, 64]}, seed=0, verbose=0, device="cpu")
        t0 = time.time()
        ppo.learn(total_timesteps=steps)
        fit_s = time.time() - t0
        plans_path = root / "O2" / "plans.json"
        o2_plans = json.loads(plans_path.read_text()) if plans_path.exists() else None
        cycles = [2, 4, 6] if not quick else [3]
        ev_wells = test if not quick else test[:2]
        res = evaluate_strategies(ev_wells, cycles, o2_plans, ppo)
        o2_note = None if o2_plans else "O2 plans not found: O1+O2 row missing"
    d = common.model_dir(ID, root)
    ppo.save(str(d / "ppo"))
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "trained_at": common.now_iso(), "timesteps": steps,
            "data_hash": common.data_hash([str([w["well_id"] for w in train_w])]), "train_wells": len(train_w), "test_wells": [w["well_id"] for w in test]}
    (d / "meta.json").write_text(json.dumps(meta))
    st, o12, pp = res.get("static"), res.get("o1_o2"), res.get("ppo")
    met: dict = {"eval_wells": len(ev_wells), "eval_cycles": cycles, "train_seconds_ppo": fit_s, "timesteps": steps}
    for k, r in res.items():
        for m in ("net", "oil", "impacts", "feasible", "risk"):
            met[f"{k}_{m}"] = r[m]
    if pp and o12 and st:
        met["ppo_vs_o1_o2_net_ratio"] = (pp["net"] - st["net"]) / max(abs(o12["net"] - st["net"]), 1.0)
    ev = {"metrics": met, "primary": {"name": "ppo_net_inr_per_cycle", "value": pp["net"] if pp else None, "target": None,
                                     "target_text": "shown vs O1+O2 (no target)", "baseline_name": "static practice", "baseline": st["net"] if st else None,
                                     "direction": "higher", "secondary": {"name": "o1_o2_net_inr_per_cycle", "value": o12["net"] if o12 else None}},
          "notes": [n for n in (o2_note,) if n], "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"],
          "data_hash": meta["data_hash"], "quick": quick}
    card = f"""# O3 RL competitor (PPO)
PPO (stable-baselines3, MLP 64x64, {steps:,} steps, ~{fit_s:.0f} s on one CPU thread) on a gym env wrapping the tabulated twin. One episode = one CSS cycle: choose steam/soak/cut-off, then (spm, kd) for four production blocks.
**Source: physics_synthetic.** Trained on {len(train_w)} wells, scored on {len(ev_wells)} held-out wells x cycles {cycles} with the env's own physics for every strategy (static practice, O1 only, O1+O2 plan, PPO).
- Reward = oil value - energy - Miner/unseat risk cost - steam cost - constraint penalties (same terms as O1), so the comparison is like-for-like.
- Metrics: {json.dumps(met)}
- Shown honestly: PPO is a single small policy trained for minutes; O1+O2 optimise explicitly per well. Where PPO trails, that is the result.
- Limits: env physics differs slightly from the M2 surrogate used by O2 (O2 is scored here through its chosen levers only); block-level pump only; no stochastic prices.
"""
    return common.write_eval(d, ID, ev, card)
