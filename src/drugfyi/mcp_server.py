"""MCP server for drugfyi."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from drugfyi.api import DrugFYI

mcp = FastMCP("drugfyi")


@mcp.tool()
def search_drugfyi(query: str) -> dict[str, Any]:
    """Search drugfyi.com for content matching the query."""
    with DrugFYI() as api:
        return api.search(query)
