"""The packaged ingestible-source declaration (CONN-TECHNITIUM-DNS-MCP-R001)."""

from __future__ import annotations


import pytest
from technitium_dns_mcp.connector_sources import declaration as declared_sources
from agent_connector_sdk.mcp.method_tools import operation_annotations, operation_verb
from agent_connector_sdk.mcp.tool_surface import operation_prefix

from technitium_dns_mcp.api_client import Api


@pytest.mark.spec("CONN-TECHNITIUM-DNS-MCP-R001")
def test_declares_ingestible_sources() -> None:
    declaration = declared_sources()
    assert declaration is not None
    assert declaration.connector == "technitium-dns-mcp"
    source = declaration.source("zones")
    assert source is not None and source.record_type == "DnsZone"
    prefix = operation_prefix("technitium-dns-mcp")
    assert source.tools == (f"{prefix}_list_zones",)
    # The engine admits a record only under the pack mapping of its type.
    assert source.record_type in declared_sources().schema_mappings
    method = getattr(Api, "list_zones")
    annotations = operation_annotations("list_zones", operation_verb(method))
    assert annotations.read_only_hint is True
