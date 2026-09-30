from collections.abc import Callable
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
    if not isinstance(response, dict):
        return {"error": "Unexpected user API response"}
    return _sanitize_user_response(response)


def _safe_user_request(
    request: Callable[..., Any], method: str, endpoint: str, **kwargs: Any
) -> dict[str, Any]:
    try:
        response = request(method, endpoint, **kwargs)
    except Exception as error:
        error_type = type(error).__name__
    else:
        return _safe_user_response(response)

    # Raise outside the handler so no original exception, URL, or body remains
    # attached as a cause/context for MCP's error formatter or server logging.
    raise RuntimeError(f"User API request failed ({error_type}; {method} {endpoint})")
