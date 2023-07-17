# EMTMadrid

Python wrapper for the Madrid EMT (Empresa Municipal de Transportes) API, providing easy access to real-time transportation data in Madrid.

## Install

Install the package using pip:

```bash
pip install madrid-emt
```

## Authentication Instructions

To use the EMT Mobilitylabs API you need to register in their [website](https://mobilitylabs.emtmadrid.es/). Once you are registered you will receive a confirmation email to activate your account. It will not work until you have completed all the steps.

## Usage

```python
import asyncio

from aiohttp import ClientSession

from emt_madrid import EMTAPIAuthenticator, EMTAPIBusStop

EMAIL = "email-from-EMT"
PASSWORD = "password-from-EMT"

STOP_ID = "stop-id-from-EMT" # For example: "72"


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
```

## Attribution

Thanks to [EMT Madrid MobilityLabs](https://mobilitylabs.emtmadrid.es/) for providing the data and [documentation](https://apidocs.emtmadrid.es/).
