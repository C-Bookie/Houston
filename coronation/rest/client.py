import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000') as resp:
            print(resp.status)
            print(await resp.text())

asyncio.run(main())
