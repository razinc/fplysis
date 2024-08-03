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
        if self.log_in:
            self.team = [i["element"] for i in asyncio.run(self.get_team())]
            self.in_the_bank = f'£{asyncio.run(self.get_transfers_status())["bank"] / 10}'
        else:
            picks = asyncio.run(self.get_picks())
            self.team = [i["element"] for i in picks[list(picks.keys())[-1]]]
            self.in_the_bank = "This is only available through login"

    async def get_user(self):
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            if self.log_in:
                import fpl_credentials
                await fpl.login(
                    email = fpl_credentials.EMAIL,
                    password = fpl_credentials.PASSWORD,
                    cookie = fpl_credentials.COOKIE,
                )
                user = await fpl.get_user(return_json = True)
            else:
                user = await fpl.get_user(self.user_id, return_json=True)
        return user

    async def get_picks(self):
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            user = await fpl.get_user(self.user_id)
            picks = await user.get_picks()
        return picks

    async def get_team(self):
        import fpl_credentials
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            await fpl.login(
                email = fpl_credentials.EMAIL,
                password = fpl_credentials.PASSWORD,
                cookie = fpl_credentials.COOKIE,
            )
            user = await fpl.get_user()
            team = await user.get_team()
        return team

    async def get_transfers_status(self):
        import fpl_credentials
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            await fpl.login(
                email = fpl_credentials.EMAIL,
                password = fpl_credentials.PASSWORD,
                cookie = fpl_credentials.COOKIE,
            )
            user = await fpl.get_user()
            transfer_status = await user.get_transfers_status()
        return transfer_status
