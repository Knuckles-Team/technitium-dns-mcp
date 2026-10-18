# CONN-TECHNITIUM-DNS-MCP — Plan

Component: Connector

Code: ../../technitium_dns_mcp/ontology/ingest_sources.json ../../tests/test_ingest_sources.py

## Design

The declaration file lists one source, `zones`. Its record type is `DnsZone`. The tool `technitium_dns_list_zones` is the operation tool of the client method `list_zones`. `register_tool_surface` serves the file as `technitium_dns_ingest_sources`. A host syncs the source through the SDK sync runner (SDK-SOURCE-INGEST-R004.20).
