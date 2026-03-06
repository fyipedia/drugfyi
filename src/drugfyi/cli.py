"""Command-line interface for drugfyi."""

from __future__ import annotations

import json

import typer

from drugfyi.api import DrugFYI

app = typer.Typer(help="DrugFYI — Drug interactions and pharmacology API client.")


@app.command()
def search(query: str) -> None:
    """Search drugfyi.com."""
    with DrugFYI() as api:
        result = api.search(query)
        typer.echo(json.dumps(result, indent=2))
