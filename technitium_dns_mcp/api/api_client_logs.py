from typing import Any

from technitium_dns_mcp.api.api_client_base import ApiClientBase, destructive


class ApiClientLogs(ApiClientBase):
    def list_logs(self, node: str | None = None) -> dict[str, Any]:
        """Lists the server log files.

        Args:
            node: Target cluster node.
        """
        return self.request("GET", "/api/logs/list", params=self._fields(node=node))

    def download_log(
        self,
        file_name: str,
        limit: int | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Reads one server log file as text.

        Args:
            file_name: Log file name from `list_logs`.
            limit: Most megabytes to read from the end of the file.
            node: Target cluster node.
        """
        return self.request(
            "GET",
            "/api/logs/download",
            params=self._fields(fileName=file_name, limit=limit, node=node),
        )

    @destructive
    def delete_log(self, log: str, node: str | None = None) -> dict[str, Any]:
        """Deletes one server log file.

        Args:
            log: Log file name from `list_logs`.
            node: Target cluster node.
        """
        return self.request(
            "POST", "/api/logs/delete", data=self._fields(log=log, node=node)
        )

    @destructive
    def delete_all_logs(self, node: str | None = None) -> dict[str, Any]:
        """Deletes every server log file.

        Args:
            node: Target cluster node.
        """
        return self.request("POST", "/api/logs/deleteAll", data=self._fields(node=node))

    def query_logs(
        self,
        name: str,
        class_path: str,
        page_number: int | None = None,
        entries_per_page: int | None = None,
        descending_order: bool | None = None,
        start: str | None = None,
        end: str | None = None,
        client_ip_address: str | None = None,
        protocol: str | None = None,
        response_type: str | None = None,
        rcode: str | None = None,
        qname: str | None = None,
        qtype: str | None = None,
        qclass: str | None = None,
        node: str | None = None,
    ) -> dict[str, Any]:
        """Searches the query log kept by a query-logging app.

        Args:
            name: Installed app name that stores query logs.
            class_path: Class path of that app's logger.
            page_number: Page to return.
            entries_per_page: Entries per page.
            descending_order: Newest first.
            start: Start date-time (ISO 8601).
            end: End date-time (ISO 8601).
            client_ip_address: Only this client.
            protocol: Only this transport: Udp, Tcp, Tls, Https or Quic.
            response_type: Only this response type: Authoritative, Recursive, Cached, Blocked and so on.
            rcode: Only this response code.
            qname: Only this query name.
            qtype: Only this query type.
            qclass: Only this query class.
            node: Target cluster node.
        """
        return self.request(
            "GET",
            "/api/logs/query",
            params=self._fields(
                name=name,
                classPath=class_path,
                pageNumber=page_number,
                entriesPerPage=entries_per_page,
                descendingOrder=descending_order,
                start=start,
                end=end,
                clientIpAddress=client_ip_address,
                protocol=protocol,
                responseType=response_type,
                rcode=rcode,
                qname=qname,
                qtype=qtype,
                qclass=qclass,
                node=node,
            ),
        )
