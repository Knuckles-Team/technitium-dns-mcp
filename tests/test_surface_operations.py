"""The settings, cache, list, log, DHCP, app, admin and backup operations are typed tools."""

import asyncio
import base64
from unittest.mock import MagicMock, patch

import pytest

from technitium_dns_mcp.api_client import Api


@pytest.fixture
def client():
    api = Api(base_url="http://localhost:5380", token="t0ken")
    response = MagicMock()
    response.status_code = 200
    response.headers = {"Content-Type": "application/json"}
    response.json.return_value = {"status": "ok", "response": {}}
    response.text = "{}"
    response.content = b"PK\x03\x04zip"
    with patch.object(api._session, "request", return_value=response) as call:
        api.calls = call
        yield api


def last(client):
    return client.calls.call_args.kwargs


@pytest.mark.parametrize(
    ("method", "args", "verb", "path"),
    [
        ("get_dns_settings", {}, "GET", "/api/settings/getDnsSettings"),
        ("get_tsig_key_names", {}, "GET", "/api/settings/getTsigKeyNames"),
        ("force_update_block_lists", {}, "POST", "/api/settings/forceUpdateBlockLists"),
        ("temporary_disable_blocking", {"minutes": 5}, "POST", "/api/settings/temporaryDisableBlocking"),
        ("list_cache", {"domain": "example.com"}, "GET", "/api/cache/list"),
        ("delete_cached_zone", {"domain": "example.com"}, "POST", "/api/cache/delete"),
        ("flush_cache", {}, "POST", "/api/cache/flush"),
        ("list_allowed", {}, "GET", "/api/allowed/list"),
        ("add_allowed", {"domain": "a.example"}, "POST", "/api/allowed/add"),
        ("delete_allowed", {"domain": "a.example"}, "POST", "/api/allowed/delete"),
        ("flush_allowed", {}, "POST", "/api/allowed/flush"),
        ("export_allowed", {}, "GET", "/api/allowed/export"),
        ("import_allowed", {"allowed_zones": ["a.example"]}, "POST", "/api/allowed/import"),
        ("list_blocked", {}, "GET", "/api/blocked/list"),
        ("add_blocked", {"domain": "ads.example"}, "POST", "/api/blocked/add"),
        ("delete_blocked", {"domain": "ads.example"}, "POST", "/api/blocked/delete"),
        ("flush_blocked", {}, "POST", "/api/blocked/flush"),
        ("export_blocked", {}, "GET", "/api/blocked/export"),
        ("import_blocked", {"blocked_zones": ["ads.example"]}, "POST", "/api/blocked/import"),
        ("list_logs", {}, "GET", "/api/logs/list"),
        ("download_log", {"file_name": "2026-11-06"}, "GET", "/api/logs/download"),
        ("delete_log", {"log": "2026-11-06"}, "POST", "/api/logs/delete"),
        ("delete_all_logs", {}, "POST", "/api/logs/deleteAll"),
        ("query_logs", {"name": "Query Logs", "class_path": "QueryLogs.App"}, "GET", "/api/logs/query"),
        ("list_dhcp_leases", {}, "GET", "/api/dhcp/leases/list"),
        ("remove_dhcp_lease", {"name": "lan", "address": "10.0.0.5"}, "POST", "/api/dhcp/leases/remove"),
        ("convert_dhcp_lease_to_reserved", {"name": "lan"}, "POST", "/api/dhcp/leases/convertToReserved"),
        ("convert_dhcp_lease_to_dynamic", {"name": "lan"}, "POST", "/api/dhcp/leases/convertToDynamic"),
        ("list_dhcp_scopes", {}, "GET", "/api/dhcp/scopes/list"),
        ("get_dhcp_scope", {"name": "lan"}, "GET", "/api/dhcp/scopes/get"),
        ("set_dhcp_scope", {"name": "lan", "router_address": "10.0.0.1"}, "POST", "/api/dhcp/scopes/set"),
        ("add_dhcp_reserved_lease", {"name": "lan", "hardware_address": "aa:bb", "ip_address": "10.0.0.9"}, "POST", "/api/dhcp/scopes/addReservedLease"),
        ("remove_dhcp_reserved_lease", {"name": "lan", "hardware_address": "aa:bb"}, "POST", "/api/dhcp/scopes/removeReservedLease"),
        ("enable_dhcp_scope", {"name": "lan"}, "POST", "/api/dhcp/scopes/enable"),
        ("disable_dhcp_scope", {"name": "lan"}, "POST", "/api/dhcp/scopes/disable"),
        ("delete_dhcp_scope", {"name": "lan"}, "POST", "/api/dhcp/scopes/delete"),
        ("list_apps", {}, "GET", "/api/apps/list"),
        ("list_store_apps", {}, "GET", "/api/apps/listStoreApps"),
        ("download_and_install_app", {"name": "x", "url": "https://example/x.zip"}, "POST", "/api/apps/downloadAndInstall"),
        ("download_and_update_app", {"name": "x", "url": "https://example/x.zip"}, "POST", "/api/apps/downloadAndUpdate"),
        ("uninstall_app", {"name": "x"}, "POST", "/api/apps/uninstall"),
        ("get_app_config", {"name": "x"}, "GET", "/api/apps/config/get"),
        ("set_app_config", {"name": "x", "config": "{}"}, "POST", "/api/apps/config/set"),
        ("list_admin_sessions", {}, "GET", "/api/admin/sessions/list"),
        ("create_api_token", {"user": "u", "token_name": "n"}, "POST", "/api/admin/sessions/createToken"),
        ("delete_admin_session", {"partial_token": "abc"}, "POST", "/api/admin/sessions/delete"),
        ("list_users", {}, "GET", "/api/admin/users/list"),
        ("create_user", {"user": "u", "password": "pw"}, "POST", "/api/admin/users/create"),
        ("get_user", {"user": "u"}, "GET", "/api/admin/users/get"),
        ("set_user", {"user": "u", "disabled": True}, "POST", "/api/admin/users/set"),
        ("delete_user", {"user": "u"}, "POST", "/api/admin/users/delete"),
        ("list_groups", {}, "GET", "/api/admin/groups/list"),
        ("create_group", {"group": "g"}, "POST", "/api/admin/groups/create"),
        ("get_group", {"group": "g"}, "GET", "/api/admin/groups/get"),
        ("set_group", {"group": "g", "members": ["u"]}, "POST", "/api/admin/groups/set"),
        ("delete_group", {"group": "g"}, "POST", "/api/admin/groups/delete"),
        ("list_permissions", {}, "GET", "/api/admin/permissions/list"),
        ("get_permissions", {"section": "Zones"}, "GET", "/api/admin/permissions/get"),
        ("set_permissions", {"section": "Zones", "user_permissions": "u|true|true|false"}, "POST", "/api/admin/permissions/set"),
    ],
)  # fmt: skip
def test_operation_calls_its_endpoint(client, method, args, verb, path):
    getattr(client, method)(**args)
    call = last(client)
    assert call["method"] == verb
    assert call["url"].endswith(path)


