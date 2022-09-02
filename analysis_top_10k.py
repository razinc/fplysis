import asyncio
import time
import fpl_custom_functions
from collections import Counter
from itertools import islice
from tqdm import tqdm

start_time = time.time()

fpl_custom_functions.create_output_dir()

current_gameweek = fpl_custom_functions.get_current_gameweek()

prev_n_gw = fpl_custom_functions.get_prev_n_gw(
    current_gameweek
)

overall_league_id = 314
top_10k = asyncio.run(fpl_custom_functions.get_top_10k(overall_league_id))

fpl_understat_mapping = fpl_custom_functions.get_fpl_understat_mapping()

picks = []
for user_id in tqdm(top_10k, desc="Parsing top 10k managers' pick"):
    user = asyncio.run(fpl_custom_functions.get_my_user_id(user_id))
    team = user["my_team"]
    for i in team:
        picks.append(i["element"])
picks = dict(Counter(picks))
picks = dict(sorted(picks.items(), key=lambda x: x[1], reverse=True))
picks = dict(islice(picks.items(), 50))

players_performance = []
for element, total in tqdm(picks.items(), desc="Analysing top 50 players      "):
    player_performance = fpl_custom_functions.get_player_analysis(
        element, current_gameweek, prev_n_gw, fpl_understat_mapping
    )
    percentage_ownership = round(total / 10000 * 100, 2)
    player_performance[list(player_performance.keys())[0]][
        "percentage_ownership"
    ] = f"{percentage_ownership}%"
    players_performance.append(player_performance)
player_table = fpl_custom_functions.get_player_table(
    players_performance, current_gameweek, prev_n_gw
)

with open("output/analysis_top_10k.txt", "w") as f:
    f.write(f"Current GW: {current_gameweek}\n\n")
    f.write("Performance:\n")
    f.write(player_table)
    f.write("\n")

end_time = time.time()
run_time = fpl_custom_functions.get_run_time(start_time, end_time)
print("\nRun time:")
print(run_time)
