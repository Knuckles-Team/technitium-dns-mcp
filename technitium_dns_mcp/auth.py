"""CONCEPT:TDNS-003 Identity credentials loader and session manager."""

import os

from agent_utilities.base_utilities import get_logger, to_boolean

from technitium_dns_mcp.api_client import Api

logger = get_logger(__name__)


def get_client() -> Api:
    """Get authenticated client for technitium_dns_mcp."""
    base_url = os.getenv("TECHNITIUM_DNS_URL") or "http://localhost:5380"
    token = os.getenv("TECHNITIUM_DNS_TOKEN", "")
    verify = to_boolean(os.getenv("TECHNITIUM_DNS_SSL_VERIFY", "True"))

    return Api(
        base_url=base_url,
        token=token,
        verify=verify,
    )
