# Usage — API / CLI / MCP

`technitium-dns-mcp` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** (`Api`) you import, and as **command-line servers**. The
layered design is described in [Architecture](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers its tools under three tags. Reads
work with no configuration beyond the connection details and a valid token.

| Tag | Surface |
|---|---|
| `user` | SSO status, login, token creation, sessions, profile, two-factor, update checks |
| `dashboard` | Analytics metrics (JSON / text / Prometheus), aggregate statistics |
| `zones` | List/create/import/export/clone zones, DNSSEC signing, record CRUD |

Example agent prompts that map onto these tools:

- *"List the authoritative zones on the primary server"* → `zones`
- *"Add an A record `app.arpa → 10.0.0.10`"* → `zones`
- *"Show me the dashboard statistics for the last day"* → `dashboard`

## As a Python API

`Api` is a granular `requests`-based facade composed from the User, Dashboard, and
Zones modules. Build one straight from the environment with `get_client`, or
construct it directly.

```python
from technitium_dns_mcp.auth import get_client

api = get_client()        # reads TECHNITIUM_DNS_* from the environment / .env

# Reads
zones = api.list_zones()                       # authoritative zones
stats = api.get_stats()                         # dashboard statistics
metrics = api.get_metrics_json()                # analytics metrics
records = api.get_records(zone="arpa")          # records in a zone
```

Construct the client directly:

```python
from technitium_dns_mcp.api_client import Api

api = Api(
    base_url="http://your-technitium:5380",
    token="your-api-token",
    verify=True,
)
zones = api.list_zones()
```

### Writes

The same client manages zones and records:

```python
api.create_zone(zone="example.arpa", type="Primary")
api.add_record(zone="example.arpa", domain="app.example.arpa", type="A", ipAddress="10.0.0.10")
api.update_record(...)
api.delete_record(...)
```

## As a CLI

The package installs two console scripts.

Run the **MCP server** (stdio by default, or an HTTP transport):

```bash
technitium-dns-mcp
TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 technitium-dns-mcp
```

Run the **Pydantic AI agent** against a running MCP server:

```bash
technitium-dns-agent --mcp-url http://localhost:8000
```

See [Deployment](deployment.md) for transports, environment configuration, and the
container recipes.
