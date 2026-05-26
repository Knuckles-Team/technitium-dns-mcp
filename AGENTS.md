# Technitium DNS MCP Agent Specs

<!-- CONCEPT:TDNS-001 -->
<!-- CONCEPT:TDNS-002 -->
<!-- CONCEPT:TDNS-003 -->

This file acts as a machine-readable README for AI coding agents collaborating on this repository.

## Tech Stack & Architecture
- **Language**: Python >= 3.11
- **Ecosystem**: `agent-utilities` Dynamic Facade
- **MCP Server**: FastMCP (stdio and HTTP support)
- **Key Files**:
  - `technitium_dns_mcp/mcp_server.py`: FastMCP entry points and tool registration.
  - `technitium_dns_mcp/api_client.py`: API facade inheriting from custom domain modules.
  - `technitium_dns_mcp/auth.py`: Credentials loading, credential validation, and authentication headers.

## Commands

### Quality & Linting
Run pre-commit hooks locally:
```bash
pre-commit run --all-files
```

### Execution & Run
Launch the FastMCP server in stdio mode:
```bash
python -m technitium_dns_mcp.mcp_server
```

### Testing Suite
Execute the entire test suite:
```bash
pytest -v
```

## Project Structure

### File Tree
```text
.
├── .bumpversion.cfg
├── .gitignore
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── docs
│   ├── concepts.md
│   ├── index.md
│   └── overview.md
├── docker
│   ├── Dockerfile
│   └── compose.yml
├── prompts
│   └── main_agent.md
├── tests
│   ├── conftest.py
│   ├── test_agent_integration.py
│   ├── test_api_client.py
│   ├── test_auth.py
│   ├── test_concept_parity.py
│   ├── test_init_dynamics.py
│   ├── test_mcp_handlers.py
│   └── test_startup.py
└── technitium_dns_mcp
    ├── __init__.py
    ├── __main__.py
    ├── agent_server.py
    ├── api_client.py
    ├── auth.py
    ├── models.py
    ├── mcp_config.json
    ├── agent_data
    │   └── IDENTITY.md
    ├── api
    │   ├── __init__.py
    │   ├── api_client_base.py
    │   ├── api_client_dashboard.py
    │   ├── api_client_user.py
    │   └── api_client_zones.py
    ├── mcp
    │   ├── __init__.py
    │   ├── mcp_dashboard.py
    │   ├── mcp_user.py
    │   └── mcp_zones.py
    └── mcp_server.py
```

## Concept Registry

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:TDNS-001` | Core API Client Operations | Dynamic API facade client integration |
| `CONCEPT:TDNS-002` | FastMCP Tools Execution | FastMCP tool registration and stdio handling |
| `CONCEPT:TDNS-003` | Identity & Gateway Security | Credential validation and SSL verification |
| `CONCEPT:ECO-4.0` | Ecosystem Compliance | Multi-package integration compliance standard |

---

## When Stuck
1. Check the local mock context implementation in `tests/conftest.py`.
2. Propose an Implementation Plan first before adding new endpoints.
