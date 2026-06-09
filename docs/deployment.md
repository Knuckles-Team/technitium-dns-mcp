# Deployment

This page covers running `technitium-dns-mcp` as a long-lived server: the transports,
a Docker Compose stack, putting it behind a Caddy reverse proxy, and giving it a DNS
name with Technitium. To provision the **Technitium DNS Server** it connects to, see
[Backing Platform](platform.md).

> `technitium-dns-mcp` ships **two** console scripts: an **MCP server**
> (`technitium-dns-mcp`) and a **Pydantic AI agent** (`technitium-dns-agent`). The MCP
> server is a typed, deterministic tool surface; the agent connects to it and drives
> the tools autonomously.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    technitium-dns-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    technitium-dns-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    technitium-dns-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`technitium-dns-mcp` is configured entirely from the environment. The **required**
set:

| Var | Default | Meaning |
|---|---|---|
| `TECHNITIUM_DNS_URL` | `http://localhost:5380` | Technitium DNS web service URL |
| `TECHNITIUM_DNS_TOKEN` | _(empty)_ | API / SSO token (Bearer) |
| `TECHNITIUM_DNS_SSL_VERIFY` | `True` | Verify TLS (set `False` for self-signed homelab) |

Plus `HOST` / `PORT` / `TRANSPORT` for HTTP transports. Copy
[`.env.example`](https://github.com/Knuckles-Team/technitium-dns-mcp/blob/main/.env.example)
to `.env` and populate the values you use; the server remains inactive when
`TECHNITIUM_DNS_TOKEN` is absent.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/technitium-dns-mcp/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  technitium-dns-mcp:
    image: knucklessg1/technitium-dns-mcp:latest
    container_name: technitium-dns-mcp
    hostname: technitium-dns-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
      - TECHNITIUM_DNS_URL
      - TECHNITIUM_DNS_TOKEN
      - TECHNITIUM_DNS_SSL_VERIFY
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
cp .env.example .env          # then edit TECHNITIUM_DNS_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Agent server

The Pydantic AI agent (`technitium-dns-agent`) connects to a running MCP server and
drives its tools. Point it at the MCP server with `--mcp-url`:

```bash
technitium-dns-agent --mcp-url http://localhost:8000 --host 0.0.0.0 --port 8080
```

A container recipe mirrors the MCP service, wiring `MCP_URL` to the MCP server by
container name and publishing the agent on `:8080`:

```yaml
# docker/agent.compose.yml
services:
  technitium-dns-agent:
    image: knucklessg1/technitium-dns-mcp:latest
    container_name: technitium-dns-agent
    hostname: technitium-dns-agent
    restart: always
    entrypoint: ["technitium-dns-agent"]
    depends_on: [technitium-dns-mcp]
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - MCP_URL=http://technitium-dns-mcp:8000
      - HOST=0.0.0.0
      - PORT=8080
    ports:
      - "8080:8080"
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
technitium-dns-mcp.arpa {
    tls internal
    reverse_proxy technitium-dns-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
technitium-dns-mcp.example.com {
    reverse_proxy technitium-dns-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy by adding an **A record** to the
authoritative zone. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=technitium-dns-mcp.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

This is the very operation `technitium-dns-mcp` automates as a tool — the
`add_record` API call and its `zones` MCP tool perform the same A-record creation
without hand-rolling `curl`.

## Register with an MCP client

Add to your client's `mcp_config.json` (multiplexer nickname `td`):

```json
{
  "mcpServers": {
    "technitium-dns-mcp": {
      "command": "uv",
      "args": ["run", "technitium-dns-mcp"],
      "env": {
        "TECHNITIUM_DNS_URL": "http://your-technitium:5380",
        "TECHNITIUM_DNS_TOKEN": "your-api-token",
        "TECHNITIUM_DNS_SSL_VERIFY": "True"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://technitium-dns-mcp.arpa/mcp`
instead.
