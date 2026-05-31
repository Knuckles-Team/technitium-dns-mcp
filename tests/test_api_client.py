import pytest
from unittest.mock import MagicMock, patch
from technitium_dns_mcp.api_client import Api


@pytest.mark.concept("TDNS-001")
def test_api_client_user_endpoints():
    client = Api(base_url="http://localhost:5380", token="test-token")

    with patch.object(client._session, "request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.text = '{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}
        mock_request.return_value = mock_response

        # Test get_sso_status
        client.get_sso_status()
        _, kwargs = mock_request.call_args
        assert kwargs["method"] == "GET"
        assert "/api/sso/status" in kwargs["url"]

        # Test login
        client.login(
            user="admin", password="password", totp="123456", include_info=True
        )
        _, kwargs = mock_request.call_args
        assert kwargs["method"] == "POST"
        assert "/api/user/login" in kwargs["url"]
        assert kwargs["data"]["user"] == "admin"
        assert kwargs["data"]["pass"] == "password"
        assert kwargs["data"]["totp"] == "123456"
        assert kwargs["data"]["includeInfo"] == "true"

        # Test create_token
        client.create_token(
            user="admin", password="password", token_name="my-token", totp="123456"
        )
        _, kwargs = mock_request.call_args
        assert kwargs["method"] == "POST"
        assert "/api/user/createToken" in kwargs["url"]
        assert kwargs["data"]["tokenName"] == "my-token"

        # Test create_single_use_token
        client.create_single_use_token()
        _, kwargs = mock_request.call_args
        assert "/api/user/createSingleUseToken" in kwargs["url"]

        # Test logout
        client.logout()
        _, kwargs = mock_request.call_args
        assert "/api/user/logout" in kwargs["url"]

        # Test get_session_info
        client.get_session_info()
        _, kwargs = mock_request.call_args
        assert "/api/user/session/get" in kwargs["url"]

        # Test delete_user_session
        client.delete_user_session(partial_token="part")
        _, kwargs = mock_request.call_args
        assert "/api/user/session/delete" in kwargs["url"]
        assert kwargs["data"]["partialToken"] == "part"

        # Test change_password
        client.change_password(
            password="old", new_password="new", totp="123", iterations=1000
        )
        _, kwargs = mock_request.call_args
        assert "/api/user/changePassword" in kwargs["url"]
        assert kwargs["data"]["pass"] == "old"
        assert kwargs["data"]["newPass"] == "new"
        assert kwargs["data"]["iterations"] == "1000"

        # Test initialize_2fa
        client.initialize_2fa()
        _, kwargs = mock_request.call_args
        assert "/api/user/2fa/init" in kwargs["url"]

        # Test enable_2fa
        client.enable_2fa(totp="123456")
        _, kwargs = mock_request.call_args
        assert "/api/user/2fa/enable" in kwargs["url"]
        assert kwargs["data"]["totp"] == "123456"

        # Test disable_2fa
        client.disable_2fa()
        _, kwargs = mock_request.call_args
        assert "/api/user/2fa/disable" in kwargs["url"]

        # Test get_user_profile_details
        client.get_user_profile_details()
        _, kwargs = mock_request.call_args
        assert "/api/user/profile/get" in kwargs["url"]

        # Test set_user_profile_details
        client.set_user_profile_details(
            display_name="User", session_timeout_seconds=3600
        )
        _, kwargs = mock_request.call_args
        assert "/api/user/profile/set" in kwargs["url"]
        assert kwargs["data"]["displayName"] == "User"
        assert kwargs["data"]["sessionTimeoutSeconds"] == "3600"

        # Test check_for_update
        client.check_for_update()
        _, kwargs = mock_request.call_args
        assert "/api/user/checkForUpdate" in kwargs["url"]


@pytest.mark.concept("TDNS-001")
def test_api_client_dashboard_endpoints():
    client = Api(base_url="http://localhost:5380", token="test-token")

    with patch.object(client._session, "request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.text = '{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}
        mock_request.return_value = mock_response

        # Test get_metrics_json
        client.get_metrics_json()
        _, kwargs = mock_request.call_args
        assert "/api/dashboard/metrics/json" in kwargs["url"]

        # Test get_metrics_text
        client.get_metrics_text()
        _, kwargs = mock_request.call_args
        assert "/api/dashboard/metrics/text" in kwargs["url"]

        # Test get_stats
        client.get_stats(
            node="node1",
            stats_type="day",
            utc=True,
            dont_trim_query_type_data=False,
            start="start",
            end="end",
        )
        _, kwargs = mock_request.call_args
        assert "/api/dashboard/stats/get" in kwargs["url"]
        assert kwargs["params"]["node"] == "node1"
        assert kwargs["params"]["type"] == "day"
        assert kwargs["params"]["utc"] == "true"
        assert kwargs["params"]["dontTrimQueryTypeData"] == "false"

        # Test get_top_stats
        client.get_top_stats(
            node="node1",
            stats_type="hour",
            start="s",
            end="e",
            stats_category="clients",
            limit=10,
            no_reverse_lookup=True,
            only_rate_limited_clients=False,
        )
        _, kwargs = mock_request.call_args
        assert "/api/dashboard/stats/getTop" in kwargs["url"]
        assert kwargs["params"]["statsType"] == "clients"
        assert kwargs["params"]["limit"] == "10"
        assert kwargs["params"]["noReverseLookup"] == "true"

        # Test delete_all_stats
        client.delete_all_stats(node="node1")
        _, kwargs = mock_request.call_args
        assert "/api/dashboard/stats/deleteAll" in kwargs["url"]
        assert kwargs["data"]["node"] == "node1"


@pytest.mark.concept("TDNS-001")
def test_api_client_zones_endpoints():
    client = Api(base_url="http://localhost:5380", token="test-token")

    with patch.object(client._session, "request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.text = '{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}
        mock_request.return_value = mock_response

        # Test list_zones
        client.list_zones(node="n1", page_number=2, zones_per_page=50)
        _, kwargs = mock_request.call_args
        assert "/api/zones/list" in kwargs["url"]
        assert kwargs["params"]["node"] == "n1"
        assert kwargs["params"]["pageNumber"] == "2"
        assert kwargs["params"]["zonesPerPage"] == "50"

        # Test list_catalog_zones
        client.list_catalog_zones(node="n1")
        _, kwargs = mock_request.call_args
        assert "/api/zones/catalogs/list" in kwargs["url"]

        # Test create_zone
        client.create_zone(zone="example.com", type="Primary", node="n1", catalog="cat")
        _, kwargs = mock_request.call_args
        assert "/api/zones/create" in kwargs["url"]
        assert kwargs["data"]["zone"] == "example.com"
        assert kwargs["data"]["type"] == "Primary"

        # Test import_zone
        client.import_zone(zone="example.com", overwrite=True, file_content="zone data")
        _, kwargs = mock_request.call_args
        assert "/api/zones/import" in kwargs["url"]
        assert kwargs["data"]["zone"] == "example.com"
        assert kwargs["data"]["overwrite"] == "true"
        assert kwargs["files"] is not None

        # Test export_zone
        client.export_zone(zone="example.com")
        _, kwargs = mock_request.call_args
        assert "/api/zones/export" in kwargs["url"]
        assert kwargs["params"]["zone"] == "example.com"

        # Test clone_zone
        client.clone_zone(zone="example.com", source_zone="source.com")
        _, kwargs = mock_request.call_args
        assert "/api/zones/clone" in kwargs["url"]

        # Test convert_zone_type
        client.convert_zone_type(zone="example.com", type="Secondary")
        _, kwargs = mock_request.call_args
        assert "/api/zones/convert" in kwargs["url"]

        # Test enable_zone / disable_zone / delete_zone / resync_zone
        client.enable_zone(zone="example.com")
        assert "/api/zones/enable" in mock_request.call_args[1]["url"]

        client.disable_zone(zone="example.com")
        assert "/api/zones/disable" in mock_request.call_args[1]["url"]

        client.delete_zone(zone="example.com")
        assert "/api/zones/delete" in mock_request.call_args[1]["url"]

        client.resync_zone(zone="example.com")
        assert "/api/zones/resync" in mock_request.call_args[1]["url"]

        # Test get_zone_options / set_zone_options
        client.get_zone_options(
            zone="example.com", include_available_catalog_zone_names=True
        )
        _, kwargs = mock_request.call_args
        assert "/api/zones/options/get" in kwargs["url"]
        assert kwargs["params"]["includeAvailableCatalogZoneNames"] == "true"

        client.set_zone_options(zone="example.com", disabled=True, catalog="new-cat")
        _, kwargs = mock_request.call_args
        assert "/api/zones/options/set" in kwargs["url"]
        assert kwargs["data"]["disabled"] == "true"
        assert kwargs["data"]["catalog"] == "new-cat"

        # Test get_zone_permissions / set_zone_permissions
        client.get_zone_permissions(zone="example.com", include_users_and_groups=True)
        _, kwargs = mock_request.call_args
        assert "/api/zones/permissions/get" in kwargs["url"]

        client.set_zone_permissions(zone="example.com", user_permissions="user1:read")
        _, kwargs = mock_request.call_args
        assert "/api/zones/permissions/set" in kwargs["url"]

        # Test sign_zone / unsign_zone
        client.sign_zone(zone="example.com", algorithm="ECDSAP256SHA256")
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/sign" in kwargs["url"]

        client.unsign_zone(zone="example.com")
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/unsign" in kwargs["url"]

        # Test get_ds_info
        client.get_ds_info(zone="example.com")
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/viewDS" in kwargs["url"]

        # Test get_dnssec_properties
        client.get_dnssec_properties(zone="example.com")
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/properties/get" in kwargs["url"]

        # Test convert_to_nsec / convert_to_nsec3
        client.convert_to_nsec(zone="example.com")
        assert (
            "/api/zones/dnssec/properties/convertToNSEC"
            in mock_request.call_args[1]["url"]
        )

        client.convert_to_nsec3(zone="example.com")
        assert (
            "/api/zones/dnssec/properties/convertToNSEC3"
            in mock_request.call_args[1]["url"]
        )

        # Test update_nsec3_params
        client.update_nsec3_params(zone="example.com", iterations=10, salt_length=8)
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/properties/updateNSEC3Params" in kwargs["url"]
        assert kwargs["data"]["iterations"] == "10"

        # Test update_dnskey_ttl
        client.update_dnskey_ttl(zone="example.com", ttl=3600)
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/properties/updateDnsKeyTtl" in kwargs["url"]

        # Test add_private_key / update_private_key / delete_private_key
        client.add_private_key(zone="example.com", key_type="Ksk", rollover_days=30)
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/properties/addPrivateKey" in kwargs["url"]

        client.update_private_key(zone="example.com", key_tag=1234, rollover_days=60)
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/properties/updatePrivateKey" in kwargs["url"]

        client.delete_private_key(zone="example.com", key_tag=1234)
        _, kwargs = mock_request.call_args
        assert "/api/zones/dnssec/properties/deletePrivateKey" in kwargs["url"]

        # Test publish_all_private_keys / rollover_dnskey / retire_dnskey
        client.publish_all_private_keys(zone="example.com")
        assert (
            "/api/zones/dnssec/properties/publishAllPrivateKeys"
            in mock_request.call_args[1]["url"]
        )

        client.rollover_dnskey(zone="example.com", key_tag=123)
        assert (
            "/api/zones/dnssec/properties/rolloverDnsKey"
            in mock_request.call_args[1]["url"]
        )

        client.retire_dnskey(zone="example.com", key_tag=123)
        assert (
            "/api/zones/dnssec/properties/retireDnsKey"
            in mock_request.call_args[1]["url"]
        )

        # Test add_record
        client.add_record(
            zone="example.com",
            domain="www.example.com",
            type="A",
            ttl=3600,
            overwrite=True,
            ipAddress="1.2.3.4",
        )
        _, kwargs = mock_request.call_args
        assert "/api/zones/records/add" in kwargs["url"]
        assert kwargs["data"]["ipAddress"] == "1.2.3.4"

        # Test get_records
        client.get_records(domain="www.example.com", zone="example.com", list_zone=True)
        _, kwargs = mock_request.call_args
        assert "/api/zones/records/get" in kwargs["url"]
        assert kwargs["params"]["listZone"] == "true"

        # Test update_record
        client.update_record(
            zone="example.com",
            domain="www.example.com",
            type="A",
            ttl=1800,
            ipAddress="5.6.7.8",
        )
        _, kwargs = mock_request.call_args
        assert "/api/zones/records/update" in kwargs["url"]
        assert kwargs["data"]["ipAddress"] == "5.6.7.8"

        # Test delete_record
        client.delete_record(
            zone="example.com", domain="www.example.com", type="A", ipAddress="5.6.7.8"
        )
        _, kwargs = mock_request.call_args
        assert "/api/zones/records/delete" in kwargs["url"]
        assert kwargs["data"]["ipAddress"] == "5.6.7.8"
