from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase


class ApiClientDhcp(ApiClientBase):
    def list_scopes(self, node: str | None = None) -> dict[str, Any]:
        """Lists all DHCP scopes.

        Args:
            node: Target server node.
        """
        params = {}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/dhcp/scopes/list", params=params)

    def get_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Gets the settings of a DHCP scope.

        Args:
            name: Scope name.
            node: Target server node.
        """
        params = {"name": name}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/dhcp/scopes/get", params=params)

    def set_scope(
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
        domain_search_list: str | None = None,
        dns_updates: bool | None = None,
        dns_overwrite_for_dynamic_lease: bool | None = None,
        dns_ttl: int | None = None,
        server_address: str | None = None,
        server_host_name: str | None = None,
        boot_file_name: str | None = None,
        router_address: str | None = None,
        use_this_dns_server: bool | None = None,
        dns_servers: str | None = None,
        wins_servers: str | None = None,
        ntp_servers: str | None = None,
        ntp_server_domain_names: str | None = None,
        static_routes: str | None = None,
        vendor_info: str | None = None,
        capwap_ac_ip_addresses: str | None = None,
        tftp_server_addresses: str | None = None,
        generic_options: str | None = None,
        exclusions: str | None = None,
        reserved_leases: str | None = None,
        allow_only_reserved_leases: bool | None = None,
        block_locally_administered_mac_addresses: bool | None = None,
        ignore_client_identifier_option: bool | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Creates a new DHCP scope, or updates an existing one.

        Args:
            name: Scope name (existing name when renaming via new_name).
            new_name: New scope name, to rename an existing scope.
            starting_address: Start of the scope's IP address range.
            ending_address: End of the scope's IP address range.
            subnet_mask: Subnet mask for the scope.
            lease_time_days: Lease time, days component.
            lease_time_hours: Lease time, hours component.
            lease_time_minutes: Lease time, minutes component.
            offer_delay_time: Delay, in milliseconds, before sending a DHCP offer.
            ping_check_enabled: Enable ping check before offering an address.
            ping_check_timeout: Ping check timeout in milliseconds.
            ping_check_retries: Number of ping check retries.
            domain_name: Domain name handed to clients.
            domain_search_list: Domain search list handed to clients.
            dns_updates: Enable dynamic DNS updates for leases.
            dns_overwrite_for_dynamic_lease: Overwrite existing DNS records for dynamic leases.
            dns_ttl: TTL for dynamically updated DNS records.
            server_address: DHCP option 54 server identifier override.
            server_host_name: DHCP option 66 TFTP server host name.
            boot_file_name: DHCP option 67 boot file name.
            router_address: Router/gateway address handed to clients.
            use_this_dns_server: Advertise this DNS server to clients.
            dns_servers: Comma-separated list of DNS server addresses.
            wins_servers: Comma-separated list of WINS server addresses.
            ntp_servers: Comma-separated list of NTP server addresses.
            ntp_server_domain_names: Comma-separated list of NTP server domain names.
            static_routes: Pipe-delimited static routes table (destination|subnetMask|router per row).
            vendor_info: Pipe-delimited vendor class info table.
            capwap_ac_ip_addresses: Comma-separated CAPWAP AC IP addresses.
            tftp_server_addresses: Comma-separated TFTP server addresses.
            generic_options: Pipe-delimited generic DHCP options table.
            exclusions: Pipe-delimited exclusion ranges (startingAddress|endingAddress per row).
            reserved_leases: Pipe-delimited reserved leases table (hostName|hardwareAddress|address|comments per row).
            allow_only_reserved_leases: Only serve leases that have a matching reservation.
            block_locally_administered_mac_addresses: Block MACs with the locally-administered bit set.
            ignore_client_identifier_option: Ignore the DHCP client identifier option, use MAC only.
            node: Target server node.
        """
        data = {"name": name}
        if new_name is not None:
            data["newName"] = new_name
        if starting_address is not None:
            data["startingAddress"] = starting_address
        if ending_address is not None:
            data["endingAddress"] = ending_address
        if subnet_mask is not None:
            data["subnetMask"] = subnet_mask
        if lease_time_days is not None:
            data["leaseTimeDays"] = str(lease_time_days)
        if lease_time_hours is not None:
            data["leaseTimeHours"] = str(lease_time_hours)
        if lease_time_minutes is not None:
            data["leaseTimeMinutes"] = str(lease_time_minutes)
        if offer_delay_time is not None:
            data["offerDelayTime"] = str(offer_delay_time)
        if ping_check_enabled is not None:
            data["pingCheckEnabled"] = str(ping_check_enabled).lower()
        if ping_check_timeout is not None:
            data["pingCheckTimeout"] = str(ping_check_timeout)
        if ping_check_retries is not None:
            data["pingCheckRetries"] = str(ping_check_retries)
        if domain_name is not None:
            data["domainName"] = domain_name
        if domain_search_list is not None:
            data["domainSearchList"] = domain_search_list
        if dns_updates is not None:
            data["dnsUpdates"] = str(dns_updates).lower()
        if dns_overwrite_for_dynamic_lease is not None:
            data["dnsOverwriteForDynamicLease"] = str(
                dns_overwrite_for_dynamic_lease
            ).lower()
        if dns_ttl is not None:
            data["dnsTtl"] = str(dns_ttl)
        if server_address is not None:
            data["serverAddress"] = server_address
        if server_host_name is not None:
            data["serverHostName"] = server_host_name
        if boot_file_name is not None:
            data["bootFileName"] = boot_file_name
        if router_address is not None:
            data["routerAddress"] = router_address
        if use_this_dns_server is not None:
            data["useThisDnsServer"] = str(use_this_dns_server).lower()
        if dns_servers is not None:
            data["dnsServers"] = dns_servers
        if wins_servers is not None:
            data["winsServers"] = wins_servers
        if ntp_servers is not None:
            data["ntpServers"] = ntp_servers
        if ntp_server_domain_names is not None:
            data["ntpServerDomainNames"] = ntp_server_domain_names
        if static_routes is not None:
            data["staticRoutes"] = static_routes
        if vendor_info is not None:
            data["vendorInfo"] = vendor_info
        if capwap_ac_ip_addresses is not None:
            data["capwapAcIpAddresses"] = capwap_ac_ip_addresses
        if tftp_server_addresses is not None:
            data["tftpServerAddresses"] = tftp_server_addresses
        if generic_options is not None:
            data["genericOptions"] = generic_options
        if exclusions is not None:
            data["exclusions"] = exclusions
        if reserved_leases is not None:
            data["reservedLeases"] = reserved_leases
        if allow_only_reserved_leases is not None:
            data["allowOnlyReservedLeases"] = str(allow_only_reserved_leases).lower()
        if block_locally_administered_mac_addresses is not None:
            data["blockLocallyAdministeredMacAddresses"] = str(
                block_locally_administered_mac_addresses
            ).lower()
        if ignore_client_identifier_option is not None:
            data["ignoreClientIdentifierOption"] = str(
                ignore_client_identifier_option
            ).lower()

        params = {}
        if node is not None:
            params["node"] = node

        return self.request("POST", "/api/dhcp/scopes/set", params=params, data=data)

    def enable_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Enables a DHCP scope.

        Args:
            name: Scope name.
            node: Target server node.
        """
        params = {"name": name}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/dhcp/scopes/enable", params=params)

    def disable_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Disables a DHCP scope.

        Args:
            name: Scope name.
            node: Target server node.
        """
        params = {"name": name}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/dhcp/scopes/disable", params=params)

    def delete_scope(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Deletes a DHCP scope.

        Args:
            name: Scope name.
            node: Target server node.
        """
        params = {"name": name}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/dhcp/scopes/delete", params=params)

    def list_leases(
        self, name: str | None = None, node: str | None = None
    ) -> dict[str, Any]:
        """Lists current DHCP leases.

        Args:
            name: Optional scope name to filter leases by.
            node: Target server node.
        """
        params = {}
        if name is not None:
            params["name"] = name
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/dhcp/leases/list", params=params)

    def remove_lease(
        self, name: str, client_identifier: str, node: str | None = None
    ) -> dict[str, Any]:
        """Removes a DHCP lease.

        Args:
            name: Scope name.
            client_identifier: Client identifier of the lease to remove.
            node: Target server node.
        """
        params = {"name": name, "clientIdentifier": client_identifier}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/dhcp/leases/remove", params=params)

    def convert_to_reserved_lease(
        self, name: str, client_identifier: str, node: str | None = None
    ) -> dict[str, Any]:
        """Converts a dynamic DHCP lease into a reserved lease.

        Args:
            name: Scope name.
            client_identifier: Client identifier of the lease to convert.
            node: Target server node.
        """
        params = {"name": name, "clientIdentifier": client_identifier}
        if node is not None:
            params["node"] = node
        return self.request(
            "GET", "/api/dhcp/leases/convertToReserved", params=params
        )

    def convert_to_dynamic_lease(
        self, name: str, client_identifier: str, node: str | None = None
    ) -> dict[str, Any]:
        """Converts a reserved DHCP lease back into a dynamic lease.

        Args:
            name: Scope name.
            client_identifier: Client identifier of the lease to convert.
            node: Target server node.
        """
        params = {"name": name, "clientIdentifier": client_identifier}
        if node is not None:
            params["node"] = node
        return self.request(
            "GET", "/api/dhcp/leases/convertToDynamic", params=params
        )
