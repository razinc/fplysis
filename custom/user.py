import asyncio

import aiohttp
from fpl import FPL


class User:
    def __init__(self, log_in=None, user_id=None):
        self.log_in = log_in
        self.user_id = user_id
        asyncio.run(self.set_attr())

    async def set_attr(self):
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            if self.log_in == True:
                import fpl_credentials

                await fpl.login(
                    email=fpl_credentials.EMAIL, password=fpl_credentials.PASSWORD
                )
                user = await fpl.get_user()
                team = [i["element"] for i in await user.get_team()]
                transfers_status = await user.get_transfers_status()
                in_the_bank = transfers_status["bank"] / 10
            else:
                user = await fpl.get_user(self.user_id)
                picks = await user.get_picks()
                team = [i["element"] for i in picks[list(picks.keys())[-1]]]
                in_the_bank = "This is only available through login"
            self.name = f"{user.player_first_name}, {user.player_last_name}"
            self.team_name = user.name
            self.team = team
            self.in_the_bank = in_the_bank
