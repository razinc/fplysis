import asyncio
import time
import fpl_custom_functions
from collections import Counter
from itertools import islice
from tqdm import tqdm

start_time = time.time()

current_gameweek = fpl_custom_functions.get_current_gameweek()
# print(f"Curent GW: {current_gameweek}\n")

# TODO: put in def
previous_three_gameweeks = [current_gameweek, current_gameweek - 1, current_gameweek - 2]
previous_three_gameweeks = [gw for gw in previous_three_gameweeks if gw > 0 ]
previous_three_gameweeks.reverse()

top_10k = asyncio.run(fpl_custom_functions.get_top_10k(314))

picks = []
for user_id in tqdm(top_10k, desc = "Parsing top 10k managers' pick"):
    pick = asyncio.run(fpl_custom_functions.get_picks_async(user_id))
    team = pick[list(pick.keys())[-1]]
    for i in team:
        picks.append(i["element"])
picks = dict(Counter(picks))
picks = dict(sorted(picks.items(),key= lambda x: x[1], reverse = True))
picks = dict(islice(picks.items(), 50))

players_performance = []
for element, total in tqdm(picks.items(), desc = "Analysing top 50 players      "):
    pick = asyncio.run(fpl_custom_functions.get_picks_async(user_id))
    player_performance = fpl_custom_functions.get_player_analysis(element, current_gameweek)
    percentage_ownership = round(total/10000*100, 2)
    player_performance[list(player_performance.keys())[0]]["percentage_ownership"] = f"{percentage_ownership}%"
    players_performance.append(player_performance)
player_table = fpl_custom_functions.get_player_table(players_performance, current_gameweek, previous_three_gameweeks)

# with open("output/analysis_my_team.txt", "w") as f:
#     # print("Performance:")
#     player_table = fpl_custom_functions.get_player_table(players_performance, current_gameweek, previous_three_gameweeks)
#     f.write(player_table)
 

with open("output/analysis_top_10k.txt", "w") as f:
    f.write(f"Current GW: {current_gameweek}\n\n")
    f.write("Performance:\n")
    f.write(player_table)
    f.write("\n")

end_time = time.time()
run_time = fpl_custom_functions.get_run_time(start_time, end_time)
print("\nRun time:")
print(run_time)
   
