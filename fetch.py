import aiohttp

async def api_call(url: str, params: dict = None):
    headers = {
        "Accept": "application/json",
    }
    print(f"Fetching URL: {url} with params: {params}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            return data