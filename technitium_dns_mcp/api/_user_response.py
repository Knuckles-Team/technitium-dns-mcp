"""Sanitized results for credential-bearing user operations."""

from typing import Any

# Credential-bearing fields in user/session and 2FA responses. Keep identifiers
# such as partialToken and tokenName: they are needed to manage sessions.
_SECRET_FIELDS = frozenset(
    {
        "token",
        "accesstoken",
        "refreshtoken",
        "sessiontoken",
        "singleusetoken",
        "password",
        "pass",
        "newpassword",
        "newpass",
        "totp",
        "secret",
        "qrcodepngimage",
        "provisioninguri",
        "recoverycodes",
        # ApiClientBase uses text for non-JSON and malformed JSON responses.
        "text",
    }
)


def _sanitize_user_response(value: Any) -> Any:
    """Copy a user response without credential fields, including nested objects."""
    if isinstance(value, dict):
        return {
            key: _sanitize_user_response(item)
            for key, item in value.items()
            if key.lower().replace("_", "").replace("-", "") not in _SECRET_FIELDS
        }
    if isinstance(value, list):
        return [_sanitize_user_response(item) for item in value]
    return value


def _safe_user_response(response: Any) -> dict[str, Any]:
    """Fail closed for an unexpected top-level JSON shape; never echo its body."""
    if not isinstance(response, dict):
        return {"error": "Unexpected user API response"}
    return _sanitize_user_response(response)
