"""Support for EMT Madrid API to get bus stop and route information."""

import asyncio
import json
import logging
import math
from typing import Any, Dict

import aiohttp
import async_timeout
from aiohttp import ClientError

from .const import BASE_URL, DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class BusStopDisabled(Exception):
    """Exception to indicate when a bus stop ID does not exist or has been disabled."""


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
        self._stop_info = {
            "stop_id": self._stop_id,
            "stop_name": None,
            "stop_coordinates": None,
            "stop_address": None,
            "lines": {},
        }

    async def authenticate(self) -> str:
        """Perform login to obtain the authentication token."""
        endpoint = "v1/mobilitylabs/user/login/"
        headers = {"email": self._email, "password": self._password}
        url = self._base_url + endpoint
        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await self._get_data(url, headers, "GET")
            if response is not None:
                self._token = self._parse_token(response)
                return self._token

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)
        return None

    def _parse_token(self, response: Dict[str, Any]) -> str:
        """Parse the response from the authentication endpoint."""
        if response.get("code") == "01":
            return response["data"][0].get("accessToken")

        _LOGGER.warning("Invalid login credentials")
        return None

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

    async def update_stop_info(self) -> Dict[str, Any]:
        """Update information about a bus stop."""
        endpoint = f"v1/transport/busemtmad/stops/{self._stop_id}/detail/"
        headers = {"accessToken": self._token}
        url = self._base_url + endpoint

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await self._get_data(url, headers, "GET")
            if response is not None:
                self._parse_stop_info(response)
                return self._stop_info
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)
        return None

    def _parse_stop_info(self, response):
        """Parse the stop info from the API response."""
        assert self._stop_info is not None
        try:
            if response.get("code") != "00":
                raise BusStopDisabled

            stop_info = response["data"][0]["stops"][0]
            self._stop_info.update(
                {
                    "stop_id": stop_info["stop"],
                    "stop_name": stop_info["name"],
                    "stop_coordinates": stop_info["geometry"]["coordinates"],
                    "stop_address": stop_info["postalAddress"],
                    "lines": self._parse_lines(stop_info["dataLine"]),
                }
            )

        except BusStopDisabled:
            _LOGGER.warning("Bus Stop disabled or does not exist")

    def _parse_lines(self, lines):
        """Parse the line info from the API response."""
        line_info = {}
        for line in lines:
            line_number = line["label"]
            line_info[line_number] = {
                "destination": line["headerA"]
                if line["direction"] == "A"
                else line["headerB"],
                "origin": line["headerA"]
                if line["direction"] == "B"
                else line["headerB"],
                "max_freq": int(line["maxFreq"]),
                "min_freq": int(line["minFreq"]),
                "start_time": line["startTime"],
                "end_time": line["stopTime"],
                "day_type": line["dayType"],
                "distance": [],
                "arrivals": [],
            }
        return line_info

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
            if response is not None:
                lines = self._stop_info["lines"].values()
                if len(lines) == 0:
                    await self.update_stop_info()
                    if len(self._stop_info["lines"]) == 0:
                        return None
                self._parse_arrivals(response)
                return self._stop_info
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout error fetching data from %s", url)
        return None

    def _parse_arrivals(self, response):
        """Parse the arrival times and distance from the API response."""
        try:
            if response.get("code") != "00":
                raise BusStopDisabled

            for line_info in self._stop_info["lines"].values():
                line_info["arrivals"] = []
                line_info["distance"] = []
            arrivals = response["data"][0].get("Arrive", [])
            for arrival in arrivals:
                line = arrival.get("line")
                line_info = self._stop_info["lines"].get(line)
                arrival_time = min(math.trunc(arrival.get("estimateArrive") / 60), 45)
                if line_info:
                    line_info["arrivals"].append(arrival_time)
                    line_info["distance"].append(arrival.get("DistanceBus"))
        except BusStopDisabled:
            _LOGGER.warning("Bus Stop disabled or does not exist")