def test_settings_change_sends_only_given_fields(client):
    client.set_dns_settings(
        recursion="Deny", forwarders=["1.1.1.1", "9.9.9.9"], enable_blocking=True
    )
    data = last(client)["data"]
    assert data["recursion"] == "Deny"
    assert data["forwarders"] == "1.1.1.1,9.9.9.9"
    assert data["enableBlocking"] == "true"
    assert "dnsServerDomain" not in data


def test_settings_read_omits_secrets(client):
    client.calls.return_value.json.return_value = {
        "response": {
            "tsigKeys": [{"keyName": "k", "sharedSecret": "s3cret"}],
            "proxy": {"password": "pw"},
        }
    }
    out = client.get_dns_settings()
    assert "s3cret" not in str(out)
    assert "pw" not in str(out)
    assert out["response"]["tsigKeys"][0]["keyName"] == "k"


def test_backup_comes_back_base64(client):
    out = client.backup_settings(zones=True)
    assert base64.b64decode(out["content_base64"]) == b"PK\x03\x04zip"
    assert out["size"] == 7
    assert last(client)["params"]["zones"] == "true"


def test_restore_uploads_the_zip(client):
    client.restore_settings(base64.b64encode(b"zipbytes").decode(), zones=True)
    call = last(client)
    assert call["files"]["file"][1] == b"zipbytes"
    assert call["data"]["zones"] == "true"


def test_record_data_has_typed_arguments(client):
    client.add_record(
        zone="z", domain="a.z", type="A", ttl=60, ip_address="10.0.0.1", ptr=True
    )
    data = last(client)["data"]
    assert data["ipAddress"] == "10.0.0.1"
    assert data["ptr"] == "true"
    client.add_record(
        zone="z", domain="z", type="MX", ttl=60, exchange="mx.z", preference=10
    )
    assert last(client)["data"]["preference"] == "10"


def test_user_creation_sends_the_password_field(client):
    client.create_user(user="u", password="pw", display_name="U")
    assert last(client)["data"]["pass"] == "pw"


def _served():
    from scion_sdk.connector import build_server

    mcp = build_server("technitium_dns_mcp", command_args=[])[1]
    return {t.name: t for t in asyncio.run(mcp.list_tools())}


def test_no_served_tool_routes_an_action():
    for name, tool in _served().items():
        assert "action" not in tool.parameters.get("properties", {}), name


@pytest.mark.parametrize(
    "name",
    [
        "restore_settings", "flush_cache", "delete_cached_zone", "flush_allowed", "flush_blocked",
        "delete_allowed", "delete_blocked", "delete_log", "delete_all_logs", "delete_dhcp_scope",
        "remove_dhcp_lease", "remove_dhcp_reserved_lease", "uninstall_app", "delete_user",
        "delete_group", "delete_admin_session",
    ],
)  # fmt: skip
def test_destructive_operations_take_confirm(name):
    tool = _served()[f"technitium_dns_{name}"]
    assert "confirm" in tool.parameters["properties"]
