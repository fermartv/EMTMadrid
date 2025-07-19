from typing import Optional

from emt_madrid.domain.emt_repository import EMTRepository
from emt_madrid.domain.stop import Stop
from emt_madrid.domain.exceptions import APIResponseError


class GetStopInfo:
    """
    Get information about a bus stop.

    Args:
        repository: EMT repository to use for data access
        stop_id: ID of the bus stop to retrieve information for
        lines: Optional list of bus lines to filter

    Methods:
        execute: Get information about a bus stop
    """

    def __init__(
        self, repository: EMTRepository, stop_id: int, lines: Optional[list[str]] = None
    ) -> None:
        """Initialize GetStopInfo object."""
        self._repository: EMTRepository = repository
        self._stop_id: int = stop_id
        self._lines: Optional[list[str]] = lines

    async def execute(self) -> Stop:
        """
        Get information about a bus stop.

        Returns:
            A Stop object containing the stop information

        Raises:
            ValueError: If the stop information cannot be retrieved
        """
        stop = await self._repository.get_stop_info(self._stop_id)

        if not self._lines:
            return stop

        stop_line_numbers = {str(line.line_number) for line in stop.stop_lines}
        missing_lines = set(self._lines) - stop_line_numbers

        if missing_lines:
            raise APIResponseError(
                f"The following lines are not available at this stop: {', '.join(sorted(missing_lines))}"
            )

        stop.stop_lines = [
            line for line in stop.stop_lines if str(line.line_number) in self._lines
        ]
        return stop
