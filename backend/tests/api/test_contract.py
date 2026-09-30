"""Every field the frontend (app/js/{hud,section,inspect,twin-data,api}.js) reads off the API, with its type.

The lists below were built by grepping those files for property reads on ``metrics``, ``derived``, ``health``, ``plan``,
``well``, ``series``, ``profile``, ``dyno``, ``live`` and ``meta``. The wire is snake_case; ``camel`` mirrors the client.
"""
from __future__ import annotations

import math

import pytest

W = "/api/wells/BGW-17"
NUM, STR, BOOL, LIST, DICT = (int, float), str, bool, list, dict

METRICS = {
    "phase": STR, "cycleDay": NUM, "dayInPhase": NUM, "spm": NUM, "kd": NUM, "stroke": NUM, "sandfaceT": NUM,
    "viscosity": NUM, "heatedRadius": NUM, "thermalBattery": NUM, "daysToCutoff": NUM, "oilRate": NUM, "waterCut": NUM,
    "liquidRate": NUM, "pumpDisplacement": NUM, "fillage": NUM, "pumpEff": NUM, "bottleneck": STR, "pprl": NUM,
    "mprl": NUM, "floatMargin": NUM, "spmSafe": NUM, "goodman": NUM, "torquePct": NUM, "motorKw": NUM,
    "kwhPerBbl": NUM, "sor": NUM, "steamTons": NUM, "cumOil": NUM, "co2PerBbl": NUM, "netPerDay": NUM,
    "fluidLevel": NUM, "submergence": NUM, "alerts": LIST, "recommendation": DICT,
}
DERIVED = {
    "hz": NUM, "amps": NUM, "ampsAvg": NUM, "profile": LIST, "stroke": NUM, "thp": NUM, "chp": NUM, "pip": NUM,
    "flowT": NUM, "pRes": NUM, "counterbalance": NUM, "beamLoad": NUM, "impactsDay": NUM, "impactsMantle": NUM,
    "impactVel": NUM, "upliftMargin": NUM, "unseatRisk": NUM, "recovery": NUM, "cost": DICT,
}
COST = {"steamDay": NUM, "powerDay": NUM, "maintDay": NUM, "chemDay": NUM, "costDay": NUM, "costBbl": NUM, "revenueDay": NUM}
REC = {"title": STR, "detail": STR, "spm": NUM, "kd": NUM, "hz": NUM, "stroke": NUM, "deltas": DICT, "confidence": NUM}
DELTAS = {"oil": NUM, "float": NUM, "energy": NUM, "impacts": NUM}
HEALTH = {"rods": LIST, "failures": LIST, "unseats": DICT, "failureWindowMonths": NUM, "mtbfDays": NUM, "mtbfMantleDays": NUM,
          "impactsDay": NUM, "impactsMantle": NUM, "impactVel": NUM, "upliftMargin": NUM, "unseatRisk30d": NUM}
ROD = {"index": int, "depthM": NUM, "taper": STR, "fatigue": NUM, "failed": BOOL}
FAILURE = {"rod": int, "depth": NUM, "size": STR, "mode": STR, "date": STR, "cause": STR}
UNSEATS = {"months": LIST, "events": LIST, "holdDownKn": NUM, "details": LIST}
SERIES = {"day": LIST, "T": LIST, "mu": LIST, "oil": LIST, "oilP10": LIST, "oilP90": LIST, "pastCycles": LIST, "planCurve": DICT}
PROFILE = {"depth": LIST, "Tfluid": LIST, "Tformation": LIST, "mu": LIST, "pressure": LIST, "depositionTop": (int, float, type(None)),
           "depositionBot": (int, float, type(None))}
DYNO = {"surface": LIST, "downhole": LIST, "xMax": NUM, "fMin": NUM, "fMax": NUM, "cls": STR, "clsConf": NUM}
PLAN = {"practice": DICT, "mantle": DICT, "ranges": DICT, "inrPerCycle": NUM, "jointShare": NUM, "oilLift": NUM, "sor": LIST}
LEVERS = {"steam": NUM, "pInj": NUM, "soak": NUM, "cutoff": NUM}
WELL = {"fluid": DICT, "rods": DICT, "unit": DICT, "completion": DICT}
FLUID = {"api": NUM, "asphaltene": NUM, "tRes": NUM, "pRes": NUM, "deadOilCp": NUM}
LIVE = {"t": NUM, "theta": NUM, "rodPos": NUM, "load": NUM, "amps": NUM, "hz": NUM, "spmActual": NUM, "thp": NUM, "chp": NUM,
        "anomalyScore": NUM, "anomalyLabel": STR, "lastStroke": DICT}
