import asyncio
import time
import fpl_custom_functions
from tqdm import tqdm
import argparse

start_time = time.time()

parser = argparse.ArgumentParser(description = "Analyse FPL team")
required_args = parser.add_argument_group('at least one of these arguments are required')
required_args.add_argument("-id", "--user_id", type = int, help = "User ID. Can be obtained in FPL Points's URL.")
required_args.add_argument("-l", "--log_in", type = bool, help = "Enable login. Email & Password must be set in fpl_credentials.py.")
args = parser.parse_args()
if not any(vars(args).values()):
    parser.error("Either --user_id or --log_in must be parsed.")

fpl_custom_functions.create_output_dir()

if args.log_in == True:
    print("There is an issue with login feature. Please use --user_id instead. For more information: https://github.com/amosbastian/fpl/issues/120")
    exit()
    my_user = asyncio.run(fpl_custom_functions.get_my_user())
    my_full_name = my_user["my_full_name"]
    my_team = my_user["my_team"]
    my_money_remaining = my_user["my_money_remaining"]
else:
    pick = asyncio.run(fpl_custom_functions.get_picks_wrapper(args.user_id))
    my_team = pick[list(pick.keys())[-1]]

current_gameweek = fpl_custom_functions.get_current_gameweek()

previous_three_gameweeks = fpl_custom_functions.get_previous_three_gameweeks(current_gameweek)

players_performance = []
for player in tqdm(my_team, desc = "Analysing my team    "):
    player_performance = fpl_custom_functions.get_player_analysis(player["element"], current_gameweek, previous_three_gameweeks)
    players_performance.append(player_performance)
    
players_performance = sorted(players_performance, key = lambda x: list(x.values())[0]["total_points_previous_three_gameweeks"], reverse = True)
with open("output/analysis_my_team.txt", "w") as f:
    if args.log_in == True: 
        f.write(f"Name           : {my_full_name}\n")
        f.write(f"Current GW     : {current_gameweek}\n")
        f.write(f"Money Remaining: £{my_money_remaining}\n\n")
    f.write("Performance:\n")
    player_table = fpl_custom_functions.get_player_table(players_performance, current_gameweek, previous_three_gameweeks)
    f.write(player_table)
 
not_my_team = []
players = asyncio.run(fpl_custom_functions.get_players_wrapper())
for player in tqdm(players, desc = "Analysing all players"):
    try:
        player_element = player.history[-1]["element"]
    except(IndexError):
        # player doesn't has any data yet
        continue
    if player_element in [i["element"] for i in my_team]:
       pass
    else:
        player_performance = fpl_custom_functions.get_player_analysis(player_element, current_gameweek, previous_three_gameweeks)
        not_my_team.append(player_performance)
with open("output/analysis_my_team.txt", "a") as f:
    # sort based on total points
    f.write("\n\nWatchlist (Total Pts):\n")
    not_my_team_tp = sorted(not_my_team, key = lambda x: list(x.values())[0]["total_points_previous_three_gameweeks"], reverse = True)
    not_my_team_tp = not_my_team_tp[0: 10]
    player_table = fpl_custom_functions.get_player_table(not_my_team_tp, current_gameweek, previous_three_gameweeks)
    f.write(player_table)

    # sort based on expected points
    f.write("\n\nWatchlist (Expected Pts):\n")
    not_my_team_ep = sorted(not_my_team, key = lambda x: list(x.values())[0]["expected_points_next"], reverse = True)
    not_my_team_ep = not_my_team_ep[0: 10]
    player_table = fpl_custom_functions.get_player_table(not_my_team_ep, current_gameweek, previous_three_gameweeks)
    f.write(player_table)

    f.write("\n")

end_time = time.time()
run_time = fpl_custom_functions.get_run_time(start_time, end_time)
print("\nRun time:")
print(run_time)
