# CONN-TECHNITIUM-DNS-MCP — Technitium DNS ingestible sources

Owner: technitium-dns-mcp. Cross-repo IDs: SDK-SOURCE-INGEST-R004.19, SDK-SOURCE-INGEST-R004.21, ARBORA-OPS-R020.6.

## Purpose and user stories

An operator syncs Technitium DNS records into the knowledge graph. The connector declares which records it can ingest and which read-only tool pages them.

## Requirements and acceptance

- FR-001: The connector declares the `zones` source in its ontology pack.
- SC-001: The packaged declaration validates, and its tool is a served read-only operation tool.

## Why a new spec

This repository had no local spec. The search `git grep -n ingest -- specs` found only the template. The SDK owns the declaration format and the runner. Arbora owns the served sync operations. This spec owns only the Technitium DNS declaration.

## Scope and interfaces

The connector ships `technitium_dns_mcp/ontology/ingest_sources.json`. The SDK serves it as the read-only `technitium_dns_ingest_sources` tool. Non-goals: write operations, scheduling and storage.

## Traceability

| Requirement | Design section | Test ID | Evidence |
|---|---|---|---|
| FR-001 | [plan.md](plan.md) | `tests/test_ingest_sources.py` |  |

## Open questions

None.