META = {"dataSource": STR, "models": LIST, "sources": LIST, "prices": DICT}


def check(obj, spec, where):
    for k, t in spec.items():
        assert k in obj, f"{where}: missing {k}"
        assert isinstance(obj[k], t), f"{where}.{k}: {type(obj[k]).__name__}"
        if isinstance(obj[k], float):
            assert math.isfinite(obj[k]), f"{where}.{k} not finite"


def test_state_contract(client, camel):
    s = camel(client.get(f"{W}/state").json())
    check(s["metrics"], METRICS, "metrics")
    check(s["derived"], DERIVED, "derived")
    check(s["derived"]["cost"], COST, "derived.cost")
    check(s["recommendation"], REC, "recommendation")
    check(s["recommendation"]["deltas"], DELTAS, "deltas")
    assert all({"level", "text"} <= set(a) for a in s["metrics"]["alerts"]) and isinstance(s["source"], str)
    check(s["metrics"]["recommendation"], {k: v for k, v in REC.items() if k not in ("hz", "stroke")}, "metrics.recommendation")           # client falls back to it
    assert len(s["derived"]["profile"]) == 36


def test_health_contract(client, camel):
    h = camel(client.get(f"{W}/health").json())
    check(h, HEALTH, "health")
    for r in h["rods"]:
        check(r, ROD, "rod")
    for f in h["failures"]:
        check(f, FAILURE, "failure")
    check(h["unseats"], UNSEATS, "unseats")
    assert all(isinstance(m, str) and m for m in h["unseats"]["months"]) and all(isinstance(e, int) for e in h["unseats"]["events"])


def test_curves_contract(client, camel):
    s = camel(client.get(f"{W}/series?spm=5.4&kd=0.5&steam=800").json())
    check(s, SERIES, "series")
    assert all(isinstance(c["oil"], list) for c in s["pastCycles"]) and {"day", "oil"} <= set(s["planCurve"])
    check(camel(client.get(f"{W}/profile").json()), PROFILE, "profile")
    d = camel(client.get(f"{W}/dyno").json())
    check(d, DYNO, "dyno")
    assert all({"x", "f"} <= set(p) for p in d["surface"] + d["downhole"]) and "impact" in d


def test_plan_well_meta_contract(client, camel):
    p = camel(client.get(f"{W}/plan/next-cycle").json())
    check(p, PLAN, "plan")
    for side in ("practice", "mantle"):
        check(p[side], {**LEVERS, "injDays": NUM}, side)
    for k in LEVERS:
        assert len(p["ranges"][k]) == 2
    w = camel(client.get(W).json())
    check(w, WELL, "well")
    check(w["fluid"], FLUID, "fluid")
    assert isinstance(w["unit"]["gearboxRatingInlb"], float) and isinstance(w["completion"]["plungerIn"], float)
    assert {"count", "lengthM", "tapers"} <= set(w["rods"])
    m = camel(client.get("/api/meta").json())
    check(m, META, "meta")
    assert all("id" in x for x in m["models"]) and all({"id", "kind"} <= set(x) for x in m["sources"])
    a = camel(client.post(f"{W}/apply", json={"spm": 5.0, "kd": 0.5}).json())
    assert a["applied"] is True and isinstance(a["auditId"], str)


def test_live_contract(client, camel):
    with client.websocket_connect(f"{W}/live") as ws:
        m = camel(ws.receive_json())
    check(m, LIVE, "live")
    check(m["lastStroke"], {"n": int, "pounded": BOOL, "severity": NUM}, "lastStroke")


@pytest.mark.parametrize("path", ["state", "profile", "dyno", "health"])
def test_scenario_endpoints_are_stateless(client, camel, path):
    q = "?day=55&spm=6&kd=0.55&steam=900"
    assert client.get(f"{W}/{path}{q}").json() == client.get(f"{W}/{path}{q}").json()
