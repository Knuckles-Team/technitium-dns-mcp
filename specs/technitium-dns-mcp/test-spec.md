# CONN-TECHNITIUM-DNS-MCP — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-TECHNITIUM-DNS-MCP-R001` | `tests/test_ingest_sources.py::test_declares_ingestible_sources` | `tests/test_ingest_sources.py::test_declares_ingestible_sources` validates the packaged file, resolves its tool to a client read operation and its record type to a manifest `schema_mappings` entry. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.

## Adoption of scion-sdk 0.10.0 (`CONN-TECHNITIUM-DNS-MCP-R002`)

| Requirement | Test | Observation |
|---|---|---|
| `CONN-TECHNITIUM-DNS-MCP-R002` | `tests/test_scion_sdk_0_10_imports.py::test_every_scion_sdk_import_resolves_on_the_pinned_release` | Every `scion_sdk` import resolves on the pinned release; a removed path fails the test. |
