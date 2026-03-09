from mcp.server.fastmcp import FastMCP
from main import get_latest_item, get_top500_stories,find_item_detail, HNResponse
import httpx
from typing import Optional, List

mcp = FastMCP("hacker-news-server")
client = httpx.AsyncClient(timeout=10.0, headers={'User-Agent': 'Mozilla/5.0'})

@mcp.tool()
async def HN_lastest_item()->int:
    """
    Get the item_id of the lastest item in hackernews website.
    item_id is an integer and further details can be obtained by calling
    the function HN_find_item_details with item_id as parameter
    """
    return await get_latest_item(client=client)

@mcp.tool()
async def HN_get_top10_stories(limit:int=10)->List[int]:
    """
    Get a item_id of top 'N' news items based on limit(default to 10)
    from hackernews website.
    item_id is an integer and further details can be obtained by calling
    the function HN_find_item_details with item_id as parameter
    """
    return await get_top500_stories(client=client, limit=limit)

@mcp.tool()
async def HN_find_item_details(item_id: int)->Optional[HNResponse]:
    """
    Gets details of the hackernews item based on item_id provided to this 
    function. Item_id is an integer. This function returns output 
    in Optional[HNResponse] format. Key item in this list is url.
    The url usually leads to the item.
    """
    return await find_item_detail(item_id=item_id, client=client)

if __name__ == "__main__":
    mcp.run()