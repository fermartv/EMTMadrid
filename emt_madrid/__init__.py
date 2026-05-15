"""Wrapper for the Madrid EMT (Empresa Municipal de Trasnportes) API."""

from .main import EMTClient
from .domain.stop import Stop
from .domain.line import Line
from .domain.bus_arrival import BusArrival
from .domain.exceptions import (
    AuthenticationError,
    StopNotFoundError,
    ArrivalsNotFoundError,
)

__all__ = [
    "EMTClient",
    "Line",
    "Stop",
    "BusArrival",
    "AuthenticationError",
    "StopNotFoundError",
    "ArrivalsNotFoundError",
]
