from __future__ import annotations

from typing import Any, Optional
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

import pytest

from emt_madrid.domain.exceptions import AuthenticationError
from emt_madrid.infrastructure.emt_api_client import EMTAuthenticatedClient, HTTPClient
from tests.unit.infrastructure.fixtures.test_autenticate_fixture import (
    CREDENTIALS,
    LOGIN_OK_RESPONSE,
    USER_NOT_FOUND_RESPONSE,
    INVALID_PASSWORD_RESPONSE,
    LOGIN_EXPIRED_TOKEN_RESPONSE,
    API_LIMIT_EXCEEDED_RESPONSE,
    TOKEN,
)


class FakeHTTPClient(HTTPClient):
    """Fake HTTP client for testing purposes."""

    exchange: AsyncMock  # Explicitly declare the type for type checking

    def __init__(self, response: Optional[dict[str, Any]] = None) -> None:
        """Initialize with optional response dictionary."""
        super().__init__(config=MagicMock())
        self._response = response or {}
        self.exchange = AsyncMock(return_value=self._response)


class TestEMTAuthenticatedClient:
    """Test cases for EMTAuthenticatedClient class."""

    @pytest.mark.asyncio
    async def test_authenticate(self):
        """Test successful authentication with valid credentials."""
        http_client = FakeHTTPClient(LOGIN_OK_RESPONSE)
        emt_authenticated_client = EMTAuthenticatedClient(http_client, CREDENTIALS)  # type: ignore

        await emt_authenticated_client.authenticate()

        assert (
            emt_authenticated_client._token.token
            == LOGIN_OK_RESPONSE["data"][0]["accessToken"]
        )
        assert emt_authenticated_client._token.expires_at == datetime.fromtimestamp(
            LOGIN_OK_RESPONSE["data"][0]["tokenDteExpiration"]["$date"] / 1000
        )

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user raises AuthenticationError."""
        http_client = FakeHTTPClient(USER_NOT_FOUND_RESPONSE)
        emt_authenticated_client = EMTAuthenticatedClient(http_client, CREDENTIALS)  # type: ignore

        with pytest.raises(AuthenticationError):
            await emt_authenticated_client.authenticate()

    @pytest.mark.asyncio
    async def test_authenticate_invalid_password(self):
        """Test authentication with invalid password raises AuthenticationError."""
        http_client = FakeHTTPClient(INVALID_PASSWORD_RESPONSE)
        emt_authenticated_client = EMTAuthenticatedClient(http_client, CREDENTIALS)  # type: ignore

        with pytest.raises(AuthenticationError):
            await emt_authenticated_client.authenticate()

    @pytest.mark.asyncio
    async def test_authenticate_api_limit_exceeded(self):
        """Test authentication with API limit exceeded raises APILimitExceededError."""
        http_client = FakeHTTPClient(API_LIMIT_EXCEEDED_RESPONSE)
        emt_authenticated_client = EMTAuthenticatedClient(http_client, CREDENTIALS)

        with pytest.raises(AuthenticationError):
            await emt_authenticated_client.authenticate()

    @pytest.mark.asyncio
    async def test_exchange_success(self) -> None:
        """Test successful exchange with valid token."""
        login_http_client = FakeHTTPClient(LOGIN_OK_RESPONSE)
        emt_authenticated_client = EMTAuthenticatedClient(
            login_http_client, CREDENTIALS
        )
        await emt_authenticated_client.authenticate()

        # Reset and configure the mock for the exchange call
        login_http_client.exchange.reset_mock()
        login_http_client.exchange.configure_mock(return_value=LOGIN_OK_RESPONSE)

        response = await emt_authenticated_client.exchange("GET", "v1/test/endpoint")

        assert response == LOGIN_OK_RESPONSE
        login_http_client.exchange.assert_called_once_with(
            "GET", "v1/test/endpoint", None, None, {"accessToken": TOKEN}
        )

    @pytest.mark.asyncio
    async def test_exchange_with_authentication_retry(self) -> None:
        """Test exchange with token refresh on expired token."""
        login_http_client = FakeHTTPClient(LOGIN_OK_RESPONSE)
        emt_authenticated_client = EMTAuthenticatedClient(
            login_http_client, CREDENTIALS
        )

        auth_mock = AsyncMock()
        emt_authenticated_client.authenticate = auth_mock  # type: ignore[method-assign]

        login_http_client.exchange.side_effect = [  # type: ignore[attr-defined]
            LOGIN_EXPIRED_TOKEN_RESPONSE,
            LOGIN_OK_RESPONSE,
        ]

        await emt_authenticated_client.exchange("GET", "v1/test/endpoint")

        auth_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_exchange_with_expired_token(self) -> None:
        """Test API exchange with expired token refreshes authentication."""
        login_http_client = FakeHTTPClient(LOGIN_EXPIRED_TOKEN_RESPONSE)
        emt_authenticated_client = EMTAuthenticatedClient(
            login_http_client, CREDENTIALS
        )
        await emt_authenticated_client.authenticate()

        mock_authenticate = AsyncMock()
        emt_authenticated_client.authenticate = mock_authenticate  # type: ignore[method-assign]

        mock_exchange = AsyncMock(return_value=LOGIN_OK_RESPONSE)
        login_http_client.exchange = mock_exchange  # type: ignore[method-assign]

        await emt_authenticated_client.exchange(
            method="GET", params=None, data=None, endpoint="v1/test/endpoint"
        )

        mock_authenticate.assert_called_once()
