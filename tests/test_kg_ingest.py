"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_zones`` / ``ingest_records`` seam
against a fake ingest transport (no engine required), asserting the submitted
``SourceRecord``/``SourceRelationship`` wire objects and the Technitium
zone/record → :DnsZone/:DnsRecord/:DnsServerNode mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from technitium_dns_mcp.kg_ingest import (
    ingest_entities,
    ingest_records,
    ingest_zones,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


def _records_by_id(request: Any) -> dict[str, Any]:
    return {r.record_id: r for r in request.records}


def _node_type_of(record: Any) -> str:
    # mapping_reference: "manifest:<connector>#schema_mappings/<node_type>"
    return record.mapping_reference.rsplit("/", 1)[-1]


def _relationship_name_of(rel: Any) -> str:
    # relation_reference: "manifest:<connector>#resources/<type>/relations/<name>"
    return rel.relation_reference.rsplit("/", 1)[-1]


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "DnsZone", "name": "home.example"},
            {"id": "b", "node_type": "DnsServerNode", "name": "n1"},
        ],
        [{"source": "a", "target": "b", "relationship": "hostedOnNode"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    assert set(_records_by_id(request)) == {"a", "b"}
    rel = request.relationships[0]
    assert rel.source.record_id == "a"
    assert rel.target.record_id == "b"
    assert _relationship_name_of(rel) == "hostedOnNode"


@pytest.mark.asyncio
async def test_ingest_entities_rejects_empty_input(ingest):
    service, transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
    assert transport.requests == []


@pytest.mark.asyncio
async def test_ingest_zones_maps_zone_and_node(ingest):
    service, transport = ingest
    resp = {
        "status": "ok",
        "response": {
            "zones": [
                {
                    "name": "home.example",
                    "type": "Primary",
                    "dnssecStatus": "SignedWithNSEC3",
                    "disabled": False,
                    "internal": False,
                },
                {"name": "10.in-addr.arpa", "type": "Primary", "disabled": False},
            ]
        },
    }
    res = await ingest_zones(resp, node="dns1", ingest=service)
    # 2 zones + 1 server node
    assert res == {"nodes": 3, "edges": 2}
    records = _records_by_id(transport.requests[0])
    zone = records["technitium:zone:home.example"]
    assert _node_type_of(zone) == "DnsZone"
    assert zone.payload["zoneType"] == "Primary"
    assert zone.payload["dnssecStatus"] == "SignedWithNSEC3"
    assert zone.payload["technitiumId"] == "home.example"
    assert _node_type_of(records["technitium:node:dns1"]) == "DnsServerNode"
    rel = transport.requests[0].relationships[0]
    assert rel.source.record_id == "technitium:zone:home.example"
    assert rel.target.record_id == "technitium:node:dns1"
    assert _relationship_name_of(rel) == "hostedOnNode"


@pytest.mark.asyncio
async def test_ingest_records_maps_records_and_rdata(ingest):
    service, transport = ingest
    resp = {
        "response": {
            "records": [
                {
                    "name": "gitlab.home.example",
                    "type": "A",
                    "ttl": 3600,
                    "disabled": False,
                    "rData": {"ipAddress": "10.0.0.12"},
                },
                {
                    "name": "www.home.example",
                    "type": "CNAME",
                    "ttl": 300,
                    "rData": {"cname": "gitlab.home.example"},
                },
            ]
        }
    }
    res = await ingest_records(resp, "home.example", ingest=service)
    assert res == {"nodes": 2, "edges": 2}
    records = _records_by_id(transport.requests[0])
    a_rec = records["technitium:record:gitlab.home.example|A|0"]
    assert _node_type_of(a_rec) == "DnsRecord"
    assert a_rec.payload["recordType"] == "A"
    assert a_rec.payload["ttl"] == 3600
    # the SDK's PersistencePrivacyGuard redacts IPv4-shaped property values.
    assert a_rec.payload["recordData"] == "[REDACTED_IPV4]"
    cname = records["technitium:record:www.home.example|CNAME|1"]
    assert cname.payload["recordData"] == "gitlab.home.example"
    # each record links back to its zone
    assert all(
        rel.target.record_id == "technitium:zone:home.example"
        and _relationship_name_of(rel) == "recordInZone"
        for rel in transport.requests[0].relationships
    )


@pytest.mark.asyncio
async def test_ingest_records_rejects_empty_response(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_records(
            {"response": {"records": []}},
            "z",
            ingest=service,
        )
