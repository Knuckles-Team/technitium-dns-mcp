import base64
from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase, destructive

_SECRET_KEYS = frozenset(
    {"sharedsecret", "proxypassword", "password", "pass", "secret", "privatekey"}
)


def _without_secrets(value: Any) -> Any:
    """Drop credential fields (TSIG shared secrets, proxy password) from a settings read."""
    if isinstance(value, dict):
        return {
            k: _without_secrets(v)
            for k, v in value.items()
            if k.lower().replace("_", "") not in _SECRET_KEYS
        }
    if isinstance(value, list):
        return [_without_secrets(v) for v in value]
    return value


class ApiClientSettings(ApiClientBase):
    def get_dns_settings(self, node: str | None = None) -> dict[str, Any]:
        """Reads the DNS server settings. TSIG shared secrets and the proxy password are omitted.

        Args:
            node: Target cluster node.
        """
        return _without_secrets(
            self.request(
                "GET", "/api/settings/getDnsSettings", params=self._fields(node=node)
            )
        )

    def set_dns_settings(
        self,
        dns_server_domain: str | None = None,
        dns_server_local_end_points: list[str] | None = None,
        default_record_ttl: int | None = None,
        use_soa_serial_date_scheme: bool | None = None,
        dns_apps_enable_automatic_update: bool | None = None,
        prefer_ipv6: bool | None = None,
        udp_payload_size: int | None = None,
        dnssec_validation: bool | None = None,
        log_queries: bool | None = None,
        enable_logging_to_file: bool | None = None,
        max_log_file_days: int | None = None,
        enable_in_memory_stats: bool | None = None,
        max_stat_file_days: int | None = None,
        recursion: str | None = None,
        recursion_network_acl: list[str] | None = None,
        randomize_name: bool | None = None,
        qname_minimization: bool | None = None,
        serve_stale: bool | None = None,
        serve_stale_ttl: int | None = None,
        cache_maximum_entries: int | None = None,
        cache_minimum_record_ttl: int | None = None,
        cache_maximum_record_ttl: int | None = None,
        cache_negative_record_ttl: int | None = None,
        cache_failure_record_ttl: int | None = None,
        forwarders: list[str] | None = None,
        forwarder_protocol: str | None = None,
        concurrent_forwarding: bool | None = None,
        forwarder_retries: int | None = None,
        forwarder_timeout: int | None = None,
        forwarder_concurrency: int | None = None,
        enable_blocking: bool | None = None,
        allow_txt_blocking_report: bool | None = None,
        blocking_bypass_list: list[str] | None = None,
        blocking_type: str | None = None,
        custom_blocking_a_records: list[str] | None = None,
        custom_blocking_aaaa_records: list[str] | None = None,
        block_list_urls: list[str] | None = None,
        block_list_update_interval_hours: int | None = None,
        node: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Changes DNS server settings. Only the fields given change.

        Args:
            dns_server_domain: The server's own domain name.
            dns_server_local_end_points: Addresses and ports the server listens on for DNS.
            default_record_ttl: Default TTL for new records.
            use_soa_serial_date_scheme: Use the date scheme for SOA serial numbers.
            dns_apps_enable_automatic_update: Update installed apps automatically.
            prefer_ipv6: Prefer IPv6 when resolving.
            udp_payload_size: EDNS UDP payload size.
            dnssec_validation: Validate DNSSEC on recursive answers.
            log_queries: Record each query in the query log.
            enable_logging_to_file: Write the server log to files.
            max_log_file_days: Days to keep log files.
            enable_in_memory_stats: Keep statistics in memory.
            max_stat_file_days: Days to keep statistics.
            recursion: Recursion policy: Deny, Allow, AllowOnlyForPrivateNetworks or UseSpecifiedNetworkACL.
            recursion_network_acl: Networks the recursion policy allows or denies.
            randomize_name: Randomize the case of query names (0x20).
            qname_minimization: Minimize query names toward upstream servers.
            serve_stale: Answer from stale cache when upstream fails.
            serve_stale_ttl: Seconds to serve stale answers.
            cache_maximum_entries: Cache size limit.
            cache_minimum_record_ttl: Smallest TTL kept in cache.
            cache_maximum_record_ttl: Largest TTL kept in cache.
            cache_negative_record_ttl: TTL for negative answers.
            cache_failure_record_ttl: TTL for failures.
            forwarders: Upstream resolvers.
            forwarder_protocol: Forwarder protocol: Udp, Tcp, Tls, Https or Quic.
            concurrent_forwarding: Query all forwarders at once.
            forwarder_retries: Retries per forwarder.
            forwarder_timeout: Forwarder timeout in milliseconds.
            forwarder_concurrency: Concurrent forwarder queries.
            enable_blocking: Turn domain blocking on or off.
            allow_txt_blocking_report: Return a TXT report for blocked names.
            blocking_bypass_list: Clients or networks that skip blocking.
            blocking_type: How a blocked name answers: AnyAddress, NxDomain or CustomAddress.
            custom_blocking_a_records: IPv4 addresses for CustomAddress blocking.
            custom_blocking_aaaa_records: IPv6 addresses for CustomAddress blocking.
            block_list_urls: Block list source URLs.
            block_list_update_interval_hours: Hours between block list updates.
            node: Target cluster node.
            **extra: Other setting names from the Technitium API, in its camelCase spelling.
        """
        data = self._fields(
            dnsServerDomain=dns_server_domain,
            dnsServerLocalEndPoints=dns_server_local_end_points,
            defaultRecordTtl=default_record_ttl,
            useSoaSerialDateScheme=use_soa_serial_date_scheme,
            dnsAppsEnableAutomaticUpdate=dns_apps_enable_automatic_update,
            preferIPv6=prefer_ipv6,
            udpPayloadSize=udp_payload_size,
            dnssecValidation=dnssec_validation,
            logQueries=log_queries,
            enableLoggingToFile=enable_logging_to_file,
            maxLogFileDays=max_log_file_days,
            enableInMemoryStats=enable_in_memory_stats,
            maxStatFileDays=max_stat_file_days,
            recursion=recursion,
            recursionNetworkACL=recursion_network_acl,
            randomizeName=randomize_name,
            qnameMinimization=qname_minimization,
            serveStale=serve_stale,
            serveStaleTtl=serve_stale_ttl,
            cacheMaximumEntries=cache_maximum_entries,
            cacheMinimumRecordTtl=cache_minimum_record_ttl,
            cacheMaximumRecordTtl=cache_maximum_record_ttl,
            cacheNegativeRecordTtl=cache_negative_record_ttl,
            cacheFailureRecordTtl=cache_failure_record_ttl,
            forwarders=forwarders,
            forwarderProtocol=forwarder_protocol,
            concurrentForwarding=concurrent_forwarding,
            forwarderRetries=forwarder_retries,
            forwarderTimeout=forwarder_timeout,
            forwarderConcurrency=forwarder_concurrency,
            enableBlocking=enable_blocking,
            allowTxtBlockingReport=allow_txt_blocking_report,
            blockingBypassList=blocking_bypass_list,
            blockingType=blocking_type,
            customBlockingARecords=custom_blocking_a_records,
            customBlockingAAAARecords=custom_blocking_aaaa_records,
            blockListUrls=block_list_urls,
            blockListUpdateIntervalHours=block_list_update_interval_hours,
            node=node,
        )
        data.update(self._fields(**extra))
        return _without_secrets(
            self.request("POST", "/api/settings/setDnsSettings", data=data)
        )

    def get_tsig_key_names(self, node: str | None = None) -> dict[str, Any]:
        """Lists the TSIG key names configured on the server (names only, no secrets).

        Args:
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/settings/getTsigKeyNames", params=self._fields(node=node)
        )

    def force_update_block_lists(self, node: str | None = None) -> dict[str, Any]:
        """Starts an immediate download of every block list.

        Args:
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/settings/forceUpdateBlockLists", data=self._fields(node=node)
        )

    def temporary_disable_blocking(
        self, minutes: int, node: str | None = None
    ) -> dict[str, Any]:
        """Turns domain blocking off for a number of minutes, then back on.

        Args:
            minutes: Minutes to disable blocking.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/settings/temporaryDisableBlocking",
            data=self._fields(minutes=minutes, node=node),
        )

    def backup_settings(
        self,
        block_lists: bool | None = None,
        logs: bool | None = None,
        scopes: bool | None = None,
        apps: bool | None = None,
        stats: bool | None = None,
        zones: bool | None = None,
        allowed_zones: bool | None = None,
        blocked_zones: bool | None = None,
        dns_settings: bool | None = None,
        log_settings: bool | None = None,
        auth_config: bool | None = None,
    ) -> dict[str, Any]:
        """Creates a backup zip of the server. The zip comes back base64 encoded.

        Args:
            block_lists: Include block list files.
            logs: Include log files.
            scopes: Include DHCP scopes.
            apps: Include installed apps.
            stats: Include statistics.
            zones: Include authoritative zones.
            allowed_zones: Include the allowed zones.
            blocked_zones: Include the blocked zones.
            dns_settings: Include the DNS settings.
            log_settings: Include the log settings.
            auth_config: Include users, groups and permissions.
        """
        return self.request_binary(
            "GET",
            "/api/settings/backup",
            params=self._fields(
                blockLists=block_lists,
                logs=logs,
                scopes=scopes,
                apps=apps,
                stats=stats,
                zones=zones,
                allowedZones=allowed_zones,
                blockedZones=blocked_zones,
                dnsSettings=dns_settings,
                logSettings=log_settings,
                authConfig=auth_config,
            ),
        )

    @destructive
    def restore_settings(
        self,
        backup_base64: str,
        block_lists: bool | None = None,
        logs: bool | None = None,
        scopes: bool | None = None,
        apps: bool | None = None,
        stats: bool | None = None,
        zones: bool | None = None,
        allowed_zones: bool | None = None,
        blocked_zones: bool | None = None,
        dns_settings: bool | None = None,
        log_settings: bool | None = None,
        auth_config: bool | None = None,
        delete_existing_files: bool | None = None,
    ) -> dict[str, Any]:
        """Restores the server from a backup zip. This overwrites live configuration.

        Args:
            backup_base64: The backup zip, base64 encoded (as `backup_settings` returns it).
            block_lists: Restore block list files.
            logs: Restore log files.
            scopes: Restore DHCP scopes.
            apps: Restore installed apps.
            stats: Restore statistics.
            zones: Restore authoritative zones.
            allowed_zones: Restore the allowed zones.
            blocked_zones: Restore the blocked zones.
            dns_settings: Restore the DNS settings.
            log_settings: Restore the log settings.
            auth_config: Restore users, groups and permissions.
            delete_existing_files: Delete existing files of the chosen kinds first.
        """
        data = self._fields(
            blockLists=block_lists,
            logs=logs,
            scopes=scopes,
            apps=apps,
            stats=stats,
            zones=zones,
            allowedZones=allowed_zones,
            blockedZones=blocked_zones,
            dnsSettings=dns_settings,
            logSettings=log_settings,
            authConfig=auth_config,
            deleteExistingFiles=delete_existing_files,
        )
        files = {
            "file": ("backup.zip", base64.b64decode(backup_base64), "application/zip")
        }
        return self.request("POST", "/api/settings/restore", data=data, files=files)
