"""CONCEPT:TD-OS.config.tdns Dynamic client facade orchestration and resource mappings."""

from technitium_dns_mcp.api.api_client_dashboard import ApiClientDashboard
from technitium_dns_mcp.api.api_client_user import ApiClientUser
from technitium_dns_mcp.api.api_client_zones import ApiClientZones


class Api(ApiClientUser, ApiClientDashboard, ApiClientZones):
    pass
