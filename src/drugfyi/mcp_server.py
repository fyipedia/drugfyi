"""MCP server for drugfyi — AI assistant tools for drugfyi.com.

Run: uvx --from "drugfyi[mcp]" python -m drugfyi.mcp_server
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DrugFYI")


@mcp.tool()
def list_drugs(limit: int = 20, offset: int = 0) -> str:
    """List drugs from drugfyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from drugfyi.api import DrugFYI

    with DrugFYI() as api:
        data = api.list_drugs(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No drugs found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def get_drug(slug: str) -> str:
    """Get detailed information about a specific drug.

    Args:
        slug: URL slug identifier for the drug.
    """
    from drugfyi.api import DrugFYI

    with DrugFYI() as api:
        data = api.get_drug(slug)
        return str(data)


@mcp.tool()
def list_interactions(limit: int = 20, offset: int = 0) -> str:
    """List interactions from drugfyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from drugfyi.api import DrugFYI

    with DrugFYI() as api:
        data = api.list_interactions(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No interactions found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def search_drug(query: str) -> str:
    """Search drugfyi.com for drugs, interactions, and pharmacology.

    Args:
        query: Search query string.
    """
    from drugfyi.api import DrugFYI

    with DrugFYI() as api:
        data = api.search(query)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return f"No results found for \"{query}\"."
        items = results[:10] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
