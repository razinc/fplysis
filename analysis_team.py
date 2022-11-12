import custom.util
from custom.user import User
from custom.constant import Gameweek
from custom.players import Players

with open("output/analysis_team.txt", "w") as f:
    user = User(log_in = custom.util.UserAuthArg.log_in, user_id = custom.util.UserAuthArg.user_id)
    
    f.write(f"Name           : {user.name}\n")
    f.write(f"Current GW     : {Gameweek.CURRENT_GW}\n")
    f.write(f"Money Remaining: {user.in_the_bank}\n\n")

    user_players = Players(fpl_ids=user.team)

    user_perf = user_players.sort_by_total_pts_prev_n_gw()
    f.write("Performance:\n")
    f.write(user_players.get_table(stats=user_perf))

    not_user_players = Players(skips=user.team)

    not_user_perf = not_user_players.sort_by_total_pts_prev_n_gw()
    f.write("\n\nWatchlist (Performance):\n")
    f.write(not_user_players.get_table(stats=not_user_perf, top=10))

    not_user_fda = not_user_players.sort_by_fda()
    if len(not_user_fda) > 0:
        f.write("\n\nWatchlist (Fixture):\n")
        f.write(not_user_players.get_table(stats=not_user_fda, top=10))

    not_user_sum_xg_xa = not_user_players.sort_by_sum_xg_xa()
    f.write("\n\nWatchlist (xG + xA):\n")
    f.write(not_user_players.get_table(stats=not_user_sum_xg_xa, top=10))

    not_user_xpts = not_user_players.sort_by_xpts()
    f.write("\n\nWatchlist (xP):\n")
    f.write(not_user_players.get_table(stats=not_user_xpts, top=10))

    f.write("\n")
