"""CONCEPT:TDNS-001 Dynamic client facade orchestration and resource mappings."""

from technitium_dns_mcp.api.api_client_user import ApiClientUser
from technitium_dns_mcp.api.api_client_dashboard import ApiClientDashboard
from technitium_dns_mcp.api.api_client_zones import ApiClientZones

__version__ = "0.15.0"


class Api(ApiClientUser, ApiClientDashboard, ApiClientZones):
    pass
