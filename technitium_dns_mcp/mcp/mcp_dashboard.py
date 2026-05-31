"""MCP tools for Technitium DNS Dashboard metrics & analytics operations."""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from technitium_dns_mcp.auth import get_client


def register_dashboard_tools(mcp: FastMCP):
    """Register Technitium DNS dashboard analytics tools.
    CONCEPT:TDNS-002
    """

    @mcp.tool(tags={"dashboard"})
    async def technitium_dns_dashboard(
        action: str = Field(
            description=(
                "Action to perform. Must be one of: "
                "'get_metrics_json', 'get_metrics_text', 'get_stats', 'get_top_stats', "
                "'delete_all_stats'"
            )
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of parameters matching the method signature.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> Any:
        """Query Technitium DNS metrics, prometheus stats, category details, or delete statistics."""
        if ctx:
            await ctx.info(f"Executing Dashboard action '{action}'...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_metrics_json":
            return client.get_metrics_json(**kwargs)
        if action == "get_metrics_text":
            return client.get_metrics_text(**kwargs)
        if action == "get_stats":
            return client.get_stats(**kwargs)
        if action == "get_top_stats":
            return client.get_top_stats(**kwargs)
        if action == "delete_all_stats":
            return client.delete_all_stats(**kwargs)

        raise ValueError(f"Unknown Dashboard action: {action}")
