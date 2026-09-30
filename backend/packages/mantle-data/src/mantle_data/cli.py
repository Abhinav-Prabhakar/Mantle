"""``mantle-data`` command line."""

from __future__ import annotations

import json

import typer

app = typer.Typer(help="Mantle data: fetch real datasets, build synthetic data, DuckDB.",
                  no_args_is_help=True)
fetch_app = typer.Typer(help="Fetch real datasets (idempotent, resumable).", no_args_is_help=True)
db_app = typer.Typer(help="DuckDB catalogue.", no_args_is_help=True)
app.add_typer(fetch_app, name="fetch")
app.add_typer(db_app, name="db")


def _progress():
    from tqdm import tqdm

    bar = tqdm(unit="B", unit_scale=True, desc="3W")
    last = [0]

    def cb(done: int, total: int | None) -> None:
        bar.total = total
        bar.update(done - last[0])
        last[0] = done

    return cb


def _fetch(which: str, convert: bool) -> None:
    from .fetch import threew, viscosity, volve, weather

    if which in ("weather", "all"):
        p = weather.fetch_weather()
        typer.echo(f"weather -> {p}")
    if which in ("viscosity", "all"):
        vs = viscosity.fetch_viscosity()
        typer.echo(f"viscosity -> {vs}")
    if which in ("volve", "all"):
        vp = volve.load_volve()
        typer.echo(f"volve -> {vp}")
    if which in ("3w", "all"):
        z = threew.fetch_3w(progress=_progress())
        typer.echo(f"3w zip -> {z}")
        if convert:
            r = threew.convert_3w(z)
            typer.echo(f"3w parquet -> {r}")


def _register_fetch() -> None:
    for name in ("3w", "weather", "viscosity", "volve", "all"):
        def cmd(convert: bool = typer.Option(True, help="convert 3W to parquet after download"), _n=name) -> None:
            _fetch(_n, convert)
        fetch_app.command(name)(cmd)


_register_fetch()


@app.command()
def build(scale: str = typer.Option("default", help="small | default | enormous"),
          only: str = typer.Option("", help="comma list of stages, e.g. S2,S4"),
          seed: int = typer.Option(20260930), no_db: bool = typer.Option(False, "--no-db")) -> None:
    """Generate physics-synthetic tables S1-S6 into data/synthetic and load DuckDB."""
    from .synth.build import build as run

    info = run(scale, only or None, seed, load_db=not no_db, log=typer.echo)
    total = sum(info["bytes"].values())
    typer.echo(json.dumps(dict(info["stages"]), indent=2, default=str))
    typer.echo(f"parquet total: {total / 1e6:.1f} MB")


@db_app.command("init")
def db_init() -> None:
    from . import db

    db.connect().close()
    typer.echo(f"initialised {db.db_path()}")


@db_app.command("load")
def db_load() -> None:
    from . import db

    for k, v in db.load().items():
        typer.echo(f"{k:20s} {v:>12,d}")


@db_app.command("stats")
def db_stats() -> None:
    from . import db

    for k, v in db.stats().items():
        typer.echo(f"{k:20s} {v:>12,d}")


if __name__ == "__main__":  # pragma: no cover
    app()
