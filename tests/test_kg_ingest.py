"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_zones`` / ``ingest_records`` seam with a
fake engine client (no engine required), asserting the txn add_node/commit + edge calls and
the Technitium zone/record → :DnsZone/:DnsRecord/:DnsServerNode mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from technitium_dns_mcp.kg_ingest import (
    ingest_entities,
    ingest_records,
    ingest_zones,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "DnsZone", "name": "home.arpa"},
            {"id": "b", "type": "DnsServerNode", "name": "n1"},
        ],
        [{"source": "a", "target": "b", "type": "hostedOnNode"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "technitium-dns-mcp"
    assert c.txn.nodes["a"]["domain"] == "technitium"
    assert c.edges.edges == [("a", "b", {"type": "hostedOnNode"})]


def test_ingest_entities_empty_is_noop():
    c = _FakeClient()
    assert ingest_entities([], client=c) is None
    assert c.txn.committed is False


def test_ingest_zones_maps_zone_and_node():
    c = _FakeClient()
    resp = {
        "status": "ok",
        "response": {
            "zones": [
                {
                    "name": "home.arpa",
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
    zone = c.txn.nodes["technitium:zone:home.arpa"]
    assert zone["type"] == "DnsZone"
    assert zone["zoneType"] == "Primary"
    assert zone["dnssecStatus"] == "SignedWithNSEC3"
    assert zone["technitiumId"] == "home.arpa"
    assert c.txn.nodes["technitium:node:dns1"]["type"] == "DnsServerNode"
    assert (
        "technitium:zone:home.arpa",
        "technitium:node:dns1",
        {"type": "hostedOnNode"},
    ) in c.edges.edges


def test_ingest_records_maps_records_and_rdata():
    c = _FakeClient()
    resp = {
        "response": {
            "records": [
                {
                    "name": "gitlab.home.arpa",
                    "type": "A",
                    "ttl": 3600,
                    "disabled": False,
                    "rData": {"ipAddress": "10.0.0.12"},
                },
                {
                    "name": "www.home.arpa",
                    "type": "CNAME",
                    "ttl": 300,
                    "rData": {"cname": "gitlab.home.arpa"},
                },
            ]
        }
    }
    res = ingest_records(resp, "home.arpa", client=c, graph="__commons__")
    assert res == {"nodes": 2, "edges": 2}
    a_rec = c.txn.nodes["technitium:record:gitlab.home.arpa|A|0"]
    assert a_rec["type"] == "DnsRecord"
    assert a_rec["recordType"] == "A"
    assert a_rec["ttl"] == 3600
    assert a_rec["recordData"] == "10.0.0.12"
    cname = c.txn.nodes["technitium:record:www.home.arpa|CNAME|1"]
    assert cname["recordData"] == "gitlab.home.arpa"
    # each record links back to its zone
    assert all(
        e[1] == "technitium:zone:home.arpa" and e[2] == {"type": "recordInZone"}
        for e in c.edges.edges
    )


def test_ingest_records_empty_response_is_noop():
    c = _FakeClient()
    assert ingest_records({"response": {"records": []}}, "z", client=c) is None
