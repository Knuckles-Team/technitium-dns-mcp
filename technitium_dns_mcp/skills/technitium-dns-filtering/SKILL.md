---
name: technitium-dns-filtering
skill_type: skill
description: >-
  Run Technitium DNS filtering, cache, logs and server settings through technitium-dns-mcp: block and allow lists, block list refresh and temporary pause, cache browsing and flush, query log search, log files, and recursion, forwarder, cache and logging settings. Use to block or allow a domain, clear a stale answer, find who queried what, or change how the server resolves.
---

# Technitium DNS filtering, cache, logs and settings

## Block and allow lists

- `technitium_dns_list_blocked` and `technitium_dns_list_allowed` read the lists (`domain` browses a subtree).
- `technitium_dns_add_blocked` and `technitium_dns_add_allowed` add a domain. `technitium_dns_delete_blocked` and `technitium_dns_delete_allowed` remove one and need `confirm=true`.
- `technitium_dns_export_blocked` and `technitium_dns_export_allowed` return the list as text. `technitium_dns_import_blocked` and `technitium_dns_import_allowed` add many.
- `technitium_dns_flush_blocked` and `technitium_dns_flush_allowed` empty a list and need `confirm=true`.
- `technitium_dns_force_update_block_lists` downloads every block list source now.
- `technitium_dns_temporary_disable_blocking` (`minutes`) pauses blocking and turns it back on by itself. State the end time to the requester.

## Cache

`technitium_dns_list_cache` browses cached names. `technitium_dns_delete_cached_zone` drops one domain. `technitium_dns_flush_cache` empties the cache. Both need `confirm=true`. Prefer dropping one domain.

## Logs

- `technitium_dns_query_logs` searches the query log kept by a query-logging app (`name` and `class_path` of the app from `technitium_dns_list_apps`), with filters for client, qname, qtype, response type and time range.
- `technitium_dns_list_logs` and `technitium_dns_download_log` read server log files. `technitium_dns_delete_log` and `technitium_dns_delete_all_logs` remove them and need `confirm=true`.

## Settings

1. `technitium_dns_get_dns_settings` (TSIG shared secrets and the proxy password are not returned). `technitium_dns_get_tsig_key_names` lists TSIG key names.
2. `technitium_dns_set_dns_settings` changes only the fields given: recursion and its network ACL, forwarders and protocol, cache limits and TTLs, logging and statistics retention, blocking type and block list URLs. Read the settings back after the change.
3. A bad recursion or forwarder value stops name resolution for every client. Change one group of settings at a time.
