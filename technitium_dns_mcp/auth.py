"""CONCEPT:TD-OS.identity.tdns Identity credentials loader and session manager."""

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

from technitium_dns_mcp.api_client import Api

logger = get_logger(__name__)


def get_client(tls_profile: ResolvedTLSProfile | None = None) -> Api:
    """Get authenticated client for technitium_dns_mcp."""
    base_url = setting("TECHNITIUM_DNS_URL", "")
    token = setting("TECHNITIUM_DNS_TOKEN", "")
    if not base_url:
        raise RuntimeError("TECHNITIUM_DNS_URL is required")

    return Api(
        base_url=base_url,
        token=token,
        tls_profile=tls_profile or resolve_configured_tls_profile("technitium_dns"),
    )
