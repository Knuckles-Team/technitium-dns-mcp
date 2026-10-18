"""The packaged ingestible-source declaration (CONN-TECHNITIUM-DNS-MCP-R001)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from agent_connector_sdk.ingest.sources import load_ingest_sources
from agent_connector_sdk.mcp.method_tools import operation_annotations, operation_verb
from agent_connector_sdk.mcp.tool_surface import operation_prefix

import technitium_dns_mcp
from technitium_dns_mcp.api_client import Api


@pytest.mark.spec("CONN-TECHNITIUM-DNS-MCP-R001")
def test_declares_ingestible_sources() -> None:
    declaration = load_ingest_sources(Path(technitium_dns_mcp.__file__).parent)
    assert declaration is not None
    assert declaration.connector == "technitium-dns-mcp"
    source = declaration.source("zones")
    assert source is not None and source.record_type == "DnsZone"
    prefix = operation_prefix("technitium-dns-mcp")
    assert source.tools == (f"{prefix}_list_zones",)
    # The engine admits a record only under the pack mapping of its type.
    manifest = yaml.safe_load(
        (Path(technitium_dns_mcp.__file__).parent / "connector_manifest.yml").read_text(
            "utf-8"
        )
    )
    assert source.record_type in manifest["schema_mappings"]
    method = getattr(Api, "list_zones")
    annotations = operation_annotations("list_zones", operation_verb(method))
    assert annotations.read_only_hint is True
