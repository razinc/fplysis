from copy import deepcopy

import custom.util
from custom.constant import Gameweek
from custom.players import Players
from custom.user import User

with open("output/analysis_team.txt", "w") as f:
    user = User(
        log_in=custom.util.UserAuthArg.log_in, user_id=custom.util.UserAuthArg.user_id
    )

    f.write(f"Name           : {user.name}\n")
    f.write(f"Current GW     : {Gameweek.CURRENT_GW}\n")
    f.write(f"Money Remaining: {user.in_the_bank}\n\n")

    user_players = Players(fpl_ids=user.team, tqdm_desc="Analysing user's team")

    user_players.sort_by_value()
    f.write("Performance:\n")
    f.write(user_players.get_table())

    not_user_players = Players(skips=user.team, tqdm_desc="Analysing all players")

    not_user_players.sort_by_value()
    f.write("\n\nWatchlist (Value):\n")
    f.write(not_user_players.get_table(top=20))

    f.write("\n")
