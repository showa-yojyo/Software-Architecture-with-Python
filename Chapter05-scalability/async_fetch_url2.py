#!/usr/bin/env python
# Code Listing #14
"""

Fetch URLs asynchronously and parse their responses - using aiohttp module

"""

# async_fetch_url2.py
import asyncio
import aiohttp
import async_timeout


async def fetch_page(session, url, timeout=60):
    """ Asynchronous URL fetcher """

    with async_timeout.timeout(timeout):
        async with session.get(url) as response:
            return response


async def parse_response(futures):

    for future in futures:
        response = await future
        data = await response.text()
        print('Response for URL', response.url,
              '=>', response.status, len(data))
        response.close()

urls = ('http://www.google.com',
        'http://www.yahoo.com',
        'http://www.facebook.com',
        'http://www.reddit.com',
        'http://www.twitter.com')

async def main():
    async with aiohttp.ClientSession() as session:
        # Wait for futures
        tasks = [asyncio.create_task(fetch_page(session, x)) for x in urls]
        done, pending = await asyncio.wait(tasks, timeout=300)
        await parse_response(done)

asyncio.run(main())
