import pytest

from custom.constant import Gameweek
from custom.players import Players
from custom.teams import teams


def test_init_with_mock(monkeypatch):
    monkeypatch.setattr(Gameweek, "PREV_N_GWS", [5, 6])
    monkeypatch.setattr(Gameweek, "NEXT_N_GWS", [8, 9])
    # TODO: this works but only patch certain key value pair in the dict, patch the whole var?
    monkeypatch.setitem(teams, 1, {"short_name": "ARS", "FDR_H": 4.38, "FDR_A": 4.18})
    monkeypatch.setitem(teams, 6, {"short_name": "BUR", "FDR_H": 1.77, "FDR_A": 1.0})
    monkeypatch.setitem(teams, 7, {"short_name": "CHE", "FDR_H": 3.68, "FDR_A": 2.42})

    async def mock_get_players(self):
        return [
            {
                "element_type": 3,
                "ep_next": "3.2",
                "ep_this": "2.7",
                "form": "2.7",
                "id": 202,
                "now_cost": 54,
                "status": "a",
                "team": 7,
                "web_name": "Gallagher",
                "expected_goals": "0.52",
                "expected_assists": "0.76",
                "fixtures": [
                    {
                        "team_h": 6,
                        "team_a": 7,
                        "event_name": "Gameweek 8",
                        "is_home": False,
                    },
                    {
                        "team_h": 7,
                        "team_a": 1,
                        "event_name": "Gameweek 9",
                        "is_home": True,
                    },
                ],
                "history": [
                    {
                        "round": 1,
                    },
                    {
                        "round": 2,
                    },
                    {
                        "round": 3,
                    },
                    {
                        "round": 4,
                    },
                    {
                        "total_points": 3,
                        "round": 5,
                    },
                    {
                        "total_points": 2,
                        "round": 6,
                    },
                    {
                        "total_points": 3,
                        "round": 7,
                        "value": 54,
                    },
                ],
            }
        ]

    monkeypatch.setattr(Players, "get_players", mock_get_players)

    players = Players(fpl_ids=[202])

    assert players.stats == {
        202: {
            "web_name": "Gallagher",
            "status": "",
            "team_short_name": "CHE",
            "pos": "MID",
            "latest_price": 5.4,
            "price_change": 0.0,
            "xg": 0.52,
            "xa": 0.76,
            "xgi": 1.28,
            "pts_prev_n_gw": {5: 3, 6: 2},
            "total_pts_prev_n_gw": 5,
            "ep_this": 2.7,
            "ep_next": 3.2,
            "fixtures": {8: ["BUR (A) (1.0)"], 9: ["ARS (H) (4.38)"]},
            "fdr_avg": 2.7,
            "weighted_value": 1.4,
        }
    }
