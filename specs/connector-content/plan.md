# CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `technitium-dns-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `technitium_dns_mcp` from it.
