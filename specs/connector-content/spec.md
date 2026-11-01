# CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: technitium-dns-mcp. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `technitium-dns-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Delivery mapping

Component: technitium-dns-mcp connector

Code: ../../technitium_dns_mcp/__init__.py

## Why a new spec

Searched `specs/` of `technitium-dns-mcp` with `git grep` for the terms of this spec. No other spec of this repository owns the capability, so this spec owns it.

## User Scenarios & Testing

### User Story 1 - Default content (Priority: P1)

The fleet operator and the engine rely on this behaviour of `technitium-dns-mcp`: `pyproject.toml` declares `technitium-dns-mcp` as the single `scion_sdk.connector` entry point. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `technitium-dns-mcp` connector built from the default branch, **When** `tests/test_default_content_surfaces.py::test_default_content_surfaces` runs, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.

### User Story 2 - Declare access contracts for the competency reads of technitium-dns-mcp (Priority: P1)

The fleet operator and the engine rely on this behaviour of `technitium-dns-mcp`: Subsystem: connector `technitium-dns-mcp`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `technitium-dns-mcp` connector built from the default branch, **When** `tests/test_access_contracts.py::test_competency_contracts_certified` runs, **Then** test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Default content. Rows: `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R001`.
- **FR-002**: Declare access contracts for the competency reads of technitium-dns-mcp. Rows: `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R002`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R001`.
- **SC-002**: Test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract. Rows: `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R002`.

## Assumptions

- The `technitium-dns-mcp` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R001` | plan.md Production caller chain | T-001 | tests/test_default_content_surfaces.py::test_default_content_surfaces |
| FR-002 | `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R002` | plan.md Production caller chain | T-002 | tests/test_access_contracts.py::test_competency_contracts_certified |
