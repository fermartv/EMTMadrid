from abc import ABC, abstractmethod

from emt_madrid.domain.stop import Stop


class EMTRepository(ABC):
    """EMT repository interface."""

    @abstractmethod
    def get_stop_info(self, stop_id: int) -> Stop:
        """Get information about a bus stop."""
        raise NotImplementedError

    @abstractmethod
    def get_nearby_stops(self, stop_id: int) -> Stop:
        """Get information about nearby stops."""
        raise NotImplementedError

    @abstractmethod
    def get_arrivals(self, stop: Stop) -> Stop:
        """Get information about arrivals at a specific stop."""
        raise NotImplementedError
