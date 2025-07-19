from enum import Enum


class DayType(Enum):
    """Day type enum."""

    WORKING_DAY = "Working day"
    SATURDAY = "Saturday"
    FESTIVE = "Festive"

    def __str__(self) -> str:
        return self.value
