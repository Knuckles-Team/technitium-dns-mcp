# Changelog

All notable changes to this project will be documented in this file.

## [2.4.0] - 2026-11-06

### Added
- Typed tools for every remaining Technitium API area: server settings (read, change, TSIG key names, block list refresh, temporary blocking pause, backup, restore), cache, allowed and blocked lists, server logs and query log search, DHCP scopes and leases, DNS apps, and administration (users, groups, permissions, sessions, API tokens). 62 new tools; destructive ones take `confirm`.
- `technitium_dns_add_record`, `technitium_dns_update_record` and `technitium_dns_delete_record` take typed record fields (`ip_address`, `cname`, `exchange`, `preference`, `text`, `priority`, `weight`, `port`, `target`, `flags`, `tag`, `value` and more) instead of a JSON string.
- Complete connector surface on `scion-sdk>=0.9.0`: 26 task contracts, data locations, three business roles with an operator prompt and three role prompts, four task skills, and ontology classes that extend the core.

### Removed
- The retired action-routed tool modules (`mcp_zones`, `mcp_user`, `mcp_dashboard`).

## [2.3.9] - 2026-11-06

### Fixed
- The DNS specialist prompt names the typed `technitium_dns_*` tools instead of the retired `technitium_dns_zones` action tool.
- Require `scion-sdk>=0.6.5` so destructive tools accept `confirm=true`.

## [2.3.8] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.5] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [0.15.0] - 2026-05-25

### Added
- Complete Technitium DNS API Client with 100% coverage across User, SSO, Dashboard, Zone management, DNSSEC, and Record operations.
- FastMCP toolsets (`technitium_dns_user`, `technitium_dns_dashboard`, `technitium_dns_zones`).
- Unified dynamic package imports inside `__init__.py`.
- Mock-driven test suites validating the entirety of the Client and MCP tool handlers.
- Integrated Pydantic AI agent server executing with standard workspace identity parameters.
