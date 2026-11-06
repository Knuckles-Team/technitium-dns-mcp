---
name: technitium-dns-dhcp-and-apps
skill_type: skill
description: >-
  Manage Technitium DHCP scopes and leases and DNS apps through technitium-dns-mcp: create and change scopes, reserve addresses, release leases, and install, configure and remove apps from the app store. Use to hand out addresses, pin a device to an address, or add a DNS app such as a query logger.
---

# Technitium DHCP and apps

## Scopes

1. `technitium_dns_list_dhcp_scopes` and `technitium_dns_get_dhcp_scope` read scopes with their options and reservations.
2. `technitium_dns_set_dhcp_scope` creates a scope or changes one: address range, subnet mask, lease time, router, DNS and NTP servers, domain name, DNS updates, reserved leases.
3. `technitium_dns_enable_dhcp_scope` and `technitium_dns_disable_dhcp_scope` switch it on or off. `technitium_dns_delete_dhcp_scope` needs `confirm=true`.
4. Two active scopes with overlapping ranges on one network hand out the same address twice. Check the existing ranges first.

## Leases

- `technitium_dns_list_dhcp_leases` lists all leases.
- `technitium_dns_add_dhcp_reserved_lease` pins a MAC address to an IP address. `technitium_dns_remove_dhcp_reserved_lease` removes the pin and needs `confirm=true`.
- `technitium_dns_convert_dhcp_lease_to_reserved` and `technitium_dns_convert_dhcp_lease_to_dynamic` change a lease's kind. `technitium_dns_remove_dhcp_lease` releases a dynamic lease and needs `confirm=true`.

## Apps

- `technitium_dns_list_apps` shows installed apps. `technitium_dns_list_store_apps` shows what the store offers.
- `technitium_dns_download_and_install_app` and `technitium_dns_download_and_update_app` take the app `name` and zip `url`.
- `technitium_dns_get_app_config` reads the app's configuration. `technitium_dns_set_app_config` replaces it entirely, so read it first and send the full text.
- `technitium_dns_uninstall_app` removes the app and its configuration and needs `confirm=true`.
