import pytest


@pytest.mark.concept("TDNS-003")
def test_auth(monkeypatch):
    from technitium_dns_mcp.auth import get_client

    monkeypatch.setenv("TECHNITIUM_DNS_URL", "https://service.invalid")
    client = get_client()
    assert client is not None
    assert hasattr(client, "request")
