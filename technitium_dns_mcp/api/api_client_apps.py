from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase, destructive


class ApiClientApps(ApiClientBase):
    def list_apps(self, node: str | None = None) -> dict[str, Any]:
        """Lists installed DNS apps.

        Args:
            node: Target cluster node.
        """
        return self.request("GET", "/api/apps/list", params=self._fields(node=node))

    def list_store_apps(self, node: str | None = None) -> dict[str, Any]:
        """Lists DNS apps available from the app store.

        Args:
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/apps/listStoreApps", params=self._fields(node=node)
        )

    def download_and_install_app(
        self, name: str, url: str, node: str | None = None
    ) -> dict[str, Any]:
        """Downloads an app zip and installs it.

        Args:
            name: App name.
            url: Download URL of the app zip.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/apps/downloadAndInstall",
            data=self._fields(name=name, url=url, node=node),
        )

    def download_and_update_app(
        self, name: str, url: str, node: str | None = None
    ) -> dict[str, Any]:
        """Downloads a newer app zip and updates the installed app.

        Args:
            name: App name.
            url: Download URL of the app zip.
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/apps/downloadAndUpdate",
            data=self._fields(name=name, url=url, node=node),
        )

    @destructive
    def uninstall_app(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Uninstalls a DNS app and deletes its configuration.

        Args:
            name: App name.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/apps/uninstall", data=self._fields(name=name, node=node)
        )

    def get_app_config(self, name: str, node: str | None = None) -> dict[str, Any]:
        """Reads an app's configuration file.

        Args:
            name: App name.
            node: Target cluster node.
        """
        return self.request(
            "GET", "/api/apps/config/get", params=self._fields(name=name, node=node)
        )

    def set_app_config(
        self, name: str, config: str, node: str | None = None
    ) -> dict[str, Any]:
        """Replaces an app's configuration file.

        Args:
            name: App name.
            config: Full configuration text (usually JSON).
            node: Target cluster node.
        """
        return self.request(
            "POST",
            "/api/apps/config/set",
            data=self._fields(name=name, config=config, node=node),
        )
