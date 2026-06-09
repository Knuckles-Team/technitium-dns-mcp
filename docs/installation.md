# Installation

`technitium-dns-mcp` is a standard Python package and a prebuilt container image.
Pick the path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Technitium DNS Server** web service — see
  [Backing Platform](platform.md) to deploy one locally.

## From PyPI (recommended)

```bash
pip install technitium-dns-mcp
```

### Optional extras

The base install is intentionally minimal. Install the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "technitium-dns-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "technitium-dns-mcp[agent]"` | Pydantic-AI agent + Logfire tracing |
| `all` | `pip install "technitium-dns-mcp[all]"` | Everything above |
| `test` | `pip install "technitium-dns-mcp[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run the MCP server and the agent
pip install "technitium-dns-mcp[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/technitium-dns-mcp.git
cd technitium-dns-mcp
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run technitium-dns-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint
`technitium-dns-mcp`):

```bash
docker pull knucklessg1/technitium-dns-mcp:latest

docker run --rm -i \
  -e TECHNITIUM_DNS_URL=http://your-technitium:5380 \
  -e TECHNITIUM_DNS_TOKEN=your-api-token \
  knucklessg1/technitium-dns-mcp:latest        # stdio transport (default)
```

For an HTTP server with a published port, see [Deployment](deployment.md).

## Verify the install

```bash
technitium-dns-mcp --help
python -c "import technitium_dns_mcp; print(technitium_dns_mcp.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the agent.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
