"""Main FastMCP server and tool registration."""

from technitium_dns_mcp.mcp.mcp_ingest import register_ingest_tools

# SDK discovery registers the register_<tag>_tools functions bound in this module.
# Every Technitium operation is a typed tool derived from the Api client.
__all__ = ["register_ingest_tools"]
