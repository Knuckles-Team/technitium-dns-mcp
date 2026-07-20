"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_zones`` / ``ingest_records`` seam with a
fake engine client (no engine required), asserting the txn add_node/commit + edge calls and
the Technitium zone/record → :DnsZone/:DnsRecord/:DnsServerNode mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from technitium_dns_mcp.kg_ingest import (
    ingest_entities,
    ingest_records,
    ingest_zones,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, source, target, props):
        self.edges.append((source, target, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "DnsZone", "name": "home.example"},
            {"id": "b", "node_type": "DnsServerNode", "name": "n1"},
        ],
        [{"source": "a", "target": "b", "relationship": "hostedOnNode"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "technitium-dns-mcp"
    assert c.txn.nodes["a"]["domain"] == "technitium"
    assert c.txn.edges == [("a", "b", {"relationship": "hostedOnNode"})]


def test_ingest_entities_rejects_empty_input():
    c = _FakeClient()
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=c)
    assert c.txn.committed is False


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
    res = ingest_zones(resp, node="dns1", client=c, graph="__commons__")
    # 2 zones + 1 server node
    assert res == {"nodes": 3, "edges": 2}
    zone = c.txn.nodes["technitium:zone:home.example"]
    assert zone["node_type"] == "DnsZone"
    assert zone["zoneType"] == "Primary"
    assert zone["dnssecStatus"] == "SignedWithNSEC3"
    assert zone["technitiumId"] == "home.example"
    assert c.txn.nodes["technitium:node:dns1"]["node_type"] == "DnsServerNode"
    assert (
        "technitium:zone:home.example",
        "technitium:node:dns1",
        {"relationship": "hostedOnNode"},
    ) in c.txn.edges


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
    res = ingest_records(resp, "home.example", client=c, graph="__commons__")
    assert res == {"nodes": 2, "edges": 2}
    a_rec = c.txn.nodes["technitium:record:gitlab.home.example|A|0"]
    assert a_rec["node_type"] == "DnsRecord"
    assert a_rec["recordType"] == "A"
    assert a_rec["ttl"] == 3600
    assert a_rec["recordData"] == "10.0.0.12"
    cname = c.txn.nodes["technitium:record:www.home.example|CNAME|1"]
    assert cname["recordData"] == "gitlab.home.example"
    # each record links back to its zone
    assert all(
        e[1] == "technitium:zone:home.example" and e[2] == {"relationship": "recordInZone"}
        for e in c.txn.edges
    )


def test_ingest_records_rejects_empty_response():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_records(
            {"response": {"records": []}},
            "z",
            client=_FakeClient(),
        )
