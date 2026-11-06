"""CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R003: the prompts name served tools."""

import json
from importlib import resources


def _prompts():
    root = resources.files("technitium_dns_mcp") / "prompts"
    return {
        p.name: json.loads(p.read_text())
        for p in root.iterdir()
        if p.name.endswith(".json")
    }


def test_prompts_name_typed_tools_only():
    prompts = _prompts()
    assert prompts
    for name, prompt in prompts.items():
        tools = prompt["agent"]["tools"]
        assert "technitium_dns_zones" not in tools, name
        assert (
            "technitium_dns_list_zones" in tools
            or prompt["agent"]["kind"] == "business-role"
        )
        assert "action=" not in json.dumps(prompt), name


def test_one_operator_and_a_prompt_per_role():
    kinds = [p["agent"]["kind"] for p in _prompts().values()]
    assert kinds.count("operator") == 1
    assert kinds.count("business-role") == 3
