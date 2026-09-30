"""``mantle-ml`` command line: train / eval / report."""

from __future__ import annotations

import typer

app = typer.Typer(help="Mantle ML: train, evaluate and report on all models.", no_args_is_help=True)


@app.command()
def train(models: list[str] = typer.Argument(None, help="ids like M3 O1 (default with --all: everything)"),
          all_: bool = typer.Option(False, "--all", help="train every model"),
          quick: bool = typer.Option(False, "--quick", help="tiny subsets, seconds per model")) -> None:
    """Train models and write artifacts + eval.json + card.md into backend/models/<id>/."""
    from . import train as tr

    ids = [m.upper() for m in models] if models else None
    if not ids and not all_:
        raise typer.BadParameter("give model ids or --all")
    tr.train(ids, quick=quick, log=typer.echo)


@app.command("eval")
def eval_() -> None:
    """Print the eval.json primary metric of every trained model."""
    from .report import collect

    for mid, ev in collect().items():
        p = ev.get("primary", {})
        typer.echo(f"{mid:3s} {p.get('name', '?'):34s} {p.get('value')}  baseline={p.get('baseline')}  target={p.get('target')}")


@app.command()
def report() -> None:
    """Write backend/models/REPORT.md (all models vs baselines vs targets)."""
    from .report import write_report

    typer.echo(f"wrote {write_report()}")


if __name__ == "__main__":  # pragma: no cover
    app()
