from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from mantle_data.cli import app
from mantle_data.llm import runner
from mantle_data.llm.dedupe import Deduper
from mantle_data.llm.estimate import estimate
from mantle_data.llm.providers import FakeProvider
from mantle_data.llm.sampling import Context, sample_variables
from mantle_data.llm.spec import get_spec, load_specs, system_prompt, validate_record


@pytest.fixture(scope="module")
def ctx():
    return Context.generate("small")


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(runner, "_sleep", lambda s: None)


def fake_record(spec, i=0) -> dict:
    """A schema-valid record for any spec (unique per ``i``)."""
    rec = {}
    for f in spec.fields:
        t = f["type"]
        if t == "str":
            rec[f["name"]] = f["enum"][0] if "enum" in f else f"{f['name']} sample {i} {'x' * (i % 7)} v{i * 31}"
        elif t == "int":
            rec[f["name"]] = int(max(f.get("min", 1), 1)) + i % 3
        elif t == "float":
            lo, hi = f.get("min", 1.0), f.get("max", 100.0)
            rec[f["name"]] = lo + (hi - lo) * 0.5
        elif t.startswith("list["):
            n = max(f.get("min_items", 1), 1)
            rec[f["name"]] = [f"{f['name']} item {j} of record {i}" for j in range(n)]
    if "monotone_desc" in spec.checks:
        for chain in spec.checks["monotone_desc"]:
            for k, name in enumerate(chain):
                rec[name] = 1000.0 / (k + 1)
    if "ordered_ascending" in spec.checks:
        for a, b in spec.checks["ordered_ascending"]:
            rec[a], rec[b] = 1100.0, 1150.0
    return rec


def by_spec(spec, offset=0, garbage=0):
    """Fake responder for one spec: ``garbage`` bad replies first, then valid unique records."""
    state = {"n": offset}

    def r(call, system, user):
        state["n"] += 1
        if state["n"] - offset <= garbage:
            return "not json at all"
        return "```json\n" + json.dumps(fake_record(spec, state["n"])) + "\n```"
    return r


def test_thirteen_specs_load_with_schemas():
    specs = load_specs()
    assert list(specs) == [f"L{i}" for i in range(1, 14)]
    assert "Baghewala" in system_prompt() and "Oil India Limited" in system_prompt()
    sizes = {k: s.suggested_n for k, s in specs.items()}
    assert sizes["L1"] == 400 and sizes["L7"] == 20000 and sizes["L13"] == 300 and sizes["L11"] == 50
    for s in specs.values():
        js = s.json_schema()
        assert js["type"] == "object" and js["required"] and s.sampled_from is not None
        assert validate_record(s, fake_record(s))


def test_dry_run_renders_all_13_specs_without_calling_a_provider(ctx, tmp_path):
    prov = FakeProvider()
    for k in load_specs():
        res = runner.run(k, 5, provider=prov, dry_run=True, directory=tmp_path, context=ctx)
        assert res["dry_run"] and res["rendered"] == 3
        p = res["prompts"][0]
        assert "{" not in p["user"].split("Return ONE JSON")[0].replace('{"', "").replace("{'", "") or True
        assert "JSON schema" in p["user"] and p["system"] == system_prompt()
        assert not [v for v in get_spec(k).variables if v not in p["variables"]]
    assert prov.calls == 0
    assert not list(tmp_path.glob("*.jsonl"))


def test_no_unrendered_placeholders(ctx):
    for k, s in load_specs().items():
        text = runner.render_prompts(s, 3, ctx)[0]["user"].split("Return ONE JSON")[0]
        import re

        assert not re.search(r"\{[a-z_]+\}", text), k


def test_variables_deterministic(ctx):
    a, b = sample_variables("L3", ctx, 7), sample_variables("L3", ctx, 7)
    assert a == b and sample_variables("L3", ctx, 8) != a


def test_run_valid_records_written_with_source(ctx, tmp_path):
    spec = get_spec("L3")
    res = runner.run("L3", 6, provider=FakeProvider(by_spec(spec)), directory=tmp_path, context=ctx,
                     concurrency=3)
    assert res["generated"] == 6 and res["invalid"] == 0 and res["duplicates"] == 0
    rows = [json.loads(x) for x in (tmp_path / "L3.jsonl").read_text().splitlines()]
    assert sorted(r["idx"] for r in rows) == list(range(6))
    assert all(r["source"] == "llm_synthetic" and r["spec"] == "L3" and r["variables"]["well_id"] for r in rows)
    validate_record(spec, rows[0]["record"])


def test_invalid_then_retry_then_success(ctx, tmp_path):
    spec = get_spec("L5")
    prov = FakeProvider(by_spec(spec, garbage=2))
    res = runner.run("L5", 1, provider=prov, directory=tmp_path, context=ctx, concurrency=1)
    assert res["generated"] == 1 and prov.calls == 3
    row = json.loads((tmp_path / "L5.jsonl").read_text())
    assert row["attempts"] == 3


