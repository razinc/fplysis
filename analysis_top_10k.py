import asyncio

import custom.util
from custom.constant import Gameweek
from custom.league import League
from custom.players import Players
from custom.user import User

with open("output/analysis_top_10k.txt", "w") as f:
    league = League()

    f.write(f"League Name    : {league.name}\n")
    f.write(f"Current GW     : {Gameweek.CURRENT_GW}\n\n")

    asyncio.run(league.get_top_10k_ownership())
    top_10k_players = Players(ownership=league.top_10k_ownership)
    f.write(top_10k_players.get_table())
