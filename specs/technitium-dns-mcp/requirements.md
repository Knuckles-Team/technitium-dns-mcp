# CONN-TECHNITIUM-DNS-MCP — Requirements

Governing spec: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-TECHNITIUM-DNS-MCP-R001` | **Declare the `zones` source.** The connector ships `technitium_dns_mcp/ontology/ingest_sources.json` with the `zones` source. The source pages records through the read-only tool `technitium_dns_list_zones`. Caller chain: the SDK source ingest runner loads the packaged `technitium_dns_mcp/ontology/ingest_sources.json`, whose `zones` source calls the read-only tool `technitium_dns_list_zones` (declared at `technitium_dns_mcp/connector_sources.py:13`). Shape: `technitium_dns_mcp/ontology/ingest_sources.json` with the `zones` source and a `schema_mappings` entry for its record type; reuses the SDK source declaration loader. Proving test: `tests/test_ingest_sources.py::test_declares_ingestible_sources`. | `tests/test_ingest_sources.py::test_declares_ingestible_sources` validates the packaged file, resolves its tool to a client read operation and its record type to a manifest `schema_mappings` entry. |
