"""Support for EMT Madrid API to get bus stop and route information."""

import asyncio
import json
import logging
from typing import Any, Dict

import aiohttp
import async_timeout
from aiohttp import ClientError

from .const import BASE_URL, DEFAULT_TIMEOUT
from .parser import parse_token, parse_stop_info, parse_arrivals

_LOGGER = logging.getLogger(__name__)


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
        stop_id: str,
    ) -> None:
        """Initialize the EMTAPIWrapper object.

        Args:
            session (aiohttp.ClientSession): The aiohttp ClientSession
                for making HTTP requests.
            email (str): The email for API login.
            password (str): The password for API login.
            stop_id (str): The ID of the bus stop.

        Raises:
            AssertionError: If email, password, or session is None.
        """
        assert email is not None, "Email must not be None"
        assert password is not None, "Password must not be None"
        assert session is not None, "Session must not be None"

        self._session = session
        self._email = email
        self._password = password
        self._stop_id = stop_id
        self._token = None
        self._base_url = BASE_URL
        self._stop_info = {
            "stop_id": self._stop_id,
            "stop_name": None,
            "stop_coordinates": None,
            "stop_address": None,
            "lines": {},
        }

    async def _get_data(
        self,
        url: str,
        headers: Dict[str, Any],
        method: str,
        data: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Get data from the EMT API."""
        assert self._session is not None
        if data is not None:
            data = json.dumps(data)

        try:
            if method == "GET":
                response = await self._session.get(
                    url, headers=headers, timeout=DEFAULT_TIMEOUT
                )
            elif method == "POST":
                response = await self._session.post(
                    url, headers=headers, data=data, timeout=DEFAULT_TIMEOUT
                )

            if response.status == 200:
                return await response.json()

            _LOGGER.warning(
                "Error %s. Failed to get data from %s", response.status, url
            )

        except TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)

        except ClientError as exc:
            _LOGGER.warning("Client error in '%s' -> %s", url, exc)

        return None

    async def authenticate(self) -> str:
        """Perform login to obtain the authentication token."""
        endpoint = "v1/mobilitylabs/user/login/"
        headers = {"email": self._email, "password": self._password}
        url = self._base_url + endpoint

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await self._get_data(url, headers, "GET")

            if response is not None:
                self._token = parse_token(response)

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)

    @property
    def token(self) -> str:
        """Return API token."""
        return self._token

    async def update_stop_info(self) -> Dict[str, Any]:
        """Update information about a bus stop."""
        endpoint = f"v1/transport/busemtmad/stops/{self._stop_id}/detail/"
        headers = {"accessToken": self._token}
        url = self._base_url + endpoint

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await self._get_data(url, headers, "GET")

            if response is None:
                return None

            parsed_stop_info = parse_stop_info(response, self._stop_info)

            if parsed_stop_info is None:
                return None

            if parsed_stop_info.get("error") == "Invalid token":
                await self.authenticate()
                return None

            self._stop_info = parsed_stop_info

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)

    async def update_bus_arrivals(self) -> Dict[str, Any]:
        """Get the next buses for a given bus stop."""
        endpoint = f"v2/transport/busemtmad/stops/{self._stop_id}/arrives/"
        headers = {"accessToken": self._token}
        data = {"stopId": self._stop_id, "Text_EstimationsRequired_YN": "Y"}
        url = self._base_url + endpoint

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await self._get_data(
                    url=url, headers=headers, method="POST", data=data
                )

            if response is None:
                return None

            lines = self._stop_info["lines"].values()
            if len(lines) == 0:
                await self.update_stop_info()
                if len(self._stop_info["lines"]) == 0:
                    return None

            parsed_arrivals = parse_arrivals(response, self._stop_info)

            if parsed_arrivals is None:
                return None

            if parsed_arrivals.get("error") == "Invalid token":
                await self.authenticate()
                return None

            self._stop_info = parsed_arrivals

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)

    def get_stop_info(self) -> Dict[str, Any]:
        """Return the stop information."""
        return self._stop_info
