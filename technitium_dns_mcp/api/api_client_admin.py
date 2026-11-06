from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase, destructive

_SECRET = frozenset({"token", "password", "pass", "newpassword", "totp", "secret"})


def _no_credentials(value: Any) -> Any:
    """Drop token and password fields; keep partial tokens, which name sessions."""
    if isinstance(value, dict):
        return {
            k: _no_credentials(v)
            for k, v in value.items()
            if k.lower().replace("_", "") not in _SECRET
        }
    if isinstance(value, list):
        return [_no_credentials(v) for v in value]
    return value


class ApiClientAdmin(ApiClientBase):
    def list_admin_sessions(self) -> dict[str, Any]:
        """Lists the active sessions of every user."""
        return _no_credentials(self.request("GET", "/api/admin/sessions/list"))

    def create_api_token(self, user: str, token_name: str) -> dict[str, Any]:
        """Creates a non-expiring API token for a user. The token is returned once.

        Args:
            user: User name.
            token_name: Name to label the token.
        """
        return self.request(
            "POST",
            "/api/admin/sessions/createToken",
            data=self._fields(user=user, tokenName=token_name),
        )

    @destructive
    def delete_admin_session(self, partial_token: str) -> dict[str, Any]:
        """Ends a session of any user.

        Args:
            partial_token: Partial token from `list_admin_sessions`.
        """
        return self.request(
            "POST",
            "/api/admin/sessions/delete",
            data=self._fields(partialToken=partial_token),
        )

    def list_users(self) -> dict[str, Any]:
        """Lists administrator users."""
        return _no_credentials(self.request("GET", "/api/admin/users/list"))

    def create_user(
        self, user: str, password: str, display_name: str | None = None
    ) -> dict[str, Any]:
        """Creates an administrator user.

        Args:
            user: User name.
            password: Initial password.
            display_name: Display name.
        """
        return _no_credentials(
            self.request(
                "POST",
                "/api/admin/users/create",
                data={
                    **self._fields(user=user, displayName=display_name),
                    "pass": password,
                },
            )
        )

    def get_user(self, user: str, include_groups: bool | None = None) -> dict[str, Any]:
        """Reads one user with their sessions and group memberships.

        Args:
            user: User name.
            include_groups: Also list all groups.
        """
        return _no_credentials(
            self.request(
                "GET",
                "/api/admin/users/get",
                params=self._fields(user=user, includeGroups=include_groups),
            )
        )

    def set_user(
        self,
        user: str,
        display_name: str | None = None,
        new_user: str | None = None,
        disabled: bool | None = None,
        session_timeout_seconds: int | None = None,
        new_password: str | None = None,
        iterations: int | None = None,
        member_of_groups: list[str] | None = None,
    ) -> dict[str, Any]:
        """Changes a user. Only the fields given change.

        Args:
            user: User name.
            display_name: Display name.
            new_user: New user name.
            disabled: Disable or enable the account.
            session_timeout_seconds: Session timeout.
            new_password: New password.
            iterations: Password hash iterations.
            member_of_groups: Full group membership list.
        """
        data = self._fields(
            user=user,
            displayName=display_name,
            newUser=new_user,
            disabled=disabled,
            sessionTimeoutSeconds=session_timeout_seconds,
            iterations=iterations,
            memberOfGroups=member_of_groups,
        )
        if new_password is not None:
            data["newPass"] = new_password
        return _no_credentials(self.request("POST", "/api/admin/users/set", data=data))

    @destructive
    def delete_user(self, user: str) -> dict[str, Any]:
        """Deletes a user and their sessions.

        Args:
            user: User name.
        """
        return self.request(
            "POST", "/api/admin/users/delete", data=self._fields(user=user)
        )

    def list_groups(self) -> dict[str, Any]:
        """Lists user groups."""
        return self.request("GET", "/api/admin/groups/list")

    def create_group(
        self, group: str, description: str | None = None
    ) -> dict[str, Any]:
        """Creates a user group.

        Args:
            group: Group name.
            description: Free text.
        """
        return self.request(
            "POST",
            "/api/admin/groups/create",
            data=self._fields(group=group, description=description),
        )

    def get_group(
        self, group: str, include_users: bool | None = None
    ) -> dict[str, Any]:
        """Reads one group with its members.

        Args:
            group: Group name.
            include_users: Also list all users.
        """
        return self.request(
            "GET",
            "/api/admin/groups/get",
            params=self._fields(group=group, includeUsers=include_users),
        )

    def set_group(
        self,
        group: str,
        new_group: str | None = None,
        description: str | None = None,
        members: list[str] | None = None,
    ) -> dict[str, Any]:
        """Changes a group. Only the fields given change.

        Args:
            group: Group name.
            new_group: New group name.
            description: Free text.
            members: Full member list.
        """
        return self.request(
            "POST",
            "/api/admin/groups/set",
            data=self._fields(
                group=group,
                newGroup=new_group,
                description=description,
                members=members,
            ),
        )

    @destructive
    def delete_group(self, group: str) -> dict[str, Any]:
        """Deletes a group.

        Args:
            group: Group name.
        """
        return self.request(
            "POST", "/api/admin/groups/delete", data=self._fields(group=group)
        )

    def list_permissions(self) -> dict[str, Any]:
        """Lists the permission sections and the access each user and group has."""
        return self.request("GET", "/api/admin/permissions/list")

    def get_permissions(
        self, section: str, include_users_and_groups: bool | None = None
    ) -> dict[str, Any]:
        """Reads the permissions of one section.

        Args:
            section: Section name, for example Zones, Cache, Settings or Administration.
            include_users_and_groups: Also list all users and groups.
        """
        return self.request(
            "GET",
            "/api/admin/permissions/get",
            params=self._fields(
                section=section, includeUsersAndGroups=include_users_and_groups
            ),
        )

    def set_permissions(
        self,
        section: str,
        user_permissions: str | None = None,
        group_permissions: str | None = None,
    ) -> dict[str, Any]:
        """Sets the permissions of one section.

        Args:
            section: Section name.
            user_permissions: `user|canView|canModify|canDelete` entries joined by `|`.
            group_permissions: `group|canView|canModify|canDelete` entries joined by `|`.
        """
        return self.request(
            "POST",
            "/api/admin/permissions/set",
            data=self._fields(
                section=section,
                userPermissions=user_permissions,
                groupPermissions=group_permissions,
            ),
        )
