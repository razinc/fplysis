import asyncio
import aiohttp
from fpl import FPL


class User:
    def __init__(self, log_in=None, user_id=None):
        self.log_in = log_in
        self.user_id = user_id
        self.builder()

    def builder(self):
        user = asyncio.run(self.get_user())
        self.name = f'{user["player_first_name"]}, {user["player_last_name"]}'
        self.team_name = user["name"]
        self.in_the_bank = "This is only available through login"
        picks = asyncio.run(self.get_picks())
        self.team = [i["element"] for i in picks[list(picks.keys())[-1]]]

    async def get_user(self):
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            user = await fpl.get_user(self.user_id, return_json=True)
        return user

    async def get_picks(self):
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            user = await fpl.get_user(self.user_id)
            picks = await user.get_picks()
        return picks
