import base64
from collections.abc import Callable
from typing import Any
from urllib.parse import urljoin

import requests
from scion_sdk.tls.profile import ResolvedTLSProfile
from scion_sdk.tls.resolve import resolve_tls_profile


def destructive[F: Callable[..., Any]](method: F) -> F:
    """Mark an operation destructive: the served tool takes ``confirm`` and asks first."""
    method.__http_method__ = "DELETE"  # type: ignore[attr-defined]
    return method


class ApiClientBase:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.tls_profile = tls_profile or resolve_tls_profile("technitium_dns")
        self._session = self.tls_profile.configure_requests_session(requests.Session())

        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})

    def close(self) -> None:
        """Release transport resources and runtime-only TLS material."""
        self._session.close()
        self.tls_profile.cleanup()

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        files: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        req_headers = {}
        if headers:
            req_headers.update(headers)

        # Technitium's native API accepts the token in query/form parameters.
        if self.token:
            if method.upper() == "GET":
                if params is None:
                    params = {}
                if "token" not in params:
                    params["token"] = self.token
            else:
                if data is None:
                    data = {}
                if isinstance(data, dict) and "token" not in data:
                    data["token"] = self.token

        try:
            response = self._session.request(
                method=method,
                url=url,
                headers=req_headers,
                params=params,
                data=data,
                files=files,
            )
        except Exception as error:
            error_type = type(error)
        else:
            return self._read_response(response)

        # Raised outside the handler, not re-raised from inside the except
        # block: the request URL carries the configured bearer token in GET
        # query parameters, and transport-level failures (connection/timeout/
        # TLS errors) embed the full URL -- and therefore the token -- in
        # their message. This is the one chokepoint every endpoint across
        # every tool domain (user, zones, dashboard, ...) shares, so fixing
        # it here, rather than per call site, is what keeps the token out of
        # MCP's error formatter and server logging everywhere, not only on
        # the user-domain calls that separately re-sanitize their response
        # bodies in `_user_response.py`.
        raise error_type(f"{error_type.__name__} during {method} {endpoint}")

    def _read_response(self, response: Any) -> Any:
        if response.status_code >= 400:
            raise Exception(f"API error: {response.status_code}")

        # Check if the response is file export / download (not JSON)
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            # Could be a file download or raw text (e.g. zone export or prometheus metrics)
            if response.status_code == 204 or not response.text.strip():
                return {"status": "ok"}
            return {"status": "ok", "text": response.text}

        try:
            return response.json()
        except Exception:
            return {"status": "ok", "text": response.text}

    @staticmethod
    def _fields(**values: Any) -> dict[str, str]:
        """Form fields for an API call: drop ``None``, spell booleans and join lists.

        Keys are the API's own camelCase names.
        """
        out: dict[str, str] = {}
        for key, value in values.items():
            if value is None:
                continue
            if isinstance(value, bool):
                out[key] = str(value).lower()
            elif isinstance(value, list | tuple):
                out[key] = ",".join(str(v) for v in value)
            else:
                out[key] = str(value)
        return out

    def request_binary(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> dict[str, Any]:
        """Call an endpoint that returns a file; the body comes back base64 encoded."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        if self.token:
            if method.upper() == "GET":
                params = {**(params or {}), "token": self.token}
            else:
                data = {**(data or {}), "token": self.token}
        try:
            response = self._session.request(
                method=method, url=url, params=params, data=data
            )
        except Exception as error:
            error_type = type(error)
        else:
            if response.status_code >= 400:
                raise Exception(f"API error: {response.status_code}")
            return {
                "status": "ok",
                "content_type": response.headers.get("Content-Type", ""),
                "size": len(response.content),
                "content_base64": base64.b64encode(response.content).decode("ascii"),
            }
        raise error_type(f"{error_type.__name__} during {method} {endpoint}")
