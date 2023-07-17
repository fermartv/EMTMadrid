"""Parsers for the EMT API responses."""

import logging
import math
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__)


class BusStopDisabled(Exception):
    """Exception to indicate when a bus stop ID does not exist or has been disabled."""


class InvalidToken(Exception):
    """Exception to indicate when the user token is invalid."""


class APILimitReached(Exception):
    """Exception to indicate when maximum number of API calls has been reached."""


def parse_token(response: Dict[str, Any]) -> Optional[str]:
    """Parse the response from the authentication endpoint."""
    try:
        if response.get("code") == "01":
            return response["data"][0].get("accessToken")
        if response.get("code") == "98":
            raise APILimitReached

        _LOGGER.warning("Invalid login credentials")

    except APILimitReached:
        _LOGGER.warning("Maximum daily API usage has been exceeded.")

    return None


def parse_stop_info(
    response: Dict[str, Any], stop_info: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Parse the stop info from the API response."""
    assert stop_info is not None
    try:
        response_code = response.get("code")
        if response_code in ("90", "81"):
            raise BusStopDisabled
        if response_code == "80":
            raise InvalidToken
        if response_code == "98":
            raise APILimitReached

        response_stop = response["data"][0]["stops"][0]
        stop_info.update(
            {
                "stop_id": response_stop["stop"],
                "stop_name": response_stop["name"],
                "stop_coordinates": response_stop["geometry"]["coordinates"],
                "stop_address": response_stop["postalAddress"],
                "lines": parse_lines(response_stop["dataLine"]),
            }
        )
        return stop_info

    except BusStopDisabled:
        _LOGGER.warning("Bus Stop disabled or does not exist")
        return None
    except InvalidToken:
        _LOGGER.warning("Invalid or expired token")
        return {"error": "Invalid token"}
    except APILimitReached:
        _LOGGER.warning("Maximum daily API usage has been exceeded.")
        return None


def parse_lines(lines: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Parse the line info from the API response."""
    line_info: Dict[str, Any] = {}
    for line in lines:
        line_number = str(line.get("label"))
        line_info[line_number] = {
            "destination": line.get("headerA")
            if line.get("direction") == "A"
            else line.get("headerB"),
            "origin": line.get("headerA")
            if line.get("direction") == "B"
            else line.get("headerB"),
            "max_freq": int(line.get("maxFreq") or 0),
            "min_freq": int(line.get("minFreq") or 0),
            "start_time": line.get("startTime"),
            "end_time": line.get("stopTime"),
            "day_type": line.get("dayType"),
            "distance": [],
            "arrivals": [],
        }
    return line_info


def parse_arrivals(
    response: Dict[str, Any], stop_info: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Parse the arrival times and distance from the API response."""
    try:
        if response.get("code") == "80" and "token" in str(response.get("description")):
            raise InvalidToken
        if response.get("code") == "80":
            raise BusStopDisabled
        if response.get("code") == "98":
            raise APILimitReached

        for line_info in stop_info["lines"].values():
            line_info["arrivals"] = []
            line_info["distance"] = []
        arrivals = response["data"][0].get("Arrive", [])
        for arrival in arrivals:
            line = arrival.get("line")
            line_info = stop_info["lines"].get(line)
            arrival_time = min(math.trunc(arrival.get("estimateArrive") / 60), 45)
            if line_info:
                line_info["arrivals"].append(arrival_time)
                line_info["distance"].append(arrival.get("DistanceBus"))
        return stop_info

    except BusStopDisabled:
        _LOGGER.warning("Bus Stop disabled or does not exist")
        return None
    except InvalidToken:
        _LOGGER.warning("Invalid or expired token")
        return {"error": "Invalid token"}
    except APILimitReached:
        _LOGGER.warning("Maximum daily API usage has been exceeded.")
        return None
