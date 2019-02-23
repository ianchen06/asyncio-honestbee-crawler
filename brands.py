import asyncio
import json

import aiohttp
import aiofiles

URL = 'https://www.honestbee.tw/api/api/brands'

cookies = {
    'appier_tp': '',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Accept': 'application/vnd.honestbee+json;version=3',
    'Referer': 'https://www.honestbee.tw/zh-TW/food',
    'Connection': 'keep-alive',
}

params_tuple = (
    ('countryCode', 'TW'),
    ('page', '3'),
    ('serviceType', 'food'),
    ('deliveryType', 'asap'),
    ('withHonestbeeMemberStore', 'true'),
    ('pageSize', '12'),
    ('uuid', ''),
    ('userId', ''),
    ('platform', 'Web'),
)

async def fetch(session, url, pg):
    params = {k:v for k,v in params_tuple}
    params['page'] = pg
    cnt = 0
    while cnt < 5:
        print("[%s][%s]"%(params['page'], cnt))
        try:
            async with session.get(url, params=params, headers=headers, cookies=cookies) as response:
                data = await response.text()
                # print(data)
                data = json.loads(data)
                if not data.get('brands'):
                    return
        except Exception as e:
            # print("[%s][%s]%s"%(params['page'], cnt, e))
            cnt += 1
            continue
        async with aiofiles.open("data/brands/%s.json"%pg, mode='w') as f:
            contents = await f.write(json.dumps(data, ensure_ascii=False))
        return data

async def main():
    async with aiohttp.ClientSession() as session:
        wg = []
        for pg in range(1,256):
            if len(wg) >= 100:
                await asyncio.gather(*wg)
                wg = []
            wg.append(fetch(session, URL, pg))
        await asyncio.gather(*wg)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
