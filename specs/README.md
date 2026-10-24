# technitium-dns-mcp specifications

These specs follow the ecosystem [spec standard](https://github.com/Knuckles-Team/pipelines/blob/main/reference/spec-standard.md): one owning spec per capability, extend an existing spec before creating one, audits and reviews land in the owning spec, one ID and title form, one file set. The `spec-standard` gate enforces it.

## Owner

This repository owns the specs with the ID prefix `CONN-TECHNITIUM-DNS-MCP`. The connector contract, certification, and transport rules belong to [agent-connector-sdk](https://github.com/Knuckles-Team/agent-connector-sdk/tree/main/specs). The spec-delivery page rules belong to [pipelines](https://github.com/Knuckles-Team/pipelines/tree/main/specs).

## Add a spec

Read the existing specs first. Extend the spec that owns the behavior. Create a spec only for a capability that no spec owns. Copy [`_template/`](_template/) to `specs/<area>/`, set the ID to `CONN-TECHNITIUM-DNS-MCP` or `CONN-TECHNITIUM-DNS-MCP-<AREA>`, and add one index line below.

## Local specifications

- [`CONN-TECHNITIUM-DNS-MCP`](technitium-dns-mcp/spec.md) — Technitium DNS ingestible source declarations.
- [`CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT`](connector-content/spec.md) — The connector serves its packaged content.
