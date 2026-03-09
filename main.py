from typing import List, Optional
from pydantic import BaseModel, ValidationError
import httpx
import asyncio


class HNResponse(BaseModel):
    id:int
    deleted:Optional[bool] = None
    type:str
    by: Optional[str] = None
    time: Optional[int] = None
    text: Optional[str] = None
    dead: Optional[bool] = None
    parent: Optional[int] = None
    poll: Optional[int] = None
    kids: Optional[List[int]] = None
    url: Optional[str] = None
    score: Optional[int] = None
    title: Optional[str] = None
    parts: Optional[List[int]] = None
    descendants: Optional[int] = None


async def main():
    async with httpx.AsyncClient(timeout=5.0, headers = {'User-Agent': 'Mozilla/5.0'}) as client:
        print(await get_latest_item(client))
        top_stores_list: List[int] = await get_top500_stories(client)
        print(top_stores_list)
        data = await find_item_detail(top_stores_list[0], client)
        if data:
            print(data.title, data.url)
        else:
            print('None Data found')

        story1 = await get_new_stories(client)
        print(await get_items_concurrently(story1, client))


async def get_latest_item(client: httpx.AsyncClient) -> int:
    url = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        raise RuntimeError("Request timed out fetching latest item")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"HN API returned {e.response.status_code} for latest item")
    except httpx.RequestError as e:
        raise RuntimeError(f"Network error fetching latest item: {e}")


async def _fetch_stories(endpoint: str, client: httpx.AsyncClient, limit: int) -> List[int]:
    url = f'https://hacker-news.firebaseio.com/v0/{endpoint}.json'
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()[:limit]
    except httpx.TimeoutException:
        raise RuntimeError(f"Request timed out fetching {endpoint}")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"HN API returned {e.response.status_code} for {endpoint}")
    except httpx.RequestError as e:
        raise RuntimeError(f"Network error fetching {endpoint}: {e}")


async def get_top500_stories(client: httpx.AsyncClient, limit: int = 10) -> List[int]:
    return await _fetch_stories('topstories', client, limit)

async def get_new_stories(client: httpx.AsyncClient, limit: int = 10) -> List[int]:
    return await _fetch_stories('newstories', client, limit)

async def get_best_stories(client: httpx.AsyncClient, limit: int = 10) -> List[int]:
    return await _fetch_stories('beststories', client, limit)

async def get_ask_stories(client: httpx.AsyncClient, limit: int = 10) -> List[int]:
    return await _fetch_stories('askstories', client, limit)

async def get_show_stories(client: httpx.AsyncClient, limit: int = 10) -> List[int]:
    return await _fetch_stories('showstories', client, limit)

async def get_job_stories(client: httpx.AsyncClient, limit: int = 10) -> List[int]:
    return await _fetch_stories('jobstories', client, limit)


async def get_items_concurrently(item_ids: List[int], client: httpx.AsyncClient) -> List[Optional[HNResponse]]:
    return list(await asyncio.gather(*[find_item_detail(item_id, client) for item_id in item_ids]))


async def find_item_detail(item_id: int, client: httpx.AsyncClient) -> Optional[HNResponse]:
    url = f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json'
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        if data is None:
            return None
        return HNResponse(**data)
    except httpx.TimeoutException:
        raise RuntimeError(f"Request timed out fetching item {item_id}")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"HN API returned {e.response.status_code} for item {item_id}")
    except httpx.RequestError as e:
        raise RuntimeError(f"Network error fetching item {item_id}: {e}")
    except ValidationError as e:
        raise RuntimeError(f"Unexpected response format for item {item_id}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
