"""Wire-First MCP tool: natively ingest Technitium DNS state into the epistemic-graph.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Lists zones (and, per zone, their
records) via the real client and pushes them into the knowledge graph as typed
``:DnsZone`` / ``:DnsRecord`` / ``:DnsServerNode`` nodes. Best-effort: returns
``{"ingested": None}`` when no engine is reachable.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from technitium_dns_mcp.auth import get_client


def register_ingest_tools(mcp: FastMCP):
    """Register the native KG ingestion tool for Technitium DNS."""

    @mcp.tool(tags={"ingest", "kg"})
    async def technitium_ingest_zones(
        params_json: str = Field(
            default="{}",
            description=(
                "JSON string of options: {'node': <server node>, 'include_records': "
                "true|false (default true), 'max_zones': <int cap for record fetch>}."
            ),
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> Any:
        """Natively ingest Technitium DNS zones (+ their records) into epistemic-graph.

        Lists authoritative zones via ``list_zones`` and pushes them as typed
        ``:DnsZone`` nodes (linked to the ``:DnsServerNode``); for each zone it also
        pulls records via ``get_records`` and ingests ``:DnsRecord`` nodes linked with
        ``:recordInZone``. Best-effort — returns ``{"ingested": None}`` with no engine.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json

        from technitium_dns_mcp.kg_ingest import ingest_records, ingest_zones

        try:
            opts = json.loads(params_json) if params_json else {}
        except Exception as e:  # noqa: BLE001
            return {"error": f"Invalid params_json: {e}"}

        node = opts.get("node")
        include_records = opts.get("include_records", True)
        max_zones = opts.get("max_zones")

        if ctx:
            await ctx.info("Ingesting Technitium DNS zones into the knowledge graph...")

        zones_resp = client.list_zones(node=node) if node else client.list_zones()
        zone_result = ingest_zones(zones_resp, node=node)

        record_results: dict[str, Any] = {}
        if include_records:
            data = (
                zones_resp.get("response", zones_resp)
                if isinstance(zones_resp, dict)
                else {}
            )
            zones = data.get("zones", []) if isinstance(data, dict) else []
            names = [
                z.get("name") for z in zones if isinstance(z, dict) and z.get("name")
            ]
            if isinstance(max_zones, int):
                names = names[:max_zones]
            for name in names:
                try:
                    recs = client.get_records(
                        domain=name, zone=name, list_zone=True, node=node
                    )
                    record_results[name] = ingest_records(recs, name, node=node)
                except Exception as e:  # noqa: BLE001 — per-zone best-effort
                    if ctx:
                        await ctx.info(f"Skipped records for zone {name}: {e}")

        return {"zones": zone_result, "records": record_results}
