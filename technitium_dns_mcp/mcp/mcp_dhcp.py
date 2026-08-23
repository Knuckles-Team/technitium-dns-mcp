"""MCP tools for Technitium DHCP scope and lease management."""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from technitium_dns_mcp.auth import get_client


def register_dhcp_tools(mcp: FastMCP):
    """Register Technitium DHCP scope and lease management tools.
    CONCEPT:TD-OS.config.tdns-3
    """

    @mcp.tool(tags={"dhcp"})
    async def technitium_dns_dhcp(
        action: str = Field(
            description=(
                "Action to perform. Must be one of: "
                "'list_scopes', 'get_scope', 'set_scope', 'enable_scope', "
                "'disable_scope', 'delete_scope', 'list_leases', 'remove_lease', "
                "'convert_to_reserved_lease', 'convert_to_dynamic_lease'"
            )
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of parameters matching the method signature.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> Any:
        """Manage Technitium DHCP scopes (create/update/enable/disable/delete) and leases (list/remove/convert)."""
        if ctx:
            await ctx.info(f"Executing DHCP action '{action}'...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_scopes":
            return client.list_scopes(**kwargs)
        if action == "get_scope":
            return client.get_scope(**kwargs)
        if action == "set_scope":
            return client.set_scope(**kwargs)
        if action == "enable_scope":
            return client.enable_scope(**kwargs)
        if action == "disable_scope":
            return client.disable_scope(**kwargs)
        if action == "delete_scope":
            return client.delete_scope(**kwargs)
        if action == "list_leases":
            return client.list_leases(**kwargs)
        if action == "remove_lease":
            return client.remove_lease(**kwargs)
        if action == "convert_to_reserved_lease":
            return client.convert_to_reserved_lease(**kwargs)
        if action == "convert_to_dynamic_lease":
            return client.convert_to_dynamic_lease(**kwargs)

        raise ValueError(f"Unknown DHCP action: {action}")
