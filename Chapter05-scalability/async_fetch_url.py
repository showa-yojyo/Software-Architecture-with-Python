#!/usr/bin/env python
# Code Listing #13
"""

Fetch URLs asynchronously - using aiohttp and print response.

"""

# async_fetch_url.py
import asyncio
import aiohttp # third-party
import async_timeout # third-party


async def fetch_page(session, url, timeout=60):
    """ Asynchronous URL fetcher """

    with async_timeout.timeout(timeout):
        async with session.get(url) as response:
            return response

# リモートがバラバラだがセッションの恩恵に預かれるのだろうか
urls = ('http://www.google.com',
        'http://www.yahoo.com',
        'http://www.facebook.com',
        'http://www.reddit.com',
        'http://www.twitter.com')

async def main():
    # このセッションの context manager はわかりやすい
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_page(session, x)) for x in urls]

        # Wait for tasks
        # すべてのタスクが終了かキャンセルしてから戻る
        done, pending = await asyncio.wait(tasks, timeout=120)

    # 終了したものをすべて出力する
    for future in done:
        await future
        response = future.result()
        #print(response)
        response.close()

asyncio.run(main())
print('Finish')
# RuntimeError: Event loop is closed
