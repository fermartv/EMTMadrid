from datetime import datetime
from typing import Any, Dict, Optional, Union

from emt_madrid.infrastructure.emt_api_endpoints import Auth
from emt_madrid.infrastructure.http_client import HTTPClient
from emt_madrid.domain.exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    APILimitExceededError,
)


class Credentials:
    """Stores and validates user credentials for EMT API authentication.

    This class is responsible for holding the email and password required for
    authenticating with the EMT API and ensuring they are valid.

    Args:
        email: User's email address for authentication
        password: User's password for authentication

    Raises:
        InvalidCredentialsError: If either email or password is None
    """

    def __init__(self, email: str, password: str) -> None:
        """Initialize Credentials object."""
        self.email = email
        self.password = password
        self._verify()

    def _verify(self) -> None:
        """Verify that both email and password are provided and not empty."""
        if not self.email or not self.password:
            raise InvalidCredentialsError(
                "Email and password must be provided and cannot be empty"
            )


class Token:
    """Manages the authentication token and its expiration.

    This class handles the storage and validation of the authentication token
    used for API requests, including checking if the token has expired.
    """

    def __init__(self) -> None:
        """Initialize Token object."""
        self.token: Optional[str] = None
        self.expires_at: Optional[datetime] = None

    @property
    def is_expired(self) -> bool:
        """Check if the token has expired."""
        return self.expires_at is not None and self.expires_at < datetime.now()


class EMTAuthenticatedClient:
    """Client for making authenticated requests to the EMT API.

    This client handles authentication and token management, automatically
    refreshing tokens when they expire. It wraps an HTTP client to add
    authentication headers to all requests.

    Args:
        http_client: An instance of HTTPClient for making HTTP requests
        credentials: User credentials for authentication
    """

    def __init__(self, http_client: HTTPClient, credentials: Credentials) -> None:
        """Initialize EMTAuthenticatedClient object."""
        self._http_client: HTTPClient = http_client
        self._credentials: Credentials = credentials
        self._token: Token = Token()

    async def authenticate(self) -> None:
        """Authenticate with the EMT API using stored credentials.

        This method updates the authentication token by making a login request
        to the EMT API using the provided credentials.

        Raises:
            AuthenticationError: If authentication fails due to invalid credentials
            Exception: For any other authentication failures
        """
        Auth.LOGIN["headers"]["email"] = self._credentials.email
        Auth.LOGIN["headers"]["password"] = self._credentials.password

        try:
            response = await self._http_client.exchange(
                method=Auth.LOGIN["method"],
                endpoint=Auth.LOGIN["endpoint"],
                headers=Auth.LOGIN["headers"],
            )
            response_data = response

            if response_data["code"] == Auth.LOGIN["responses"]["invalid_password"]:
                raise AuthenticationError("Invalid password")
            if response_data["code"] == Auth.LOGIN["responses"]["user_does_not_exist"]:
                raise AuthenticationError("User does not exist")
            if response_data["code"] == Auth.LOGIN["responses"]["api_limit_exceeded"]:
                raise APILimitExceededError("API limit exceeded")
            if (
                response_data["code"]
                == Auth.LOGIN["responses"]["authentication_successful"]
            ):
                self._token.token = response_data.get("data")[0].get("accessToken")
                token_expiration_date = (
                    response_data.get("data")[0].get("tokenDteExpiration").get("$date")
                )
                self._token.expires_at = datetime.fromtimestamp(
                    token_expiration_date / 1000
                )

        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}") from e

    async def exchange(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make an authenticated HTTP request to the EMT API.

        This method automatically handles authentication token management,
        including refreshing the token if it has expired, before making
        the actual request.

        Args:
            method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
            endpoint: API endpoint path (relative to the base URL)
            params: Optional query parameters to include in the request
            data: Optional request body data (for POST/PUT requests)
            headers: Optional additional headers to include in the request

        Returns:
            dict: The parsed JSON response from the API

        Raises:
            aiohttp.ClientResponseError: If the HTTP request fails
            ValueError: If authentication is required but not available
            Exception: For other unexpected errors during the request
        """
        if self._token.is_expired or self._token.token is None:
            await self.authenticate()
        headers = {"accessToken": self._token.token}
        return await self._http_client.exchange(method, endpoint, params, data, headers)
