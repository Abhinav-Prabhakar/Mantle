from __future__ import annotations

import io
import json
import zipfile
from datetime import date

import httpx
import numpy as np
import pandas as pd
import pytest

from mantle_data import schemas as S
from mantle_data.fetch import common, threew, viscosity, volve, weather

# ---------------------------------------------------------------- resumable download


def make_transport(content: bytes, fail_first: int = 0, ignore_range: bool = False):
    state = {"n": 0, "ranges": []}

    def handler(req: httpx.Request) -> httpx.Response:
        state["n"] += 1
        if state["n"] <= fail_first:
            return httpx.Response(500)
        rng = req.headers.get("range")
        state["ranges"].append(rng)
        if rng and not ignore_range:
            start = int(rng.split("=")[1].split("-")[0])
            if start >= len(content):
                return httpx.Response(416)
            body = content[start:]
            return httpx.Response(206, content=body, headers={
                "content-range": f"bytes {start}-{len(content) - 1}/{len(content)}"})
        return httpx.Response(200, content=content)

    return httpx.MockTransport(handler), state


def client(tr):
    return httpx.Client(transport=tr, follow_redirects=True)


def test_download_resumes_partial_file(tmp_path):
    data = np.random.default_rng(0).bytes(50_000)
    dest = tmp_path / "f.bin"
    dest.write_bytes(data[:12_345])
    tr, st = make_transport(data)
    common.download("http://x/f", dest, expected_size=len(data), client=client(tr), backoff=0)
    assert dest.read_bytes() == data and st["ranges"] == ["bytes=12345-"]
    assert common.sha256_file(dest) == common.sha256_bytes(data)


def test_download_idempotent_when_complete(tmp_path):
    data = b"abc" * 100
    dest = tmp_path / "f.bin"
    dest.write_bytes(data)
    tr, st = make_transport(data)
    common.download("http://x/f", dest, expected_size=len(data), client=client(tr), backoff=0)
    assert st["n"] == 0
    common.download("http://x/f", dest, client=client(tr), backoff=0)     # size unknown: 416 -> done
    assert dest.read_bytes() == data


def test_download_retries_then_succeeds_and_restarts_if_range_ignored(tmp_path):
    data = b"z" * 5000
    tr, st = make_transport(data, fail_first=2)
    dest = tmp_path / "a.bin"
    common.download("http://x/f", dest, client=client(tr), backoff=0)
    assert dest.read_bytes() == data and st["n"] == 3
    dest2 = tmp_path / "b.bin"
    dest2.write_bytes(b"junk")
    tr2, _ = make_transport(data, ignore_range=True)
    common.download("http://x/f", dest2, client=client(tr2), backoff=0)
    assert dest2.read_bytes() == data


def test_download_gives_up_after_max_retries(tmp_path):
    tr, _ = make_transport(b"x", fail_first=99)
    with pytest.raises(httpx.HTTPError):
        common.download("http://x/f", tmp_path / "c.bin", client=client(tr), backoff=0, max_retries=3)


def test_licenses_file_is_idempotent(tmp_path):
    common.update_licenses(tmp_path, "R2", "one")
    common.update_licenses(tmp_path, "R1", "two")
    common.update_licenses(tmp_path, "R2", "one v2")
    t = (tmp_path / "LICENSES.md").read_text()
    assert t.count("## R2") == 1 and "one v2" in t and "## R1" in t


# ---------------------------------------------------------------- weather (mocked Open-Meteo)


def om_payload(a: date, b: date) -> dict:
    ts = pd.date_range(a, b + pd.Timedelta(days=1), freq="h", inclusive="left")
    n = len(ts)
    return {"hourly": {"time": [t.strftime("%Y-%m-%dT%H:%M") for t in ts],
                       "temperature_2m": list(np.linspace(10, 40, n)), "relative_humidity_2m": [30.0] * n,
                       "wind_speed_10m": [8.0] * n, "shortwave_radiation": [100.0] * n}}


