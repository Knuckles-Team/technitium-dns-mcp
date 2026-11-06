# CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py::test_default_content_surfaces` (planned) | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
| T-002 | `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R002` | `tests/test_access_contracts.py::test_competency_contracts_certified` (planned) | Test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract. |
| T-003 | `CONN-TECHNITIUM-DNS-MCP-CONNECTOR-CONTENT-R003` | `tests/test_prompt_tools.py::test_dns_specialist_prompt_names_typed_tools_only` | The prompt lists `technitium_dns_list_zones` and contains no `action=` routing text. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.
