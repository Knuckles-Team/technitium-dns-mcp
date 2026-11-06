"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        task="publish-dns-record",
        description="Add a DNS record to an existing zone and read it back.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_zones",
                params=("node", "page_number", "zones_per_page"),
                result=("zones",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_records",
                params=(
                    "domain",
                    "zone",
                    "node",
                    "list_zone",
                    "page_number",
                    "records_per_page",
                ),
                result=("records",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_add_record",
                params=(
                    "zone",
                    "domain",
                    "type",
                    "ttl",
                    "overwrite",
                    "node",
                    "comments",
                    "expiry_ttl",
                    "ip_address",
                    "ptr",
                    "create_ptr_zone",
                    "update_svcb_hints",
                    "name_server",
                    "glue",
                    "cname",
                    "ptr_name",
                    "exchange",
                    "preference",
                    "text",
                    "split_text",
                    "priority",
                    "weight",
                    "port",
                    "target",
                    "flags",
                    "tag",
                    "value",
                    "params_json",
                ),
                result=("addedRecord",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="change-dns-record",
        description="Change the data or TTL of an existing record.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_records",
                params=(
                    "domain",
                    "zone",
                    "node",
                    "list_zone",
                    "page_number",
                    "records_per_page",
                ),
                result=("records",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_update_record",
                params=(
                    "zone",
                    "domain",
                    "type",
                    "ttl",
                    "node",
                    "new_domain",
                    "comments",
                    "expiry_ttl",
                    "ip_address",
                    "new_ip_address",
                    "ptr",
                    "create_ptr_zone",
                    "name_server",
                    "new_name_server",
                    "cname",
                    "ptr_name",
                    "new_ptr_name",
                    "exchange",
                    "new_exchange",
                    "preference",
                    "new_preference",
                    "text",
                    "new_text",
                    "split_text",
                    "priority",
                    "new_priority",
                    "weight",
                    "new_weight",
                    "port",
                    "new_port",
                    "target",
                    "new_target",
                    "flags",
                    "new_flags",
                    "tag",
                    "new_tag",
                    "value",
                    "new_value",
                    "params_json",
                ),
                result=("updatedRecord",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="remove-dns-record",
        description="Delete one record after reading the zone.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_records",
                params=(
                    "domain",
                    "zone",
                    "node",
                    "list_zone",
                    "page_number",
                    "records_per_page",
                ),
                result=("records",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_record",
                params=(
                    "zone",
                    "domain",
                    "type",
                    "node",
                    "ip_address",
                    "name_server",
                    "ptr_name",
                    "exchange",
                    "preference",
                    "text",
                    "priority",
                    "weight",
                    "port",
                    "target",
                    "flags",
                    "tag",
                    "value",
                    "params_json",
                    "confirm",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                    Refusal("NOT_FOUND", "no record matches the name, type and data"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="create-zone",
        description="Create an authoritative or forwarder zone and set its options.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_zones",
                params=("node", "page_number", "zones_per_page"),
                result=("zones",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_create_zone",
                params=(
                    "zone",
                    "type",
                    "node",
                    "catalog",
                    "use_soa_serial_date_scheme",
                    "primary_name_server_addresses",
                    "zone_transfer_protocol",
                    "tsig_key_name",
                    "validate_zone",
                    "initialize_forwarder",
                    "protocol",
                    "forwarder",
                    "dnssec_validation",
                    "proxy_type",
                    "proxy_address",
                    "proxy_port",
                    "proxy_username",
                    "proxy_password",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_zone_options",
                params=(
                    "zone",
                    "node",
                    "include_available_catalog_zone_names",
                    "include_available_tsig_key_names",
                ),
                result=("zone options",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_zone_options",
                params=(
                    "zone",
                    "node",
                    "disabled",
                    "catalog",
                    "override_catalog_query_access",
                    "override_catalog_zone_transfer",
                    "override_catalog_notify",
                    "primary_name_server_addresses",
                    "primary_zone_transfer_protocol",
                    "primary_zone_transfer_tsig_key_name",
                    "validate_zone",
                    "query_access",
                    "query_access_network_acl",
                    "zone_transfer",
                    "zone_transfer_network_acl",
                    "zone_transfer_tsig_key_names",
                    "notify",
                    "notify_name_servers",
                    "notify_secondary_catalogs_name_servers",
                    "update",
                    "update_network_acl",
                    "update_security_policies",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-zone-lifecycle",
        description="Enable, disable, resync, clone, convert or delete a zone.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_zones",
                params=("node", "page_number", "zones_per_page"),
                result=("zones",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_list_catalog_zones",
                params=("node",),
                result=("catalogZones",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_enable_zone",
                params=("zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_disable_zone",
                params=("zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_resync_zone",
                params=("zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_clone_zone",
                params=("zone", "source_zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_convert_zone_type",
                params=("zone", "type", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_zone",
                params=("zone", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="transfer-zone-file",
        description="Export a zone to a zone file or import one, for migration.",
        steps=(
            ToolStep(
                tool="technitium_dns_export_zone",
                params=("zone", "node"),
                result=("text",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_import_zone",
                params=(
                    "zone",
                    "node",
                    "overwrite",
                    "overwrite_zone",
                    "overwrite_soa_serial",
                    "file_content",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="set-zone-permissions",
        description="Read and change which users and groups can view, modify or delete a zone.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_zone_permissions",
                params=("zone", "node", "include_users_and_groups"),
                result=("permissions",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_zone_permissions",
                params=("zone", "node", "user_permissions", "group_permissions"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="sign-zone-dnssec",
        description="Sign a zone, read its DS record and tune NSEC or NSEC3, or unsign it.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_dnssec_properties",
                params=("zone", "node"),
                result=("dnssecStatus", "dnssecPrivateKeys"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_sign_zone",
                params=(
                    "zone",
                    "node",
                    "algorithm",
                    "pem_ksk_private_key",
                    "pem_zsk_private_key",
                    "hash_algorithm",
                    "ksk_key_size",
                    "zsk_key_size",
                    "curve",
                    "dns_key_ttl",
                    "zsk_rollover_days",
                    "nx_proof",
                    "iterations",
                    "salt_length",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_ds_info",
                params=("zone", "node"),
                result=("dsRecords",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_convert_to_nsec",
                params=("zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_convert_to_nsec3",
                params=("zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_update_nsec3_params",
                params=("zone", "iterations", "salt_length", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_update_dnskey_ttl",
                params=("zone", "ttl", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_unsign_zone",
                params=("zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="rotate-dnssec-keys",
        description="Add, publish, roll over, retire and delete DNSSEC private keys.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_dnssec_properties",
                params=("zone", "node"),
                result=("dnssecPrivateKeys",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_add_private_key",
                params=(
                    "zone",
                    "key_type",
                    "rollover_days",
                    "algorithm",
                    "pem_private_key",
                    "hash_algorithm",
                    "key_size",
                    "curve",
                    "node",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_update_private_key",
                params=("zone", "key_tag", "rollover_days", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_publish_all_private_keys",
                params=("zone", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_rollover_dnskey",
                params=("zone", "key_tag", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_retire_dnskey",
                params=("zone", "key_tag", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_private_key",
                params=("zone", "key_tag", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="review-dns-health",
        description="Read query statistics, top clients and domains, metrics and update status.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_stats",
                params=(
                    "node",
                    "stats_type",
                    "utc",
                    "dont_trim_query_type_data",
                    "start",
                    "end",
                ),
                result=("stats",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_top_stats",
                params=(
                    "node",
                    "stats_type",
                    "start",
                    "end",
                    "stats_category",
                    "limit",
                    "no_reverse_lookup",
                    "only_rate_limited_clients",
                ),
                result=("topClients", "topDomains"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_metrics_json",
                params=(),
                result=("metrics",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_metrics_text",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_check_for_update",
                params=(),
                result=("updateAvailable",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_all_stats",
                params=("node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="read-server-settings",
        description="Read server settings and TSIG key names (secrets are omitted).",
        steps=(
            ToolStep(
                tool="technitium_dns_get_dns_settings",
                params=("node",),
                result=("settings",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_tsig_key_names",
                params=("node",),
                result=("keyNames",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="change-server-settings",
        description="Change recursion, forwarders, cache, logging or blocking settings.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_dns_settings",
                params=("node",),
                result=("settings",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_dns_settings",
                params=(
                    "dns_server_domain",
                    "dns_server_local_end_points",
                    "default_record_ttl",
                    "use_soa_serial_date_scheme",
                    "dns_apps_enable_automatic_update",
                    "prefer_ipv6",
                    "udp_payload_size",
                    "dnssec_validation",
                    "log_queries",
                    "enable_logging_to_file",
                    "max_log_file_days",
                    "enable_in_memory_stats",
                    "max_stat_file_days",
                    "recursion",
                    "recursion_network_acl",
                    "randomize_name",
                    "qname_minimization",
                    "serve_stale",
                    "serve_stale_ttl",
                    "cache_maximum_entries",
                    "cache_minimum_record_ttl",
                    "cache_maximum_record_ttl",
                    "cache_negative_record_ttl",
                    "cache_failure_record_ttl",
                    "forwarders",
                    "forwarder_protocol",
                    "concurrent_forwarding",
                    "forwarder_retries",
                    "forwarder_timeout",
                    "forwarder_concurrency",
                    "enable_blocking",
                    "allow_txt_blocking_report",
                    "blocking_bypass_list",
                    "blocking_type",
                    "custom_blocking_a_records",
                    "custom_blocking_aaaa_records",
                    "block_list_urls",
                    "block_list_update_interval_hours",
                    "node",
                    "params_json",
                ),
                result=("settings",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-block-list",
        description="Block domains, import or export the blocked list, refresh block list sources and pause blocking.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_blocked",
                params=("domain", "node"),
                result=("zones",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_add_blocked",
                params=("domain", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_blocked",
                params=("domain", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_flush_blocked",
                params=("node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_export_blocked",
                params=("node",),
                result=("text",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_import_blocked",
                params=("blocked_zones", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_force_update_block_lists",
                params=("node",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_temporary_disable_blocking",
                params=("minutes", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-allow-list",
        description="Allow domains that block lists would block, and import or export the allowed list.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_allowed",
                params=("domain", "node"),
                result=("zones",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_add_allowed",
                params=("domain", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_allowed",
                params=("domain", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_flush_allowed",
                params=("node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_export_allowed",
                params=("node",),
                result=("text",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_import_allowed",
                params=("allowed_zones", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-dns-cache",
        description="Browse the cache and remove one domain or the whole cache.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_cache",
                params=("domain", "node"),
                result=("zones", "records"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_cached_zone",
                params=("domain", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_flush_cache",
                params=("node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="review-query-logs",
        description="Search the query log and read server log files.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_logs",
                params=("node",),
                result=("logFiles",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_download_log",
                params=("file_name", "limit", "node"),
                result=("text",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_query_logs",
                params=(
                    "name",
                    "class_path",
                    "page_number",
                    "entries_per_page",
                    "descending_order",
                    "start",
                    "end",
                    "client_ip_address",
                    "protocol",
                    "response_type",
                    "rcode",
                    "qname",
                    "qtype",
                    "qclass",
                    "node",
                ),
                result=("entries",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="prune-logs",
        description="Delete one server log file or all of them.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_logs",
                params=("node",),
                result=("logFiles",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_log",
                params=("log", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_all_logs",
                params=("node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-dhcp-scopes",
        description="Create, change, enable, disable and delete DHCP scopes.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_dhcp_scopes",
                params=("node",),
                result=("scopes",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_dhcp_scope",
                params=("name", "node"),
                result=("scope",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_dhcp_scope",
                params=(
                    "name",
                    "new_name",
                    "starting_address",
                    "ending_address",
                    "subnet_mask",
                    "lease_time_days",
                    "lease_time_hours",
                    "lease_time_minutes",
                    "offer_delay_time",
                    "ping_check_enabled",
                    "ping_check_timeout",
                    "ping_check_retries",
                    "domain_name",
                    "domain_search_list",
                    "dns_updates",
                    "dns_ttl",
                    "server_address",
                    "router_address",
                    "use_this_dns_server",
                    "dns_servers",
                    "ntp_servers",
                    "reserved_leases",
                    "allow_only_reserved_leases",
                    "block_locally_administered_mac_addresses",
                    "ignore_client_identifier_option",
                    "node",
                    "params_json",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_enable_dhcp_scope",
                params=("name", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_disable_dhcp_scope",
                params=("name", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_dhcp_scope",
                params=("name", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-dhcp-leases",
        description="List leases, reserve or release an address.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_dhcp_leases",
                params=("node",),
                result=("leases",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_add_dhcp_reserved_lease",
                params=(
                    "name",
                    "hardware_address",
                    "ip_address",
                    "host_name",
                    "comments",
                    "node",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_remove_dhcp_reserved_lease",
                params=("name", "hardware_address", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_remove_dhcp_lease",
                params=(
                    "name",
                    "hardware_address",
                    "client_identifier",
                    "address",
                    "node",
                    "confirm",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_convert_dhcp_lease_to_reserved",
                params=(
                    "name",
                    "hardware_address",
                    "client_identifier",
                    "address",
                    "node",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_convert_dhcp_lease_to_dynamic",
                params=(
                    "name",
                    "hardware_address",
                    "client_identifier",
                    "address",
                    "node",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-dns-apps",
        description="Install, update, configure and remove DNS apps.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_apps",
                params=("node",),
                result=("apps",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_list_store_apps",
                params=("node",),
                result=("storeApps",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_download_and_install_app",
                params=("name", "url", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_download_and_update_app",
                params=("name", "url", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_app_config",
                params=("name", "node"),
                result=("config",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_app_config",
                params=("name", "config", "node"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_uninstall_app",
                params=("name", "node", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="administer-users-and-groups",
        description="Create, change and delete users and groups.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_users",
                params=(),
                result=("users",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_user",
                params=("user", "include_groups"),
                result=("userDetails",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_create_user",
                params=("user", "password", "display_name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_user",
                params=(
                    "user",
                    "display_name",
                    "new_user",
                    "disabled",
                    "session_timeout_seconds",
                    "new_password",
                    "iterations",
                    "member_of_groups",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_user",
                params=("user", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_list_groups",
                params=(),
                result=("groups",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_group",
                params=("group", "include_users"),
                result=("groupDetails",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_create_group",
                params=("group", "description"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_group",
                params=("group", "new_group", "description", "members"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_group",
                params=("group", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="administer-permissions",
        description="Read and set section permissions for users and groups.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_permissions",
                params=(),
                result=("permissions",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_permissions",
                params=("section", "include_users_and_groups"),
                result=("section",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_permissions",
                params=("section", "user_permissions", "group_permissions"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="administer-sessions",
        description="List active sessions, end one, and create an API token for a user.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_admin_sessions",
                params=(),
                result=("sessions",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_admin_session",
                params=("partial_token", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_create_api_token",
                params=("user", "token_name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-own-session",
        description="Sign in, sign out, manage tokens, password, two-factor and profile of the calling user.",
        steps=(
            ToolStep(
                tool="technitium_dns_get_sso_status",
                params=(),
                result=("ssoEnabled",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_login",
                params=("user", "password", "totp", "include_info"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_session_info",
                params=(),
                result=("username", "tokenName"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_create_token",
                params=("user", "password", "token_name", "totp"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_create_single_use_token",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_delete_user_session",
                params=("partial_token", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_change_password",
                params=("password", "new_password", "totp", "iterations"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_initialize_2fa",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_enable_2fa",
                params=("totp",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_disable_2fa",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_get_user_profile_details",
                params=(),
                result=("displayName",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_set_user_profile_details",
                params=("display_name", "session_timeout_seconds"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="back-up-and-restore",
        description="Download a backup of the server and restore from one.",
        steps=(
            ToolStep(
                tool="technitium_dns_backup_settings",
                params=(
                    "block_lists",
                    "logs",
                    "scopes",
                    "apps",
                    "stats",
                    "zones",
                    "allowed_zones",
                    "blocked_zones",
                    "dns_settings",
                    "log_settings",
                    "auth_config",
                ),
                result=("size", "content_base64"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_dns_restore_settings",
                params=(
                    "backup_base64",
                    "block_lists",
                    "logs",
                    "scopes",
                    "apps",
                    "stats",
                    "zones",
                    "allowed_zones",
                    "blocked_zones",
                    "dns_settings",
                    "log_settings",
                    "auth_config",
                    "delete_existing_files",
                    "confirm",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="map-dns-to-graph",
        description="Mirror zones and records into the knowledge graph.",
        steps=(
            ToolStep(
                tool="technitium_dns_list_zones",
                params=("node", "page_number", "zones_per_page"),
                result=("zones",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="technitium_ingest_zones",
                params=("params_json",),
                result=("zones", "records"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        task="publish-dns-record",
        tools=(
            "technitium_dns_list_zones",
            "technitium_dns_get_records",
            "technitium_dns_add_record",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations", "dns-record-manager"),
    ),
    SurfaceLink(
        task="change-dns-record",
        tools=("technitium_dns_get_records", "technitium_dns_update_record"),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations", "dns-record-manager"),
    ),
    SurfaceLink(
        task="remove-dns-record",
        tools=("technitium_dns_get_records", "technitium_dns_delete_record"),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations", "dns-record-manager"),
    ),
    SurfaceLink(
        task="create-zone",
        tools=(
            "technitium_dns_list_zones",
            "technitium_dns_create_zone",
            "technitium_dns_get_zone_options",
            "technitium_dns_set_zone_options",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations",),
    ),
    SurfaceLink(
        task="manage-zone-lifecycle",
        tools=(
            "technitium_dns_list_zones",
            "technitium_dns_list_catalog_zones",
            "technitium_dns_enable_zone",
            "technitium_dns_disable_zone",
            "technitium_dns_resync_zone",
            "technitium_dns_clone_zone",
            "technitium_dns_convert_zone_type",
            "technitium_dns_delete_zone",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations",),
    ),
    SurfaceLink(
        task="transfer-zone-file",
        tools=("technitium_dns_export_zone", "technitium_dns_import_zone"),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations", "dns-migration-utility"),
    ),
    SurfaceLink(
        task="set-zone-permissions",
        tools=(
            "technitium_dns_get_zone_permissions",
            "technitium_dns_set_zone_permissions",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations", "technitium-dns-administration"),
    ),
    SurfaceLink(
        task="sign-zone-dnssec",
        tools=(
            "technitium_dns_get_dnssec_properties",
            "technitium_dns_sign_zone",
            "technitium_dns_get_ds_info",
            "technitium_dns_convert_to_nsec",
            "technitium_dns_convert_to_nsec3",
            "technitium_dns_update_nsec3_params",
            "technitium_dns_update_dnskey_ttl",
            "technitium_dns_unsign_zone",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations",),
    ),
    SurfaceLink(
        task="rotate-dnssec-keys",
        tools=(
            "technitium_dns_get_dnssec_properties",
            "technitium_dns_add_private_key",
            "technitium_dns_update_private_key",
            "technitium_dns_publish_all_private_keys",
            "technitium_dns_rollover_dnskey",
            "technitium_dns_retire_dnskey",
            "technitium_dns_delete_private_key",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations",),
    ),
    SurfaceLink(
        task="review-dns-health",
        tools=(
            "technitium_dns_get_stats",
            "technitium_dns_get_top_stats",
            "technitium_dns_get_metrics_json",
            "technitium_dns_get_metrics_text",
            "technitium_dns_check_for_update",
            "technitium_dns_delete_all_stats",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-mcp-operations", "technitium-dns-filtering"),
    ),
    SurfaceLink(
        task="read-server-settings",
        tools=("technitium_dns_get_dns_settings", "technitium_dns_get_tsig_key_names"),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-filtering",),
    ),
    SurfaceLink(
        task="change-server-settings",
        tools=("technitium_dns_get_dns_settings", "technitium_dns_set_dns_settings"),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-filtering",),
    ),
    SurfaceLink(
        task="manage-block-list",
        tools=(
            "technitium_dns_list_blocked",
            "technitium_dns_add_blocked",
            "technitium_dns_delete_blocked",
            "technitium_dns_flush_blocked",
            "technitium_dns_export_blocked",
            "technitium_dns_import_blocked",
            "technitium_dns_force_update_block_lists",
            "technitium_dns_temporary_disable_blocking",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-filtering",),
    ),
    SurfaceLink(
        task="manage-allow-list",
        tools=(
            "technitium_dns_list_allowed",
            "technitium_dns_add_allowed",
            "technitium_dns_delete_allowed",
            "technitium_dns_flush_allowed",
            "technitium_dns_export_allowed",
            "technitium_dns_import_allowed",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-filtering",),
    ),
    SurfaceLink(
        task="manage-dns-cache",
        tools=(
            "technitium_dns_list_cache",
            "technitium_dns_delete_cached_zone",
            "technitium_dns_flush_cache",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-filtering",),
    ),
    SurfaceLink(
        task="review-query-logs",
        tools=(
            "technitium_dns_list_logs",
            "technitium_dns_download_log",
            "technitium_dns_query_logs",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-filtering",),
    ),
    SurfaceLink(
        task="prune-logs",
        tools=(
            "technitium_dns_list_logs",
            "technitium_dns_delete_log",
            "technitium_dns_delete_all_logs",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-filtering",),
    ),
    SurfaceLink(
        task="manage-dhcp-scopes",
        tools=(
            "technitium_dns_list_dhcp_scopes",
            "technitium_dns_get_dhcp_scope",
            "technitium_dns_set_dhcp_scope",
            "technitium_dns_enable_dhcp_scope",
            "technitium_dns_disable_dhcp_scope",
            "technitium_dns_delete_dhcp_scope",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-dhcp-and-apps",),
    ),
    SurfaceLink(
        task="manage-dhcp-leases",
        tools=(
            "technitium_dns_list_dhcp_leases",
            "technitium_dns_add_dhcp_reserved_lease",
            "technitium_dns_remove_dhcp_reserved_lease",
            "technitium_dns_remove_dhcp_lease",
            "technitium_dns_convert_dhcp_lease_to_reserved",
            "technitium_dns_convert_dhcp_lease_to_dynamic",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-dhcp-and-apps",),
    ),
    SurfaceLink(
        task="manage-dns-apps",
        tools=(
            "technitium_dns_list_apps",
            "technitium_dns_list_store_apps",
            "technitium_dns_download_and_install_app",
            "technitium_dns_download_and_update_app",
            "technitium_dns_get_app_config",
            "technitium_dns_set_app_config",
            "technitium_dns_uninstall_app",
        ),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-network-operator"),
        skills=("technitium-dns-dhcp-and-apps",),
    ),
    SurfaceLink(
        task="administer-users-and-groups",
        tools=(
            "technitium_dns_list_users",
            "technitium_dns_get_user",
            "technitium_dns_create_user",
            "technitium_dns_set_user",
            "technitium_dns_delete_user",
            "technitium_dns_list_groups",
            "technitium_dns_get_group",
            "technitium_dns_create_group",
            "technitium_dns_set_group",
            "technitium_dns_delete_group",
        ),
        prompts=(
            "technitium-dns-mcp-operator",
            "technitium-dns-mcp-platform-administrator",
        ),
        skills=("technitium-dns-administration",),
    ),
    SurfaceLink(
        task="administer-permissions",
        tools=(
            "technitium_dns_list_permissions",
            "technitium_dns_get_permissions",
            "technitium_dns_set_permissions",
        ),
        prompts=(
            "technitium-dns-mcp-operator",
            "technitium-dns-mcp-platform-administrator",
        ),
        skills=("technitium-dns-administration",),
    ),
    SurfaceLink(
        task="administer-sessions",
        tools=(
            "technitium_dns_list_admin_sessions",
            "technitium_dns_delete_admin_session",
            "technitium_dns_create_api_token",
        ),
        prompts=(
            "technitium-dns-mcp-operator",
            "technitium-dns-mcp-platform-administrator",
        ),
        skills=("technitium-dns-administration",),
    ),
    SurfaceLink(
        task="manage-own-session",
        tools=(
            "technitium_dns_get_sso_status",
            "technitium_dns_login",
            "technitium_dns_logout",
            "technitium_dns_get_session_info",
            "technitium_dns_create_token",
            "technitium_dns_create_single_use_token",
            "technitium_dns_delete_user_session",
            "technitium_dns_change_password",
            "technitium_dns_initialize_2fa",
            "technitium_dns_enable_2fa",
            "technitium_dns_disable_2fa",
            "technitium_dns_get_user_profile_details",
            "technitium_dns_set_user_profile_details",
        ),
        prompts=(
            "technitium-dns-mcp-operator",
            "technitium-dns-mcp-platform-administrator",
        ),
        skills=("technitium-dns-administration",),
    ),
    SurfaceLink(
        task="back-up-and-restore",
        tools=("technitium_dns_backup_settings", "technitium_dns_restore_settings"),
        prompts=(
            "technitium-dns-mcp-operator",
            "technitium-dns-mcp-platform-administrator",
        ),
        skills=("technitium-dns-administration",),
    ),
    SurfaceLink(
        task="map-dns-to-graph",
        tools=("technitium_dns_list_zones", "technitium_ingest_zones"),
        prompts=("technitium-dns-mcp-operator", "technitium-dns-mcp-dns-administrator"),
        skills=("technitium-dns-mcp-operations",),
    ),
)

LOCATIONS = (
    DataLocation(
        name="dns-zones",
        holds=("DnsZone", "DnsRecord"),
        instance="TECHNITIUM_DNS_URL",
        read_tool="technitium_dns_list_zones",
        federation_key="name",
    ),
    DataLocation(
        name="dns-server",
        holds=("DnsServerNode",),
        instance="TECHNITIUM_DNS_URL",
        read_tool="technitium_dns_get_dns_settings",
    ),
    DataLocation(
        name="dns-dnssec",
        holds=("DnssecKey",),
        instance="TECHNITIUM_DNS_URL",
        read_tool="technitium_dns_get_dnssec_properties",
    ),
    DataLocation(
        name="dns-filtering",
        holds=("DnsFilterEntry",),
        instance="TECHNITIUM_DNS_URL",
        read_tool="technitium_dns_list_blocked",
        federation_key="domain",
    ),
    DataLocation(
        name="dns-dhcp",
        holds=("DhcpScope", "DhcpLease"),
        instance="TECHNITIUM_DNS_URL",
        read_tool="technitium_dns_list_dhcp_scopes",
        federation_key="name",
    ),
    DataLocation(
        name="dns-apps",
        holds=("DnsApp",),
        instance="TECHNITIUM_DNS_URL",
        read_tool="technitium_dns_list_apps",
        federation_key="name",
    ),
    DataLocation(
        name="dns-accounts",
        holds=("DnsAdminAccount",),
        instance="TECHNITIUM_DNS_URL",
        read_tool="technitium_dns_list_users",
        federation_key="username",
    ),
)

ROLES = (
    BusinessRole(
        name="dns administrator",
        description="Publish, change and retire zones and records, and keep DNSSEC healthy.",
        tasks=(
            "publish-dns-record",
            "change-dns-record",
            "remove-dns-record",
            "create-zone",
            "manage-zone-lifecycle",
            "transfer-zone-file",
            "set-zone-permissions",
            "sign-zone-dnssec",
            "rotate-dnssec-keys",
            "map-dns-to-graph",
        ),
    ),
    BusinessRole(
        name="network operator",
        description="Run filtering, cache, logging, DHCP and apps so the network resolves and leases correctly.",
        tasks=(
            "review-dns-health",
            "read-server-settings",
            "change-server-settings",
            "manage-block-list",
            "manage-allow-list",
            "manage-dns-cache",
            "review-query-logs",
            "prune-logs",
            "manage-dhcp-scopes",
            "manage-dhcp-leases",
            "manage-dns-apps",
        ),
    ),
    BusinessRole(
        name="platform administrator",
        description="Control who can administer DNS, and keep backups of the server.",
        tasks=(
            "administer-users-and-groups",
            "administer-permissions",
            "administer-sessions",
            "manage-own-session",
            "back-up-and-restore",
        ),
    ),
)
