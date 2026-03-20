"""HTTP API client for drugfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install drugfyi[api]``

Usage::

    from drugfyi.api import DrugFYI

    with DrugFYI() as api:
        items = api.list_drug_classes()
        detail = api.get_drug_classe("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class DrugFYI:
    """API client for the drugfyi.com REST API.

    Provides typed access to all drugfyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://drugfyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://drugfyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_comparisons(self, **params: Any) -> dict[str, Any]:
        """List all comparisons."""
        return self._get("/api/v1/comparisons/", **params)

    def get_comparison(self, slug: str) -> dict[str, Any]:
        """Get comparison by slug."""
        return self._get(f"/api/v1/comparisons/" + slug + "/")

    def list_drug_classes(self, **params: Any) -> dict[str, Any]:
        """List all drug classes."""
        return self._get("/api/v1/drug-classes/", **params)

    def get_drug_classe(self, slug: str) -> dict[str, Any]:
        """Get drug classe by slug."""
        return self._get(f"/api/v1/drug-classes/" + slug + "/")

    def list_drug_targets(self, **params: Any) -> dict[str, Any]:
        """List all drug targets."""
        return self._get("/api/v1/drug-targets/", **params)

    def get_drug_target(self, slug: str) -> dict[str, Any]:
        """Get drug target by slug."""
        return self._get(f"/api/v1/drug-targets/" + slug + "/")

    def list_drugs(self, **params: Any) -> dict[str, Any]:
        """List all drugs."""
        return self._get("/api/v1/drugs/", **params)

    def get_drug(self, slug: str) -> dict[str, Any]:
        """Get drug by slug."""
        return self._get(f"/api/v1/drugs/" + slug + "/")

    def list_families(self, **params: Any) -> dict[str, Any]:
        """List all families."""
        return self._get("/api/v1/families/", **params)

    def get_family(self, slug: str) -> dict[str, Any]:
        """Get family by slug."""
        return self._get(f"/api/v1/families/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def list_guides(self, **params: Any) -> dict[str, Any]:
        """List all guides."""
        return self._get("/api/v1/guides/", **params)

    def get_guide(self, slug: str) -> dict[str, Any]:
        """Get guide by slug."""
        return self._get(f"/api/v1/guides/" + slug + "/")

    def list_interactions(self, **params: Any) -> dict[str, Any]:
        """List all interactions."""
        return self._get("/api/v1/interactions/", **params)

    def get_interaction(self, slug: str) -> dict[str, Any]:
        """Get interaction by slug."""
        return self._get(f"/api/v1/interactions/" + slug + "/")

    def list_journeys(self, **params: Any) -> dict[str, Any]:
        """List all journeys."""
        return self._get("/api/v1/journeys/", **params)

    def get_journey(self, slug: str) -> dict[str, Any]:
        """Get journey by slug."""
        return self._get(f"/api/v1/journeys/" + slug + "/")

    def list_milestones(self, **params: Any) -> dict[str, Any]:
        """List all milestones."""
        return self._get("/api/v1/milestones/", **params)

    def get_milestone(self, slug: str) -> dict[str, Any]:
        """Get milestone by slug."""
        return self._get(f"/api/v1/milestones/" + slug + "/")

    def list_side_effects(self, **params: Any) -> dict[str, Any]:
        """List all side effects."""
        return self._get("/api/v1/side-effects/", **params)

    def get_side_effect(self, slug: str) -> dict[str, Any]:
        """Get side effect by slug."""
        return self._get(f"/api/v1/side-effects/" + slug + "/")

    def list_target_interactions(self, **params: Any) -> dict[str, Any]:
        """List all target interactions."""
        return self._get("/api/v1/target-interactions/", **params)

    def get_target_interaction(self, slug: str) -> dict[str, Any]:
        """Get target interaction by slug."""
        return self._get(f"/api/v1/target-interactions/" + slug + "/")

    def list_therapeutic_areas(self, **params: Any) -> dict[str, Any]:
        """List all therapeutic areas."""
        return self._get("/api/v1/therapeutic-areas/", **params)

    def get_therapeutic_area(self, slug: str) -> dict[str, Any]:
        """Get therapeutic area by slug."""
        return self._get(f"/api/v1/therapeutic-areas/" + slug + "/")

    def list_tools(self, **params: Any) -> dict[str, Any]:
        """List all tools."""
        return self._get("/api/v1/tools/", **params)

    def get_tool(self, slug: str) -> dict[str, Any]:
        """Get tool by slug."""
        return self._get(f"/api/v1/tools/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> DrugFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
