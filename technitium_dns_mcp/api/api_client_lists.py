from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase, destructive


class ApiClientCache(ApiClientBase):
    def list_cache(
        self, domain: str | None = None, node: str | None = None
    ) -> dict[str, Any]:
        """Lists cached records under a domain (the root when no domain is given).

        Args:
            domain: Domain to list; empty lists the top of the cache.
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/cache/list", params=self._fields(domain=domain, node=node)
        )

    @destructive
    def delete_cached_zone(
        self, domain: str, node: str | None = None
    ) -> dict[str, Any]:
        """Removes one domain and its subdomains from the cache.

        Args:
            domain: Domain to remove.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/cache/delete", data=self._fields(domain=domain, node=node)
        )

    @destructive
    def flush_cache(self, node: str | None = None) -> dict[str, Any]:
        """Empties the whole DNS cache.

        Args:
            node: Target cluster node.
        """
        return self.request("POST", "/api/cache/flush", data=self._fields(node=node))


class ApiClientAllowed(ApiClientBase):
    def list_allowed(
        self, domain: str | None = None, node: str | None = None
    ) -> dict[str, Any]:
        """Lists allowed domains under a domain (the root when no domain is given).

        Args:
            domain: Domain to list; empty lists the top level.
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/allowed/list", params=self._fields(domain=domain, node=node)
        )

    def add_allowed(self, domain: str, node: str | None = None) -> dict[str, Any]:
        """Adds a domain to the allowed list so it is never blocked.

        Args:
            domain: Domain to allow.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/allowed/add", data=self._fields(domain=domain, node=node)
        )

    @destructive
    def delete_allowed(self, domain: str, node: str | None = None) -> dict[str, Any]:
        """Removes a domain from the allowed list.

        Args:
            domain: Domain to remove.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/allowed/delete", data=self._fields(domain=domain, node=node)
        )

    @destructive
    def flush_allowed(self, node: str | None = None) -> dict[str, Any]:
        """Empties the allowed list.

        Args:
            node: Target cluster node.
        """
        return self.request("POST", "/api/allowed/flush", data=self._fields(node=node))

    def export_allowed(self, node: str | None = None) -> dict[str, Any]:
        """Exports the allowed list as text, one domain per line.

        Args:
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/allowed/export", params=self._fields(node=node)
        )

    def import_allowed(
        self, allowed_zones: list[str], node: str | None = None
    ) -> dict[str, Any]:
        """Imports domains into the allowed list.

        Args:
            allowed_zones: Domains to allow.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/allowed/import",
            data=self._fields(allowedZones=allowed_zones, node=node),
        )


class ApiClientBlocked(ApiClientBase):
    def list_blocked(
        self, domain: str | None = None, node: str | None = None
    ) -> dict[str, Any]:
        """Lists blocked domains under a domain (the root when no domain is given).

        Args:
            domain: Domain to list; empty lists the top level.
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/blocked/list", params=self._fields(domain=domain, node=node)
        )

    def add_blocked(self, domain: str, node: str | None = None) -> dict[str, Any]:
        """Adds a domain to the blocked list.

        Args:
            domain: Domain to block.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/blocked/add", data=self._fields(domain=domain, node=node)
        )

    @destructive
    def delete_blocked(self, domain: str, node: str | None = None) -> dict[str, Any]:
        """Removes a domain from the blocked list.

        Args:
            domain: Domain to remove.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/blocked/delete", data=self._fields(domain=domain, node=node)
        )

    @destructive
    def flush_blocked(self, node: str | None = None) -> dict[str, Any]:
        """Empties the blocked list.

        Args:
            node: Target cluster node.
        """
        return self.request("POST", "/api/blocked/flush", data=self._fields(node=node))

    def export_blocked(self, node: str | None = None) -> dict[str, Any]:
        """Exports the blocked list as text, one domain per line.

        Args:
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/blocked/export", params=self._fields(node=node)
        )

    def import_blocked(
        self, blocked_zones: list[str], node: str | None = None
    ) -> dict[str, Any]:
        """Imports domains into the blocked list.

        Args:
            blocked_zones: Domains to block.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/blocked/import",
            data=self._fields(blockedZones=blocked_zones, node=node),
        )
