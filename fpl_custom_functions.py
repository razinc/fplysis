import aiohttp
import asyncio
import fpl_credentials
import time
import itertools
from fpl import FPL
from prettytable import PrettyTable
from collections import OrderedDict
from operator import getitem
from tqdm import tqdm
from os import mkdir

def create_output_dir():
    try:
        mkdir("output")
    except(FileExistsError):
        pass

async def get_my_user():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email = fpl_credentials.EMAIL, password = fpl_credentials.PASSWORD)
        user = await fpl.get_user()
        full_name = f"{user.player_first_name}, {user.player_last_name}"
        team =  await user.get_team()
        money_remaining = await user.get_transfers_status()
        money_remaining = money_remaining["bank"] / 10

        return {"my_full_name": full_name,
            "my_team": team,
            "my_money_remaining": money_remaining
            }

async def get_all_players():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        # TOFIX: "Too Many Requests"
        players = await fpl.get_players(include_summary = True)
    return players

async def get_gameweeks_async():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        return await fpl.get_gameweeks()

def get_current_gameweek():
    gameweeks = asyncio.run(get_gameweeks_async())
    for gameweek in gameweeks:
        if gameweek.finished == True or gameweek.is_current == True:
            current_gameweek = gameweek.id
    return current_gameweek

async def get_player_async(element):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        return await fpl.get_player(element, include_summary = True)

async def get_team_async(team_id):
    async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            return await fpl.get_team(team_id)

def get_next_three_fixtures(player, current_gameweek):
    next_three_gameweeks = [current_gameweek+1, current_gameweek+2, current_gameweek+3]
    next_three_fixtures = []
    gameweeks = [i.get("event_name") for i in player.fixtures]
    for gw in next_three_gameweeks:
        if f"Gameweek {gw}" in gameweeks:
            i = gameweeks.index(f"Gameweek {gw}")

            if player.fixtures[i]["is_home"] == True:
                team_code = player.fixtures[i]["team_a"]
                where = "H"
            else:
                team_code = player.fixtures[i]["team_h"]
                where = "A"
            difficulty = player.fixtures[i]["difficulty"]
            team = asyncio.run(get_team_async(team_code))
            team_nname = team.short_name
            next_three_fixtures.append(f"{team_nname} ({where}) ({difficulty})")
        else:
            next_three_fixtures.append("Blank GW")
    return next_three_fixtures

def get_player_pos(player):
    element_type = player.element_type
    if element_type == 1:
        return "GK"
    elif element_type == 2:
        return "DEF"
    elif element_type == 3:
        return "MID"
    elif element_type == 4:
        return "FOR"

def get_player_analysis(element, current_gameweek, previous_three_gameweeks):
    player_performance = {}

    player = asyncio.run(get_player_async(element))
    web_name = player.web_name

    next_three_fixtures = get_next_three_fixtures(player, current_gameweek)

    pos = get_player_pos(player)

    points_previous_three_gameweeks = []
    
    expected_points = player.ep_this

    rounds = [i["round"] for i in player.history]
    for gw in previous_three_gameweeks:
        if gw in rounds:
            i = rounds.index(gw)
            points_previous_three_gameweeks.append(player.history[i]["total_points"])
        else:
            points_previous_three_gameweeks.append("Blank GW")
    
    latest_price = player.now_cost / 10
    price_change = round(latest_price - player.history[-1]["value"] / 10, 1)
    
    team = asyncio.run(get_team_async(player.team))
    team_nname = team.short_name

    player_performance[f"{web_name}"] = {
            "points_previous_three_gameweeks": points_previous_three_gameweeks,
            "total_points_previous_three_gameweeks": sum([0 if i == "Blank GW" else i for i in points_previous_three_gameweeks]),
            "expected_points": expected_points,
            "team": team_nname,
            "pos": pos,
            "next_3_fxts": next_three_fixtures,
            "latest_price": latest_price,
            "price_change": price_change}
    return player_performance

def get_player_table(players_performance, current_gameweek, previous_three_gameweeks):
    player_table = PrettyTable()
    if "percentage_ownership" in list(players_performance[0].values())[0]:
        header = ["Name", "Pos", "Team", "10k Ownership"]
    else:
        header = ["Name", "Pos", "Team"]
    for gw in previous_three_gameweeks:
        header.append(f"GW {gw} Pts")
    header.append("Total Pts")
    header.append("Expected Pts")
    header.append(f"Latest Price")
    header.append("Price Change")
    header.extend([f"GW {current_gameweek + 1} Fxt",
        f"GW {current_gameweek + 2} Fxt",
        f"GW {current_gameweek + 3} Fxt"])
    player_table.field_names = header
    for i in players_performance:
        for k, v in i.items():
            row = [k]
            row.append(v["pos"])
            row.append(v["team"])
            if "percentage_ownership" in v:
                row.append(v["percentage_ownership"])
            row.extend(v["points_previous_three_gameweeks"])
            row.append(v["total_points_previous_three_gameweeks"])
            row.append(v["expected_points"])
            row.append("£" + str(v["latest_price"]))
            price_change = v["price_change"]
            row.append(f"£{price_change}")
            row.extend(v["next_3_fxts"])
            player_table.add_row(row)
    return player_table.get_string()

async def get_top_10k(league_id):
    top_10k = []
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email = fpl_credentials.EMAIL, password = fpl_credentials.PASSWORD)
        overall_league = await fpl.get_classic_league(league_id)
        for i in tqdm(range(1, 203, 1), desc = "Parsing top 10k managers      "):
            pg = await overall_league.get_standings(page=i, page_new_entries=1, phase=1)
            for y in pg["results"]:
                top_10k.append(y["entry"])
    return top_10k[0:10000]

async def get_picks_async(user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        user = await fpl.get_user(user_id)
        return await user.get_picks()

def get_run_time(start_time, end_time):
    run_time = end_time - start_time
    if run_time < 60:
        run_time = round(run_time, 2)
        run_time = f"{run_time} seconds"
    elif run_time >= 60 and run_time < 3600:
        run_time = run_time / 60
        run_time = round(run_time, 2)
        run_time = f"{run_time} minutes"
    elif run_time >= 3600:
        run_time = run_time / 60 / 60
        run_time = round(run_time, 2)
        run_time = f"{run_time} hours"
    return run_time

def get_previous_three_gameweeks(current_gameweek):
    previous_three_gameweeks = [current_gameweek, current_gameweek - 1, current_gameweek - 2]
    previous_three_gameweeks = [gw for gw in previous_three_gameweeks if gw > 0 ]
    previous_three_gameweeks.reverse()
    return previous_three_gameweeks
