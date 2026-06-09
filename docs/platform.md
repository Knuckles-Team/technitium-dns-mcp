# Backing Platform — Technitium DNS Server

`technitium-dns-mcp` is a **client** of a Technitium DNS Server. This page provides a
Docker recipe for deploying one locally to serve as the target of
`TECHNITIUM_DNS_URL`. For production topologies, follow the upstream
[Technitium DNS documentation](https://technitium.com/dns/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

Technitium publishes the `technitium/dns-server` image. The following stack runs one
DNS server with its web console / API on `:5380`:

```yaml
# docker/technitium.compose.yml
services:
  technitium:
    image: technitium/dns-server:latest
    container_name: technitium-dns
    hostname: dns-server
    restart: always
    environment:
      - DNS_SERVER_DOMAIN=technitium.arpa
      - DNS_SERVER_ADMIN_PASSWORD=${DNS_SERVER_ADMIN_PASSWORD}
      - DNS_SERVER_WEB_SERVICE_PORT=5380
      - DNS_SERVER_WEB_SERVICE_ENABLE_HTTPS=false
    ports:
      - "53:53/udp"
      - "53:53/tcp"
      - "5380:5380/tcp"
    volumes:
      - technitium_config:/etc/dns

volumes:
  technitium_config:
```

```bash
DNS_SERVER_ADMIN_PASSWORD=change-me \
  docker compose -f docker/technitium.compose.yml up -d

# The web console / API answers on :5380
curl -s http://localhost:5380/api/dashboard/stats/get
```

## Connect technitium-dns-mcp

Obtain an API token from the Technitium web console (or via the API) and point the
connector at the server:

```bash
export TECHNITIUM_DNS_URL=http://localhost:5380
export TECHNITIUM_DNS_TOKEN=your-api-token
export TECHNITIUM_DNS_SSL_VERIFY=False          # plain HTTP / self-signed homelab

technitium-dns-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places the DNS server and the MCP server on one Docker network, so
the connector reaches Technitium by container name:

```yaml
# docker/stack.compose.yml
services:
  technitium:
    image: technitium/dns-server:latest
    hostname: dns-server
    environment:
      - DNS_SERVER_DOMAIN=technitium.arpa
      - DNS_SERVER_ADMIN_PASSWORD=${DNS_SERVER_ADMIN_PASSWORD}
      - DNS_SERVER_WEB_SERVICE_PORT=5380
      - DNS_SERVER_WEB_SERVICE_ENABLE_HTTPS=false
    ports:
      - "53:53/udp"
      - "53:53/tcp"
      - "5380:5380/tcp"
    volumes:
      - technitium_config:/etc/dns

  technitium-dns-mcp:
    image: knucklessg1/technitium-dns-mcp:latest
    depends_on: [technitium]
    environment:
      - TECHNITIUM_DNS_URL=http://technitium:5380
      - TECHNITIUM_DNS_TOKEN=${TECHNITIUM_DNS_TOKEN}
      - TECHNITIUM_DNS_SSL_VERIFY=False
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports:
      - "8000:8000"

volumes:
  technitium_config:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

With the server running, the [Python API](usage.md#as-a-python-api) and the
[MCP tools](usage.md#as-an-mcp-server) manage zones, records, DNSSEC, and analytics.
