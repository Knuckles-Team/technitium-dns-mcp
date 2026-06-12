# Technitium DNS MCP Server & Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](pyproject.toml)

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, and guidance for provisioning the Technitium DNS Server are maintained
> in the [official documentation](https://knuckles-team.github.io/technitium-dns-mcp/).

A production-grade Model Context Protocol (MCP) server and graph-based Pydantic AI agent integration for **Technitium DNS Server**. Exposes comprehensive, 100% covered REST API endpoints for user SSO, analytics metrics, authoritative zones, DNSSEC, and dynamic DNS record operations.

---

## 🚀 Key Features

- **100% API Coverage**: Complete mapping of Technitium User/SSO, Dashboard Analytics, Zone Management, DNSSEC, and Record Actions.
- **FastMCP Protocol Integration**: Dynamically registers stdio and streamable-http endpoints for large-scale AI tool discovery.
- **Autonomous Agent Layer**: Bundled with a Pydantic AI Agent that operates natively using advanced instruction graphs and local toolchains.
- **Strict Compliance**: Designed in accordance with standard codebase-wide architectural patterns (`agent-packages`).

---

## 🛠️ Installation & Setup

Install package in editable mode with all optional dependencies:

```bash
pip install -e .[all]
```

### Environment Variables

Configure `.env` using `.env.example` as a template:

```bash
# Server Endpoint & TLS
TECHNITIUM_DNS_URL=http://localhost:5380
TECHNITIUM_DNS_SSL_VERIFY=True

# Credentials / API Tokens
TECHNITIUM_DNS_TOKEN=your-secure-token
```

---

## ⚙️ Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.


---

## 🖥️ Running the Servers

### Run MCP Server (stdio by default)

```bash
technitium-dns-mcp
```

Or start a streamable HTTP server:

```bash
TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 technitium-dns-mcp
```

### Run Pydantic AI Agent

```bash
technitium-dns-agent --mcp-url http://localhost:8000
```

---

## 🧪 Running Tests

Ensure high reliability across all components with standard test suites:

```bash
pytest -v tests/
```

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/technitium-dns-mcp/) and
is the recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/technitium-dns-mcp/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/technitium-dns-mcp/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/technitium-dns-mcp/usage/) | the MCP tools, the `Api` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/technitium-dns-mcp/platform/) | deploy Technitium DNS Server with Docker |
| [Overview](https://knuckles-team.github.io/technitium-dns-mcp/overview/) | the layered API / MCP / agent architecture |
| [Concepts](https://knuckles-team.github.io/technitium-dns-mcp/concepts/) | concept registry (`CONCEPT:TDNS-*`) |

---

Version: 0.30.0

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`technitium-dns-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/technitium-dns-mcp/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://technitium-dns-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->
