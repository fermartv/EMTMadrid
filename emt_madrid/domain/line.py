from dataclasses import dataclass
from datetime import time
from typing import Optional
from emt_madrid.domain.day_type import DayType


@dataclass
class Line:
    """Bus line information."""

    line_number: str
    origin: str
    destination: str
    max_frequency: Optional[int] = None
    min_frequency: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    day_type: Optional[DayType] = None
    arrival: Optional[int] = None
    next_arrival: Optional[int] = None

    def __str__(self) -> str:
        """Return a string representation of the line."""
        return f"Line {self.line_number}: {self.origin} → {self.destination} - {self.arrival} min - {self.next_arrival} min"
