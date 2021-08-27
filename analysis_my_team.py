# import aiohttp
# import asyncio
# import fpl_credentials
# import time
# import itertools
# import fpl_custom_functions
# from fpl import FPL
# from prettytable import PrettyTable
# from collections import OrderedDict
# from operator import getitem

start_time = time.time()

my_team = asyncio.run(fpl_custom_functions.get_my_team_async())

current_gameweek = fpl_custom_functions.get_current_gameweek()
print(f"Curent GW: {current_gameweek}\n")

previous_three_gameweeks = [current_gameweek, current_gameweek - 1, current_gameweek - 2]
previous_three_gameweeks = [gw for gw in previous_three_gameweeks if gw > 0 ]
previous_three_gameweeks.reverse()

players_performance = []
for player in my_team:
    player_performance = fpl_custom_functions.get_player_analysis(player["element"], current_gameweek)
    players_performance.append(player_performance)
players_performance = sorted(players_performance, key = lambda x: list(x.values())[0]["ttl_pts_previous_three_gameweeks"], reverse = True)
print("Performance:")
fpl_custom_functions.print_player_table(players_performance, current_gameweek, previous_three_gameweeks)

# not_my_team = []
# for player in players:
#     player_element = player.__dict__["history"][-1]["element"]
#     if any([True if x["element"] == player_element else False for x in team]):
#        pass
#     else:
#         player_performance = asyncio.run(get_player_analysis(player[player_element]))
#         not_my_team.append(player_performance)
# not_my_team = sorted(not_my_team, key = lambda x: list(x.values())[0]["ttl_pts_previous_three_gameweeks"], reverse = True)
# not_my_team = not_my_team[0: 10]
# print("\nWatchlist:")
# print_player_table(not_my_team)

# TODO: check if there are DGW games in the next 5 gameweek & suggest top performing players

end_time = time.time()
run_time = end_time - start_time
if run_time < 60:
    run_time = round(run_time, 2)
    print(f"\nTime Taken: {run_time} s")
else:
    run_time = run_time / 60
    run_time = round(run_time, 2)
    print(f"\nTime Taken: {run_time} min")

