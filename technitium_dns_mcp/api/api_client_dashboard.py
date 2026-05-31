from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase


class ApiClientDashboard(ApiClientBase):
    def get_metrics_json(self) -> dict[str, Any]:
        """Gets metrics in JSON format for the dashboard."""
        return self.request("GET", "/api/dashboard/metrics/json")

    def get_metrics_text(self) -> dict[str, Any]:
        """Gets metrics in Prometheus metrics format."""
        return self.request("GET", "/api/dashboard/metrics/text")

    def get_stats(
        self,
        node: str | None = None,
        stats_type: str | None = None,
        utc: bool | None = None,
        dont_trim_query_type_data: bool | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> dict[str, Any]:
        """Retrieves server statistical charts data.

        Args:
            node: Target server node.
            stats_type: Period/type (e.g. 'hour', 'day', 'month').
            utc: If stats time is in UTC.
            dont_trim_query_type_data: Avoid trimming query type graphs.
            start: Start date-time string (e.g. 'YYYY-MM-DD HH:MM:SS').
            end: End date-time string (e.g. 'YYYY-MM-DD HH:MM:SS').
        """
        params = {}
        if node is not None:
            params["node"] = node
        if stats_type is not None:
            params["type"] = stats_type
        if utc is not None:
            params["utc"] = str(utc).lower()
        if dont_trim_query_type_data is not None:
            params["dontTrimQueryTypeData"] = str(dont_trim_query_type_data).lower()
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return self.request("GET", "/api/dashboard/stats/get", params=params)

    def get_top_stats(
        self,
        node: str | None = None,
        stats_type: str | None = None,
        start: str | None = None,
        end: str | None = None,
        stats_category: str | None = None,
        limit: int | None = None,
        no_reverse_lookup: bool | None = None,
        only_rate_limited_clients: bool | None = None,
    ) -> dict[str, Any]:
        """Retrieves top stats data for queries, clients, domains, etc.

        Args:
            node: Target server node.
            stats_type: Period/type (e.g. 'hour', 'day', 'month').
            start: Start date-time string.
            end: End date-time string.
            stats_category: The stats type (e.g. 'clients', 'domains', 'queryTypes').
            limit: Limit of results to return.
            no_reverse_lookup: Avoid performing PTR lookups for clients (optional).
            only_rate_limited_clients: Get only rate-limited clients (optional).
        """
        params = {}
        if node is not None:
            params["node"] = node
        if stats_type is not None:
            params["type"] = stats_type
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if stats_category is not None:
            # Map category parameter to 'statsType' expected by Technitium API
            params["statsType"] = stats_category
        if limit is not None:
            params["limit"] = str(limit)
        if no_reverse_lookup is not None:
            params["noReverseLookup"] = str(no_reverse_lookup).lower()
        if only_rate_limited_clients is not None:
            params["onlyRateLimitedClients"] = str(only_rate_limited_clients).lower()
        return self.request("GET", "/api/dashboard/stats/getTop", params=params)

    def delete_all_stats(self, node: str | None = None) -> dict[str, Any]:
        """Deletes all statistics from the server.

        Args:
            node: Target server node (optional).
        """
        data = {}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/dashboard/stats/deleteAll", data=data)
