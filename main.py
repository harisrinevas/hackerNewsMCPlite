from typing import List, Optional
from pydantic import BaseModel
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

async def get_latest_item(client: httpx.AsyncClient)->int:
    url = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
    response = await client.get(url)
    response.raise_for_status()
    return response.json()

async def get_top500_stories(client: httpx.AsyncClient, limit: int=10)->List[int]:
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    response = await client.get(url)
    response.raise_for_status()
    data =response.json()
    return data[:limit]

async def find_item_detail(item_id: int, client: httpx.AsyncClient)->Optional[HNResponse]:
    url = f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json'
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()
    if data:
        return HNResponse(**data)
    return None

if __name__ == "__main__":
    asyncio.run(main())
