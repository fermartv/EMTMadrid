from dataclasses import dataclass, field

from emt_madrid.domain.bus_arrival import BusArrival
from emt_madrid.domain.line import Line


@dataclass
class Stop:
    """Bus stop information with real-time arrivals.

    Attributes:
        stop_id: Unique identifier for the bus stop.
        stop_name: Name of the bus stop.
        stop_address: Physical address of the bus stop.
        stop_coordinates: GPS coordinates as [longitude, latitude].
        stop_lines: List of Line objects that serve this stop.
        bus_arrivals: List of BusArrival objects with real-time arrival data,
            including bus GPS coordinates for tracking.
    """

    stop_id: int
    stop_name: str
    stop_address: str
    stop_coordinates: list[float]
    stop_lines: list[Line]
    bus_arrivals: list[BusArrival] = field(default_factory=list)

    def __str__(self) -> str:
        """Return a string representation of the stop."""
        result = f"Stop {self.stop_id} - {self.stop_name} at {self.stop_address}\n"
        result += f"  Coordinates: {self.stop_coordinates}\n"
        result += f"  Lines: {self.stop_lines}\n"
        if self.bus_arrivals:
            result += "  Bus Arrivals:\n"
            for bus in self.bus_arrivals:
                result += f"    - Bus {bus.bus_id} (Line {bus.line}) → {bus.destination} in {bus.estimate_arrive_sec}s at {bus.coordinates}\n"
        return result
