"""CONCEPT:TD-OS.config.tdns Dynamic client facade orchestration and resource mappings."""

from technitium_dns_mcp.api.api_client_admin import ApiClientAdmin
from technitium_dns_mcp.api.api_client_apps import ApiClientApps
from technitium_dns_mcp.api.api_client_dashboard import ApiClientDashboard
from technitium_dns_mcp.api.api_client_dhcp import ApiClientDhcp
from technitium_dns_mcp.api.api_client_lists import (
    ApiClientAllowed,
    ApiClientBlocked,
    ApiClientCache,
)
from technitium_dns_mcp.api.api_client_logs import ApiClientLogs
from technitium_dns_mcp.api.api_client_settings import ApiClientSettings
from technitium_dns_mcp.api.api_client_user import ApiClientUser
from technitium_dns_mcp.api.api_client_zones import ApiClientZones


class Api(
    ApiClientUser,
    ApiClientDashboard,
    ApiClientZones,
    ApiClientSettings,
    ApiClientCache,
    ApiClientAllowed,
    ApiClientBlocked,
    ApiClientLogs,
    ApiClientDhcp,
    ApiClientApps,
    ApiClientAdmin,
):
    pass
