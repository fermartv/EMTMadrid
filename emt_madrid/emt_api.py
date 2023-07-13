"""Support for EMT Madrid API to get bus stop and route information."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

import aiohttp
import async_timeout
from aiohttp import ClientError

from .const import BASE_URL, DEFAULT_TIMEOUT
from .parser import parse_arrivals, parse_stop_info, parse_token

_LOGGER = logging.getLogger(__name__)


class EMTAPIAuthenticator:
    """
    Authenticates the user and obtains a token for accessing the EMT API.

    Args:
        session (aiohttp.ClientSession): An instance of `aiohttp.ClientSession`
            for making HTTP requests.
        email (str): The user's email address.
        password (str): The user's password.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        email: str,
        password: str,
    ) -> None:
        """Initialize the EMTAPIAuthenticator object."""
        assert email is not None, "Email must not be None"
        assert password is not None, "Password must not be None"
        assert session is not None, "Session must not be None"

        self._session: aiohttp.ClientSession = session
        self._credentials: Dict[str, Any] = {"email": email, "password": password}
        self._token: Optional[str] = None
        self._base_url: str = BASE_URL

    async def _get_data(
        self,
        url: str,
        headers: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Get data from the EMT API."""
        assert self._session is not None

        try:
            response = await self._session.get(
                url, headers=headers, timeout=DEFAULT_TIMEOUT
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

    async def authenticate(self) -> Optional[str]:
        """Perform login to obtain the authentication token."""
        endpoint = "v1/mobilitylabs/user/login/"
        email = self._credentials.get("email")
        password = self._credentials.get("password")
        headers = {"email": email, "password": password}
        url = self._base_url + endpoint

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await self._get_data(url, headers)

            if response is not None:
                self._token = parse_token(response)
                return self._token

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)
        return None

    @property
    def token(self) -> Optional[str]:
        """Return API token."""
        return self._token


class EMTAPIBusStop:
    """
    Represents a bus stop in the EMT (Empresa Municipal de Transportes) API.

    Args:
        session (aiohttp.ClientSession): An instance of `aiohttp.ClientSession`
            for making HTTP requests.
        token (str): The API token for accessing the EMT API.
        stop_id (str): The ID of the bus stop.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str,
        stop_id: str,
    ) -> None:
        """Initialize the EMTAPIBusStop object."""
        assert session is not None, "Session must not be None"
        if token is None:
            _LOGGER.warning("Token must not be None")

        self._session: aiohttp.ClientSession = session
        self._stop_id: str = stop_id
        self._token: str = token
        self._base_url: str = BASE_URL
        self._stop_info: Dict[str, Any] = {
            "stop_id": self._stop_id,
            "stop_name": None,
            "stop_coordinates": None,
            "stop_address": None,
            "lines": {},
        }

        self._update_semaphore = asyncio.Semaphore(1)

    async def _get_data(
        self,
        url: str,
        headers: Dict[str, Any],
        method: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Get data from the EMT API."""
        assert self._session is not None
        if data is not None:
            data_json = json.dumps(data)

        if self._token is None:
            return None

        try:
            if method == "GET":
                response = await self._session.get(
                    url, headers=headers, timeout=DEFAULT_TIMEOUT
                )
            elif method == "POST":
                response = await self._session.post(
                    url, headers=headers, data=data_json, timeout=DEFAULT_TIMEOUT
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

    def set_token(self, token: str) -> None:
        """Set the API token."""
        self._token = token

    @property
    def token(self) -> str:
        """Return API token."""
        return self._token

    async def update_stop_info(self) -> None:
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
                return None

            async with self._update_semaphore:
                self._stop_info = parsed_stop_info

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)

    async def update_bus_arrivals(self) -> None:
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
                return None

            async with self._update_semaphore:
                self._stop_info = parsed_arrivals

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)

    def get_stop_info(self) -> Dict[str, Any]:
        """Return the stop information."""
        return self._stop_info

    def get_arrival_time(self, line: str) -> Optional[List[Optional[int]]]:
        """Retrieve arrival times in minutes for the specified bus line."""
        arrivals = self._stop_info.get("lines", {}).get(line, {}).get("arrivals")
        if arrivals is None:
            _LOGGER.warning("Unable to get arrival time for line %s", line)
            return None
        while len(arrivals) < 2:
            arrivals.append(None)
        return arrivals

    def get_line_info(self, line: str) -> Optional[Dict[str, Any]]:
        """Retrieve the information for a specific line."""
        lines = self._stop_info.get("lines", {})
        if line in lines:
            line_info = lines.get(line)
            if "distance" in line_info and len(line_info["distance"]) == 0:
                line_info["distance"].append(None)
            return line_info

        _LOGGER.warning("Bus line %s not found", line)
        return None
