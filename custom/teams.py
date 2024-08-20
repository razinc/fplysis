import asyncio

import aiohttp
from fpl import FPL


def builder():
    fdr = asyncio.run(get_fdr())

    teams = {}
    for team in asyncio.run(get_teams()):
        if len(fdr) == 0:
            fdr_h = team["strength"]
            fdr_a = fdr_h  # only 1 value is provided in the api
        else:
            fdr_h = round(fdr[team["name"]]["all"]["H"], 2)
            fdr_a = round(fdr[team["name"]]["all"]["A"], 2)

        teams[team["id"]] = {
            "short_name": team["short_name"],
            "FDR_H": fdr_h,
            "FDR_A": fdr_a,
        }
    return teams


async def get_fdr():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        fdr = await fpl.FDR()
    return fdr


async def get_teams():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        teams = await fpl.get_teams(return_json=True)
    return teams


teams = builder()
