# technitium-dns-mcp

Technitium DNS Server **API + MCP Server and Agent** for the agent-utilities
ecosystem — authoritative-zone, record, analytics, and account management exposed as
typed, deterministic tools an agent can call.

!!! info "Official documentation"
    This site is the canonical reference for `technitium-dns-mcp`, maintained
    alongside every release.

[![PyPI](https://img.shields.io/pypi/v/technitium-dns-mcp)](https://pypi.org/project/technitium-dns-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/technitium-dns-mcp)](https://github.com/Knuckles-Team/technitium-dns-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/technitium-dns-mcp)

## Overview

`technitium-dns-mcp` wraps the [Technitium DNS Server](https://technitium.com/dns/)
HTTP API with typed, deterministic MCP tools and a Pydantic AI agent. It provides:

- **`Api`** — a granular `requests`-based REST facade covering the User/SSO,
  Dashboard analytics, and authoritative-zone surfaces of the Technitium API.
- **A FastMCP tool surface** grouped under the `user`, `dashboard`, and `zones` tags,
  registering account, metrics, zone, DNSSEC, and record operations.
- **A Pydantic AI agent** (`technitium-dns-agent`) that drives the MCP tools for
  autonomous DNS administration.

The server remains inactive when credentials are absent and connects to any
Technitium instance over its web service port.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `Api` client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy Technitium DNS Server with Docker.
- :material-sitemap: **[Architecture](overview.md)** — the layered API / MCP / agent design.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:TDNS-*` registry.

</div>

## Quick start

```bash
pip install "technitium-dns-mcp[mcp]"
technitium-dns-mcp                       # stdio MCP server (default transport)
```

Connect it to a Technitium DNS Server:

```bash
export TECHNITIUM_DNS_URL=http://your-technitium:5380
export TECHNITIUM_DNS_TOKEN=your-api-token
technitium-dns-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, reverse proxy, DNS).
