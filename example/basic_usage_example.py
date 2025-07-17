import asyncio
import os

import aiohttp
from dotenv import load_dotenv

from emt_madrid.main import EMTClient

# Load environment variables from .env file
load_dotenv()

STOP = 72
LINES = ["27", "150"]


if __name__ == "__main__":

    async def main():
        # Get required environment variables
        email = os.getenv("EMT_API_EMAIL")
        password = os.getenv("EMT_API_PASSWORD")
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
