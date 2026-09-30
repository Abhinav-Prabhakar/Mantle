"""DuckDB access: read the well's records (S1 roster, S2 cycles, S5 failures/unseats/workovers), write the audit log."""

from __future__ import annotations

import json
import threading
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

AUDIT_DDL = """CREATE TABLE IF NOT EXISTS audit_log (
    audit_id VARCHAR PRIMARY KEY, ts TIMESTAMP, well_id VARCHAR, action VARCHAR, payload VARCHAR, actor VARCHAR)"""


class UnknownWellError(KeyError):
    pass


@dataclass
class WellData:
    row: dict[str, Any]
    cycles: pd.DataFrame
    workovers: pd.DataFrame
    failures: pd.DataFrame
    unseats: pd.DataFrame
    as_of: date

    @property
    def well_id(self) -> str:
        return str(self.row["well_id"])

    @property
    def current(self) -> dict[str, Any]:
        """The in-progress cycle (highest cycle number)."""
        return self.cycles.iloc[-1].to_dict()

    @property
    def cycle_no(self) -> int:
        return int(self.current["cycle_no"])

    @property
    def current_day(self) -> int:
        return int(self.current["n_days"]) - 1

    @property
    def cycle_start(self) -> date:
        return _d(self.current["start_date"])

    def scenario_date(self, day: float) -> date:
        return self.cycle_start + timedelta(days=int(round(day)))


def _d(v: Any) -> date:
    return v.date() if isinstance(v, (datetime, pd.Timestamp)) else v


class Store:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.con = duckdb.connect(str(self.path))
        self.lock = threading.RLock()
        with self.lock:
            self.con.execute(AUDIT_DDL)
        self._wells: dict[str, WellData] = {}
        self._roster: pd.DataFrame | None = None

    def close(self) -> None:
        with self.lock:
            self.con.close()

    def _df(self, sql: str, *params: Any) -> pd.DataFrame:
        with self.lock:
            return self.con.cursor().execute(sql, list(params)).df()

    def roster(self) -> pd.DataFrame:
        if self._roster is None:
            self._roster = self._df("SELECT * FROM wells ORDER BY well_id")
        return self._roster

    def well(self, well_id: str) -> WellData:
        if well_id in self._wells:
            return self._wells[well_id]
        r = self.roster()
        r = r[r.well_id == well_id]
        if r.empty:
            raise UnknownWellError(well_id)
        cycles = self._df("SELECT * FROM cycles WHERE well_id = ? ORDER BY cycle_no", well_id)
        if cycles.empty:
            raise UnknownWellError(well_id)
        row = {k: (v.item() if hasattr(v, "item") else v) for k, v in r.iloc[0].to_dict().items()}
        as_of = self._df("SELECT max(date) AS d FROM cycle_daily WHERE well_id = ?", well_id)["d"].iloc[0]
        wd = WellData(
            row=row, cycles=cycles,
            workovers=self._df("SELECT * FROM workovers WHERE well_id = ? ORDER BY date", well_id),
            failures=self._df("SELECT * FROM failures WHERE well_id = ? ORDER BY date", well_id),
            unseats=self._df("SELECT * FROM unseats WHERE well_id = ? ORDER BY date", well_id),
            as_of=_d(as_of),
        )
        self._wells[well_id] = wd
        return wd

    def past_cycles(self, well_id: str) -> list[dict]:
        """Completed cycles with their daily oil (bbl/d) by actual cycle day."""
        out = []
        cyc = self._df("SELECT cycle_no, soak_days, cum_oil_bbl, steam_t, spm, kd, cutoff_day FROM cycles "
                       "WHERE well_id = ? AND complete ORDER BY cycle_no", well_id)
        for c in cyc.to_dict("records"):
            d = self._df("SELECT day, oil_bpd FROM cycle_daily WHERE well_id = ? AND cycle_no = ? ORDER BY day",
                         well_id, int(c["cycle_no"]))
            out.append({**c, "day": d["day"].to_numpy(), "oil": d["oil_bpd"].to_numpy()})
        return out

    def table_count(self, table: str) -> int:
        try:
            return int(self._df(f'SELECT count(*) AS n FROM "{table}"')["n"].iloc[0])
        except duckdb.Error:
            return 0

    def audit(self, well_id: str, action: str, payload: dict, actor: str = "api") -> dict:
        aid = "AUD-" + uuid.uuid4().hex[:12]
        now = datetime.now().replace(microsecond=0)
        with self.lock:
            self.con.cursor().execute("INSERT INTO audit_log VALUES (?, ?, ?, ?, ?, ?)",
                                      [aid, now, well_id, action, json.dumps(payload), actor])
        return {"audit_id": aid, "at": now.isoformat()}

    def audit_rows(self, well_id: str | None = None) -> pd.DataFrame:
        if well_id:
            return self._df("SELECT * FROM audit_log WHERE well_id = ? ORDER BY ts", well_id)
        return self._df("SELECT * FROM audit_log ORDER BY ts")


def maint_per_day(wd: WellData, on: date, window_days: int) -> float:
    """Recorded workover cost in the ``window_days`` before ``on`` (S5), per day."""
    w = wd.workovers
    if w.empty:
        return 0.0
    dates = pd.to_datetime(w["date"]).dt.date
    m = (dates > on - timedelta(days=window_days)) & (dates <= on)
    return float(w.loc[m, "cost_inr"].sum()) / window_days


def days_since_workover(wd: WellData, on: date) -> float:
    w = wd.workovers
    dates = [d for d in pd.to_datetime(w["date"]).dt.date if d <= on] if not w.empty else []
    return float((on - max(dates)).days) if dates else 365.0


def taper_at(sections: list[dict], depth: float) -> str:
    for s in sections:
        if depth <= s["to"]:
            return s["label"]
    return sections[-1]["label"]


def rod_sections(row: dict) -> list[dict]:
    return json.loads(row["rod_sections"])


def to_np(a: Any) -> np.ndarray:
    return np.asarray(a, dtype=float)
