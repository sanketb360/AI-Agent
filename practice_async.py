# practice_async.py
import asyncio
import ssl

import aiohttp
import certifi

async def fetch_example():
    """Practice async HTTP."""
    url = "https://api.github.com/repos/python/cpython"

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(url) as response:
            data = await response.json()
            print(f"✅ Fetched: {data['name']}")
            return data

# Run it
asyncio.run(fetch_example())