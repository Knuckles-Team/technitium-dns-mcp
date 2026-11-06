---
name: technitium-dns-administration
skill_type: skill
description: >-
  Administer Technitium DNS accounts, permissions, sessions and backups through technitium-dns-mcp: users, groups, section permissions, API tokens, active sessions, the calling user's own session, two-factor and profile, and backup and restore. Use to give or remove access, hand a service an API token, end a session, or take and restore a server backup.
---

# Technitium DNS administration

## Users and groups

- `technitium_dns_list_users`, `technitium_dns_get_user`, `technitium_dns_list_groups`, `technitium_dns_get_group` read accounts.
- `technitium_dns_create_user`, `technitium_dns_set_user` (rename, disable, set password, set groups, session timeout), `technitium_dns_create_group`, `technitium_dns_set_group`.
- `technitium_dns_delete_user` and `technitium_dns_delete_group` need `confirm=true`.

## Permissions

`technitium_dns_list_permissions` and `technitium_dns_get_permissions` (`section` such as Zones, Cache, Settings, Administration) read access. `technitium_dns_set_permissions` sets `user_permissions` and `group_permissions` as `name|canView|canModify|canDelete` entries. Name only the entries you mean to change. Zone-level access is set with `technitium_dns_set_zone_permissions`.

## Sessions and tokens

- `technitium_dns_list_admin_sessions` shows every session with its partial token.
- `technitium_dns_delete_admin_session` ends one and needs `confirm=true`.
- `technitium_dns_create_api_token` makes a non-expiring token for a user. The token appears once in the reply. Hand it over and do not store it.

## The calling user

`technitium_dns_get_sso_status`, `technitium_dns_login`, `technitium_dns_logout`, `technitium_dns_get_session_info`, `technitium_dns_create_token`, `technitium_dns_create_single_use_token`, `technitium_dns_delete_user_session`, `technitium_dns_change_password`, `technitium_dns_initialize_2fa`, `technitium_dns_enable_2fa`, `technitium_dns_disable_2fa`, `technitium_dns_get_user_profile_details`, `technitium_dns_set_user_profile_details`. Credential values are removed from these replies.

## Backup and restore

1. `technitium_dns_backup_settings` returns the backup zip as `content_base64` with its `size`. Choose sections (zones, DNS settings, scopes, apps, lists, auth config, logs, stats).
2. `technitium_dns_restore_settings` (`backup_base64`) overwrites live configuration for the sections chosen and needs `confirm=true`. Say which sections it replaces before asking.
