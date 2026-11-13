"""Each competency recording is certified against its access contract."""

import asyncio
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastmcp import Client
from scion_sdk.access_contract import parse_access_contracts
from scion_sdk.connector import build_server

from technitium_dns_mcp.api_client import Api

ROOT = Path(__file__).resolve().parents[1]


def _field(row, path):
    for part in path.split("."):
        row = row[part]
    return row


@pytest.mark.spec("CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R002")
def test_competency_contracts_certified(monkeypatch):
    monkeypatch.setenv("TECHNITIUM_DNS_URL", "http://localhost:5380")
    monkeypatch.setenv("TECHNITIUM_DNS_TOKEN", "fixture-token")
    contracts = parse_access_contracts(
        (ROOT / "technitium_dns_mcp/ontology/access_contracts.ttl").read_text()
    )
    (contract,) = contracts
    assert contract.entity == "record"
    assert contract.access_kind == "mcp_tool"
    recording = json.loads((ROOT / "tests/recordings/record.json").read_text())

    async def call():
        mcp = build_server("technitium_dns_mcp", command_args=[])[1]
        with patch.object(Api, "get_records", return_value=recording):
            async with Client(mcp) as client:
                return await client.call_tool(
                    contract.operation,
                    {"domain": "www.example.invalid", "zone": "example.invalid"},
                    raise_on_error=False,
                )

    result = asyncio.run(call())
    assert not result.is_error
    body = json.loads(result.content[0].text)
    assert body == recording
    rows = _field(body, contract.records_path)
    assert rows and contract.key_field in rows[0]
    for _, field in contract.predicates:
        assert _field(rows[0], field)
    ontology = (ROOT / "technitium_dns_mcp/ontology/technitium.ttl").read_text()
    for prop, _ in contract.predicates:
        assert f":{prop.rsplit('#', 1)[-1]} a owl:DatatypeProperty" in ontology
