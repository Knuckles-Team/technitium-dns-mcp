# Exercise served MCP errors with fake token-bearing URLs and request bodies.

import json
import traceback
from unittest.mock import MagicMock

import pytest
import requests
from scion_sdk.mcp.tool_surface import register_tool_surface
from fastmcp import Client, FastMCP
from test_user_response_security import ACTIONS, client


@pytest.fixture(
    params=[
        requests.ConnectionError,
        requests.exceptions.SSLError,
        requests.HTTPError,
        RuntimeError,
    ]
)
def transport_failure(request):
    return request.param(
        "https://dns.invalid/api/user/session/get?token=mock-configured-token "
        "POST body: pass=fake-password; token=mock-configured-token "
        "response: fake-response-secret"
    )


@pytest.fixture(params=["transport", "response"])
def failing_client(client, transport_failure, request):
    if request.param == "transport":
        client._session.request.side_effect = transport_failure
    else:
        response = MagicMock()
        response.status_code = 200
        response.headers.get.side_effect = transport_failure
        client._session.request.return_value = response
    return client


@pytest.mark.parametrize("action,params", ACTIONS)
def test_safe_exception_has_no_original_chain(
    failing_client, action, params, *, transport_failure
):
    with pytest.raises(RuntimeError, match="User API request failed") as captured:
        getattr(failing_client, action)(**params)
    assert type(transport_failure).__name__ in str(captured.value)
    assert captured.value.__cause__ is None
    assert captured.value.__context__ is None
    rendered = "".join(traceback.format_exception(captured.value))
    assert "mock-configured-token" not in rendered
    assert "fake-password" not in rendered
    assert "fake-response-secret" not in rendered
    assert failing_client.token == "mock-configured-token"


@pytest.fixture
def served_tool(failing_client, monkeypatch):
    monkeypatch.setattr(
        "technitium_dns_mcp.mcp.mcp_user.get_client", lambda: failing_client
    )
    monkeypatch.setattr(
        "scion_sdk.config.setting", lambda key, default=None: default
    )
    server = FastMCP("transport-security", mask_error_details=False)
    register_tool_surface(
        server,
        client_cls=type(failing_client),
        get_client=lambda: failing_client,
        service="technitium-dns-mcp",
    )
    return server


@pytest.mark.asyncio
@pytest.mark.parametrize("action,params", ACTIONS)
async def test_call_tool_never_exposes_transport_secrets(
    served_tool, caplog, capsys, *, action, params
):
    server = served_tool
    name = f"technitium_dns_{action}"
    arguments = params
    async with Client(server) as mcp_client:
        result = await mcp_client.call_tool(name, arguments, raise_on_error=False)
    assert result.is_error
    rendered = str(result)
    assert "User API request failed" in rendered
    captured = capsys.readouterr()
    diagnostics = rendered + caplog.text + captured.out + captured.err
    assert "mock-configured-token" not in diagnostics
    assert "fake-password" not in diagnostics
    assert "fake-response-secret" not in diagnostics
