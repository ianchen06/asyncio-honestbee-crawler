import asyncio
import json

import aiohttp
import aiofiles

URL = 'https://www.honestbee.tw/api/api/dining_vouchers/onboarding_list'

cookies = {
    'appier_tp': '',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Accept': 'application/vnd.honestbee+json;version=2',
    'Referer': 'https://www.honestbee.tw/zh-TW/beehive/dine-in-restaurants',
    'Connection': 'keep-alive',
}

params_tuple = (
    ('countryCode', 'TW'),
    ('serviceType', 'food'),
    ('locale', 'zh-TW'),
    ('page', '1'),
    ('pageSize', '48'),
)

async def fetch(session, url, pg):
    params = {k:v for k,v in params_tuple}
    params['page'] = pg
    async with session.get(url, params=params, headers=headers, cookies=cookies) as response:
        data = await response.json()
    async with aiofiles.open("data/%s.json"%pg, mode='w') as f:
        contents = await f.write(json.dumps(data, ensure_ascii=False))
    return data

async def main():
    async with aiohttp.ClientSession() as session:
        for f in asyncio.as_completed([fetch(session, URL, pg) for pg in range(1, 50)]):
            print(await f)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
