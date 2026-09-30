"""DuckDB catalogue (``data/mantle.duckdb``) and the query helpers the API will use."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import duckdb
import pandas as pd

from .paths import db_path, processed_dir, reference_dir, synthetic_dir

# tables copied into the database file (small) from a parquet file under synthetic/ or processed/
SYNTH_TABLES = ["wells", "cycles", "cycle_daily", "failures", "unseats", "workovers", "optimiser_traces",
                "telemetry_events"]
PROCESSED_TABLES = ["weather", "threew_events", "volve_production"]
# large tables exposed as views over parquet (never copied)
VIEWS = {"telemetry": ("synthetic", "telemetry/*/*.parquet"), "dyno_cards": ("synthetic", "dyno_cards/*.parquet"),
         "threew_sample": ("processed", "threew_sample.parquet")}


def connect(path: Path | str | None = None, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    p = Path(path) if path else db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(p), read_only=read_only)


def _q(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def load(synthetic: Path | None = None, processed: Path | None = None, path: Path | str | None = None,
         viscosity_csv: Path | None = None) -> dict[str, int]:
    """(Re)create every table/view from whatever parquet exists; returns row counts."""
    syn = Path(synthetic) if synthetic else synthetic_dir()
    proc = Path(processed) if processed else processed_dir()
    counts: dict[str, int] = {}
    con = connect(path)
    try:
        for name in SYNTH_TABLES:
            f = syn / f"{name}.parquet"
            if f.exists():
                con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_parquet({_q(f)})")
        for name in PROCESSED_TABLES:
            f = proc / f"{name}.parquet"
            if f.exists():
                con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_parquet({_q(f)})")
        csv = viscosity_csv or reference_dir() / "viscosity_literature.csv"
        if csv.exists():
            con.execute(
                "CREATE OR REPLACE TABLE viscosity_lit AS SELECT *, 'real' AS source FROM "
                f"read_csv_auto({_q(csv)})"
            )
        for name, (root, pattern) in VIEWS.items():
            base = syn if root == "synthetic" else proc
            files = list(base.glob(pattern))
            if files:
                extra = ", hive_partitioning=true" if name == "telemetry" else ""
                con.execute(
                    f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_parquet({_q(base / pattern)}{extra})"
                )
        for (t,) in con.execute("SELECT table_name FROM information_schema.tables").fetchall():
            counts[t] = con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
    finally:
        con.close()
    return counts


def stats(path: Path | str | None = None) -> dict[str, int]:
    con = connect(path, read_only=True)
    try:
        return {t: con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
                for (t,) in con.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall()}
    finally:
        con.close()


class MantleDB:
    """Read helpers used by the API layer (one short-lived read-only connection per instance)."""

    def __init__(self, path: Path | str | None = None):
        self.con = connect(path, read_only=True)

    def close(self) -> None:
        self.con.close()

    def __enter__(self) -> MantleDB:
        return self

    def __exit__(self, *a) -> None:
        self.close()

    def _df(self, sql: str, *params) -> pd.DataFrame:
        return self.con.execute(sql, list(params)).df()

    def wells(self) -> pd.DataFrame:
        return self._df("SELECT * FROM wells ORDER BY well_id")

    def get_well(self, well_id: str) -> dict | None:
        df = self._df("SELECT * FROM wells WHERE well_id = ?", well_id)
        return None if df.empty else df.iloc[0].to_dict()

    def well_cycles(self, well_id: str) -> pd.DataFrame:
        return self._df("SELECT * FROM cycles WHERE well_id = ? ORDER BY cycle_no", well_id)

    def cycle_daily(self, well_id: str, cycle_no: int) -> pd.DataFrame:
        return self._df("SELECT * FROM cycle_daily WHERE well_id = ? AND cycle_no = ? ORDER BY day",
                        well_id, cycle_no)

    def failures(self, well_id: str) -> pd.DataFrame:
        return self._df("SELECT * FROM failures WHERE well_id = ? ORDER BY date", well_id)

    def as_of(self, well_id: str) -> date:
        r = self.con.execute("SELECT max(date) FROM cycle_daily WHERE well_id = ?", [well_id]).fetchone()[0]
        return r if r is not None else date.today()

    def unseats(self, well_id: str, months: int = 12, as_of: date | None = None) -> pd.DataFrame:
        """Unseat events in the ``months`` before ``as_of`` (default: the well's latest daily row)."""
        end = as_of or self.as_of(well_id)
        return self._df(
            "SELECT * FROM unseats WHERE well_id = ? AND date > (CAST(? AS DATE) - to_months(?)) "
            "AND date <= ? ORDER BY date", well_id, end, months, end,
        )

    def past_cycle_curves(self, well_id: str) -> list[dict]:
        """Completed cycles as arrays (day, oil, sandface T, viscosity, cum oil) for the Well View overlay."""
        out = []
        for c in self._df("SELECT cycle_no, cum_oil_bbl, sor, steam_t FROM cycles WHERE well_id = ? "
                          "AND complete ORDER BY cycle_no", well_id).to_dict("records"):
            d = self.cycle_daily(well_id, c["cycle_no"])
            out.append({
                "n": int(c["cycle_no"]), "cum_oil": float(c["cum_oil_bbl"]), "sor": float(c["sor"]),
                "steam_t": float(c["steam_t"]), "day": d["day"].tolist(), "oil": d["oil_bpd"].tolist(),
                "T": d["sandface_t_c"].tolist(), "mu": d["viscosity_cp"].tolist(),
                "cum": d["cum_oil_bbl"].tolist(),
            })
        return out

    def telemetry_window(self, well_id: str, t0: datetime | str, t1: datetime | str) -> pd.DataFrame:
        return self._df(
            "SELECT * FROM telemetry WHERE well_id = ? AND ts >= CAST(? AS TIMESTAMP) "
            "AND ts < CAST(? AS TIMESTAMP) ORDER BY ts", well_id, str(t0), str(t1),
        )