def test_weather_fetch_offline_idempotent(tmp_path, monkeypatch):
    monkeypatch.setenv("MANTLE_DATA_DIR", str(tmp_path))
    calls = []

    def handler(req: httpx.Request) -> httpx.Response:
        q = dict(req.url.params)
        calls.append(q)
        assert q["latitude"] == "27.95" and q["longitude"] == "71.95" and q["timezone"] == "Asia/Kolkata"
        assert q["hourly"] == "temperature_2m,relative_humidity_2m,wind_speed_10m,shortwave_radiation"
        return httpx.Response(200, json=om_payload(date.fromisoformat(q["start_date"]),
                                                   date.fromisoformat(q["end_date"])))

    c = httpx.Client(transport=httpx.MockTransport(handler))
    p = weather.fetch_weather(end=date(2019, 3, 31), client=c)
    df = pd.read_parquet(p)
    assert df["ts"].min() == pd.Timestamp("2018-01-01") and df["ts"].max() == pd.Timestamp("2019-03-31 23:00")
    assert len(df) == (365 + 90) * 24 and df["source"].eq("real").all()
    assert len(calls) == 2
    weather.fetch_weather(end=date(2019, 3, 31), client=c)          # cached: no new requests
    assert len(calls) == 2
    assert "CC BY 4.0" in (tmp_path / "raw" / "LICENSES.md").read_text()
    S.validate_frame(S.Weather, df.drop(columns=[]), sample=50)


# ---------------------------------------------------------------- 3W (fixture zip)


def make_3w_zip(path, per_class=3):
    rng = np.random.default_rng(0)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("dataset/dataset.ini", "[x]")
        for cls in range(10):
            for k in range(per_class):
                origin = ["WELL", "SIMULATED", "DRAWN"][k % 3]
                idx = pd.date_range("2017-01-01", periods=600, freq="s")
                df = pd.DataFrame({"P-PDG": rng.normal(2e7, 1e5, 600), "T-TPT": rng.normal(100, 1, 600),
                                   "class": np.where(np.arange(600) > 300, cls, 0), "state": 0}, index=idx)
                df.index.name = "timestamp"
                buf = io.BytesIO()
                df.to_parquet(buf)
                z.writestr(f"dataset/{cls}/{origin}-{cls}000{k}_2017010100000{k}.parquet", buf.getvalue())


def test_threew_convert_index_and_sample(tmp_path):
    zp = tmp_path / "3w.zip"
    make_3w_zip(zp)
    out = tmp_path / "proc"
    res = threew.convert_3w(zp, out, sample_per_class=2, sample_freq="60s")
    idx = pd.read_parquet(res["index"])
    assert len(idx) == 30 and set(idx["event_class"]) == set(range(10)) and idx["n_rows"].eq(600).all()
    assert set(idx["origin"]) == {"real", "simulated", "drawn"}
    S.validate_frame(S.ThreeWEvent, idx.assign(path=idx["path"]), sample=None)
    one = pd.read_parquet(res["dir"] / "class=3" / f"{idx[idx.event_class == 3].iloc[0]['instance_id']}.parquet")
    assert {"timestamp", "p_pdg", "t_tpt", "class", "instance_id", "event_class"} <= set(one.columns)
    assert one["p_pdg"].dtype == np.float32
    sm = pd.read_parquet(res["sample"])
    assert set(sm["event_class"]) == set(range(10)) and sm["instance_id"].nunique() == 20
    assert len(sm) < 20 * 600 and sm["source"].eq("real").all()
    # real instances are preferred in the sample
    assert (sm.groupby("event_class")["origin"].apply(lambda s: "real" in set(s))).all()
    again = threew.convert_3w(zp, out, sample_per_class=2)          # idempotent: reuses converted files
    assert len(pd.read_parquet(again["index"])) == 30


