"""Main FastMCP server and tool registration."""

from technitium_dns_mcp.mcp.mcp_dashboard import register_dashboard_tools
from technitium_dns_mcp.mcp.mcp_ingest import register_ingest_tools
from technitium_dns_mcp.mcp.mcp_user import register_user_tools
from technitium_dns_mcp.mcp.mcp_zones import register_zones_tools

# SDK discovery registers the register_<tag>_tools functions bound in this module.
__all__ = [
    "register_dashboard_tools",
    "register_ingest_tools",
    "register_user_tools",
    "register_zones_tools",
]
