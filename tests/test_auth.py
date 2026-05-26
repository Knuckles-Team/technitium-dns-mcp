import pytest


@pytest.mark.concept("TDNS-003")
def test_auth():
    from technitium_dns_mcp.auth import get_client

    client = get_client()
    assert client is not None
    assert hasattr(client, "request")
