# The configured connector token (TECHNITIUM_DNS_TOKEN) rides in the GET
# query string on every authenticated request, not only the "user" domain
# calls that tests/test_user_transport_security.py exercises. A transport
# failure (connection/timeout/TLS error) on ANY endpoint -- zones, dashboard,
# user -- embeds the full request URL, including that token, in its message.
# These tests prove the containment lives at the one chokepoint every
# endpoint shares (ApiClientBase.request), not only in the user-domain
# wrapper, using fake credentials and transports throughout.

import traceback

import pytest
import requests

from technitium_dns_mcp.api_client import Api


@pytest.fixture
def client():
    instance = Api(base_url="https://dns.invalid", token="mock-configured-token")
    yield instance
    instance.close()


@pytest.mark.parametrize(
    "transport_failure",
    [
        requests.ConnectionError(
            "HTTPSConnectionPool(host='dns.invalid', port=443): Max retries "
            "exceeded with url: /api/zones/list?token=mock-configured-token "
            "(Caused by fake-cause)"
        ),
        requests.exceptions.SSLError(
            "fake-ssl-failure url=/api/dashboard/stats/get?token=mock-configured-token"
        ),
        requests.Timeout(
            "fake-timeout url=/api/zones/records/get?token=mock-configured-token"
        ),
    ],
)
@pytest.mark.parametrize(
    "action,kwargs,endpoint",
    [
        ("list_zones", {}, "/api/zones/list"),
        ("get_stats", {}, "/api/dashboard/stats/get"),
        (
            "get_records",
            {"domain": "example.test", "zone": "example.test"},
            "/api/zones/records/get",
        ),
    ],
)
def test_non_user_transport_failures_never_leak_the_configured_token(
    client, monkeypatch, transport_failure, action, kwargs, endpoint
):
    def raise_transport_failure(*_args, **_kwargs):
        raise transport_failure

    monkeypatch.setattr(client._session, "request", raise_transport_failure)

    with pytest.raises(Exception) as captured:
        getattr(client, action)(**kwargs)

    assert captured.value.__cause__ is None
    assert captured.value.__context__ is None
    assert type(transport_failure).__name__ in str(captured.value)
    assert endpoint in str(captured.value)

    rendered = "".join(traceback.format_exception(captured.value))
    assert "mock-configured-token" not in rendered
    assert "token=" not in rendered
    assert client.token == "mock-configured-token"


def test_base_request_transport_failure_preserves_exception_type(client, monkeypatch):
    def raise_connection_error(*_args, **_kwargs):
        raise requests.ConnectionError(
            "url: /api/zones/list?token=mock-configured-token"
        )

    monkeypatch.setattr(client._session, "request", raise_connection_error)

    # Preserving the original exception TYPE (not just a generic RuntimeError)
    # is what lets tests/test_user_transport_security.py's user-domain
    # wrapper (_safe_user_request, which only inspects type(error).__name__)
    # keep surfacing an accurate diagnostic without re-leaking the message.
    with pytest.raises(requests.ConnectionError) as captured:
        client.list_zones()
    assert "mock-configured-token" not in str(captured.value)
