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

> **Install the slim `[mcp]` extra.** The `technitium-dns-mcp[mcp]` extra pulls only the
> FastMCP / FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster. Use the
> full `[agent]` extra only when you need the integrated Pydantic AI agent.

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `technitium-dns-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `technitium-dns-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `technitium-dns-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "technitium-dns-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "technitium-dns-mcp[agent]"

# Everything (development)
uv pip install "technitium-dns-mcp[all]"      # or: python -m pip install "technitium-dns-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/technitium-dns-mcp:mcp` | `--target mcp` | `technitium-dns-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `technitium-dns-mcp` |
| `knucklessg1/technitium-dns-mcp:latest` | `--target agent` (default) | `technitium-dns-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `technitium-dns-agent` |

```bash
docker build --target mcp   -t knucklessg1/technitium-dns-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/technitium-dns-mcp:latest docker/   # full agent
```

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

### Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `TECHNITIUM_DNS_URL` | `http://localhost:5380` | Technitium DNS Server URL (default is http://localhost:5380) |
| `TECHNITIUM_DNS_TOKEN` | — | Technitium DNS API Token / SSO Token |
| `TECHNITIUM_DNS_SSL_VERIFY` | `True` | SSL Verification (default: True) |
| `TRANSPORT` | `stdio` | MCP transport configuration (streamable-http or stdio) |
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `DASHBOARDTOOL` | `True` | MCP tools table (condensed action-routed surface). |
| `USERTOOL` | `True` |  |
| `ZONESTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `EUNOMIA_TYPE` | `none` | Authorization mode: `none` | `embedded` | `remote` |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` | Embedded Eunomia policy file |
| `EUNOMIA_REMOTE_URL` | — | Remote Eunomia authorization server URL |
| `ENABLE_OTEL` | `False` | Enable OpenTelemetry export |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | OTLP collector endpoint |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_9 package + 19 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


Every variable the server reads, grouped by purpose. See [`.env.example`](.env.example)
for a copy-paste starting point.

#### Connection & credentials
| Variable | Description | Default |
|----------|-------------|---------|
| `TECHNITIUM_DNS_URL` | Base URL of the Technitium DNS Server | `http://localhost:5380` |
| `TECHNITIUM_DNS_TOKEN` | API token / SSO token | — |
| `TECHNITIUM_DNS_SSL_VERIFY` | TLS verification | `True` |

#### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |

#### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`):
`DASHBOARDTOOL`, `USERTOOL`, `ZONESTOOL` — see the
[Available MCP Tools](#available-mcp-tools) table below.

#### Agent runtime (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |

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

Version: 0.34.0

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `technitium-dns-mcp` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx technitium-dns-mcp` · or `uv tool install technitium-dns-mcp` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/technitium-dns-mcp:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->

## Available MCP Tools

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `technitium_dns_dashboard` | `DASHBOARDTOOL` | Query Technitium DNS metrics, prometheus stats, category details, or delete statistics. |
| `technitium_dns_user` | `USERTOOL` | Manage Technitium DNS user sessions, authentication, credentials, and profile settings. |
| `technitium_dns_zones` | `ZONESTOOL` | Manage Technitium DNS authoritative zones, DNSSEC properties/keys, and perform DNS record CRUD. |

_3 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->
