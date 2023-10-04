import asyncio
import aiohttp
from fpl import FPL

async def get_teams():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        teams = await fpl.get_teams(return_json = True)
    return teams

def builder():
    teams = {}
    for team in asyncio.run(get_teams()):
        teams[team["id"]] = {"short_name": team["short_name"]}
    return teams

teams = builder()
