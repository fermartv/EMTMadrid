"""Wrapper for the Madrid EMT (Empresa Municipal de Trasnportes) API."""

from .main import EMTClient
from .domain.stop import Stop
from .domain.line import Line

__all__ = ["EMTClient", "Line", "Stop"]
