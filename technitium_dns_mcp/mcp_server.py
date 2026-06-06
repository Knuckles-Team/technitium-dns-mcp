"""Main FastMCP server and tool registration."""

import sys
from typing import Any

from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from fastmcp.utilities.logging import get_logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from technitium_dns_mcp.mcp.mcp_dashboard import register_dashboard_tools
from technitium_dns_mcp.mcp.mcp_user import register_user_tools
from technitium_dns_mcp.mcp.mcp_zones import register_zones_tools

__version__ = "0.28.0"
logger = get_logger(name="technitium_dns_mcp")


def get_mcp_instance() -> tuple[Any, ...]:
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="Technitium DNS MCP",
        version=__version__,
        instructions="Technitium DNS Server MCP Server - Managed dynamic operations.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    # Always register all tools
    register_user_tools(mcp)
    register_dashboard_tools(mcp)
    register_zones_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"Technitium DNS MCP v{__version__}", file=sys.stderr)
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    mcp_server()
