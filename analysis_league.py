import asyncio
import time
import fpl_custom_functions
from tqdm import tqdm
from collections import Counter
from collections import OrderedDict
from operator import getitem

# TODO: port to fpl_custom_functions.py
import fpl_credentials
import aiohttp
from fpl import FPL
import json
import matplotlib.pyplot as plt
import numpy as np

start_time = time.time()

fpl_custom_functions.create_output_dir()

current_gameweek = fpl_custom_functions.get_current_gameweek()

# TODO: port to fpl_custom_functions.py
async def get_classic_league_async(league_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email = fpl_credentials.EMAIL, password = fpl_credentials.PASSWORD)
        classic_league = await fpl.get_classic_league(league_id, return_json = True)
    return classic_league

# TODO: port to fpl_custom_functions.py
async def get_gameweek_points(id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        user = await fpl.get_user(id)
        history =  await user.get_gameweek_history()
    gameweek_points = [i["points"] for i in history]
    return gameweek_points

# TODO: port to fpl_custom_functions.py
async def get_gameweek_cumulative_points(id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        user = await fpl.get_user(id)
        history =  await user.get_gameweek_history()
    gameweek_cumulative_points = [i["total_points"] for i in history]
    return gameweek_cumulative_points

classic_league = asyncio.run(get_classic_league_async(fpl_credentials.LEAGUE_ID))
league_name = classic_league["league"]["name"]
results = classic_league["standings"]["results"]
team_names = [i["entry_name"] for i in results]
manager_ids = [i["entry"] for i in results]
rank = []
for team_name, manager_id in zip(team_names, manager_ids):
    rank.append({manager_id: {"team_name": team_name}})

with open("output/analysis_league.csv", "w") as f:
    f.write(f"League name: {league_name}\n\n")
    f.write("Gameweek Points:\n")
    f.write("Rank,Team Name," + ",".join([f"GW {str(i)}" for i in range(1, current_gameweek + 1)]) + "\n")
    for i, manager in enumerate(tqdm(rank, desc = "Analysing managers       "), start = 1):
        manager_id = list(manager.keys())[0]
        team_name = list(manager.values())[0]["team_name"]
        gameweek_points = asyncio.run(get_gameweek_points(manager_id))
        gameweek_cumulative_points = asyncio.run(get_gameweek_cumulative_points(manager_id))
        if len(gameweek_points) != current_gameweek:
            blank = [0 for i in range(current_gameweek - len(gameweek_points))]
            gameweek_points = blank + gameweek_points
            gameweek_cumulative_points = blank + gameweek_cumulative_points
        standing = str(i)
        if standing == "1":
            standing = "🥇"
        elif standing == "2":
            standing = "🥈"
        elif standing == "3":
            standing = "🥉"
        f.write(standing + "," + team_name + "," + ",".join([str(i) for i in gameweek_points]) + "\n")
        manager[manager_id]["gameweek_points"] = gameweek_points
        manager[manager_id]["gameweek_cumulative_points"] = gameweek_cumulative_points

    f.write("\nGameweek Cumulative Points:\n")
    f.write("Team Name," + ",".join([f"GW {str(i)}" for i in range(1, current_gameweek + 1)]) + "\n")
    # TODO: insert tqdm
    for i in rank:
        team_name = list(i.values())[0]["team_name"]
        gameweek_cumulative_points = list(i.values())[0]["gameweek_cumulative_points"]
        f.write(team_name + "," + ",".join([str(i) for i in gameweek_cumulative_points]) +"\n")

    f.write("\nWeekly Top Team:\n")
    f.write("GW,Team Name,Points\n")
    goat_team = []
    for gameweek in tqdm(range(1, current_gameweek + 1), desc = "Analysing weekly top team"):
        top_weekly_points = max([list(i.values())[0]["gameweek_points"][gameweek - 1] for i in rank])
        top_weekly_teams = []
        for manager in rank:
            team_name = list(manager.values())[0]["team_name"]
            history = list(manager.values())[0]["gameweek_points"]
            if top_weekly_points == history[gameweek -1]:
                top_weekly_teams.append(team_name)
                goat_team.append(team_name)
        top_weekly_teams = "🤝".join(top_weekly_teams)
        f.write(f"{gameweek},{top_weekly_teams},{top_weekly_points}\n")

    f.write("\nGOAT:\n")
    f.write("Team Name,Count\n")
    goat_team = dict(Counter(goat_team))
    goat_team = dict(sorted(goat_team.items(),key= lambda x:x[1], reverse = True))
    for k, v in tqdm(goat_team.items(), desc = "Analysing GOAT team      "):
        f.write(f"{k},{v}\n")

end_time = time.time()
run_time = fpl_custom_functions.get_run_time(start_time, end_time)
print("\nRun time:")
print(run_time)
