import pytest


@pytest.mark.concept("TDNS-002")
def test_startup():
    # Basic import test
    import technitium_dns_mcp

    assert technitium_dns_mcp.__version__ == "0.15.0"
