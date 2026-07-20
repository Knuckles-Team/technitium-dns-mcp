from typing import Any
from urllib.parse import urljoin

import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)


class ApiClientBase:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.tls_profile = tls_profile or resolve_configured_tls_profile(
            "technitium_dns"
        )
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

        response = self._session.request(
            method=method,
            url=url,
            headers=req_headers,
            params=params,
            data=data,
            files=files,
        )

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
