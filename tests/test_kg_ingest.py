"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_zones`` / ``ingest_records`` seam with a
fake engine client (no engine required), asserting the txn add_node/commit + edge calls and
the Technitium zone/record → :DnsZone/:DnsRecord/:DnsServerNode mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.security.actor_identity import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session

from technitium_dns_mcp.kg_ingest import (
    ingest_entities,
    ingest_records,
    ingest_zones,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"

    @staticmethod
    def shacl_validate_committed(_data_graph: str) -> Any:
        """EG's committed-GraphSchema SHACL authority (agent-utilities EH-385)."""
        from epistemic_graph.generated.rdf_report import ShaclValidationReport

        digest = "sha256:" + "0" * 64
        return ShaclValidationReport(
            conforms=True, results=[], composed_digest=digest, schema_digests=[digest]
        )


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "DnsZone", "name": "home.example"},
            {"id": "b", "node_type": "DnsServerNode", "name": "n1"},
        ],
        [{"source": "a", "target": "b", "relationship": "hostedOnNode"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "technitium-dns-mcp"
    assert c.nodes.values["a"]["domain"] == "technitium"
    assert c.changes.edges == [("a", "b", {"relationship": "hostedOnNode"})]


def test_ingest_entities_rejects_empty_input():
    c = _FakeClient()
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=c)
    assert len(c.changes.applied) == 0


def test_ingest_zones_maps_zone_and_node():
    c = _FakeClient()
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
    res = ingest_zones(resp, node="dns1", client=c)
    # 2 zones + 1 server node
    assert res == {"nodes": 3, "edges": 2}
    zone = c.nodes.values["technitium:zone:home.example"]
    assert zone["node_type"] == "DnsZone"
    assert zone["zoneType"] == "Primary"
    assert zone["dnssecStatus"] == "SignedWithNSEC3"
    assert zone["technitiumId"] == "home.example"
    assert c.nodes.values["technitium:node:dns1"]["node_type"] == "DnsServerNode"
    assert (
        "technitium:zone:home.example",
        "technitium:node:dns1",
        {"relationship": "hostedOnNode"},
    ) in c.changes.edges


def test_ingest_records_maps_records_and_rdata():
    c = _FakeClient()
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
    res = ingest_records(resp, "home.example", client=c)
    assert res == {"nodes": 2, "edges": 2}
    a_rec = c.nodes.values["technitium:record:gitlab.home.example|A|0"]
    assert a_rec["node_type"] == "DnsRecord"
    assert a_rec["recordType"] == "A"
    assert a_rec["ttl"] == 3600
    # native_ingest's governed PII scrubber redacts IPv4-shaped values.
    assert a_rec["recordData"] == "[REDACTED_IPV4]"
    cname = c.nodes.values["technitium:record:www.home.example|CNAME|1"]
    assert cname["recordData"] == "gitlab.home.example"
    # each record links back to its zone
    assert all(
        e[1] == "technitium:zone:home.example"
        and e[2] == {"relationship": "recordInZone"}
        for e in c.changes.edges
    )


def test_ingest_records_rejects_empty_response():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_records(
            {"response": {"records": []}},
            "z",
            client=_FakeClient(),
        )
