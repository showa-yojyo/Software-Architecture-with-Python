# Code Listing #13

"""

Fetch URLs asynchronously - using aiohttp and print response.

"""

# async_fetch_url.py
import asyncio
import aiohttp
import async_timeout


async def fetch_page(session, url, timeout=60):
    """ Asynchronous URL fetcher """

    with async_timeout.timeout(timeout):
        async with session.get(url) as response:
            return response


urls = ('http://www.google.com',
        'http://www.yahoo.com',
        'http://www.facebook.com',
        'http://www.reddit.com',
        'http://www.twitter.com')

# TODO: 修正方法がわからない

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_page(session, x)) for x in urls]

        # Wait for tasks
        done, pending = await asyncio.wait(tasks, timeout=120)

        for future in done:
            response = future.result()
            print(response)
            response.close()

asyncio.run(main())
