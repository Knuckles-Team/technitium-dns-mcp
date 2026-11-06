---
name: technitium-dns-mcp-operations
skill_type: skill
description: >-
  Administer Technitium DNS zones, records and DNSSEC through technitium-dns-mcp: create and manage zones, add, change and delete records, sign zones and rotate keys, import and export zone files, read statistics, and map DNS into the knowledge graph. Use for any change to what the server answers authoritatively.
---

# Technitium DNS operations

Scope every call to a zone (and a `node` on a cluster). Read first, write, read back.

## Records

1. `technitium_dns_list_zones` confirms the zone exists. `technitium_dns_get_records` (`domain`, `zone`, `list_zone=true` for the whole zone) reads current records.
2. `technitium_dns_add_record` takes `zone`, `domain`, `type`, `ttl` and the typed fields for the type: `ip_address` (A, AAAA), `cname`, `name_server`, `ptr_name`, `exchange` with `preference`, `text`, `priority` `weight` `port` `target`, `flags` `tag` `value`.
3. `technitium_dns_update_record` takes the current value and its `new_` value. `technitium_dns_delete_record` takes the record data that picks one record and `confirm=true`.
4. `technitium_dns_get_records` again to prove the change.

## Zones

- `technitium_dns_create_zone`, then `technitium_dns_get_zone_options` and `technitium_dns_set_zone_options` for zone transfer, notify and update policy.
- `technitium_dns_enable_zone`, `technitium_dns_disable_zone`, `technitium_dns_resync_zone`, `technitium_dns_clone_zone`, `technitium_dns_convert_zone_type`. `technitium_dns_delete_zone` needs `confirm=true`. `technitium_dns_list_catalog_zones` lists catalog zones.
- `technitium_dns_get_zone_permissions` and `technitium_dns_set_zone_permissions` control who can edit a zone.
- `technitium_dns_export_zone` and `technitium_dns_import_zone` move a zone as a zone file.

## DNSSEC

- Sign: `technitium_dns_sign_zone`, then `technitium_dns_get_ds_info` for the DS record to give the parent zone. `technitium_dns_get_dnssec_properties` shows status and keys.
- Denial of existence: `technitium_dns_convert_to_nsec`, `technitium_dns_convert_to_nsec3`, `technitium_dns_update_nsec3_params`. `technitium_dns_update_dnskey_ttl` sets the DNSKEY TTL.
- Keys: `technitium_dns_add_private_key`, `technitium_dns_update_private_key`, `technitium_dns_publish_all_private_keys`, `technitium_dns_rollover_dnskey`, `technitium_dns_retire_dnskey`. `technitium_dns_delete_private_key` needs `confirm=true`. `technitium_dns_unsign_zone` removes signing.

## Health and graph

- `technitium_dns_get_stats`, `technitium_dns_get_top_stats`, `technitium_dns_get_metrics_json`, `technitium_dns_get_metrics_text`, `technitium_dns_check_for_update`. `technitium_dns_delete_all_stats` clears statistics and needs `confirm=true`.
- `technitium_ingest_zones` writes zones and records to the knowledge graph.

## Rules

- Never print a token, password or key material.
- A delete, a flush or an unsign needs the requester's explicit yes.
