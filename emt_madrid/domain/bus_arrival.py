from dataclasses import dataclass
from typing import Optional


@dataclass
class BusArrival:
    """Real-time bus arrival information with GPS coordinates.

    Attributes:
        line: The bus line number.
        bus_id: Unique identifier for the bus vehicle.
        destination: The bus destination stop.
        coordinates: GPS coordinates of the bus as [longitude, latitude].
        estimate_arrive_sec: Estimated time until arrival at the stop in seconds.
        distance_bus: Distance from the bus to the stop in meters.
        is_head: Whether this bus is the head of the line.
        deviation: Route deviation in seconds (0 if on schedule).
        position_type_bus: Position type indicator from the API.
    """

    line: str
    bus_id: int
    destination: str
    coordinates: list[float]
    estimate_arrive_sec: Optional[int] = None
    distance_bus: Optional[int] = None
    is_head: bool = False
    deviation: int = 0
    position_type_bus: str = "0"

    def __str__(self) -> str:
        """Return a string representation of the bus arrival."""
        return f"Bus {self.bus_id} (Line {self.line}) → {self.destination} in {self.estimate_arrive_sec}s at {self.coordinates}"
