from emt_madrid.domain.emt_repository import EMTRepository
from emt_madrid.domain.stop import Stop


class GetArrivals:
    """
    Get information about arrivals at a specific stop.

    Args:
        repository: EMT repository to use for data access
        stop: The bus stop to update with arrival information

    Methods:
        execute: Get information about arrivals at a specific stop
    """

    def __init__(self, repository: EMTRepository, stop: Stop) -> None:
        """Initialize GetArrivals object."""
        self._repository: EMTRepository = repository
        self._stop: Stop = stop

    async def execute(self) -> Stop:
        """
        Get information about arrivals at a specific stop.

        Returns:
            The same Stop object with updated arrival information for each line

        Raises:
            ValueError: If the arrival information cannot be retrieved
        """
        return await self._repository.get_arrivals(self._stop)
