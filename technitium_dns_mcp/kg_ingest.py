"""Native epistemic-graph ingestion for Technitium DNS records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The connector natively pushes its
DNS state into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:DnsZone``, ``:DnsRecord``, ``:DnssecKey``, ``:DnsServerNode``) + links, using the
lightweight engine client (``GraphComputeEngine()._client`` + ``txn``) — the same fast
client the blob ``MediaStore`` uses, NOT the heavy in-process ingestion engine.

Everything is best-effort and dependency-/engine-guarded: with no agent-utilities KG stack
or no reachable engine, every entry point **no-ops** (returns ``None``), so the connector
keeps working with zero KG infrastructure. Nodes carry the shared provenance
(``domain``/``source``) and match the classes federated by ``technitium_dns_mcp.ontology``.
Node ids follow ``technitium:<class>:<externalId>``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("technitium_dns_mcp.kg")

_SOURCE = "technitium-dns-mcp"
_DOMAIN = "technitium"
_DEFAULT_GRAPH = "__commons__"


def _fallback_client() -> tuple[Any | None, str]:
    """Resolve ``(engine_client, graph)`` directly (self-contained txn fallback).

    Used when the shared ``native_ingest`` primitive is not present in the installed
    agent_utilities. Returns ``(None, "")`` when no engine is reachable; never raises.
    """
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed nodes (+ edges) into epistemic-graph.

    Prefers the shared ``agent_utilities...native_ingest.ingest_entities`` primitive;
    falls back to a self-contained txn write when it is not installed. Returns
    ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None

    # Preferred path: the shared primitive (once present in the installed agent_utilities).
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            ingest_entities as _shared,
        )

        return _shared(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )
    except Exception as e:  # noqa: BLE001 — primitive absent; use fallback
        logger.debug("KG ingest: shared primitive unavailable (%s); using fallback", e)

    if client is None:
        client, graph = _fallback_client()
    if client is None:
        return None
    graph = graph or _DEFAULT_GRAPH

    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


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
        "type": "DnsZone",
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
) -> dict[str, int] | None:
    """Map a ``list_zones`` response → ``:DnsZone`` (+ ``:DnsServerNode``) nodes and ingest."""
    zones = _unwrap(zones_resp, "zones")
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    node_id = f"technitium:node:{node}" if node else None
    if node_id:
        entities.append(
            {"id": node_id, "type": "DnsServerNode", "name": node, "technitiumId": node}
        )
    for zone in zones:
        if not zone.get("name"):
            continue
        ent = _zone_entity(zone, node)
        entities.append(ent)
        if node_id:
            relationships.append(
                {"source": ent["id"], "target": node_id, "type": "hostedOnNode"}
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
) -> dict[str, int] | None:
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
            "type": "DnsRecord",
            "name": name,
            "recordType": rtype,
            "ttl": rec.get("ttl"),
            "disabled": rec.get("disabled"),
            "recordData": _render_rdata(rec),
            "zone": zone,
            "technitiumId": f"{name}|{rtype}",
        }
        entities.append({k: v for k, v in ent.items() if v is not None})
        relationships.append({"source": rid, "target": zone_id, "type": "recordInZone"})
    return ingest_entities(entities, relationships, client=client, graph=graph)
