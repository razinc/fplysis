import asyncio
import time
import fpl_custom_functions
from tqdm import tqdm

start_time = time.time()

my_team = asyncio.run(fpl_custom_functions.get_my_team_async())

current_gameweek = fpl_custom_functions.get_current_gameweek()
# print(f"Curent GW: {current_gameweek}\n")

previous_three_gameweeks = [current_gameweek, current_gameweek - 1, current_gameweek - 2]
previous_three_gameweeks = [gw for gw in previous_three_gameweeks if gw > 0 ]
previous_three_gameweeks.reverse()

# print("Analysing my team.")
players_performance = []
for player in tqdm(my_team, desc = "Analysing my team    "):
    player_performance = fpl_custom_functions.get_player_analysis(player["element"], current_gameweek)
    players_performance.append(player_performance)
players_performance = sorted(players_performance, key = lambda x: list(x.values())[0]["total_points_previous_three_gameweeks"], reverse = True)
with open("output/analysis_my_team.txt", "w") as f:
    # print("Performance:")
    f.write(f"Current GW: {current_gameweek}\n\n")
    f.write("Performance:\n")
    player_table = fpl_custom_functions.get_player_table(players_performance, current_gameweek, previous_three_gameweeks)
    f.write(player_table)
    # fpl_custom_functions.get_player_table(players_performance, current_gameweek, previous_three_gameweeks)

# print("\nAnalysing all players.")
not_my_team = []
players = asyncio.run(fpl_custom_functions.get_all_players())
for player in tqdm(players, desc = "Analysing all players"):
    try:
        player_element = player.history[-1]["element"]
    except(IndexError):
        # player doesn't has any data yet
        continue
    if player_element in [i["element"] for i in my_team]:
       pass
    else:
        player_performance = fpl_custom_functions.get_player_analysis(player_element, current_gameweek)
        not_my_team.append(player_performance)
not_my_team = sorted(not_my_team, key = lambda x: list(x.values())[0]["total_points_previous_three_gameweeks"], reverse = True)
not_my_team = not_my_team[0: 10]
with open("output/analysis_my_team.txt", "a") as f:
    f.write("\n\nWatchlist:\n")
    player_table = fpl_custom_functions.get_player_table(not_my_team, current_gameweek, previous_three_gameweeks)
    f.write(player_table)
    f.write("\n")

end_time = time.time()
run_time = fpl_custom_functions.get_run_time(start_time, end_time)
print("\nRun time:")
print(run_time)

