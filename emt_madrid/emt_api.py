"""Support for EMT Madrid API to get bus stop and route information."""

import logging
from typing import Any, Optional

import aiohttp
import async_timeout
from aiohttp import ClientError

from .const import BASE_URL, DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class LoginFailedException(Exception):
    """Exception for login failure."""


class EMTAPIWrapper:
    """Wrapper class for the EMT API.

    Provides methods to interact with the EMT API,
    including authentication and accessing endpoint data.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        email: str,
        password: str,
        stop_id: int = None,
    ) -> None:
        """Initialize the EMTAPIWrapper object.

        Args:
            email (str): The email for API login.
            password (str): The password for API login.
        """
        self._session = session
        self._email = email
        self._password = password
        self._stop_id = stop_id
        assert self._email is not None
        assert self._password is not None

        self._token = None
        self._base_url = BASE_URL

    async def authenticate(self) -> str:
        """Perform login to obtain the authentication token."""
        endpoint = "v1/mobilitylabs/user/login/"
        headers = {"email": self._email, "password": self._password}
        url = self._base_url + endpoint

        try:
            response = await self._get_data(url, headers, "GET")
            if response is not None:
                self._token = self._parse_token(response)
                return self._token

        except TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)
        except ClientError as exc:
            _LOGGER.warning("Client error in '%s' -> %s", url, exc)
        return None

    def _parse_token(self, response: dict[str, Any]) -> str:
        """Parse the response from the authentication endpoint."""
        if response.get("code") == "01":
            return response["data"][0].get("accessToken")

        _LOGGER.warning("Invalid login credentials")
        return None

    async def _get_data(
        self, url: str, headers: dict[str, Any], method: str
    ) -> dict[str, Any]:
        """Get data from the EMT API."""
        assert self._session is not None
        async with async_timeout.timeout(DEFAULT_TIMEOUT):
            if method == "GET":
                response = await self._session.get(
                    url,
                    headers=headers,
                )
            elif method == "POST":
                response = await self._session.post(
                    url,
                    headers=headers,
                )
        if response.status == 200:
            return await response.json()

        _LOGGER.warning("Error %s. Failed to get data from %s", response.status, url)
        return None

    async def get_stop_info(self, stop_id: Optional[int] = None) -> dict[str, Any]:
        """Get information about a bus stop."""
        stop_id = self._stop_id if stop_id is None else stop_id
        endpoint = f"v1/transport/busemtmad/stops/{stop_id}/detail/"
        headers = {"accessToken": self._token}

        response = await self._get_data(self._base_url + endpoint, headers, "GET")
        return response

    # def get_next_buses(self, stop_id):
    #     """Get the next buses for a given bus stop."""
    #     return
