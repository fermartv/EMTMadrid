from datetime import time

from emt_madrid.domain.day_type import DayType
from emt_madrid.domain.emt_repository import EMTRepository
from emt_madrid.domain.exceptions import (
    APIResponseError,
    StopNotFoundError,
    ArrivalsNotFoundError,
)
from emt_madrid.domain.line import Line
from emt_madrid.domain.stop import Stop
from emt_madrid.infrastructure.emt_api_client import EMTAuthenticatedClient
from emt_madrid.infrastructure.emt_api_endpoints import Stops


class EMTAPIRepository(EMTRepository):
    """EMT API repository to retrieve bus stop information and arrival times."""

    def __init__(self, emt_authenticated_client: EMTAuthenticatedClient) -> None:
        """Initialize EMTAPIRepository object."""
        self.emt_authenticated_client = emt_authenticated_client

    async def get_nearby_stops(self, stop_id: int) -> Stop:
        """Get information about nearby stops using the ARROUNDSTOP endpoint.

        Args:
            stop_id: The ID of the bus stop to find nearby stops for

        Returns:
            A Stop object containing the nearest stop information

        Raises:
            ValueError: If no nearby stops are found
        """
        try:
            endpoint = Stops.ARROUNDSTOP["endpoint"].format(stop_id=stop_id)
            response = await self.emt_authenticated_client.exchange(
                method=Stops.ARROUNDSTOP["method"], endpoint=endpoint
            )

            if not response:
                raise APIResponseError(f"No response from stop: {stop_id}")

            if (
                response.get("code", {})
                != Stops.ARROUNDSTOP["responses"]["stop_data_retrieved"]
            ):
                raise APIResponseError(
                    f"Failed to retrieve nearby stops for stop {stop_id}. Code: {response.get('code')}"
                )

            stops_data = response.get("data", [])

            if not stops_data:
                raise StopNotFoundError(
                    stop_id=stop_id,
                    message=f"No nearby stops found for stop {stop_id}. Code: {response.get('code')}",
                )

            stop_data = stops_data[0]

            coordinates = stop_data["geometry"]["coordinates"]
            lines = []
            if "lines" in stop_data:
                lines = self._get_lines_from_around_stop(stop_data["lines"])

            return Stop(
                stop_id=stop_data["stopId"],
                stop_name=stop_data["stopName"],
                stop_address=stop_data["address"].strip(),
                stop_coordinates=coordinates,
                stop_lines=lines,
            )

        except Exception as e:
            raise StopNotFoundError(stop_id, str(e)) from e

    def _get_lines_from_around_stop(self, lines: list[dict]) -> list[Line]:
        """Get a list of lines from the around stop endpoint response."""
        result = []
        for line in lines:
            if line["to"] == "B":
                origin = line["nameA"]
                destination = line["nameB"]
            else:
                origin = line["nameB"]
                destination = line["nameA"]
            result.append(
                Line(
                    line_number=str(line["line"]),
                    origin=origin,
                    destination=destination,
                )
            )
        return result

    async def get_stop_info(self, stop_id: int) -> Stop:
        """Get information about a bus stop.

        Args:
            stop_id: The ID of the bus stop

        Returns:
            A Stop object containing the stop information

        Raises:
            StopNotFoundError: If the stop information cannot be retrieved
        """
        try:
            endpoint = Stops.DETAIL["endpoint"].format(stop_id=stop_id)
            response = await self.emt_authenticated_client.exchange(
                method=Stops.DETAIL["method"], endpoint=endpoint
            )

            if not response:
                raise APIResponseError(f"No response from stop: {stop_id}")

            if response.get("code", {}) == Stops.DETAIL["responses"]["stop_not_found"]:
                raise StopNotFoundError(
                    message=f"Stop {stop_id} not found. Code: {response.get('code')}"
                )

            if (
                response.get("code", {})
                == Stops.DETAIL["responses"]["detail_not_available"]
            ):
                return await self.get_nearby_stops(stop_id)

            stops_data = response.get("data", [])

            if not stops_data:
                raise APIResponseError(
                    f"No information found for stop {stop_id}. Code: {response.get('code')}"
                )

            stop_data = stops_data[0].get("stops", [{}])[0] if stops_data else {}
            coordinates = []
            if "geometry" in stop_data:
                coordinates = stop_data["geometry"]["coordinates"]
            lines = []
            if "dataLine" in stop_data:
                lines = self._get_lines_from_stop(stop_data["dataLine"])

            return Stop(
                stop_id=stop_id,
                stop_name=stop_data.get("name", "Unknown"),
                stop_address=stop_data.get("postalAddress", "Unknown"),
                stop_coordinates=coordinates,
                stop_lines=lines,
            )

        except Exception as e:
            raise StopNotFoundError(stop_id, str(e)) from e

    def _get_lines_from_stop(self, lines: list[dict]) -> list[Line]:
        """Get a list of lines from the stop endpoint response."""
        result = []
        for line in lines:
            day_type = DayType.WORKING_DAY
            if line["dayType"] == "SA":
                day_type = DayType.SATURDAY
            elif line["dayType"] == "FE":
                day_type = DayType.FESTIVE

            result.append(
                Line(
                    line_number=line["label"],
                    origin=line["headerA"],
                    destination=line["headerB"],
                    max_frequency=int(line["maxFreq"]),
                    min_frequency=int(line["minFreq"]),
                    start_time=time.fromisoformat(line["startTime"]),
                    end_time=time.fromisoformat(line["stopTime"]),
                    day_type=day_type,
                )
            )
        return result

    async def get_arrivals(self, stop: Stop) -> Stop:
        """Get information about arrivals at a specific stop.

        Args:
            stop: The bus stop to update with arrival information

        Returns:
            The same Stop object with updated arrival information for each line

        Raises:
            ArrivalsNotFoundError: If the arrival information cannot be retrieved
        """
        try:
            endpoint = Stops.ARRIVAL["endpoint"].format(stop_id=stop.stop_id)
            data = Stops.ARRIVAL["data"].copy()
            data["stopId"] = str(stop.stop_id)
            response = await self.emt_authenticated_client.exchange(
                method=Stops.ARRIVAL["method"], endpoint=endpoint, data=data
            )

            if not response:
                raise APIResponseError(f"No response from stop: {stop.stop_id}")

            if response.get("code") == Stops.ARRIVAL["responses"]["stop_not_found"]:
                raise StopNotFoundError(
                    stop_id=stop.stop_id,
                    message=f"No nearby stops found for stop {stop.stop_id}. Code: {response.get('code')}",
                )

            arrivals_data = response.get("data", [{}])[0].get("Arrive", [])

            if not arrivals_data:
                raise ArrivalsNotFoundError(
                    stop_id=stop.stop_id,
                    message=f"No arrival information found for stop {stop.stop_id}",
                )

            line_arrivals = {}
            for arrival in arrivals_data:
                try:
                    line_number = str(arrival["line"])
                    if line_number not in line_arrivals:
                        line_arrivals[line_number] = []
                    line_arrivals[line_number].append(
                        int(arrival["estimateArrive"]) // 60
                    )
                except (KeyError, ValueError):
                    continue

            for line in stop.stop_lines:
                arrivals = line_arrivals.get(line.line_number, [])

                sorted_arrivals = sorted(set(arrivals))

                if not sorted_arrivals:
                    line.arrival = None
                    line.next_arrival = None
                else:
                    line.arrival = sorted_arrivals[0]
                    line.next_arrival = (
                        sorted_arrivals[1] if len(sorted_arrivals) > 1 else None
                    )

            return stop

        except Exception as e:
            raise ArrivalsNotFoundError(stop.stop_id, str(e)) from e
