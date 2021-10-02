import asyncio
import time
import fpl_custom_functions
from collections import Counter
from itertools import islice

start_time = time.time()

current_gameweek = fpl_custom_functions.get_current_gameweek()
print(f"Curent GW: {current_gameweek}\n")

# TODO; put in def
previous_three_gameweeks = [current_gameweek, current_gameweek - 1, current_gameweek - 2]
previous_three_gameweeks = [gw for gw in previous_three_gameweeks if gw > 0 ]
previous_three_gameweeks.reverse()

top_10k = asyncio.run(fpl_custom_functions.get_top_10k(314))

picks = []
for user_id in top_10k:
    pick = asyncio.run(fpl_custom_functions.get_picks_async(user_id))
    team = pick[list(pick.keys())[-1]]
    for i in team:
        picks.append(i["element"])
picks = dict(Counter(picks))
picks = dict(sorted(picks.items(),key= lambda x: x[1], reverse = True))
picks = dict(islice(picks.items(), 50))

players_performance = []
for element, total in picks.items():
    player_performance = fpl_custom_functions.get_player_analysis(element, current_gameweek)
    percentage_ownership = round(total/10000*100, 2)
    player_performance[list(player_performance.keys())[0]]["percentage_ownership"] = f"{percentage_ownership}%"
    players_performance.append(player_performance)

fpl_custom_functions.print_player_table(players_performance, current_gameweek, previous_three_gameweeks)

end_time = time.time()
run_time = end_time - start_time
if run_time < 60:
    run_time = round(run_time, 2)
    print(f"\nTime Taken: {run_time} s")
else:
    run_time = run_time / 60
    run_time = round(run_time, 2)
    print(f"\nTime Taken: {run_time} min")
