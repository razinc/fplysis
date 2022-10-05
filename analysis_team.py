from custom.util import MkdirOutput
from custom.user import User
from custom.players import Players
from custom.constant import Gameweek

MkdirOutput.create_output_dir()

with open("output/analysis_team.txt", "w") as f:
    f.write(f"Name           : {User.name}\n")
    f.write(f"Current GW     : {Gameweek.current_gw}\n")
    f.write(f"Money Remaining: {User.in_the_bank}\n\n")

    user_players = Players(fpl_ids = User.team)
    
    user_perf = user_players.sort_by_total_pts_prev_n_gw()
    f.write("Performance:\n")
    f.write(user_players.get_table(stats = user_perf))
    
    not_user_players = Players(skips = User.team)

    not_user_perf = not_user_players.sort_by_total_pts_prev_n_gw()
    f.write("\n\nWatchlist (Performance):\n")
    f.write(not_user_players.get_table(stats = not_user_perf, top = 10))
    
    not_user_fda = not_user_players.sort_by_fda()
    f.write("\n\nWatchlist (Fixture):\n")
    f.write(not_user_players.get_table(stats = not_user_fda, top = 10))

    not_user_sum_xg_xa = not_user_players.sort_by_sum_xg_xa()
    f.write("\n\nWatchlist (xG + xA):\n")
    f.write(not_user_players.get_table(stats = not_user_sum_xg_xa, top = 10))
  
    not_user_xpts = not_user_players.sort_by_xpts()
    f.write("\n\nWatchlist (xP):\n")
    f.write(not_user_players.get_table(stats = not_user_xpts, top = 10))

    f.write("\n")
