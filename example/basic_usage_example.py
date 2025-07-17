import asyncio
import os
import sys

import aiohttp
from dotenv import load_dotenv

from emt_madrid.main import EMTClient

# Load environment variables from .env file
load_dotenv()

STOP = 72
LINES = ["27", "150"]


def get_required_env_var(name: str) -> str | None:
    """Get a required environment variable or exit with an error if not found."""
    value = os.getenv(name)
    if not value:
        print(f"Error: {name} environment variable is not set")
        print("Please create a .env file with your EMT API credentials:")
        print("EMT_API_EMAIL=your_email@example.com")
        print("EMT_API_PASSWORD=your_password")
        sys.exit(1)
    return value


if __name__ == "__main__":

    async def main():
        # Get required environment variables
        email = get_required_env_var("EMT_API_EMAIL")
        password = get_required_env_var("EMT_API_PASSWORD")
        if not email or not password:
            raise ValueError(
                "EMT_API_EMAIL and EMT_API_PASSWORD environment variables must be set"
            )

        # Create a session and pass it to the EMTClient
        async with aiohttp.ClientSession() as session:
            emt_client = EMTClient(
                email=email,
                password=password,
                stop_id=STOP,
                lines=LINES,
                session=session,
            )

            stop = await emt_client.get_arrivals()
            print(stop)

    asyncio.run(main())
