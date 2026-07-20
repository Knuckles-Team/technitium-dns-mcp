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

> **Install the connector-focused `[mcp]` extra.** Examples use `technitium-dns-mcp[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent]` extra additionally
> enables model orchestration.

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `technitium-dns-mcp[mcp]` | Connector-focused MCP server (`agent-utilities[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | You only run the **MCP server** (smallest install / image) |
| `technitium-dns-mcp[agent]` | Agent runtime (`agent-utilities[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | You run the **integrated agent** |
| `technitium-dns-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "technitium-dns-mcp[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "technitium-dns-mcp[agent]"

# Everything (development)
uv pip install "technitium-dns-mcp[all]"      # or: python -m pip install "technitium-dns-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/technitium-dns-mcp:mcp` | `--target mcp` | `technitium-dns-mcp[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `technitium-dns-mcp` |
| `example/technitium-dns-mcp@sha256:<digest>` | `--target agent` (default) | `technitium-dns-mcp[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `technitium-dns-agent` |

```bash
docker build --target mcp   -t example/technitium-dns-mcp:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/technitium-dns-mcp:agent-local docker/   # agent runtime
```

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` additionally enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

### Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `TECHNITIUM_DNS_URL` | Required | Technitium DNS Server URL |
| `TECHNITIUM_DNS_TOKEN` | — | Technitium DNS API Token / SSO Token |
| `TLS_PROFILE` | — | Named `AgentConfig` transport-security profile; verification is mandatory. |
| `TLS_PROFILES_REF` | — | Runtime secret reference for the TLS profile catalog. |
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
| `TECHNITIUM_DNS_URL` | Base URL of the Technitium DNS Server | Required |
| `TECHNITIUM_DNS_TOKEN` | API token / SSO token | — |
| `TLS_PROFILE` | Named `AgentConfig` transport-security profile; verification is mandatory | — |
| `TLS_PROFILES_REF` | Runtime secret reference for the TLS profile catalog | — |

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

Version: 1.0.1

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`technitium-dns-mcp` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/technitium-dns-mcp/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
<!-- END GENERATED: additional-deployment-options -->


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `technitium-dns-mcp` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "technitium-dns-mcp[mcp]"`, then run `technitium-dns-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `technitium-dns-mcp` |
| Immutable container | deploy `registry.example.invalid/technitium-dns-mcp@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

## Available MCP Tools

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `technitium_dns_dashboard` | `DASHBOARDTOOL` | Query Technitium DNS metrics, prometheus stats, category details, or delete statistics. |
| `technitium_dns_user` | `USERTOOL` | Manage Technitium DNS user sessions, authentication, credentials, and profile settings. |
| `technitium_dns_zones` | `ZONESTOOL` | Manage Technitium DNS authoritative zones, DNSSEC properties/keys, and perform DNS record CRUD. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>52 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `technitium_dns_add_private_key` | `ZONESTOOL` | Adds a private DNSSEC key to the zone. |
| `technitium_dns_add_record` | `ZONESTOOL` | Adds a new DNS record. |
| `technitium_dns_change_password` | `USERTOOL` | Changes password for the current user session. |
| `technitium_dns_check_for_update` | `USERTOOL` | Checks for software updates. |
| `technitium_dns_clone_zone` | `ZONESTOOL` | Clones a zone from an existing local zone. |
| `technitium_dns_convert_to_nsec` | `ZONESTOOL` | Converts proof of non-existence to NSEC. |
| `technitium_dns_convert_to_nsec3` | `ZONESTOOL` | Converts proof of non-existence to NSEC3. |
| `technitium_dns_convert_zone_type` | `ZONESTOOL` | Converts zone type. |
| `technitium_dns_create_single_use_token` | `USERTOOL` | Creates a single-use token. |
| `technitium_dns_create_token` | `USERTOOL` | Creates an API token for long-term programmatic access. |
| `technitium_dns_create_zone` | `ZONESTOOL` | Creates a new zone. |
| `technitium_dns_delete_all_stats` | `DASHBOARDTOOL` | Deletes all statistics from the server. |
| `technitium_dns_delete_private_key` | `ZONESTOOL` | Deletes a private DNSSEC key. |
| `technitium_dns_delete_record` | `ZONESTOOL` | Deletes matching DNS record(s). |
| `technitium_dns_delete_user_session` | `USERTOOL` | Deletes a specific user session token. |
| `technitium_dns_delete_zone` | `ZONESTOOL` | Deletes authoritative zone. |
| `technitium_dns_disable_2fa` | `USERTOOL` | Disables 2FA for the current user. |
| `technitium_dns_disable_zone` | `ZONESTOOL` | Disables authoritative zone. |
| `technitium_dns_enable_2fa` | `USERTOOL` | Enables 2FA with the provided TOTP code. |
| `technitium_dns_enable_zone` | `ZONESTOOL` | Enables authoritative zone. |
| `technitium_dns_export_zone` | `ZONESTOOL` | Exports authoritative zone file. |
| `technitium_dns_get_dnssec_properties` | `ZONESTOOL` | Retrieves DNSSEC properties/keys for a zone. |
| `technitium_dns_get_ds_info` | `ZONESTOOL` | Retrieves DNSSEC Delegation Signer (DS) records information. |
| `technitium_dns_get_metrics_json` | `DASHBOARDTOOL` | Gets metrics in JSON format for the dashboard. |
| `technitium_dns_get_metrics_text` | `DASHBOARDTOOL` | Gets metrics in Prometheus metrics format. |
| `technitium_dns_get_records` | `ZONESTOOL` | Retrieves DNS records matching the domain. |
| `technitium_dns_get_session_info` | `USERTOOL` | Gets info about the current session. |
| `technitium_dns_get_sso_status` | `USERTOOL` | Gets SSO status of the server. |
| `technitium_dns_get_stats` | `DASHBOARDTOOL` | Retrieves server statistical charts data. |
| `technitium_dns_get_top_stats` | `DASHBOARDTOOL` | Retrieves top stats data for queries, clients, domains, etc. |
| `technitium_dns_get_user_profile_details` | `USERTOOL` | Retrieves user profile details. |
| `technitium_dns_get_zone_options` | `ZONESTOOL` | Gets settings/options of a zone. |
| `technitium_dns_get_zone_permissions` | `ZONESTOOL` | Gets user/group permissions of a zone. |
| `technitium_dns_import_zone` | `ZONESTOOL` | Imports zone content from a zone file. |
| `technitium_dns_initialize_2fa` | `USERTOOL` | Initializes Time-based One-Time Password setup. |
| `technitium_dns_list_catalog_zones` | `ZONESTOOL` | Lists all catalog zones. |
| `technitium_dns_list_zones` | `ZONESTOOL` | Lists authoritative zones. |
| `technitium_dns_login` | `USERTOOL` | Log in to the DNS server to obtain a session token. |
| `technitium_dns_logout` | `USERTOOL` | Logs out the current session. |
| `technitium_dns_publish_all_private_keys` | `ZONESTOOL` | Publishes all private DNSSEC keys. |
| `technitium_dns_resync_zone` | `ZONESTOOL` | Forces authoritative secondary zone resynchronization. |
| `technitium_dns_retire_dnskey` | `ZONESTOOL` | Retires the DNSKEY. |
| `technitium_dns_rollover_dnskey` | `ZONESTOOL` | Rolls over the DNSKEY. |
| `technitium_dns_set_user_profile_details` | `USERTOOL` | Updates user profile settings. |
| `technitium_dns_set_zone_options` | `ZONESTOOL` | Sets settings/options for a zone. |
| `technitium_dns_set_zone_permissions` | `ZONESTOOL` | Sets permissions for a zone. |
| `technitium_dns_sign_zone` | `ZONESTOOL` | Signs the zone with DNSSEC. |
| `technitium_dns_unsign_zone` | `ZONESTOOL` | Unsigns/removes DNSSEC from a zone. |
| `technitium_dns_update_dnskey_ttl` | `ZONESTOOL` | Updates DNSKEY TTL. |
| `technitium_dns_update_nsec3_params` | `ZONESTOOL` | Updates NSEC3 parameters. |
| `technitium_dns_update_private_key` | `ZONESTOOL` | Updates private key parameters. |
| `technitium_dns_update_record` | `ZONESTOOL` | Updates an existing DNS record. |

</details>

_3 action-routed tool(s) (default) · 52 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
