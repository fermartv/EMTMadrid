from emt_madrid.domain.line import Line
from emt_madrid.domain.stop import Stop


class TestData:
    @staticmethod
    def a_stop(
        stop_id: int = 123,
        line_numbers: list[str] | None = None,
        stop_name: str = "Test Stop",
        stop_address: str = "Test Address",
        stop_coordinates: list[float] = [0, 0],
    ) -> Stop:
        lines = [
            Line(
                line_number=str(num),
                origin="Test Origin",
                destination="Test Destination",
            )
            for num in (line_numbers or [])
        ]

        return Stop(
            stop_id=stop_id,
            stop_name=stop_name,
            stop_address=stop_address,
            stop_coordinates=stop_coordinates,
            stop_lines=lines,
        )
