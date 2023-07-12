# EMTMadrid

Python wrapper for the Madrid EMT (Empresa Municipal de Transportes) API, providing easy access to real-time transportation data in Madrid.

## Example code

    import asyncio

    from aiohttp import ClientSession

    from emt_madrid import EMTAPIAuthenticator, EMTAPIBusStop

    EMAIL = "email-from-EMT"
    PASSWORD = "password-from-EMT"

    STOP_ID = "72"


    async def fetch_bus_info():
        """Fetches bus information from the EMT API."""
        async with ClientSession() as session:
            emt_api_authenticator = EMTAPIAuthenticator(session, EMAIL, PASSWORD)
            await emt_api_authenticator.authenticate()
            token = emt_api_authenticator.token
            emt_api_bus_stop = EMTAPIBusStop(session, token, STOP_ID)
            await emt_api_bus_stop.update_stop_info()
            await emt_api_bus_stop.update_bus_arrivals()
            return emt_api_bus_stop.get_stop_info()


    async def main():
        """Main function to execute the code."""
        bus_info = await fetch_bus_info()
        print(bus_info)


    asyncio.run(main())
