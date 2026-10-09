"""Native epistemic-graph ingestion for Technitium DNS records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges through the
``agent_connector_sdk.ingest`` knowledge-ingest facade, which owns the transaction
and raises ``IngestError`` when the authoritative engine cannot commit.
"""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

_SOURCE = "technitium-dns-mcp"
_DOMAIN = "technitium"
_BINDING = IngestBinding(connector=_SOURCE, stream=_DOMAIN)


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={
            k: v for k, v in record.items() if k not in ("id", "node_type")
        },
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    properties = {
        k: v
        for k, v in record.items()
        if k not in ("source", "target", "relationship")
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=properties or None,
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships in one change set."""
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(e) for e in entities),
        relationships=tuple(_to_relationship(r) for r in relationships or ()),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


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


async def ingest_zones(
    zones_resp: Any,
    *,
    node: str | None = None,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map a ``list_zones`` response → ``:DnsZone`` (+ ``:DnsServerNode``) nodes and ingest."""
    zones = _unwrap(zones_resp, "zones")
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    node_id = f"technitium:node:{node}" if node else None
    if node_id:
        entities.append(
            {
                "id": node_id,
                "node_type": "DnsServerNode",
                "name": node,
                "technitiumId": node,
            }
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
    return await ingest_entities(entities, relationships, ingest=ingest)


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


async def ingest_records(
    records_resp: Any,
    zone: str,
    *,
    node: str | None = None,
    ingest: KnowledgeIngest | None = None,
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
        relationships.append(
            {"source": rid, "target": zone_id, "relationship": "recordInZone"}
        )
    return await ingest_entities(entities, relationships, ingest=ingest)
