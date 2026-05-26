import pytest


@pytest.mark.concept("TDNS-001")
def test_init_dynamics():
    import technitium_dns_mcp

    assert technitium_dns_mcp._MCP_AVAILABLE is True
