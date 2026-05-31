from typing import Any
from technitium_dns_mcp.api.api_client_base import ApiClientBase


class ApiClientZones(ApiClientBase):
    def list_zones(
        self,
        node: str | None = None,
        page_number: int | None = None,
        zones_per_page: int | None = None,
    ) -> dict[str, Any]:
        """Lists authoritative zones.

        Args:
            node: Target server node.
            page_number: Page number for pagination.
            zones_per_page: Number of zones per page.
        """
        params = {}
        if node is not None:
            params["node"] = node
        if page_number is not None:
            params["pageNumber"] = str(page_number)
        if zones_per_page is not None:
            params["zonesPerPage"] = str(zones_per_page)
        return self.request("GET", "/api/zones/list", params=params)

    def list_catalog_zones(self, node: str | None = None) -> dict[str, Any]:
        """Lists all catalog zones.

        Args:
            node: Target server node.
        """
        params = {}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/zones/catalogs/list", params=params)

    def create_zone(
        self,
        zone: str,
        type: str,
        node: str | None = None,
        catalog: str | None = None,
        use_soa_serial_date_scheme: bool | None = None,
        primary_name_server_addresses: str | None = None,
        zone_transfer_protocol: str | None = None,
        tsig_key_name: str | None = None,
        validate_zone: bool | None = None,
        initialize_forwarder: bool | None = None,
        protocol: str | None = None,
        forwarder: str | None = None,
        dnssec_validation: bool | None = None,
        proxy_type: str | None = None,
        proxy_address: str | None = None,
        proxy_port: int | None = None,
        proxy_username: str | None = None,
        proxy_password: str | None = None,
    ) -> dict[str, Any]:
        """Creates a new zone.

        Args:
            zone: Zone domain name.
            type: Type of the zone (e.g. 'Primary', 'Secondary', 'Forwarder', 'Stub').
            node: Target server node.
            catalog: Catalog zone name if any.
            use_soa_serial_date_scheme: Use date scheme for SOA serial.
            primary_name_server_addresses: Addresses for secondary/stub zones.
            zone_transfer_protocol: Transfer protocol (e.g. 'Tsl', 'Tcp', 'Udp').
            tsig_key_name: Name of TSIG key.
            validate_zone: Validate zone data on create.
            initialize_forwarder: Init forwarder zone.
            protocol: Protocol for forwarders.
            forwarder: Forwarder server address.
            dnssec_validation: Enable DNSSEC validation.
            proxy_type: Proxy type.
            proxy_address: Proxy address.
            proxy_port: Proxy port.
            proxy_username: Proxy username.
            proxy_password: Proxy password.
        """
        data = {"zone": zone, "type": type}
        if node is not None:
            data["node"] = node
        if catalog is not None:
            data["catalog"] = catalog
        if use_soa_serial_date_scheme is not None:
            data["useSoaSerialDateScheme"] = str(use_soa_serial_date_scheme).lower()
        if primary_name_server_addresses is not None:
            data["primaryNameServerAddresses"] = primary_name_server_addresses
        if zone_transfer_protocol is not None:
            data["zoneTransferProtocol"] = zone_transfer_protocol
        if tsig_key_name is not None:
            data["tsigKeyName"] = tsig_key_name
        if validate_zone is not None:
            data["validateZone"] = str(validate_zone).lower()
        if initialize_forwarder is not None:
            data["initializeForwarder"] = str(initialize_forwarder).lower()
        if protocol is not None:
            data["protocol"] = protocol
        if forwarder is not None:
            data["forwarder"] = forwarder
        if dnssec_validation is not None:
            data["dnssecValidation"] = str(dnssec_validation).lower()
        if proxy_type is not None:
            data["proxyType"] = proxy_type
        if proxy_address is not None:
            data["proxyAddress"] = proxy_address
        if proxy_port is not None:
            data["proxyPort"] = str(proxy_port)
        if proxy_username is not None:
            data["proxyUsername"] = proxy_username
        if proxy_password is not None:
            data["proxyPassword"] = proxy_password

        return self.request("POST", "/api/zones/create", data=data)

    def import_zone(
        self,
        zone: str,
        node: str | None = None,
        overwrite: bool | None = None,
        overwrite_zone: bool | None = None,
        overwrite_soa_serial: bool | None = None,
        file_content: str | None = None,
    ) -> dict[str, Any]:
        """Imports zone content from a zone file.

        Args:
            zone: Zone domain name.
            node: Target server node.
            overwrite: Overwrite records flag.
            overwrite_zone: Complete zone overwrite.
            overwrite_soa_serial: Overwrite serial.
            file_content: Text zone data payload.
        """
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        if overwrite is not None:
            data["overwrite"] = str(overwrite).lower()
        if overwrite_zone is not None:
            data["overwriteZone"] = str(overwrite_zone).lower()
        if overwrite_soa_serial is not None:
            data["overwriteSoaSerial"] = str(overwrite_soa_serial).lower()

        files = None
        if file_content is not None:
            files = {"file": ("zone.txt", file_content, "text/plain")}

        return self.request("POST", "/api/zones/import", data=data, files=files)

    def export_zone(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Exports authoritative zone file.

        Args:
            zone: Zone domain name.
            node: Target server node.
        """
        params = {"zone": zone}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/zones/export", params=params)

    def clone_zone(
        self, zone: str, source_zone: str, node: str | None = None
    ) -> dict[str, Any]:
        """Clones a zone from an existing local zone.

        Args:
            zone: Target zone name.
            source_zone: Source zone name.
            node: Target server node.
        """
        data = {"zone": zone, "sourceZone": source_zone}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/zones/clone", data=data)

    def convert_zone_type(
        self, zone: str, type: str, node: str | None = None
    ) -> dict[str, Any]:
        """Converts zone type.

        Args:
            zone: Zone domain name.
            type: Target type.
            node: Target server node.
        """
        data = {"zone": zone, "type": type}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/zones/convert", data=data)

    def enable_zone(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Enables authoritative zone.

        Args:
            zone: Zone domain name.
            node: Target server node.
        """
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/zones/enable", data=data)

    def disable_zone(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Disables authoritative zone.

        Args:
            zone: Zone domain name.
            node: Target server node.
        """
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/zones/disable", data=data)

    def delete_zone(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Deletes authoritative zone.

        Args:
            zone: Zone domain name.
            node: Target server node.
        """
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/zones/delete", data=data)

    def resync_zone(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Forces authoritative secondary zone resynchronization.

        Args:
            zone: Zone domain name.
            node: Target server node.
        """
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/zones/resync", data=data)

    def get_zone_options(
        self,
        zone: str,
        node: str | None = None,
        include_available_catalog_zone_names: bool | None = None,
        include_available_tsig_key_names: bool | None = None,
    ) -> dict[str, Any]:
        """Gets settings/options of a zone.

        Args:
            zone: Zone domain name.
            node: Target server node.
            include_available_catalog_zone_names: Include catalog names.
            include_available_tsig_key_names: Include TSIG key names.
        """
        params = {"zone": zone}
        if node is not None:
            params["node"] = node
        if include_available_catalog_zone_names is not None:
            params["includeAvailableCatalogZoneNames"] = str(
                include_available_catalog_zone_names
            ).lower()
        if include_available_tsig_key_names is not None:
            params["includeAvailableTsigKeyNames"] = str(
                include_available_tsig_key_names
            ).lower()
        return self.request("GET", "/api/zones/options/get", params=params)

    def set_zone_options(
        self,
        zone: str,
        node: str | None = None,
        disabled: bool | None = None,
        catalog: str | None = None,
        override_catalog_query_access: bool | None = None,
        override_catalog_zone_transfer: bool | None = None,
        override_catalog_notify: bool | None = None,
        primary_name_server_addresses: str | None = None,
        primary_zone_transfer_protocol: str | None = None,
        primary_zone_transfer_tsig_key_name: str | None = None,
        validate_zone: bool | None = None,
        query_access: str | None = None,
        query_access_network_acl: str | None = None,
        zone_transfer: str | None = None,
        zone_transfer_network_acl: str | None = None,
        zone_transfer_tsig_key_names: str | None = None,
        notify: str | None = None,
        notify_name_servers: str | None = None,
        notify_secondary_catalogs_name_servers: str | None = None,
        update: str | None = None,
        update_network_acl: str | None = None,
        update_security_policies: str | None = None,
    ) -> dict[str, Any]:
        """Sets settings/options for a zone."""
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        if disabled is not None:
            data["disabled"] = str(disabled).lower()
        if catalog is not None:
            data["catalog"] = catalog
        if override_catalog_query_access is not None:
            data["overrideCatalogQueryAccess"] = str(
                override_catalog_query_access
            ).lower()
        if override_catalog_zone_transfer is not None:
            data["overrideCatalogZoneTransfer"] = str(
                override_catalog_zone_transfer
            ).lower()
        if override_catalog_notify is not None:
            data["overrideCatalogNotify"] = str(override_catalog_notify).lower()
        if primary_name_server_addresses is not None:
            data["primaryNameServerAddresses"] = primary_name_server_addresses
        if primary_zone_transfer_protocol is not None:
            data["primaryZoneTransferProtocol"] = primary_zone_transfer_protocol
        if primary_zone_transfer_tsig_key_name is not None:
            data["primaryZoneTransferTsigKeyName"] = primary_zone_transfer_tsig_key_name
        if validate_zone is not None:
            data["validateZone"] = str(validate_zone).lower()
        if query_access is not None:
            data["queryAccess"] = query_access
        if query_access_network_acl is not None:
            data["queryAccessNetworkACL"] = query_access_network_acl
        if zone_transfer is not None:
            data["zoneTransfer"] = zone_transfer
        if zone_transfer_network_acl is not None:
            data["zoneTransferNetworkACL"] = zone_transfer_network_acl
        if zone_transfer_tsig_key_names is not None:
            data["zoneTransferTsigKeyNames"] = zone_transfer_tsig_key_names
        if notify is not None:
            data["notify"] = notify
        if notify_name_servers is not None:
            data["notifyNameServers"] = notify_name_servers
        if notify_secondary_catalogs_name_servers is not None:
            data["notifySecondaryCatalogsNameServers"] = (
                notify_secondary_catalogs_name_servers
            )
        if update is not None:
            data["update"] = update
        if update_network_acl is not None:
            data["updateNetworkACL"] = update_network_acl
        if update_security_policies is not None:
            data["updateSecurityPolicies"] = update_security_policies

        return self.request("POST", "/api/zones/options/set", data=data)

    def get_zone_permissions(
        self,
        zone: str,
        node: str | None = None,
        include_users_and_groups: bool | None = None,
    ) -> dict[str, Any]:
        """Gets user/group permissions of a zone."""
        params = {"zone": zone}
        if node is not None:
            params["node"] = node
        if include_users_and_groups is not None:
            params["includeUsersAndGroups"] = str(include_users_and_groups).lower()
        return self.request("GET", "/api/zones/permissions/get", params=params)

    def set_zone_permissions(
        self,
        zone: str,
        node: str | None = None,
        user_permissions: str | None = None,
        group_permissions: str | None = None,
    ) -> dict[str, Any]:
        """Sets permissions for a zone."""
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        if user_permissions is not None:
            data["userPermissions"] = user_permissions
        if group_permissions is not None:
            data["groupPermissions"] = group_permissions
        return self.request("POST", "/api/zones/permissions/set", data=data)

    def sign_zone(
        self,
        zone: str,
        node: str | None = None,
        algorithm: str | None = None,
        pem_ksk_private_key: str | None = None,
        pem_zsk_private_key: str | None = None,
        hash_algorithm: str | None = None,
        ksk_key_size: int | None = None,
        zsk_key_size: int | None = None,
        curve: str | None = None,
        dns_key_ttl: int | None = None,
        zsk_rollover_days: int | None = None,
        nx_proof: str | None = None,
        iterations: int | None = None,
        salt_length: int | None = None,
    ) -> dict[str, Any]:
        """Signs the zone with DNSSEC."""
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        if algorithm is not None:
            data["algorithm"] = algorithm
        if pem_ksk_private_key is not None:
            data["pemKskPrivateKey"] = pem_ksk_private_key
        if pem_zsk_private_key is not None:
            data["pemZskPrivateKey"] = pem_zsk_private_key
        if hash_algorithm is not None:
            data["hashAlgorithm"] = hash_algorithm
        if ksk_key_size is not None:
            data["kskKeySize"] = str(ksk_key_size)
        if zsk_key_size is not None:
            data["zskKeySize"] = str(zsk_key_size)
        if curve is not None:
            data["curve"] = curve
        if dns_key_ttl is not None:
            data["dnsKeyTtl"] = str(dns_key_ttl)
        if zsk_rollover_days is not None:
            data["zskRolloverDays"] = str(zsk_rollover_days)
        if nx_proof is not None:
            data["nxProof"] = nx_proof
        if iterations is not None:
            data["iterations"] = str(iterations)
        if salt_length is not None:
            data["saltLength"] = str(salt_length)

        return self.request("POST", "/api/zones/dnssec/sign", data=data)

    def unsign_zone(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Unsigns/removes DNSSEC from a zone."""
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request("POST", "/api/zones/dnssec/unsign", data=data)

    def get_ds_info(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Retrieves DNSSEC Delegation Signer (DS) records information."""
        params = {"zone": zone}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/zones/dnssec/viewDS", params=params)

    def get_dnssec_properties(
        self, zone: str, node: str | None = None
    ) -> dict[str, Any]:
        """Retrieves DNSSEC properties/keys for a zone."""
        params = {"zone": zone}
        if node is not None:
            params["node"] = node
        return self.request("GET", "/api/zones/dnssec/properties/get", params=params)

    def convert_to_nsec(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Converts proof of non-existence to NSEC."""
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/convertToNSEC", data=data
        )

    def convert_to_nsec3(self, zone: str, node: str | None = None) -> dict[str, Any]:
        """Converts proof of non-existence to NSEC3."""
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/convertToNSEC3", data=data
        )

    def update_nsec3_params(
        self,
        zone: str,
        iterations: int,
        salt_length: int,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Updates NSEC3 parameters."""
        data = {
            "zone": zone,
            "iterations": str(iterations),
            "saltLength": str(salt_length),
        }
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/updateNSEC3Params", data=data
        )

    def update_dnskey_ttl(
        self, zone: str, ttl: int, node: str | None = None
    ) -> dict[str, Any]:
        """Updates DNSKEY TTL."""
        data = {"zone": zone, "ttl": str(ttl)}
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/updateDnsKeyTtl", data=data
        )

    def add_private_key(
        self,
        zone: str,
        key_type: str,
        rollover_days: int,
        algorithm: str | None = None,
        pem_private_key: str | None = None,
        hash_algorithm: str | None = None,
        key_size: int | None = None,
        curve: str | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Adds a private DNSSEC key to the zone."""
        data = {"zone": zone, "keyType": key_type, "rolloverDays": str(rollover_days)}
        if node is not None:
            data["node"] = node
        if algorithm is not None:
            data["algorithm"] = algorithm
        if pem_private_key is not None:
            data["pemPrivateKey"] = pem_private_key
        if hash_algorithm is not None:
            data["hashAlgorithm"] = hash_algorithm
        if key_size is not None:
            data["keySize"] = str(key_size)
        if curve is not None:
            data["curve"] = curve

        return self.request(
            "POST", "/api/zones/dnssec/properties/addPrivateKey", data=data
        )

    def update_private_key(
        self, zone: str, key_tag: int, rollover_days: int, node: str | None = None
    ) -> dict[str, Any]:
        """Updates private key parameters."""
        data = {
            "zone": zone,
            "keyTag": str(key_tag),
            "rolloverDays": str(rollover_days),
        }
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/updatePrivateKey", data=data
        )

    def delete_private_key(
        self, zone: str, key_tag: int, node: str | None = None
    ) -> dict[str, Any]:
        """Deletes a private DNSSEC key."""
        data = {"zone": zone, "keyTag": str(key_tag)}
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/deletePrivateKey", data=data
        )

    def publish_all_private_keys(
        self, zone: str, node: str | None = None
    ) -> dict[str, Any]:
        """Publishes all private DNSSEC keys."""
        data = {"zone": zone}
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/publishAllPrivateKeys", data=data
        )

    def rollover_dnskey(
        self, zone: str, key_tag: int, node: str | None = None
    ) -> dict[str, Any]:
        """Rolls over the DNSKEY."""
        data = {"zone": zone, "keyTag": str(key_tag)}
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/rolloverDnsKey", data=data
        )

    def retire_dnskey(
        self, zone: str, key_tag: int, node: str | None = None
    ) -> dict[str, Any]:
        """Retires the DNSKEY."""
        data = {"zone": zone, "keyTag": str(key_tag)}
        if node is not None:
            data["node"] = node
        return self.request(
            "POST", "/api/zones/dnssec/properties/retireDnsKey", data=data
        )

    def add_record(
        self,
        zone: str,
        domain: str,
        type: str,
        ttl: int,
        overwrite: bool | None = None,
        node: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Adds a new DNS record.

        Args:
            zone: Zone domain name.
            domain: Domain name of the record.
            type: Record type (A, AAAA, CNAME, TXT, MX, SRV, NS, CAA, PTR, etc.).
            ttl: Time-To-Live value in seconds.
            overwrite: Set True to overwrite existing records with same domain and type.
            node: Target server node.
            **kwargs: Extra parameters depending on record type (e.g. ipAddress, nameServer, text, mailExchange, priority).
        """
        data = {"zone": zone, "domain": domain, "type": type, "ttl": str(ttl)}
        if overwrite is not None:
            data["overwrite"] = str(overwrite).lower()
        if node is not None:
            data["node"] = node

        # Append dynamic keyword arguments mapping directly to API inputs
        for k, v in kwargs.items():
            if v is not None:
                data[k] = str(v)

        return self.request("POST", "/api/zones/records/add", data=data)

    def get_records(
        self,
        domain: str,
        zone: str,
        node: str | None = None,
        list_zone: bool | None = None,
        page_number: int | None = None,
        records_per_page: int | None = None,
    ) -> dict[str, Any]:
        """Retrieves DNS records matching the domain.

        Args:
            domain: Domain name.
            zone: Zone domain name.
            node: Target server node.
            list_zone: If True, lists all records under the zone instead.
            page_number: Page number for paginated lists.
            records_per_page: Count per page.
        """
        params = {"domain": domain, "zone": zone}
        if node is not None:
            params["node"] = node
        if list_zone is not None:
            params["listZone"] = str(list_zone).lower()
        if page_number is not None:
            params["pageNumber"] = str(page_number)
        if records_per_page is not None:
            params["recordsPerPage"] = str(records_per_page)

        return self.request("GET", "/api/zones/records/get", params=params)

    def update_record(
        self,
        zone: str,
        domain: str,
        type: str,
        ttl: int | None = None,
        node: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Updates an existing DNS record."""
        data = {"zone": zone, "domain": domain, "type": type}
        if ttl is not None:
            data["ttl"] = str(ttl)
        if node is not None:
            data["node"] = node

        for k, v in kwargs.items():
            if v is not None:
                data[k] = str(v)

        return self.request("POST", "/api/zones/records/update", data=data)

    def delete_record(
        self,
        zone: str,
        domain: str,
        type: str,
        node: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Deletes matching DNS record(s)."""
        data = {"zone": zone, "domain": domain, "type": type}
        if node is not None:
            data["node"] = node

        for k, v in kwargs.items():
            if v is not None:
                data[k] = str(v)

        return self.request("POST", "/api/zones/records/delete", data=data)
