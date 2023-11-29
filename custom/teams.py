import asyncio

import aiohttp
from fpl import FPL


async def get_teams():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        teams = await fpl.get_teams(return_json=True)
    return teams


async def get_fdr():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        fdr = await fpl.FDR()
    return fdr


def builder():
    fdr = asyncio.run(get_fdr())

    # temporary workaround to fix wrong team mapping
    try:
        fdr["Sheffield Utd"] = fdr["Southampton"]
        del fdr["Southampton"]
    except KeyError:
        pass

    teams = {}
    for team in asyncio.run(get_teams()):
        teams[team["id"]] = {
            "short_name": team["short_name"],
            "FDR_H": round(fdr[team["name"]]["all"]["H"], 2),
            "FDR_A": round(fdr[team["name"]]["all"]["A"], 2),
        }
    return teams


teams = builder()
