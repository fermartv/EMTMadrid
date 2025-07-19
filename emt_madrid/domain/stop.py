from dataclasses import dataclass

from emt_madrid.domain.line import Line


@dataclass
class Stop:
    """Bus stop information."""

    stop_id: int
    stop_name: str
    stop_address: str
    stop_coordinates: list[float]
    stop_lines: list[Line]

    def __str__(self) -> str:
        """Return a string representation of the stop."""
        return f"Stop {self.stop_id} - {self.stop_name} at {self.stop_address} with lines {self.stop_lines}"
