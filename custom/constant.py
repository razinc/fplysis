import aiohttp
import asyncio
from fpl import FPL
import fpl_credentials
import pandas as pd
from understat import Understat


class Gameweek:
    async def set_attr():
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            gameweeks = await fpl.get_gameweeks()
            for gameweek in gameweeks:
                if gameweek.finished == True or gameweek.is_current == True:
                    current_gw = gameweek.id
                no_of_prev_gws = 3
                prev_n_gws = [
                    i
                    for i in range(current_gw, current_gw - no_of_prev_gws, -1)
                    if i > 0
                ]
                prev_n_gws.reverse()
                no_of_next_gws = 5
                next_n_gws = [
                    i for i in range(current_gw + 1, current_gw + no_of_next_gws + 1)
                ]
        return {
            "current_gw": current_gw,
            "no_of_prev_gws": no_of_prev_gws,
            "prev_n_gws": prev_n_gws,
            "no_of_next_gws": no_of_next_gws,
            "next_n_gws": next_n_gws,
        }

    current_gw, no_of_prev_gws, prev_n_gws, no_of_next_gws, next_n_gws = asyncio.run(
        set_attr()
    ).values()
    next_gw = current_gw + 1
    season = "2022"


class FplToUnderstat:
    def set_attr():
        df_understat = pd.read_csv(
            "https://raw.githubusercontent.com/ChrisMusson/FPL-ID-Map/main/Understat.csv"
        )
        df_season = pd.read_csv(
            "https://raw.githubusercontent.com/ChrisMusson/FPL-ID-Map/main/FPL/22-23.csv"
        )
        mapping = {}
        for row in df_understat.values:
            code, first_name, second_name, web_name, understat = row
            try:
                understat = int(understat)
            except ValueError:
                # player doesn't has understat id
                pass
            try:
                srs_season_code = df_season["code"]
                player_index = srs_season_code[srs_season_code == code].index[0]
                player_id = df_season["22-23"].iloc[player_index]
            except IndexError:
                # player is available in df_understat but not in df_season. player is already retired.
                continue
            mapping[player_id] = {
                "code": code,
                "first_name": first_name,
                "second_name": second_name,
                "web_name": web_name,
                "understat": understat,
            }
        return mapping

    mapping = set_attr()

    # async def get_player_grouped_stats(understat_id):
    #     async with aiohttp.ClientSession() as session:
    #         understat = Understat(session)
    #         return await understat.get_player_grouped_stats(understat_id)