import httpx
import random
import asyncio

class ProxyManager:
    def __init__(self, index=-1, proxy=['']):
        self.index = index
        self.proxy = proxy
        with open("data/links.txt", "r") as links:
            links = [line.strip() for line in links]
            for link in links:
                print(f'Adding... {link}')
                try:
                    self.proxy.extend(httpx.get(link, timeout=5.0).text.split('\n'))
                except Exception as e:
                    print(e)
        self.proxy = list(set(self.proxy))
        self.proxies_number = len(self.proxy)
        print('Number of proxies:', self.proxies_number)
    
    async def async_random_proxy(self):
        if not self.proxy:
            return None
        proxy = await asyncio.to_thread(random.choice, self.proxy)
        if proxy and '://' not in proxy:
            proxy = 'http://' + proxy
        return proxy
