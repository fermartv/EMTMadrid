from typing import Optional

import aiohttp

from emt_madrid.domain.emt_repository import EMTRepository
from emt_madrid.domain.stop import Stop
from emt_madrid.infrastructure.emt_api_client import Credentials, EMTAuthenticatedClient
from emt_madrid.infrastructure.emt_api_config import EMTAPIConfig
from emt_madrid.infrastructure.http_client import HTTPClient
from emt_madrid.infrastructure.emt_api_repository import EMTAPIRepository
from emt_madrid.use_cases.get_stop_info import GetStopInfo
from emt_madrid.use_cases.get_arrivals import GetArrivals


class EMTClient:
    """
    EMT client to retrieve bus stop information and arrival times.

    Args:
        email: EMT API account email
        password: EMT API account password
        stop_id: ID of the bus stop to monitor
        session: aiohttp.ClientSession to use for HTTP requests
        lines: Optional list of bus lines to filter

    Methods:
        initialize: Initialize the client
        get_arrivals: Get information about arrivals at a specific stop
    """

    def __init__(
        self,
        email: str,
        password: str,
        stop_id: int,
        session: aiohttp.ClientSession,
        lines: Optional[list[str]] = None,
    ) -> None:
        """Initialize EMT client."""
        self._repository: EMTRepository | None = None
        self._stop_id: int = stop_id
        self._lines: Optional[list[str]] = lines
        self._email: str = email
        self._password: str = password
        self._session: aiohttp.ClientSession = session
        self._stop: Stop | None = None
        http_client = HTTPClient(config=EMTAPIConfig(), session=self._session)
        credentials = Credentials(email=self._email, password=self._password)
        emt_authenticated_client = EMTAuthenticatedClient(
            http_client=http_client, credentials=credentials
        )
        self._repository = EMTAPIRepository(
            emt_authenticated_client=emt_authenticated_client
        )

    async def get_stop_info(self) -> Stop:
        """
        Get information about a bus stop.

        Returns:
            A Stop object containing the stop information

        Raises:
            ValueError: If the stop information cannot be retrieved
        """
        get_stop_info = GetStopInfo(self._repository, self._stop_id, self._lines)
        self._stop = await get_stop_info.execute()
        return self._stop

    async def get_arrivals(self) -> Stop:
        """
        Get information about arrivals at a specific stop.

        Returns:
            The same Stop object with updated arrival information for each line

        Raises:
            ValueError: If the arrival information cannot be retrieved
        """
        if self._stop is None:
            await self.get_stop_info()
        get_arrivals = GetArrivals(self._repository, self._stop)
        self._stop = await get_arrivals.execute()
        return self._stop
