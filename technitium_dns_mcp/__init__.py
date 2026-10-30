"""CONCEPT:AU-ECO.messaging.native-backend-abstraction Unified ecosystem initialization dynamic check."""

from scion_sdk.connector import Connector

from technitium_dns_mcp.api_client import Api
from technitium_dns_mcp.auth import get_client

connector = Connector(
    api=Api,
    get_client=get_client,
    tools="technitium_dns_mcp.mcp_server",
    instructions="Technitium DNS Server MCP Server - Managed dynamic operations.",
    transports=(
        "stdio",
        "streamable-http",
    ),
)
