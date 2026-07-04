# Technitium DNS Concept Registry

## Concepts

### TD-OS.config.tdns: Core API Client Operations
- **Description**: Robust granular REST API client with full coverage of the Technitium HTTP API. Handles login, dashboard, zone control, and record CRUD.
- **Traceability**: `technitium_dns_mcp/api/`

### TD-OS.config.tdns-2: FastMCP Tools Execution
- **Description**: FastMCP wrapper exposing operations through stdio and http channels.
- **Traceability**: `technitium_dns_mcp/mcp/`

### TD-OS.identity.tdns: Identity & Gateway Security
- **Description**: Secure credential loading, Bearer token auth support, and SSL verification settings.
- **Traceability**: `technitium_dns_mcp/auth.py`
