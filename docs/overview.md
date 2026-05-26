# Architecture Overview

This package splits into three clear tiers:
1. **API Layer**: `api/` folder contains granular subclasses for User, Dashboard, and Zones API operations.
2. **MCP Layer**: `mcp/` registers FastMCP tools invoking the API client under semantic tags.
3. **Agent Layer**: Exposes graph-based autonomous agents using `agent_server.py`.
