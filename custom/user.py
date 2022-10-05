import aiohttp
import asyncio
from fpl import FPL
from custom.util import AnalTeamArg
import fpl_credentials


class User:
    async def set_attr():
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            if AnalTeamArg.log_in == True:
                await fpl.login(
                    email=fpl_credentials.EMAIL, password=fpl_credentials.PASSWORD
                )
                user = await fpl.get_user()
                team = [i["element"] for i in await user.get_team()]
                transfers_status = await user.get_transfers_status()
                in_the_bank = transfers_status["bank"] / 10
            else:
                user = await fpl.get_user(AnalTeamArg.user_id)
                picks = await user.get_picks()
                team = [i["element"] for i in picks[list(picks.keys())[-1]]]
                in_the_bank = "This is only available through login"
            name = f"{user.player_first_name}, {user.player_last_name}"
            team_name = user.name
            team = team
            return {
                "name": name,
                "team_name": team_name,
                "team": team,
                "in_the_bank": in_the_bank,
            }

    name, team_name, team, in_the_bank = asyncio.run(set_attr()).values()