def test_threew_fetch_records_checksum_and_licence(tmp_path, monkeypatch):
    monkeypatch.setenv("MANTLE_DATA_DIR", str(tmp_path))
    data = b"PK" + b"0" * 5000

    def handler(req):
        r = req.headers.get("range")
        if r == "bytes=0-0":
            return httpx.Response(206, content=data[:1], headers={"content-range": f"bytes 0-0/{len(data)}"})
        return httpx.Response(200, content=data)

    real = httpx.Client
    monkeypatch.setattr(httpx, "Client", lambda **kw: real(transport=httpx.MockTransport(handler),
                                                           **{k: v for k, v in kw.items() if k != "transport"}))
    z = threew.fetch_3w()
    assert z.read_bytes() == data
    man = json.loads((tmp_path / "raw" / "3w_manifest.json").read_text())
    assert man["sha256"] == common.sha256_bytes(data) and man["size"] == len(data)
    lic = (tmp_path / "raw" / "LICENSES.md").read_text()
    assert "CC BY 4.0" in lic and "Vargas" in lic


def test_threew_class_names_cover_all_ten_events():
    assert sorted(threew.EVENT_NAMES) == list(range(10))
    assert threew.parse_instance("dataset/1/WELL-00001_20140124213136.parquet")["origin"] == "real"
    assert threew.parse_instance("SIMULATED-00007_20180101000000.parquet")["origin"] == "simulated"


# ---------------------------------------------------------------- viscosity + volve


def test_viscosity_reference_csv_committed_and_valid():
    from mantle_data.paths import BACKEND_DIR

    df = pd.read_csv(BACKEND_DIR / "data" / "reference" / "viscosity_literature.csv")
    assert list(df.columns) == viscosity.COLUMNS
    assert df["licence"].eq("CC BY 4.0").all() and df["citation"].str.contains("s13202-015-0184-8").all()
    assert set(df["data_kind"]) == {"column_statistic"}
    S.validate_frame(S.ViscosityLit, df.assign(source="real", density_g_cc=df["density_g_cc"]).drop(
        columns=[]), sample=None)
    assert df["temperature_c"].between(20, 160).all() and df["api"].between(11.7, 18.8).all()


def test_viscosity_table1_transcription_checks():
    rows = viscosity.rows_from(viscosity.TABLE1)
    assert [r["sample_id"] for r in rows] == ["ALOMAIR2016-T1-mean", "ALOMAIR2016-T1-min", "ALOMAIR2016-T1-max"]
    pdf = viscosity.raw_dir() / viscosity.PDF_NAME
    if pdf.exists():
        assert viscosity.extract_table1(pdf) == viscosity.TABLE1


def test_volve_skips_when_absent(tmp_path, capsys):
    assert volve.load_volve(tmp_path / "nope.xlsx") is None
    assert "skipping" in capsys.readouterr().out


def test_volve_loads_user_supplied_workbook(tmp_path, monkeypatch):
    monkeypatch.setenv("MANTLE_DATA_DIR", str(tmp_path))
    x = tmp_path / "volve.xlsx"
    pd.DataFrame({"DATEPRD": pd.date_range("2010-01-01", periods=5), "BORE_OIL_VOL": [1, 2, 3, 4, 5]}).to_excel(
        x, index=False)
    out = volve.load_volve(x)
    df = pd.read_parquet(out)
    assert len(df) == 5 and df["source"].eq("real").all() and "date" in df


# ---------------------------------------------------------------- network (skipped by default)


@pytest.mark.network
def test_network_weather_small_range(tmp_path, monkeypatch):
    monkeypatch.setenv("MANTLE_DATA_DIR", str(tmp_path))
    p = weather.fetch_weather(end=date(2018, 1, 10))
    assert len(pd.read_parquet(p)) == 10 * 24


@pytest.mark.network
def test_network_3w_remote_size():
    assert threew.remote_size() > 1_000_000_000
