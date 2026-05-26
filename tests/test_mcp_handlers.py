import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fastmcp import FastMCP
from technitium_dns_mcp.mcp.mcp_user import register_user_tools
from technitium_dns_mcp.mcp.mcp_dashboard import register_dashboard_tools
from technitium_dns_mcp.mcp.mcp_zones import register_zones_tools


@pytest.mark.asyncio
async def test_mcp_user_handler(mock_ctx):
    mcp = FastMCP("test-mcp")
    register_user_tools(mcp)

    tools = await mcp.list_tools()
    assert "technitium_dns_user" in [t.name for t in tools]

    # Find the tool
    tool = [t for t in tools if t.name == "technitium_dns_user"][0]

    mock_client = MagicMock()
    mock_client.get_sso_status.return_value = {"status": "ok"}

    res = await tool.fn(
        action="get_sso_status",
        params_json="{}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"status": "ok"}
    mock_client.get_sso_status.assert_called_once()


@pytest.mark.asyncio
async def test_mcp_dashboard_handler(mock_ctx):
    mcp = FastMCP("test-mcp")
    register_dashboard_tools(mcp)

    tools = await mcp.list_tools()
    tool = [t for t in tools if t.name == "technitium_dns_dashboard"][0]

    mock_client = MagicMock()
    mock_client.get_metrics_json.return_value = {"status": "ok"}

    res = await tool.fn(
        action="get_metrics_json",
        params_json="{}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"status": "ok"}
    mock_client.get_metrics_json.assert_called_once()


@pytest.mark.asyncio
async def test_mcp_zones_handler(mock_ctx):
    mcp = FastMCP("test-mcp")
    register_zones_tools(mcp)

    tools = await mcp.list_tools()
    tool = [t for t in tools if t.name == "technitium_dns_zones"][0]

    mock_client = MagicMock()
    mock_client.list_zones.return_value = {"status": "ok"}

    res = await tool.fn(
        action="list_zones",
        params_json='{"node": "n1"}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"status": "ok"}
    mock_client.list_zones.assert_called_once_with(node="n1")
