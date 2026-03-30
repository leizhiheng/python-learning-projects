import time
import requests

def fetch_url(url):
    print(f"开始获取:{url}")
    time.sleep(2)
    print(f"完成获取：{url}")
    return f"来自 {url} 的数据"

def main_sync():
    urls = ['https://example.com/1', 'https://example.com/2', 'https://example.com/3']
    results = []
    start = time.time()

    for url in urls:
        result = fetch_url(url)
        results.append(result)
    
    end = time.time()
    print(f"同步版本总耗时：{end - start:.2f} 秒")
    print(f"结果：{results}")

import asyncio
import aiohttp

async def fetch_url_async(session, url):
    print(f"开始异步获取：{url}")
    async with session.get(url) as response:
        await asyncio.sleep(2)
        text = await response.text()
        print(f"完成异步请求：{url}")
        return f"来自 {url} 的数据（长度：{len(text)})"

async def main_async():
    urls = ['https://httpbin.org/get', 'https://httpbin.org/delay/1', 'https://httpbin.org/headers']

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_url_async(session, url))
            tasks.append(task)
        
        print("所有任务已创建，开始并发执行")

        results = await asyncio.gather(*tasks)

        return results

if __name__ == "__main__":
    # main_sync()
    
    start = time.time()
    final_results = asyncio.run(main_async())
    end = time.time()
    
    print(f"\n异步版本总耗时：{end - start:.2f} 秒")
    for res in final_results:
        print(res)