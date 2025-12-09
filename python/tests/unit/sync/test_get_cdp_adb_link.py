# -*- coding: utf-8 -*-
"""
Unit tests for GetCdpLink and GetAdbLink API methods
"""
from unittest.mock import MagicMock, MagicMock, Mock, patch

import pytest
from alibabacloud_tea_openapi import utils_models as open_api_util_models

from agentbay.api import models
from agentbay.api.client import Client


class TestGetCdpLink:
    """Test GetCdpLink API"""

    @pytest.fixture
    def client(self):
        """Create a test client"""
        config = open_api_util_models.Config(
            access_key_id="test_key",
            access_key_secret="test_secret",
            endpoint="test.endpoint.com",
        )
        return Client(config)

    @pytest.mark.sync


    def test_get_cdp_link_success(self, client):
        """Test get_cdp_link with successful response"""
        # Prepare mock response
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 200,
            "body": {
                "Code": "200",
                "Success": True,
                "RequestId": "test-request-id",
                "Message": "Success",
                "HttpStatusCode": 200,
                "Data": {"Url": "ws://test-cdp-url:9222"},
            },
        }

        # Mock the do_rpcrequest method
        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            request = models.GetCdpLinkRequest(
                authorization="test-auth-token", session_id="test-session-id"
            )
            response = client.get_cdp_link(request)

            # Assertions
            assert response is not None
            assert response.status_code == 200
            assert response.body is not None
            assert response.body.success is True
            assert response.body.data is not None
            assert response.body.data.url == "ws://test-cdp-url:9222"

    @pytest.mark.sync


    def test_get_cdp_link_with_options(self, client):
        """Test get_cdp_link_with_options"""
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 200,
            "body": {
                "Code": "200",
                "Success": True,
                "RequestId": "test-request-id",
                "Data": {"Url": "ws://test-cdp-url:9222"},
            },
        }

        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            from darabonba.runtime import RuntimeOptions

            request = models.GetCdpLinkRequest(
                authorization="test-auth-token", session_id="test-session-id"
            )
            runtime = RuntimeOptions()
            response = client.get_cdp_link_with_options(request, runtime)

            assert response is not None
            assert response.status_code == 200
            assert response.body.data.url == "ws://test-cdp-url:9222"

    @pytest.mark.sync
    @pytest.mark.sync

    def test_get_cdp_link_async(self, client):
        """Test get_cdp_link_async"""
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 200,
            "body": {
                "Code": "200",
                "Success": True,
                "RequestId": "test-request-id",
                "Data": {"Url": "ws://test-cdp-url:9222"},
            },
        }

        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            request = models.GetCdpLinkRequest(
                authorization="test-auth-token", session_id="test-session-id"
            )
            response = client.get_cdp_link(request)

            assert response is not None
            assert response.status_code == 200
            assert response.body.data.url == "ws://test-cdp-url:9222"

    @pytest.mark.sync


    def test_get_cdp_link_failure(self, client):
        """Test get_cdp_link with failed response"""
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 400,
            "body": {
                "Code": "400",
                "Success": False,
                "RequestId": "test-request-id",
                "Message": "Invalid session",
                "HttpStatusCode": 400,
                "Data": None,
            },
        }

        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            request = models.GetCdpLinkRequest(
                authorization="test-auth-token", session_id="invalid-session"
            )
            response = client.get_cdp_link(request)

            assert response is not None
            assert response.status_code == 400
            assert response.body.success is False
            assert response.body.message == "Invalid session"


class TestGetAdbLink:
    """Test GetAdbLink API"""

    @pytest.fixture
    def client(self):
        """Create a test client"""
        config = open_api_util_models.Config(
            access_key_id="test_key",
            access_key_secret="test_secret",
            endpoint="test.endpoint.com",
        )
        return Client(config)

    @pytest.mark.sync


    def test_get_adb_link_success(self, client):
        """Test get_adb_link with successful response"""
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 200,
            "body": {
                "Code": "200",
                "Success": True,
                "RequestId": "test-request-id",
                "Message": "Success",
                "HttpStatusCode": 200,
                "Data": {"Url": "adb://test-adb-url:5555"},
            },
        }

        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            import json

            options = json.dumps({"adbkey_pub": "test-public-key"})
            request = models.GetAdbLinkRequest(
                authorization="test-auth-token",
                session_id="test-session-id",
                option=options,
            )
            response = client.get_adb_link(request)

            assert response is not None
            assert response.status_code == 200
            assert response.body is not None
            assert response.body.success is True
            assert response.body.data is not None
            assert response.body.data.url == "adb://test-adb-url:5555"

    @pytest.mark.sync


    def test_get_adb_link_with_options(self, client):
        """Test get_adb_link_with_options"""
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 200,
            "body": {
                "Code": "200",
                "Success": True,
                "RequestId": "test-request-id",
                "Data": {"Url": "adb://test-adb-url:5555"},
            },
        }

        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            import json

            from darabonba.runtime import RuntimeOptions

            options = json.dumps({"adbkey_pub": "test-public-key"})
            request = models.GetAdbLinkRequest(
                authorization="test-auth-token",
                session_id="test-session-id",
                option=options,
            )
            runtime = RuntimeOptions()
            response = client.get_adb_link_with_options(request, runtime)

            assert response is not None
            assert response.status_code == 200
            assert response.body.data.url == "adb://test-adb-url:5555"

    @pytest.mark.sync
    @pytest.mark.sync

    def test_get_adb_link_async(self, client):
        """Test get_adb_link_async"""
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 200,
            "body": {
                "Code": "200",
                "Success": True,
                "RequestId": "test-request-id",
                "Data": {"Url": "adb://test-adb-url:5555"},
            },
        }

        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            import json

            options = json.dumps({"adbkey_pub": "test-public-key"})
            request = models.GetAdbLinkRequest(
                authorization="test-auth-token",
                session_id="test-session-id",
                option=options,
            )
            response = client.get_adb_link(request)

            assert response is not None
            assert response.status_code == 200
            assert response.body.data.url == "adb://test-adb-url:5555"

    @pytest.mark.sync


    def test_get_adb_link_failure(self, client):
        """Test get_adb_link with failed response"""
        mock_response = {
            "headers": {"x-request-id": "test-request-id"},
            "statusCode": 400,
            "body": {
                "Code": "400",
                "Success": False,
                "RequestId": "test-request-id",
                "Message": "Invalid session",
                "HttpStatusCode": 400,
                "Data": None,
            },
        }

        with patch.object(client, "do_rpcrequest", return_value=mock_response):
            request = models.GetAdbLinkRequest(
                authorization="test-auth-token",
                session_id="invalid-session",
                option="{}",
            )
            response = client.get_adb_link(request)

            assert response is not None
            assert response.status_code == 400
            assert response.body.success is False
            assert response.body.message == "Invalid session"
