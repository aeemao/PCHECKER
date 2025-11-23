import re
import httpx
import asyncio
import datetime

from proxy import ProxyManager

async def test_proxy(proxy, semaphore):
    async with semaphore:
        try:
            if re.search(r'://0[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:', proxy):
                return
                
            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(
                    retries=1,
                    proxy=proxy), 
                timeout=2.0
            ) as client:
                response = await client.get('https://httpbin.org/ip')
                print(f"✅ {response.status_code} {proxy} {datetime.datetime.now()}")
                with open("data/proxies.txt", "a") as file:
                    file.write(f'{proxy}\n')
        except Exception:
            pass

async def test_proxies(manager):
    semaphore = asyncio.Semaphore(200)
    print('Loading proxies...')
    proxies = [await manager.async_random_proxy() for i in range(manager.proxies_number)]
    print('Creating tasks...')
    tasks = [test_proxy(proxy, semaphore) for proxy in proxies]
    print('Starting...')
    await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    manager = ProxyManager()
    await test_proxies(manager)

if __name__ == '__main__':
    asyncio.run(main())