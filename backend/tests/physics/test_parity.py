"""JS <-> Python parity: every numeric field of the browser twin must match the Python port."""

from __future__ import annotations

import math

import pytest

from mantle_physics import rig
from mantle_physics.derived import derive
from mantle_physics.twin import WellSim
from mantle_physics.viscosity import viscosity_cp

REL, ABS = 1e-6, 1e-9
_max_err = {"rel": 0.0}


def compare(js, py, path=""):
    """Recursively compare JS-decoded JSON with the Python ``to_json()`` output."""
    if isinstance(js, dict):
        assert isinstance(py, dict), f"{path}: type {type(py)}"
        assert set(js) == set(py), f"{path}: keys differ: {set(js) ^ set(py)}"
        for k in js:
            compare(js[k], py[k], f"{path}.{k}")
    elif isinstance(js, list):
        assert len(js) == len(py), f"{path}: len {len(js)} != {len(py)}"
        for i, (a, b) in enumerate(zip(js, py, strict=True)):
            compare(a, b, f"{path}[{i}]")
    elif isinstance(js, bool) or js is None or isinstance(js, str):
        assert js == py, f"{path}: {js!r} != {py!r}"
    else:
        assert py is not None, f"{path}: python None vs {js}"
        err = abs(js - py)
        tol = max(ABS, REL * max(abs(js), abs(py)))
        assert err <= tol, f"{path}: js={js!r} py={py!r} err={err:.3e}"
        scale = max(abs(js), abs(py), 1e-12)
        if err > ABS:
            _max_err["rel"] = max(_max_err["rel"], err / scale)


def make_sim(inp):
    return WellSim(spm=inp["spm"], cycle_day=inp["cycleDay"], kd=inp["kd"], steam=inp["steam"])


def test_scenario_count(oracle):
    assert len(oracle["scenarios"]) >= 45


def test_scenarios(oracle):
    for sc in oracle["scenarios"]:
        inp = sc["input"]
        tag = f"scenario{inp}"
        sim = make_sim(inp)
        compare(sc["state0"], sim.state.to_json(), tag + ".state0")
        for _ in range(inp["steps"]):
            sim.step(0.05)
        compare(sc["state"], sim.state.to_json(), tag + ".state")
        compare(sc["theta"], sim.theta, tag + ".theta")
        m = sim.metrics()
        compare(sc["metrics"], m.to_json(), tag + ".metrics")
        compare(sc["series"], sim.series().to_json(), tag + ".series")
        compare(sc["profile"], sim.profile().to_json(), tag + ".profile")
        compare(sc["dyno"]["n180"], sim.dyno_card(180).to_json(), tag + ".dyno180")
        compare(sc["dyno"]["n12"], sim.dyno_card(12).to_json(), tag + ".dyno12")
        compare(sc["derived"], derive(m, sim.state), tag + ".derived")
        compare(sc["derivedNoState"], derive(m, None), tag + ".derivedNoState")


def test_stateful_sequence(oracle):
    sim = WellSim()
    for entry in oracle["sequence"]:
        s = entry["set"]
        sim.set(spm=s.get("spm"), cycle_day=s.get("cycleDay"), kd=s.get("kd"), steam=s.get("steam"))
        for _ in range(15):
            sim.step(0.05)
        tag = f"seq{s}"
        compare(entry["state"], sim.state.to_json(), tag + ".state")
        compare(entry["theta"], sim.theta, tag + ".theta")
        compare(entry["metrics"], sim.metrics().to_json(), tag + ".metrics")
        compare(entry["series"], sim.series().to_json(), tag + ".series")


def test_unit_pose_and_rod_position(oracle):
    for e in oracle["unitPose"]:
        p = rig.unit_pose(e["theta"])
        compare(e["pose"], p.to_json(), f"pose({e['theta']})")
        compare(e["pos"], rig.rod_position(e["theta"]), "rodPosition")
    compare(oracle["stroke"], rig.STROKE.to_json(), "STROKE")


def test_depth_scale(oracle):
    for e in oracle["depth"]:
        if "d" in e and "back" in e:
            compare(e["y"], rig.depth_to_y(e["d"]), "depthToY")
            compare(e["back"], rig.y_to_depth(rig.depth_to_y(e["d"])), "roundtrip")
        else:
            compare(e["d"], rig.y_to_depth(e["y"]), "yToDepth")


def test_viscosity(oracle):
    for e in oracle["viscosity"]:
        T = e["T"] if e["T"] is not None else float("nan")
        compare(e["mu"], viscosity_cp(T), f"mu({T})")


def test_cycle_constants(oracle):
    from mantle_physics import CYCLE

    assert oracle["cycle"] == CYCLE


def test_zzz_report_max_error(capsys):
    # runs last in this module (alphabetical within file order); documents the observed error
    with capsys.disabled():
        print(f"\n[parity] max relative error observed: {_max_err['rel']:.3e}")
    assert math.isfinite(_max_err["rel"])
    assert pytest.approx(0, abs=1e-6) == _max_err["rel"]
