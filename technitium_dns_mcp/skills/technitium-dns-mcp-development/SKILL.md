---
name: technitium-dns-mcp-development
skill_type: skill
domain: development
description: >-
  Develop, test, and publish the technitium-dns-mcp connector without breaking
  its typed Technitium DNS API facade, MCP tools, credential and TLS boundary,
  packaged resources, ontology, or governed Pages contract.
license: MIT
tags: [technitium, dns, mcp, connector, development, testing, pages, specs]
tier: repository
metadata:
  author: Genius
  version: '0.1.0'
---

# Technitium DNS MCP Development

Use this skill for changes inside the `technitium-dns-mcp` connector. It owns
the Technitium DNS API calls, source mappings, MCP registration, packaged
prompts and skills, and connector-owned documentation. Shared transport and
connector contracts belong to `agent-connector-sdk`; admission, serving, and
durable graph state belong to their owning repositories.

## Repository map

- `technitium_dns_mcp/api_client.py` composes the User, Dashboard, and Zones
  API facades. Preserve their request parameters, response envelopes, and
  endpoint paths when adding or changing operations.
- `technitium_dns_mcp/auth.py` loads the configured URL and token and applies
  the connector TLS profile. Keep credentials out of source, fixtures, logs,
  exception text, and skill content.
- `technitium_dns_mcp/mcp/` registers the typed `user`, `dashboard`, `zones`,
  and `ingest` tool groups. Keep action names, routing, and redaction stable.
- `technitium_dns_mcp/connector_sources.py` and `kg_ingest.py` own the
  read-only source declaration and graph-ingestion mapping. The `zones`
  source must continue to page through `technitium_dns_list_zones`.
- `technitium_dns_mcp/ontology/`, `prompts/`, and `skills/` are packaged
  resources. `technitium_dns_mcp/ontology/technitium.ttl` is the ontology
  authority and must not be changed for documentation or workflow work.
- `specs/connector-content/` and `specs/technitium-dns-mcp/` own the
  repository specifications and generated status evidence.

## Before editing

1. Work in a real Git worktree based on the exact current `origin/main` and
   identify the owning requirement with `git grep -n "<term>" -- specs`.
2. Trace a changed MCP action from its dispatcher through the typed API facade,
   auth/TLS boundary, and response shape. Reuse the existing client and test
   seams rather than creating a second request path.
3. Use mocked HTTP sessions and task-local fixtures. Never contact a live DNS
   server or require a token in a local gate.
4. Generated `specs/*/status.json` files are outputs of
   `pipelines-hook spec-status`; do not hand-edit them or infer proof from a
   marker alone.

## Implementation contract

- Preserve the stable connector identity `technitium-dns-mcp`, the
  `technitium_dns_mcp:connector` entry point, and the stdio/streamable-HTTP
  transport declarations.
- Route API operations through the existing typed facade and preserve query
  parameter filtering, pagination, API response normalization, and safe
  handling of configured bearer tokens.
- Keep TLS verification and profile selection at the auth/transport boundary;
  do not add endpoint or credential bypasses for tests or examples.
- Keep source ingestion read-only and bounded. It must remain graceful when a
  graph engine is unavailable and must not invent records or mutate the DNS
  service through an ingest tool.
- Keep ontology classes, mappings, tool names, prompts, and package-data paths
  aligned. If a packaged skill or other metadata changes, bump the project
  version and refresh the matching `uv.lock` self-package entry in the same
  release slice.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver one small, reviewable slice at a time.

- Name the owning requirement and its proof before editing.
- Keep a slice to one connector concern: one API/MCP behavior, one test seam,
  one workflow/configuration repair, or one substantive skill.
- Run the smallest affected checks first, then the repository pre-commit suite
  and required pre-push hooks. Fix failures and warnings rather than bypassing
  hooks.
- Record exact source and test commands in the review handoff. Stage only
  reviewed paths; never stage caches, credentials, generated site output, or a
  whole shared checkout.
- Never claim a spec or Pages row from YAML alone. Generated status records, a
  successful exact-source workflow, and the published snapshot must agree.

## Spec delivery and Pages

The canonical Pages caller is `.github/workflows/pages.yml`. It declares the
`docs` content source, enables the version-1 dashboard with
`.config/spec-dashboard.json`, and runs on `main` plus an explicit
`workflow_dispatch`. Keep `docs/**`, `mkdocs.yml`, `README.md`, `specs/**`,
the dashboard config, and the workflow itself in its push trigger.

The shared renderer owns the HTML layout and writes `spec-delivery/snapshot.json`;
do not commit generated site output. Preserve the `spec-delivery/` link in the
documentation landing page. Rebuild status evidence through the central hook
after spec changes and inspect the generated diff. Pages proof is complete only
when a successful hosted run has `headSha` equal to the reviewed source
revision and the public snapshot returns HTTP 200 with this connector's records.
Local config or MkDocs rendering proves wiring, not publication.

## Verification

From the repository root, use the locked environment:

    uv sync --locked
    uvx pre-commit run --all-files
    uv run --all-extras pytest -q

For focused feedback, run the smallest affected test file with mocked HTTP
responses. For workflow/configuration slices, validate the JSON, assert every
workflow path exists, and inspect `git diff --check`; do not call live
Technitium or graph-engine endpoints. Keep exact-source hosted and public-page
evidence separate from local test results.

## Safety

Never commit `.env` files, API tokens, private endpoints, raw DNS records,
generated site output, request dumps, or local caches. Preserve credential
validation, TLS verification, token redaction, destructive-operation guards,
and the existing ontology/runtime behavior while changing docs, skills, or
workflow wiring.
