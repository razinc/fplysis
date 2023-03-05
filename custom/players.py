import asyncio
from collections import OrderedDict
from itertools import islice
from operator import getitem

import aiohttp
import pandas as pd
from fpl import FPL
from prettytable import PrettyTable
from tqdm import tqdm
from understat import Understat

from custom.constant import FplToUnderstat, Gameweek


class Players:
    def __init__(self, fpl_ids=None, skips=[], ownership=None):
        if ownership is not None:
            self.fpl_ids = ownership.keys()
        else:
            self.fpl_ids = fpl_ids
        self.skips = skips
        asyncio.run(self.set_attr(ownership))

    async def set_attr(self, ownership):
        stats = {}
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            players = await fpl.get_players(self.fpl_ids, include_summary=True)
            if ownership is not None:
                desc = "Parsing top ownership players "
            elif self.fpl_ids is None:
                desc = "Analysing all players"
            else:
                desc = "Analysing user's team"
            for player in tqdm(players, desc=desc):
                fpl_id = player.id

                # skip players on loan/ transfer
                if player.status == "u":
                    continue

                if fpl_id in self.skips:
                    continue

                team = await fpl.get_team(player.team)
                team_short_name = team.short_name

                element_type = player.element_type
                if element_type == 1:
                    pos = "GK"
                if element_type == 2:
                    pos = "DEF"
                if element_type == 3:
                    pos = "MID"
                if element_type == 4:
                    pos = "FOR"

                latest_price = player.now_cost / 10
                try:
                    price_change = round(
                        latest_price - player.history[-1]["value"] / 10, 1
                    )
                # player has not plays yet
                except IndexError:
                    pass

                try:
                    understat_id = FplToUnderstat.MAPPING[fpl_id]["understat"]
                except KeyError:
                    # no data available in df_season
                    understat_id = float("Nan")
                if pd.isna(understat_id) == True or understat_id == "N/A":
                    xg = "N/A"
                    xa = "N/A"
                    sum_xg_xa = 0
                else:
                    understat = Understat(session)
                    player_grouped_stats = await understat.get_player_grouped_stats(
                        understat_id
                    )
                    if player_grouped_stats["season"][0]["season"] == Gameweek.SEASON:
                        xg = round(float(player_grouped_stats["season"][0]["xG"]), 2)
                        xa = round(float(player_grouped_stats["season"][0]["xA"]), 2)
                        sum_xg_xa = xg + xa
                    else:
                        xg = "N/A"
                        xa = "N/A"
                        sum_xg_xa = 0

                history = player.history
                rounds = [i["round"] for i in history]
                pts_prev_n_gw = {}
                total_pts_prev_n_gw = 0
                for gw in Gameweek.PREV_N_GWS:
                    if gw not in rounds:
                        pts_prev_n_gw[gw] = "Blank GW"
                        continue
                    else:
                        pts_prev_n_gw[gw] = 0
                    for i in [i for i, j in enumerate(rounds) if j == gw]:
                        pts_prev_n_gw[gw] = (
                            pts_prev_n_gw[gw] + history[i]["total_points"]
                        )
                        total_pts_prev_n_gw = (
                            total_pts_prev_n_gw + history[i]["total_points"]
                        )

                fixtures = {}
                fixture_difficulty_sum = 0
                total_games = 0
                gameweeks = [i.get("event_name") for i in player.fixtures]
                for gw in Gameweek.NEXT_N_GWS:
                    fixtures[gw] = []
                    if f"Gameweek {gw}" in gameweeks:
                        indices = [
                            i for i, x in enumerate(gameweeks) if x == f"Gameweek {gw}"
                        ]
                        for i in indices:
                            if player.fixtures[i]["is_home"] == True:
                                team_code = player.fixtures[i]["team_a"]
                                where = "H"
                            else:
                                team_code = player.fixtures[i]["team_h"]
                                where = "A"
                            difficulty = player.fixtures[i]["difficulty"]
                            fixture_difficulty_sum = fixture_difficulty_sum + difficulty
                            total_games = total_games + 1
                            team_against = await fpl.get_team(team_code)
                            team_against_short_name = team_against.short_name
                            fixtures[gw].append(
                                f"{team_against_short_name} ({where}) ({difficulty})"
                            )
                    else:
                        fixtures[gw] = ["Blank GW"]

                stats[fpl_id] = {
                    "web_name": player.web_name,
                    "team_short_name": team_short_name,
                    "pos": pos,
                    "latest_price": f"£{latest_price}",
                    "price_change": f"£{price_change}",
                    "understat_id": understat_id,
                    "xg": xg,
                    "xa": xa,
                    "sum_xg_xa": sum_xg_xa,
                    "pts_prev_n_gw": pts_prev_n_gw,
                    "total_pts_prev_n_gw": total_pts_prev_n_gw,
                    "ep_this": float(player.ep_this),
                    "ep_next": float(player.ep_next),
                    "fixtures": fixtures,
                    "fixture_difficulty_avg": round(
                        fixture_difficulty_sum / total_games, 1
                    ),
                }

                if ownership is not None:
                    stats[fpl_id]["ownership"] = f"{ownership[fpl_id]}%"

            self.stats = stats

    def sort_by_total_pts_prev_n_gw(self):
        self.stats = OrderedDict(
            sorted(
                self.stats.items(),
                key=lambda x: getitem(x[1], "total_pts_prev_n_gw"),
                reverse=True,
            )
        )

    def sort_by_fda(self):
        self.sort_by_total_pts_prev_n_gw()
        self.stats = {
            k: v for k, v in self.stats.items() if v["fixture_difficulty_avg"] < 2.4
        }

    def sort_by_sum_xg_xa(self):
        self.stats = OrderedDict(
            sorted(
                self.stats.items(),
                key=lambda x: getitem(x[1], "sum_xg_xa"),
                reverse=True,
            )
        )

    def sort_by_xpts(self):
        self.stats = OrderedDict(
            sorted(
                self.stats.items(), key=lambda x: getitem(x[1], "ep_next"), reverse=True
            )
        )

    def get_table(self, top=None):
        table = PrettyTable()
        header = (
            ["Name", "Team", "Pos", "Price", "xG", "xA"]
            + [f"GW{gw} Pts" for gw in Gameweek.PREV_N_GWS]
            + ["Σ Pts"]
            + [f"GW{Gameweek.NEXT_GW} xP"]
            + [f"GW{gw} Fxt" for gw in Gameweek.NEXT_N_GWS]
            + ["FDA"]
        )
        if "ownership" in list(dict(islice(self.stats.items(), 1)).values())[0]:
            header.append("Top 10k Ownership")

        table.field_names = header
        for k, v in dict(islice(self.stats.items(), top)).items():
            row = (
                [
                    v["web_name"],
                    v["team_short_name"],
                    v["pos"],
                    v["latest_price"],
                    v["xg"],
                    v["xa"],
                ]
                + list(v["pts_prev_n_gw"].values())
                + [v["total_pts_prev_n_gw"], v["ep_next"]]
            )
            fixtures = v["fixtures"]
            for fixture in list(v["fixtures"].values()):
                row.append("\n".join(fixture))
            row.append(v["fixture_difficulty_avg"])
            if "ownership" in list(dict(islice(self.stats.items(), 1)).values())[0]:
                row.append(v["ownership"])
            table.add_row(row)
        return table.get_string()
