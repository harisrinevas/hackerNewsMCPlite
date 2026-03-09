from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP, Context
from main import (
    get_latest_item, get_top500_stories, find_item_detail,
    get_new_stories, get_best_stories, get_ask_stories,
    get_show_stories, get_job_stories, get_items_concurrently,
    HNResponse
)
import httpx
from typing import Optional, List


@asynccontextmanager
async def lifespan(_server: FastMCP):
    async with httpx.AsyncClient(timeout=10.0, headers={'User-Agent': 'Mozilla/5.0'}) as client:
        yield {"client": client}


mcp = FastMCP("hacker-news-server", lifespan=lifespan)


@mcp.tool()
async def HN_latest_item(ctx: Context) -> int:
    """
    Get the item_id of the latest item on Hacker News.
    item_id is an integer. Use HN_find_item_details to get full details.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_latest_item(client=client)


@mcp.tool()
async def HN_get_top_stories(ctx: Context, limit: int = 10) -> List[int]:
    """
    Get item_ids of the top N stories on Hacker News (default 10, max 500).
    Use HN_get_stories_with_details to fetch full details in one call.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_top500_stories(client=client, limit=limit)


@mcp.tool()
async def HN_get_new_stories(ctx: Context, limit: int = 10) -> List[int]:
    """
    Get item_ids of the newest N stories on Hacker News (default 10, max 500).
    Use HN_get_stories_with_details to fetch full details in one call.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_new_stories(client=client, limit=limit)


@mcp.tool()
async def HN_get_best_stories(ctx: Context, limit: int = 10) -> List[int]:
    """
    Get item_ids of the best N stories on Hacker News (default 10, max 500).
    Use HN_get_stories_with_details to fetch full details in one call.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_best_stories(client=client, limit=limit)


@mcp.tool()
async def HN_get_ask_stories(ctx: Context, limit: int = 10) -> List[int]:
    """
    Get item_ids of the top N Ask HN stories (default 10, max 200).
    Use HN_get_stories_with_details to fetch full details in one call.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_ask_stories(client=client, limit=limit)


@mcp.tool()
async def HN_get_show_stories(ctx: Context, limit: int = 10) -> List[int]:
    """
    Get item_ids of the top N Show HN stories (default 10, max 200).
    Use HN_get_stories_with_details to fetch full details in one call.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_show_stories(client=client, limit=limit)


@mcp.tool()
async def HN_get_job_stories(ctx: Context, limit: int = 10) -> List[int]:
    """
    Get item_ids of the latest N job postings on Hacker News (default 10, max 200).
    Use HN_get_stories_with_details to fetch full details in one call.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_job_stories(client=client, limit=limit)


@mcp.tool()
async def HN_find_item_details(ctx: Context, item_id: int) -> Optional[HNResponse]:
    """
    Get full details of a Hacker News item by item_id.
    Returns title, url, score, author, type, kids, and more.
    Returns None if the item is deleted or does not exist.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await find_item_detail(item_id=item_id, client=client)


@mcp.tool()
async def HN_get_stories_with_details(ctx: Context, item_ids: List[int]) -> List[Optional[HNResponse]]:
    """
    Fetch full details for a list of Hacker News item_ids concurrently.
    Much faster than calling HN_find_item_details one at a time.
    Pass a list of item_ids obtained from any of the story list tools.
    Returns None for deleted or non-existent items.
    """
    client = ctx.request_context.lifespan_context["client"]
    return await get_items_concurrently(item_ids=item_ids, client=client)


if __name__ == "__main__":
    mcp.run()