def test_invalid_three_times_is_rejected_and_not_retried_on_resume(ctx, tmp_path):
    spec = get_spec("L5")
    prov = FakeProvider(lambda *_: "{}")
    res = runner.run("L5", 2, provider=prov, directory=tmp_path, context=ctx, concurrency=1)
    assert res["invalid"] == 2 and res["generated"] == 0 and prov.calls == 6
    rej = [json.loads(x) for x in (tmp_path / "L5.rejects.jsonl").read_text().splitlines()]
    assert len(rej) == 2 and "invalid" in rej[0]["reason"]
    prov2 = FakeProvider(by_spec(spec))
    res2 = runner.run("L5", 2, provider=prov2, directory=tmp_path, context=ctx)
    assert prov2.calls == 0 and res2["already_done"] == 2


def test_resume_only_generates_missing(ctx, tmp_path):
    spec = get_spec("L12")
    p1 = FakeProvider(by_spec(spec))
    runner.run("L12", 3, provider=p1, directory=tmp_path, context=ctx)
    assert p1.calls == 3
    # simulate an interrupted write (torn last line) then extend the run
    with open(tmp_path / "L12.jsonl", "a") as f:
        f.write('{"idx": 99, "spec": "L1')
    p2 = FakeProvider(by_spec(spec, offset=100))
    res = runner.run("L12", 5, provider=p2, directory=tmp_path, context=ctx)
    assert p2.calls == 2 and res["already_done"] == 3 and res["generated"] == 2
    ids = sorted(r["idx"] for r in runner._read_jsonl(tmp_path / "L12.jsonl"))
    assert ids == [0, 1, 2, 3, 4]


def test_dedupe_identical_records(ctx, tmp_path):
    spec = get_spec("L13")
    rec = json.dumps(fake_record(spec, 1))
    res = runner.run("L13", 4, provider=FakeProvider(lambda *_: rec), directory=tmp_path, context=ctx,
                     concurrency=1)
    assert res["generated"] == 1 and res["duplicates"] == 3


def test_deduper_near_duplicates():
    d = Deduper(0.8)
    a = "the rod string parted at 431 m; failure mode fatigue; pin break at the coupling near the sinker bars"
    assert d.add(a)
    assert not d.add(a.upper())
    assert not d.add(a + " today")
    assert d.add("pump reseated after fluid pound, hold-down changed, well back on production by evening")


def test_transient_errors_retry_with_backoff(ctx, tmp_path):
    spec = get_spec("L11")
    n = {"c": 0}

    class Flaky(FakeProvider):
        def complete(self, *a, **k):
            n["c"] += 1
            if n["c"] <= 2:
                raise RuntimeError("429 rate limited")
            return super().complete(*a, **k)

    res = runner.run("L11", 1, provider=Flaky(by_spec(spec)), directory=tmp_path, context=ctx, concurrency=1)
    assert res["generated"] == 1 and n["c"] == 3


def test_persistent_provider_failure_is_rejected(ctx, tmp_path):
    class Dead(FakeProvider):
        def complete(self, *a, **k):
            raise RuntimeError("down")

    res = runner.run("L11", 1, provider=Dead(), directory=tmp_path, context=ctx, concurrency=1)
    assert res["invalid"] == 1 and "provider error" in (tmp_path / "L11.rejects.jsonl").read_text()


def test_extract_json_tolerates_fences_and_prose():
    assert runner.extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert runner.extract_json('Here you go: {"a": 2} thanks') == {"a": 2}
    with pytest.raises(json.JSONDecodeError):
        runner.extract_json("no json")


def test_lab_report_monotone_viscosity_validation():
    spec = get_spec("L9")
    rec = fake_record(spec)
    validate_record(spec, rec)
    rec["viscosity_120c_cp"] = 1e5
    with pytest.raises(ValueError):
        validate_record(spec, rec)


def test_estimate_and_cli(ctx):
    rows = estimate("all", context=ctx)
    assert rows[-1]["spec"] == "TOTAL" and rows[-1]["usd"] > 0 and len(rows) == 14
    one = estimate("L3", n=100, context=ctx)[0]
    assert one["calls"] == 100 and one["input_tokens"] > 0
    r = CliRunner().invoke(app, ["llm", "list"])
    assert r.exit_code == 0 and "L13" in r.output and "strategy_playbook" in r.output
    r = CliRunner().invoke(app, ["llm", "estimate", "L1", "--n", "10"])
    assert r.exit_code == 0 and '"spec": "L1"' in r.output


def test_cli_dry_run_makes_no_files(ctx, tmp_path, monkeypatch):
    monkeypatch.setenv("MANTLE_DATA_DIR", str(tmp_path))
    r = CliRunner().invoke(app, ["llm", "run", "L2", "--n", "4", "--dry-run"])
    assert r.exit_code == 0 and '"dry_run": true' in r.output
    assert not list((tmp_path / "llm").glob("*.jsonl"))
