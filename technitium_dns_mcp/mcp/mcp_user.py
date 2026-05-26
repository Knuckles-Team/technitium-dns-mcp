"""MCP tools for Technitium DNS User & SSO operations."""

from typing import Any
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from technitium_dns_mcp.auth import get_client


def register_user_tools(mcp: FastMCP):
    """Register Technitium DNS user management tools.
    CONCEPT:TDNS-002
    """

    @mcp.tool(tags={"user"})
    async def technitium_dns_user(
        action: str = Field(
            description=(
                "Action to perform. Must be one of: "
                "'get_sso_status', 'login', 'create_token', 'create_single_use_token', "
                "'logout', 'get_session_info', 'delete_user_session', 'change_password', "
                "'initialize_2fa', 'enable_2fa', 'disable_2fa', 'get_user_profile_details', "
                "'set_user_profile_details', 'check_for_update'"
            )
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters matching the method signature."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> Any:
        """Manage Technitium DNS user sessions, authentication, credentials, and profile settings."""
        if ctx:
            await ctx.info(f"Executing User action '{action}'...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_sso_status":
            return client.get_sso_status(**kwargs)
        if action == "login":
            return client.login(**kwargs)
        if action == "create_token":
            return client.create_token(**kwargs)
        if action == "create_single_use_token":
            return client.create_single_use_token(**kwargs)
        if action == "logout":
            return client.logout(**kwargs)
        if action == "get_session_info":
            return client.get_session_info(**kwargs)
        if action == "delete_user_session":
            return client.delete_user_session(**kwargs)
        if action == "change_password":
            return client.change_password(**kwargs)
        if action == "initialize_2fa":
            return client.initialize_2fa(**kwargs)
        if action == "enable_2fa":
            return client.enable_2fa(**kwargs)
        if action == "disable_2fa":
            return client.disable_2fa(**kwargs)
        if action == "get_user_profile_details":
            return client.get_user_profile_details(**kwargs)
        if action == "set_user_profile_details":
            return client.set_user_profile_details(**kwargs)
        if action == "check_for_update":
            return client.check_for_update(**kwargs)

        raise ValueError(f"Unknown User action: {action}")
