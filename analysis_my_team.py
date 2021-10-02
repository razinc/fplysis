# TODO: reduce input for get_player_analysis
# TODO: reduce input for print_player_table
# TODO: add log decorator
# TODO: add time decorator
# TODO: fix 'Too Many Requests'
# TODO: check if there are DGW games in the next 5 gameweek & suggest top performing players
# TODO: run_time
# TODO: seperate get_my_team_async (error when async def calling another async def)
# TODO: difference between dir(object) or object.__dict__

import asyncio
import time
import fpl_custom_functions

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
players_performance = sorted(players_performance, key = lambda x: list(x.values())[0]["total_points_previous_three_gameweeks"], reverse = True)
print("Performance:")
fpl_custom_functions.print_player_table(players_performance, current_gameweek, previous_three_gameweeks)

not_my_team = []
players = asyncio.run(fpl_custom_functions.get_all_players())
for player in players:
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
print("\nWatchlist:")
fpl_custom_functions.print_player_table(not_my_team, current_gameweek, previous_three_gameweeks)

end_time = time.time()
run_time = end_time - start_time
if run_time < 60:
    run_time = round(run_time, 2)
    print(f"\nTime Taken: {run_time} s")
else:
    run_time = run_time / 60
    run_time = round(run_time, 2)
    print(f"\nTime Taken: {run_time} min")
