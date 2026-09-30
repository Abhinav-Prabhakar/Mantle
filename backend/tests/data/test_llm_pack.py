from __future__ import annotations

import json
import re

import pytest
from typer.testing import CliRunner

from mantle_data.cli import app
from mantle_data.llm import pack as P
from mantle_data.llm.importer import import_replies, parse_reply
from mantle_data.llm.sampling import Context
from mantle_data.llm.spec import get_spec, load_specs

from .test_llm import fake_record


@pytest.fixture(scope="module")
def ctx():
    return Context.generate("small")


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("MANTLE_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("MANTLE_PACKS_DIR", str(tmp_path / "packs"))
    return tmp_path


def reply_for(spec_id, ids, offset=0):
    spec = get_spec(spec_id)
    return [{"item_id": i, **fake_record(spec, offset + k)} for k, i in enumerate(ids)]


def test_every_spec_renders_without_placeholders(ctx, env):
    for sid, spec in load_specs().items():
        r = P.pack(sid, n=4, batch=3, ctx=ctx)
        assert r["batches"] == 2
        text = (env / "packs" / sid / f"{sid}_batch_001.md").read_text()
        for v in spec.variables:
            assert "{" + v + "}" not in text, (sid, v)
        assert "## Output contract" in text and "exactly 3 objects" in text and f"item_id: {sid}-00000" in text
        assert '"item_id"' in text and "JSON schema" in text and "Baghewala" in text
    assert set(P.DEFAULTS) == set(load_specs())


def test_pack_appends_new_items(ctx, env):
    P.pack("L4", n=3, batch=2, ctx=ctx)
    P.pack("L4", n=2, batch=2, ctx=ctx)
    m = P.read_manifest(env / "packs" / "L4")
    assert [x["idx"] for x in m] == [0, 1, 2, 3, 4] and [x["batch"] for x in m] == [1, 1, 2, 3, 3]


def test_parse_reply_tolerates_noise():
    txt = ('Sure! Here you go:\n```json\n[{"item_id": "L3-00000", "a": 1},\n {"item_id": "L3-00001", "a": "}"}]\n```\n'
           "Hope it helps [x]")
    assert [o["item_id"] for o in parse_reply(txt)] == ["L3-00000", "L3-00001"]
    assert parse_reply('{"items": [{"item_id": "L3-00002"}]}')[0]["item_id"] == "L3-00002"


def test_import_roundtrip_reject_dedupe_idempotent_retry(ctx, env):
    P.pack("L3", n=6, batch=3, ctx=ctx)
    ids = [f"L3-{i:05d}" for i in range(6)]
    good = reply_for("L3", ids[:3])
    bad = {**reply_for("L3", [ids[3]], 10)[0], "depth_m": 99999}       # violates max
    dup = {**good[0], "item_id": ids[4]}                                # same text as L3-00000
    reps = env / "packs" / "L3" / "replies"
    (reps / "a.md").write_text("Here is the JSON:\n```json\n" + json.dumps(good) + "\n```\nDone.")
    (reps / "b.txt").write_text(json.dumps([bad, dup]))
    rep = import_replies(env / "packs")
    r = rep["specs"]["L3"]
    assert sorted(r["accepted"]) == ids[:3]
    assert [x["item_id"] for x in r["rejected"]] == [ids[3]] and "depth_m" in r["rejected"][0]["reason"]
    assert [x["item_id"] for x in r["duplicates"]] == [ids[4]]
    assert r["missing"] == [ids[5]]
    rows = [json.loads(x) for x in (env / "data" / "llm" / "L3.jsonl").read_text().splitlines()]
    assert len(rows) == 3 and all(x["source"] == "llm_synthetic" and "item_id" not in x["record"] for x in rows)
    assert rows[0]["variables"]["well_id"] and rows[0]["item_id"] == ids[0]
    assert rep["db_rows"] == 3
    # idempotent
    rep2 = import_replies(env / "packs")
    assert rep2["specs"]["L3"]["accepted"] == [] and len(rep2["specs"]["L3"]["already_imported"]) == 3
    assert len((env / "data" / "llm" / "L3.jsonl").read_text().splitlines()) == 3
    # retry only the failed / missing ids (not the accepted, not the duplicate)
    r = P.pack_retry("L3", out=env / "packs")
    assert sorted(r["item_ids"]) == [ids[3], ids[5]] and r["batches"] == 1
    text = (env / "packs" / "L3" / "L3_retry_001.md").read_text()
    assert ids[3] in text and ids[5] in text and ids[0] not in text and "previous attempt was rejected" in text
    # fixing them clears the status
    (reps / "c.json").write_text(json.dumps(reply_for("L3", [ids[3], ids[5]], 50)))
    rep3 = import_replies(env / "packs")
    assert sorted(rep3["specs"]["L3"]["accepted"]) == [ids[3], ids[5]]
    assert P.pack_retry("L3", out=env / "packs")["items"] == 0
    assert not list((env / "packs" / "L3").glob("*_retry_*.md"))


def test_unknown_and_missing_item_ids_and_garbage(ctx, env):
    P.pack("L5", n=2, batch=2, ctx=ctx)
    reps = env / "packs" / "L5" / "replies"
    (reps / "x.json").write_text(json.dumps([{"item_id": "L5-09999"}, {"foo": 1}]))
    (reps / "y.txt").write_text("sorry, I cannot")
    rep = import_replies(reps, env / "packs")
    assert len(rep["unparseable"]) == 1
    reasons = [x["reason"] for r in rep["specs"].values() for x in r["rejected"]]
    assert any("unknown item_id" in x for x in reasons) and any("malformed item_id" in x for x in reasons)


def test_cli_pack_and_import(ctx, env, monkeypatch):
    monkeypatch.setattr(Context, "load", classmethod(lambda cls, synthetic=None: ctx))
    run = CliRunner().invoke
    res = run(app, ["llm", "pack", "L13", "--n", "4", "--batch", "2"])
    assert res.exit_code == 0 and "4 items -> 2 file(s)" in res.output
    ids = [f"L13-{i:05d}" for i in range(4)]
    f = env / "packs" / "L13" / "replies" / "r.json"
    f.write_text(json.dumps(reply_for("L13", ids[:2])[:1]))
    res = run(app, ["llm", "import", str(f)])
    assert res.exit_code == 0 and "accepted 1" in res.output and "missing 1" in res.output
    res = run(app, ["llm", "pack", "L13", "--retry-failed"])
    assert "1 failed/missing items" in res.output and re.search(r"L13_retry_001\.md", res.output)
