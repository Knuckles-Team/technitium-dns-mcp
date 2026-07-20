"""Native epistemic-graph ingestion for Technitium DNS records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges. The required agent-utilities
native-ingest primitive owns the transaction and raises NativeIngestError when the
authoritative engine cannot commit.
"""

from __future__ import annotations

from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

_SOURCE = "technitium-dns-mcp"
_DOMAIN = "technitium"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through agent-utilities."""
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def _unwrap(resp: Any, key: str) -> list[dict[str, Any]]:
    """Pull a list out of a Technitium API response (``{status, response:{<key>:[...]}}``)."""
    if resp is None:
        return []
    data = resp
    if isinstance(resp, dict):
        data = resp.get("response", resp)
    if isinstance(data, dict):
        items = data.get(key)
    elif isinstance(data, list):
        items = data
    else:
        items = None
    if isinstance(items, dict):
        items = [items]
    return [i for i in (items or []) if isinstance(i, dict)]


def _zone_entity(zone: dict[str, Any], node: str | None) -> dict[str, Any]:
    name = zone.get("name")
    ent = {
        "id": f"technitium:zone:{name}",
        "node_type": "DnsZone",
        "name": name,
        "zoneType": zone.get("type"),
        "dnssecStatus": zone.get("dnssecStatus"),
        "disabled": zone.get("disabled"),
        "internal": zone.get("internal"),
        "technitiumId": name,
    }
    if node:
        ent["node"] = node
    return {k: v for k, v in ent.items() if v is not None}


def ingest_zones(
    zones_resp: Any,
    *,
    node: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map a ``list_zones`` response → ``:DnsZone`` (+ ``:DnsServerNode``) nodes and ingest."""
    zones = _unwrap(zones_resp, "zones")
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    node_id = f"technitium:node:{node}" if node else None
    if node_id:
        entities.append(
            {"id": node_id, "node_type": "DnsServerNode", "name": node, "technitiumId": node}
        )
    for zone in zones:
        if not zone.get("name"):
            continue
        ent = _zone_entity(zone, node)
        entities.append(ent)
        if node_id:
            relationships.append(
                {"source": ent["id"], "target": node_id, "relationship": "hostedOnNode"}
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def _render_rdata(rec: dict[str, Any]) -> str | None:
    """Best-effort flatten of a record's ``rData`` payload to a text value."""
    rdata = rec.get("rData")
    if rdata is None:
        return None
    if isinstance(rdata, str):
        return rdata
    if isinstance(rdata, dict):
        for k in (
            "ipAddress",
            "cname",
            "nameServer",
            "text",
            "value",
            "exchange",
            "target",
            "ptrName",
            "domain",
        ):
            if rdata.get(k):
                return str(rdata[k])
        # Fall back to a compact rendering of the whole payload.
        return ", ".join(f"{k}={v}" for k, v in rdata.items() if v is not None) or None
    return str(rdata)


def ingest_records(
    records_resp: Any,
    zone: str,
    *,
    node: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map a ``get_records`` response → ``:DnsRecord`` nodes (+ ``:recordInZone``) and ingest."""
    records = _unwrap(records_resp, "records")
    zone_id = f"technitium:zone:{zone}"
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for idx, rec in enumerate(records):
        name = rec.get("name")
        rtype = rec.get("type")
        if name is None or rtype is None:
            continue
        rid = f"technitium:record:{name}|{rtype}|{idx}"
        ent = {
            "id": rid,
            "node_type": "DnsRecord",
            "name": name,
            "recordType": rtype,
            "ttl": rec.get("ttl"),
            "disabled": rec.get("disabled"),
            "recordData": _render_rdata(rec),
            "zone": zone,
            "technitiumId": f"{name}|{rtype}",
        }
        entities.append({k: v for k, v in ent.items() if v is not None})
        relationships.append({"source": rid, "target": zone_id, "relationship": "recordInZone"})
    return ingest_entities(entities, relationships, client=client, graph=graph)
