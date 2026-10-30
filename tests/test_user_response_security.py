# Credential output regression tests use only fake credentials and transports.

import copy
import json
from unittest.mock import MagicMock

import pytest
from scion_sdk.tls.resolve import resolve_tls_profile
from scion_sdk.mcp.tool_surface import register_tool_surface
from fastmcp import Client, FastMCP

from technitium_dns_mcp.api_client import Api

ACTIONS = [
    ("login", {"user": "example", "password": "fake-password", "totp": "123456"}),
    (
        "create_token",
        {"user": "example", "password": "fake-password", "token_name": "test"},
    ),
    ("create_single_use_token", {}),
    ("get_session_info", {}),
    ("initialize_2fa", {}),
]
SECRET_KEYS = [
    "token",
    "access_token",
    "refresh-token",
    "sessionToken",
    "singleUseToken",
    "password",
    "pass",
    "newPassword",
    "newPass",
    "totp",
    "secret",
    "qrCodePngImage",
    "provisioningUri",
    "recoveryCodes",
    "TOKEN",
]


@pytest.fixture
def client():
    instance = Api(
        base_url="https://dns.invalid",
        token="mock-configured-token",
        tls_profile=resolve_tls_profile("technitium_dns"),
    )
    instance._session.request = MagicMock()
    yield instance
    instance.close()


def set_response(client, payload):
    response = MagicMock()
    response.status_code = 200
    response.headers = {"Content-Type": "application/json"}
    response.json.return_value = payload
    response.text = json.dumps(payload)
    client._session.request.return_value = response
    return response


def sensitive_response():
    secrets = {key: f"fake-secret-{key}" for key in SECRET_KEYS}
    metadata = {"tokenName": "test", "partialToken": "identifier", "totpEnabled": False}
    payload = {
        "status": "ok",
        **secrets,
        "response": {**metadata, "sessions": [secrets]},
    }
    expected = {"status": "ok", "response": {**metadata, "sessions": [{}]}}
    return payload, expected


@pytest.mark.parametrize("action,params", ACTIONS)
def test_sensitive_api_responses_are_copied_and_auth_preserved(client, action, params):
    payload, expected = sensitive_response()
    original = copy.deepcopy(payload)
    set_response(client, payload)

    assert getattr(client, action)(**params) == expected
    assert payload == original
    assert client.token == "mock-configured-token"
    assert client._session.headers["Authorization"] == "Bearer mock-configured-token"
    request = client._session.request.call_args.kwargs
    sent = request["params"] if request["method"] == "GET" else request["data"]
    assert sent["token"] == "mock-configured-token"
    if "password" in params:
        assert sent["pass"] == params["password"]
    if "totp" in params:
        assert sent["totp"] == params["totp"]


@pytest.mark.parametrize("action,params", ACTIONS)
@pytest.mark.parametrize("content_type", ["text/plain", "application/json"])
def test_raw_response_never_escapes(client, action, params, *, content_type):
    response = set_response(client, {})
    response.headers = {"Content-Type": content_type}
    response.text = 'malformed {"token": "fake-raw-secret"'
    response.json.side_effect = ValueError("fake-parser-secret")
    assert getattr(client, action)(**params) == {"status": "ok"}


@pytest.mark.parametrize("payload", ["fake-secret", ["fake-secret"], None, 42])
def test_unexpected_json_shape_fails_closed(client, payload):
    set_response(client, payload)
    assert client.get_session_info() == {"error": "Unexpected user API response"}


def test_nested_lists_and_error_metadata(client):
    set_response(
        client,
        {
            "status": "error",
            "errorMessage": "Denied",
            "response": [
                [{"token": "fake-secret", "allowed": True}],
                None,
                3,
            ],
        },
    )
    assert client.get_session_info() == {
        "status": "error",
        "errorMessage": "Denied",
        "response": [[{"allowed": True}], None, 3],
    }


def test_unrelated_download_is_preserved(client):
    response = set_response(client, {})
    response.headers = {"Content-Type": "text/plain"}
    response.text = "example.test. IN A 192.0.2.1"
    assert client.export_zone("example.test") == {"status": "ok", "text": response.text}


@pytest.mark.asyncio
@pytest.mark.parametrize("response_kind", ["json", "text", "malformed"])
@pytest.mark.parametrize("action,params", ACTIONS)
@pytest.mark.parametrize("user_enabled", [True])
async def test_registered_surfaces_sanitize(
    client, monkeypatch, *, action, params, user_enabled, response_kind
):
    monkeypatch.setattr(
        "scion_sdk.config.setting",
        lambda key, default=None: user_enabled if key == "USERTOOL" else default,
    )
    server = FastMCP("security-test")
    register_tool_surface(
        server,
        client_cls=Api,
        get_client=lambda: client,
        service="technitium-dns-mcp",
    )
    tools = {tool.name: tool for tool in await server.list_tools()}
    payload, expected = sensitive_response()
    response = set_response(client, payload)
    if response_kind != "json":
        response.headers = {
            "Content-Type": (
                "text/plain" if response_kind == "text" else "application/json"
            )
        }
        response.text = "fake-secret-raw-body"
        response.json.side_effect = ValueError("fake-secret-parser")
        expected = {"status": "ok"}
    assert "technitium_dns_user" not in tools
    async with Client(server) as mcp_client:
        result = await mcp_client.call_tool(
            f"technitium_dns_{action}", params, raise_on_error=False
        )
    served = result.structured_content
    if served is not None and set(served) == {"result"}:
        served = served["result"]
    assert served == expected
    assert "fake-secret" not in json.dumps(served)
