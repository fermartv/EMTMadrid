import asyncio
import json
import os
from typing import Any, Dict, List

import aiohttp
from dotenv import load_dotenv

from emt_madrid.main import EMTClient

# Load environment variables from .env file
load_dotenv()

# Configuration
START_STOP = 70
END_STOP = 75
MAX_CONCURRENT_REQUESTS = 10  # Limit concurrent requests to avoid overwhelming the API
OUTPUT_FILE = "stops.json"

# Semaphore to limit concurrency
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def fetch_stop(stop_id: int, session: aiohttp.ClientSession) -> Dict[str, Any]:
    """Fetch information for a single stop."""
    async with semaphore:
        try:
            email = os.getenv("EMT_API_EMAIL")
            password = os.getenv("EMT_API_PASSWORD")
            if not email or not password:
                raise ValueError(
                    "EMT_API_EMAIL and EMT_API_PASSWORD environment variables must be set"
                )

            emt_client = EMTClient(
                email=email,
                password=password,
                stop_id=stop_id,
                session=session,
            )
            stop = await emt_client.get_stop_info()
            print(f"Fetched stop {stop.stop_id} - {stop.stop_name}")
            # Convert Stop object to dictionary for JSON serialization
            stop_dict = (
                {
                    "stop_id": stop.stop_id,
                    "stop_name": stop.stop_name,
                    "stop_address": stop.stop_address,
                    "stop_coordinates": stop.stop_coordinates,
                    "stop_lines": [
                        {
                            "line_number": line.line_number,
                            "origin": line.origin,
                            "destination": line.destination,
                            "min_frequency": line.min_frequency,
                            "max_frequency": line.max_frequency,
                            "day_type": str(line.day_type) if line.day_type else None,
                        }
                        for line in stop.stop_lines
                    ],
                }
                if stop
                else None
            )
            return {"stop_id": stop_id, "data": stop_dict, "error": None}
        except Exception as e:
            print(f"Error fetching stop {stop_id}: {str(e)}")
            return {"stop_id": stop_id, "data": None, "error": str(e)}


async def fetch_all_stops() -> List[Dict[str, Any]]:
    """Fetch information for all stops from START_STOP to END_STOP."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_stop(stop_id, session) for stop_id in range(START_STOP, END_STOP + 1)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out any exceptions that weren't caught
        valid_results = [r for r in results if not isinstance(r, Exception)]
        return valid_results


def save_results(results: List[Dict[str, Any]]) -> None:
    """Save results to a JSON file."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    print(f"Fetching stops from {START_STOP} to {END_STOP}...")
    results = asyncio.run(fetch_all_stops())
    save_results(results)

    # Print some statistics
    successful = sum(1 for r in results if r["data"] is not None)
    failed = len(results) - successful
    print("\nCompleted!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful / len(results)) * 100:.2f}%")
    print(f"Results saved to {OUTPUT_FILE}")
