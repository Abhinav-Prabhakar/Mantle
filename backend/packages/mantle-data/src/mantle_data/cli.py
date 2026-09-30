"""``mantle-data`` command line."""

from __future__ import annotations

import json

import typer

app = typer.Typer(help="Mantle data: fetch real datasets, build synthetic data, run LLM synthesis, DuckDB.",
                  no_args_is_help=True)
fetch_app = typer.Typer(help="Fetch real datasets (idempotent, resumable).", no_args_is_help=True)
llm_app = typer.Typer(help="LLM-synthetic records (L1-L13).", no_args_is_help=True)
db_app = typer.Typer(help="DuckDB catalogue.", no_args_is_help=True)
app.add_typer(fetch_app, name="fetch")
app.add_typer(llm_app, name="llm")
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


@llm_app.command("list")
def llm_list() -> None:
    from .llm.spec import load_specs

    for s in load_specs().values():
        typer.echo(f"{s.id:4s} {s.name:24s} N={s.suggested_n:<7d} vars={','.join(s.variables)}")


@llm_app.command("estimate")
def llm_estimate(spec: str = typer.Argument("all"), n: int = typer.Option(0, help="override N"),
                 model: str = typer.Option("claude-sonnet-5-5")) -> None:
    from .llm.estimate import estimate

    for row in estimate(spec, n or None, model):
        typer.echo(json.dumps(row))


@llm_app.command("pack")
def llm_pack(spec: str = typer.Argument("all", help="L1..L13 or all"),
             n: int = typer.Option(0, help="NEW items to add (0 = starter default per spec)"),
             batch: int = typer.Option(0, help="items per file (0 = default per spec)"),
             seed: int = typer.Option(20260930), out: str = typer.Option("", help="packs dir (default: <repo>/llm-packs)"),
             retry_failed: bool = typer.Option(False, "--retry-failed", help="only failed/missing item_ids")) -> None:
    """Render paste-ready Markdown batches for a chat LLM."""
    from .llm.pack import pack as do_pack
    from .llm.pack import pack_retry, spec_ids
    from .llm.sampling import Context

    ctx = None if retry_failed else Context.load()
    for sid in spec_ids(spec):
        if retry_failed:
            r = pack_retry(sid, batch or None, out or None)
            typer.echo(f"{sid}: {r['items']} failed/missing items -> {r['batches']} retry file(s)")
        else:
            r = do_pack(sid, n or None, batch or None, seed, out or None, ctx)
            typer.echo(f"{sid}: {r['items']} items -> {r['batches']} file(s)")
        for f in r["files"]:
            typer.echo(f"  {f}")


@llm_app.command("import")
def llm_import(path: str = typer.Argument(..., help="reply file or directory (e.g. ../llm-packs)"),
               packs: str = typer.Option("", help="packs dir holding the manifests"),
               no_db: bool = typer.Option(False, "--no-db")) -> None:
    """Validate + dedupe chat-LLM replies and append them to data/llm/<spec>.jsonl and DuckDB."""
    from .llm.importer import format_report, import_replies

    typer.echo(format_report(import_replies(path, packs or None, load_db=not no_db)))


@llm_app.command("run")
def llm_run(spec: str, n: int = typer.Option(100), model: str = typer.Option("claude-sonnet-5-5"),
            provider: str = typer.Option("anthropic", help="anthropic | openai-compatible"),
            concurrency: int = typer.Option(8), dry_run: bool = typer.Option(False, "--dry-run"),
            seed: int = typer.Option(20260930), base_url: str = typer.Option("", help="OpenAI-compatible URL")) -> None:
    from .llm.runner import run

    res = run(spec, n, model=model, provider=provider, concurrency=concurrency, dry_run=dry_run, seed=seed,
              base_url=base_url or None)
    typer.echo(json.dumps(res, default=str))


if __name__ == "__main__":  # pragma: no cover
    app()
