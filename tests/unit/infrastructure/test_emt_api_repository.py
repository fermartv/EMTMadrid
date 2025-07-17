import pytest
import unittest.mock

from emt_madrid.infrastructure.emt_api_repository import EMTAPIRepository
from tests.unit.infrastructure.fixtures.test_stop_get_info_fixture import (
    STOP_GET_INFO_OK_RESPONSE,
    STOP_GET_INFO_OK,
    STOP_GET_INFO_NOT_FOUND_RESPONSE,
    STOP_GET_INFO_DETAIL_NOT_AVAILABLE_RESPONSE,
    STOP_GET_INFO_NO_DATA_RESPONSE,
)
from tests.unit.infrastructure.fixtures.test_get_nearby_stops_fixture import (
    GET_NEARBY_STOPS_OK_RESPONSE,
    GET_NEARBY_STOPS_OK,
    GET_NEARBY_STOPS_NOT_FOUND_RESPONSE,
    GET_NEARBY_STOPS_NO_DATA_RESPONSE,
)
from tests.unit.infrastructure.fixtures.test_get_arrivals_fixture import (
    STOP_GET_ARRIVALS_OK,
    STOP_GET_ARRIVALS_OK_RESPONSE,
    STOP_GET_ARRIVALS_NOT_FOUND_RESPONSE,
    STOP_GET_ARRIVALS_NO_DATA_RESPONSE,
)
from emt_madrid.domain.exceptions import APIResponseError


class FakeEMTAuthenticatedClient:
    def __init__(self, response: dict | None = None) -> None:
        self._response: dict | None = response

    async def exchange(
        self, method: str, endpoint: str, data: dict | None = None
    ) -> dict:
        if self._response is None:
            return {}
        return self._response


class TestStopGetInfo:
    @pytest.mark.asyncio
    async def test_get_stop_info(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(STOP_GET_INFO_OK_RESPONSE)
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        stop = await emt_api_repository.get_stop_info(STOP_GET_INFO_OK.stop_id)

        assert stop == STOP_GET_INFO_OK

    @pytest.mark.asyncio
    async def test_get_stop_info_not_found(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            STOP_GET_INFO_NOT_FOUND_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_stop_info(STOP_GET_INFO_OK.stop_id)

    @pytest.mark.asyncio
    async def test_get_stop_info_detail_not_available(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            STOP_GET_INFO_DETAIL_NOT_AVAILABLE_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with unittest.mock.patch.object(
            emt_api_repository, "get_nearby_stops"
        ) as mock_get_nearby_stops:
            await emt_api_repository.get_stop_info(STOP_GET_INFO_OK.stop_id)
            mock_get_nearby_stops.assert_called_once_with(STOP_GET_INFO_OK.stop_id)

    @pytest.mark.asyncio
    async def test_get_stop_info_no_response(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient()
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_stop_info(STOP_GET_INFO_OK.stop_id)

    @pytest.mark.asyncio
    async def test_get_stop_info_no_data(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            STOP_GET_INFO_NO_DATA_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_stop_info(STOP_GET_INFO_OK.stop_id)


class TestGetNearbyStops:
    @pytest.mark.asyncio
    async def test_get_nearby_stops(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            GET_NEARBY_STOPS_OK_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        stop = await emt_api_repository.get_nearby_stops(GET_NEARBY_STOPS_OK.stop_id)

        assert stop == GET_NEARBY_STOPS_OK

    @pytest.mark.asyncio
    async def test_get_nearby_stops_not_found(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            GET_NEARBY_STOPS_NOT_FOUND_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_nearby_stops(GET_NEARBY_STOPS_OK.stop_id)

    @pytest.mark.asyncio
    async def test_get_nearby_stops_no_response(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient()
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_nearby_stops(GET_NEARBY_STOPS_OK.stop_id)

    @pytest.mark.asyncio
    async def test_get_nearby_stops_no_data(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            GET_NEARBY_STOPS_NO_DATA_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_nearby_stops(GET_NEARBY_STOPS_OK.stop_id)


class TestGetArrivals:
    @pytest.mark.asyncio
    async def test_get_arrivals(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            STOP_GET_ARRIVALS_OK_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        stop = await emt_api_repository.get_arrivals(STOP_GET_INFO_OK)

        assert stop == STOP_GET_ARRIVALS_OK

    @pytest.mark.asyncio
    async def test_get_arrivals_not_found(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            STOP_GET_ARRIVALS_NOT_FOUND_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_arrivals(STOP_GET_INFO_OK)

    @pytest.mark.asyncio
    async def test_get_arrivals_no_response(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient()
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_arrivals(STOP_GET_INFO_OK)

    @pytest.mark.asyncio
    async def test_get_arrivals_no_data(self) -> None:
        emt_authenticated_client = FakeEMTAuthenticatedClient(
            STOP_GET_ARRIVALS_NO_DATA_RESPONSE
        )
        emt_api_repository = EMTAPIRepository(emt_authenticated_client)  # type: ignore

        with pytest.raises(APIResponseError):
            await emt_api_repository.get_arrivals(STOP_GET_INFO_OK)
