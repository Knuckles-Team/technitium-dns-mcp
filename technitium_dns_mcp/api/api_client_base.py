from typing import Any
from urllib.parse import urljoin

import requests
import urllib3


class ApiClientBase:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        verify: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session = requests.Session()
        self._session.verify = verify

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})

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

        # Merge token as query param / form param if not in header to ensure backward compatibility
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
            raise Exception(f"API error: {response.status_code} - {response.text}")

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
