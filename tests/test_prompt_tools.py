"""CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R003: the DNS specialist prompt names served tools."""

import json
from importlib import resources


def test_dns_specialist_prompt_names_typed_tools_only():
    path = resources.files("technitium_dns_mcp") / "prompts" / "dns_specialist.json"
    prompt = json.loads(path.read_text())
    assert "technitium_dns_zones" not in prompt["tools"]
    assert "technitium_dns_list_zones" in prompt["tools"]
    assert "action=" not in json.dumps(prompt)
