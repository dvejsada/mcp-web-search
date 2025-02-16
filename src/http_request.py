import httpx

async def make_request(url, params:dict = None):
    async with httpx.AsyncClient() as client:
        response = await client.request(url=url, method="GET", params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()