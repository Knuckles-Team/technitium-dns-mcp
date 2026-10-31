# Changelog

All notable changes to this project will be documented in this file.

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
