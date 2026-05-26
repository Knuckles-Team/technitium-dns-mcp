"""MCP tools for Technitium DNS Authoritative Zones, DNSSEC, and Record operations."""

from typing import Any
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from technitium_dns_mcp.auth import get_client


def register_zones_tools(mcp: FastMCP):
    """Register Technitium DNS zone management and record CRUD tools.
    CONCEPT:TDNS-002
    """

    @mcp.tool(tags={"zones"})
    async def technitium_dns_zones(
        action: str = Field(
            description=(
                "Action to perform. Must be one of: "
                "'list_zones', 'list_catalog_zones', 'create_zone', 'import_zone', "
                "'export_zone', 'clone_zone', 'convert_zone_type', 'enable_zone', "
                "'disable_zone', 'delete_zone', 'resync_zone', 'get_zone_options', "
                "'set_zone_options', 'get_zone_permissions', 'set_zone_permissions', "
                "'sign_zone', 'unsign_zone', 'get_ds_info', 'get_dnssec_properties', "
                "'convert_to_nsec', 'convert_to_nsec3', 'update_nsec3_params', "
                "'update_dnskey_ttl', 'add_private_key', 'update_private_key', "
                "'delete_private_key', 'publish_all_private_keys', 'rollover_dnskey', "
                "'retire_dnskey', 'add_record', 'get_records', 'update_record', "
                "'delete_record'"
            )
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters matching the method signature."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(default=None, description="MCP context"),
    ) -> Any:
        """Manage Technitium DNS authoritative zones, DNSSEC properties/keys, and perform DNS record CRUD."""
        if ctx:
            await ctx.info(f"Executing Zones action '{action}'...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_zones":
            return client.list_zones(**kwargs)
        if action == "list_catalog_zones":
            return client.list_catalog_zones(**kwargs)
        if action == "create_zone":
            return client.create_zone(**kwargs)
        if action == "import_zone":
            return client.import_zone(**kwargs)
        if action == "export_zone":
            return client.export_zone(**kwargs)
        if action == "clone_zone":
            return client.clone_zone(**kwargs)
        if action == "convert_zone_type":
            return client.convert_zone_type(**kwargs)
        if action == "enable_zone":
            return client.enable_zone(**kwargs)
        if action == "disable_zone":
            return client.disable_zone(**kwargs)
        if action == "delete_zone":
            return client.delete_zone(**kwargs)
        if action == "resync_zone":
            return client.resync_zone(**kwargs)
        if action == "get_zone_options":
            return client.get_zone_options(**kwargs)
        if action == "set_zone_options":
            return client.set_zone_options(**kwargs)
        if action == "get_zone_permissions":
            return client.get_zone_permissions(**kwargs)
        if action == "set_zone_permissions":
            return client.set_zone_permissions(**kwargs)
        if action == "sign_zone":
            return client.sign_zone(**kwargs)
        if action == "unsign_zone":
            return client.unsign_zone(**kwargs)
        if action == "get_ds_info":
            return client.get_ds_info(**kwargs)
        if action == "get_dnssec_properties":
            return client.get_dnssec_properties(**kwargs)
        if action == "convert_to_nsec":
            return client.convert_to_nsec(**kwargs)
        if action == "convert_to_nsec3":
            return client.convert_to_nsec3(**kwargs)
        if action == "update_nsec3_params":
            return client.update_nsec3_params(**kwargs)
        if action == "update_dnskey_ttl":
            return client.update_dnskey_ttl(**kwargs)
        if action == "add_private_key":
            return client.add_private_key(**kwargs)
        if action == "update_private_key":
            return client.update_private_key(**kwargs)
        if action == "delete_private_key":
            return client.delete_private_key(**kwargs)
        if action == "publish_all_private_keys":
            return client.publish_all_private_keys(**kwargs)
        if action == "rollover_dnskey":
            return client.rollover_dnskey(**kwargs)
        if action == "retire_dnskey":
            return client.retire_dnskey(**kwargs)
        if action == "add_record":
            # Extract kwargs and separate base arguments from type-specific details
            zone = kwargs.pop("zone")
            domain = kwargs.pop("domain")
            type = kwargs.pop("type")
            ttl = int(kwargs.pop("ttl"))
            overwrite = kwargs.pop("overwrite", None)
            node = kwargs.pop("node", None)
            return client.add_record(
                zone=zone,
                domain=domain,
                type=type,
                ttl=ttl,
                overwrite=overwrite,
                node=node,
                **kwargs,
            )
        if action == "get_records":
            return client.get_records(**kwargs)
        if action == "update_record":
            zone = kwargs.pop("zone")
            domain = kwargs.pop("domain")
            type = kwargs.pop("type")
            ttl = kwargs.pop("ttl", None)
            if ttl is not None:
                ttl = int(ttl)
            node = kwargs.pop("node", None)
            return client.update_record(
                zone=zone,
                domain=domain,
                type=type,
                ttl=ttl,
                node=node,
                **kwargs,
            )
        if action == "delete_record":
            zone = kwargs.pop("zone")
            domain = kwargs.pop("domain")
            type = kwargs.pop("type")
            node = kwargs.pop("node", None)
            return client.delete_record(
                zone=zone,
                domain=domain,
                type=type,
                node=node,
                **kwargs,
            )

        raise ValueError(f"Unknown Zones action: {action}")
