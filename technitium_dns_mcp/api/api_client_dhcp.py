from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase, destructive


class ApiClientDhcp(ApiClientBase):
    def list_dhcp_leases(self, node: str | None = None) -> dict[str, Any]:
        """Lists DHCP leases for every scope.

        Args:
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/dhcp/leases/list", params=self._fields(node=node)
        )

    @destructive
    def remove_dhcp_lease(
        self,
        name: str,
        hardware_address: str | None = None,
        client_identifier: str | None = None,
        address: str | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Removes a dynamic lease from a scope.

        Args:
            name: Scope name.
            hardware_address: MAC address of the lease.
            client_identifier: Client identifier of the lease.
            address: IP address of the lease.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/dhcp/leases/remove",
            data=self._fields(
                name=name,
                hardwareAddress=hardware_address,
                clientIdentifier=client_identifier,
                address=address,
                node=node,
            ),
        )

    def convert_dhcp_lease_to_reserved(
        self,
        name: str,
        hardware_address: str | None = None,
        client_identifier: str | None = None,
        address: str | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Turns a dynamic lease into a reserved lease.

        Args:
            name: Scope name.
            hardware_address: MAC address of the lease.
            client_identifier: Client identifier of the lease.
            address: IP address of the lease.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/dhcp/leases/convertToReserved",
            data=self._fields(
                name=name,
                hardwareAddress=hardware_address,
                clientIdentifier=client_identifier,
                address=address,
                node=node,
            ),
        )

    def convert_dhcp_lease_to_dynamic(
        self,
        name: str,
        hardware_address: str | None = None,
        client_identifier: str | None = None,
        address: str | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Turns a reserved lease back into a dynamic lease.

        Args:
            name: Scope name.
            hardware_address: MAC address of the lease.
            client_identifier: Client identifier of the lease.
            address: IP address of the lease.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/dhcp/leases/convertToDynamic",
            data=self._fields(
                name=name,
                hardwareAddress=hardware_address,
                clientIdentifier=client_identifier,
                address=address,
                node=node,
            ),
        )

    def list_dhcp_scopes(self, node: str | None = None) -> dict[str, Any]:
        """Lists DHCP scopes.

        Args:
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/dhcp/scopes/list", params=self._fields(node=node)
        )

    def get_dhcp_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Reads one DHCP scope with its options and reserved leases.

        Args:
            name: Scope name.
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/dhcp/scopes/get", params=self._fields(name=name, node=node)
        )

    def set_dhcp_scope(
        self,
        name: str,
        new_name: str | None = None,
        starting_address: str | None = None,
        ending_address: str | None = None,
        subnet_mask: str | None = None,
        lease_time_days: int | None = None,
        lease_time_hours: int | None = None,
        lease_time_minutes: int | None = None,
        offer_delay_time: int | None = None,
        ping_check_enabled: bool | None = None,
        ping_check_timeout: int | None = None,
        ping_check_retries: int | None = None,
        domain_name: str | None = None,
        domain_search_list: list[str] | None = None,
        dns_updates: bool | None = None,
        dns_ttl: int | None = None,
        server_address: str | None = None,
        router_address: str | None = None,
        use_this_dns_server: bool | None = None,
        dns_servers: list[str] | None = None,
        ntp_servers: list[str] | None = None,
        reserved_leases: str | None = None,
        allow_only_reserved_leases: bool | None = None,
        block_locally_administered_mac_addresses: bool | None = None,
        ignore_client_identifier_option: bool | None = None,
        node: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Creates a DHCP scope or changes an existing one. Only the fields given change.

        Args:
            name: Scope name.
            new_name: New name to rename the scope.
            starting_address: First address of the pool.
            ending_address: Last address of the pool.
            subnet_mask: Subnet mask.
            lease_time_days: Lease days.
            lease_time_hours: Lease hours.
            lease_time_minutes: Lease minutes.
            offer_delay_time: Milliseconds to wait before offering.
            ping_check_enabled: Ping an address before offering it.
            ping_check_timeout: Ping timeout in milliseconds.
            ping_check_retries: Ping retries.
            domain_name: Domain name option handed to clients.
            domain_search_list: Domain search list option.
            dns_updates: Create DNS records for leases.
            dns_ttl: TTL of those DNS records.
            server_address: Next-server address.
            router_address: Default gateway handed to clients.
            use_this_dns_server: Hand out this server as the DNS server.
            dns_servers: DNS servers handed to clients.
            ntp_servers: NTP servers handed to clients.
            reserved_leases: Reserved leases, `hostname|mac|address|comments` separated by `|` and `|` pairs as the API takes them.
            allow_only_reserved_leases: Offer only reserved leases.
            block_locally_administered_mac_addresses: Refuse randomised client MAC addresses.
            ignore_client_identifier_option: Ignore the client identifier option.
            node: Target cluster node.
            **extra: Other scope fields from the Technitium API, in its camelCase spelling.
        """
        data = self._fields(
            name=name,
            newName=new_name,
            startingAddress=starting_address,
            endingAddress=ending_address,
            subnetMask=subnet_mask,
            leaseTimeDays=lease_time_days,
            leaseTimeHours=lease_time_hours,
            leaseTimeMinutes=lease_time_minutes,
            offerDelayTime=offer_delay_time,
            pingCheckEnabled=ping_check_enabled,
            pingCheckTimeout=ping_check_timeout,
            pingCheckRetries=ping_check_retries,
            domainName=domain_name,
            domainSearchList=domain_search_list,
            dnsUpdates=dns_updates,
            dnsTtl=dns_ttl,
            serverAddress=server_address,
            routerAddress=router_address,
            useThisDnsServer=use_this_dns_server,
            dnsServers=dns_servers,
            ntpServers=ntp_servers,
            reservedLeases=reserved_leases,
            allowOnlyReservedLeases=allow_only_reserved_leases,
            blockLocallyAdministeredMacAddresses=block_locally_administered_mac_addresses,
            ignoreClientIdentifierOption=ignore_client_identifier_option,
            node=node,
        )
        data.update(self._fields(**extra))
        return self.request("POST", "/api/dhcp/scopes/set", data=data)

    def add_dhcp_reserved_lease(
        self,
        name: str,
        hardware_address: str,
        ip_address: str,
        host_name: str | None = None,
        comments: str | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Adds a reserved lease to a scope.

        Args:
            name: Scope name.
            hardware_address: MAC address to reserve for.
            ip_address: Address to reserve.
            host_name: Host name for the lease.
            comments: Free text.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/dhcp/scopes/addReservedLease",
            data=self._fields(
                name=name,
                hardwareAddress=hardware_address,
                ipAddress=ip_address,
                hostName=host_name,
                comments=comments,
                node=node,
            ),
        )

    @destructive
    def remove_dhcp_reserved_lease(
        self, name: str, hardware_address: str, node: str | None = None
    ) -> dict[str, Any]:
        """Removes a reserved lease from a scope.

        Args:
            name: Scope name.
            hardware_address: MAC address of the reservation.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/dhcp/scopes/removeReservedLease",
            data=self._fields(name=name, hardwareAddress=hardware_address, node=node),
        )

    def enable_dhcp_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Enables a DHCP scope.

        Args:
            name: Scope name.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/dhcp/scopes/enable", data=self._fields(name=name, node=node)
        )

    def disable_dhcp_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Disables a DHCP scope. Clients stop receiving offers from it.

        Args:
            name: Scope name.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/dhcp/scopes/disable", data=self._fields(name=name, node=node)
        )

    @destructive
    def delete_dhcp_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Deletes a DHCP scope and its leases.

        Args:
            name: Scope name.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/dhcp/scopes/delete", data=self._fields(name=name, node=node)
        )
