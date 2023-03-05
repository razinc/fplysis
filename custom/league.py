import asyncio
from collections import Counter
from itertools import islice

import aiohttp
import fpl_credentials
from fpl import FPL
from tqdm import tqdm

from custom.constant import OVERALL_LEAGUE_ID


class League:
    def __init__(self, league_id=OVERALL_LEAGUE_ID):
        self.league_id = league_id
        asyncio.run(self.set_attr())

    async def set_attr(self):
        top_10k = []
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            await fpl.login(
                email=fpl_credentials.EMAIL, password=fpl_credentials.PASSWORD
            )
            league = await fpl.get_classic_league(self.league_id)
            self.name = league.league["name"]
            for page in tqdm(range(1, 203, 1), desc="Parsing top 10k managers      "):
                rank = await league.get_standings(
                    page=page, page_new_entries=1, phase=1
                )
                for row in rank["results"]:
                    top_10k.append(row["entry"])
            self.top_10k = top_10k[0:10000]

    async def get_top_10k_ownership(self):
        top_10k_ownership = []
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            for user_id in tqdm(self.top_10k, desc="Parsing top 10k picks         "):
                user = await fpl.get_user(user_id)
                picks = await user.get_picks()
                team = [i["element"] for i in picks[list(picks.keys())[-1]]]
                top_10k_ownership = top_10k_ownership + team
        top_10k_ownership = dict(Counter(top_10k_ownership))
        top_10k_ownership = dict(
            sorted(top_10k_ownership.items(), key=lambda x: x[1], reverse=True)
        )
        top_10k_ownership = dict(islice(top_10k_ownership.items(), 50))
        top_10k_ownership = {
            k: round(v / len(self.top_10k) * 100, 2)
            for k, v in top_10k_ownership.items()
        }
        self.top_10k_ownership = top_10k_ownership
