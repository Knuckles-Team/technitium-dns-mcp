"""CONCEPT:TD-OS.identity.tdns Identity credentials loader and session manager."""

from agent_connector_sdk.config import setting
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile
from agent_connector_sdk.utilities import get_logger

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
        tls_profile=tls_profile or resolve_tls_profile("technitium_dns"),
    )
