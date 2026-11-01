# CONN-TECHNITIUM-DNS-MCP — Technitium DNS ingestible sources

Owner: technitium-dns-mcp. Cross-repo IDs: SCION-SOURCE-INGEST-R004.19, SCION-SOURCE-INGEST-R004.21, ARBORA-OPS-R020.6.

## Purpose and user stories

An operator syncs Technitium DNS records into the knowledge graph. The connector declares which records it can ingest and which read-only tool pages them.

## Why a new spec

This repository had no local spec. The search `git grep -n ingest -- specs` found only the template. The SDK owns the declaration format and the runner. Arbora owns the served sync operations. This spec owns only the Technitium DNS declaration.

## Scope and interfaces

The connector ships `technitium_dns_mcp/ontology/ingest_sources.json`. The SDK serves it as the read-only `technitium_dns_ingest_sources` tool. Non-goals: write operations, scheduling and storage.

## Open questions

None.

## Delivery mapping

Component: technitium-dns-mcp connector

Code: ../../technitium_dns_mcp/__init__.py

## User Scenarios & Testing

### User Story 1 - Declare the `zones` source (Priority: P1)

The fleet operator and the engine rely on this behaviour of `technitium-dns-mcp`: The connector ships `technitium_dns_mcp/ontology/ingest_sources.json` with the `zones` source. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `technitium-dns-mcp` connector built from the default branch, **When** `tests/test_ingest_sources.py::test_declares_ingestible_sources` runs, **Then** `tests/test_ingest_sources.py::test_declares_ingestible_sources` validates the packaged file, resolves its tool to a client read operation and its record type to a manifest `schema_mappings` entry.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Declare the `zones` source. Rows: `CONN-TECHNITIUM-DNS-MCP-R001`.

## Success Criteria

- **SC-001**: `tests/test_ingest_sources.py::test_declares_ingestible_sources` validates the packaged file, resolves its tool to a client read operation and its record type to a manifest `schema_mappings` entry. Rows: `CONN-TECHNITIUM-DNS-MCP-R001`.

## Assumptions

- The `technitium-dns-mcp` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-TECHNITIUM-DNS-MCP-R001` | plan.md Production caller chain | T-001 | tests/test_ingest_sources.py::test_declares_ingestible_sources |
