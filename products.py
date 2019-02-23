import asyncio
import json
import time

import aiohttp
import aiofiles

timeout = aiohttp.ClientTimeout(total=20)

URL = 'https://www.honestbee.tw/api/api/stores/%s/directory'

cookies = {
    'ajs_group_id': 'null',
    'appier_tp': '',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Accept': 'application/vnd.honestbee+json;version=2',
    'Referer': 'https://www.honestbee.tw/zh-TW/food/restaurants/the-kaffa-lovers',
    'Connection': 'keep-alive',
}

async def fetch_products(session, store_id, cat_id):
    url = 'https://www.honestbee.tw/api/api/categories/%s/products?storeId=%s&page=1'%(cat_id, store_id)
    cnt = 0
    while cnt < 5:
        try:
            t1 = time.time()
            async with session.get(url, headers=headers, cookies=cookies, timeout=timeout) as response:
                data = await response.text()
                t2 = time.time()
                print("[%s][%s][%s]%s secs"%(store_id, cat_id, cnt, t2-t1))
                # print(data)
                data = json.loads(data)
                # print(data)
        except Exception as e:
            # print("[%s][%s]%s"%(params['page'], cnt, e))
            print(e)
            cnt += 1
            continue
        async with aiofiles.open("data/products/%s.json"%(f"{store_id}-{cat_id}"), mode='w') as f:
            contents = await f.write(json.dumps(data, ensure_ascii=False))
        return data

async def fetch_cats(session, url, store_id):
    url = URL%store_id
    cnt = 0
    while cnt < 5:
        try:
            async with session.get(url, headers=headers, cookies=cookies, timeout=timeout) as response:
                t1 = time.time()
                data = await response.text()
                t2 = time.time()
                print("[%s][%s][%s]"%(store_id, cnt, t2-t1))
                # print(data)
                data = json.loads(data)
                cats = [x.get('id') for x in data.get('departments')[0].get('categories')]
                # print(cats)
                await asyncio.gather(*[fetch_products(session, store_id, cat_id) for cat_id in cats])
        except Exception as e:
            # print("[%s][%s]%s"%(params['page'], cnt, e))
            cnt += 1
            continue
        # async with aiofiles.open("data/products/%s.json"%pg, mode='w') as f:
        #     contents = await f.write(json.dumps(data, ensure_ascii=False))
        return data

async def main():
    store_ids = [x.strip() for x in open('./store_ids.txt').readlines()]
    async with aiohttp.ClientSession() as session:
        wg = []
        for store_id in store_ids:
            if len(wg) >= 100:
                await asyncio.gather(*wg)
                wg = []
            wg.append(fetch_cats(session, URL, store_id))
        await asyncio.gather(*wg)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
