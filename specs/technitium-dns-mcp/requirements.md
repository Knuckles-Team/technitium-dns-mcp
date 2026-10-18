# CONN-TECHNITIUM-DNS-MCP — Requirements

Governing spec: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-TECHNITIUM-DNS-MCP-R001` | **Declare the `zones` source.** The connector ships `technitium_dns_mcp/ontology/ingest_sources.json` with the `zones` source. The source pages records through the read-only tool `technitium_dns_list_zones`. | `tests/test_ingest_sources.py::test_declares_ingestible_sources` validates the packaged file, resolves its tool to a client read operation and its record type to a manifest `schema_mappings` entry. |
