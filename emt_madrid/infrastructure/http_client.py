from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import aiohttp

from emt_madrid.infrastructure.emt_api_config import EMTAPIConfig


class HTTPClient:
    """
    HTTP client for making requests to the EMT API.

    Args:
        config: EMTAPIConfig object containing API configuration
        session: Optional aiohttp.ClientSession to use for HTTP requests
    """

    def __init__(
        self, config: EMTAPIConfig, session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        """Initialize HTTPClient with default base URL"""
        self.session: Optional[aiohttp.ClientSession] = session
        self.base_url: str = config.BASE_URL

    async def exchange(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with the specified method

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: Endpoint URL (can be relative if base_url is set)
            params: Query parameters
            data: Request body data
            headers: Request headers

        Returns:
            Response JSON data as dictionary

        Raises:
            aiohttp.ClientResponseError: If HTTP response status is not successful
        """
        url = urljoin(self.base_url, endpoint)

        async with self.session.request(
            method=method,
            url=url,
            params=params,
            json=data if isinstance(data, dict) else None,
            data=data if not isinstance(data, dict) else None,
            headers=headers,
        ) as response:
            response.raise_for_status()
            return await response.json()
