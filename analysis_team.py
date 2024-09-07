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

    user_players.sort_by_total_pts_prev_n_gw()
    f.write("Performance:\n")
    f.write(user_players.get_table())

    not_user_players = Players(skips=user.team, tqdm_desc="Analysing all players")

    not_user_players.sort_by_total_pts_prev_n_gw()
    f.write("\n\nWatchlist (Performance):\n")
    f.write(not_user_players.get_table(top=10))

    # copy of not_user_players is required because sort_by_fda() works by sort_by_total_pts_prev_n_gw() first and filter players with hard fixture.
    # if a copy is not created, subsequent sorts are not accurate because some players are filtered
    fda = deepcopy(not_user_players)
    fda.sort_by_fda()
    if len(fda.stats) > 0:
        f.write("\n\nWatchlist (Fixture):\n")
        f.write(fda.get_table(top=10))

    not_user_players.sort_by_xgi()
    f.write("\n\nWatchlist (xGI):\n")
    f.write(not_user_players.get_table(top=10))

    not_user_players.sort_by_xpts()
    f.write("\n\nWatchlist (xP):\n")
    f.write(not_user_players.get_table(top=10))

    f.write("\n")
