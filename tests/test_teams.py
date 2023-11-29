import pytest

from custom.teams import builder, get_teams


def test_teams(monkeypatch):
    async def mock_get_teams():
        return [
            {
                "code": 3,
                "draw": 0,
                "form": None,
                "id": 1,
                "loss": 0,
                "name": "Arsenal",
                "played": 0,
                "points": 0,
                "position": 0,
                "short_name": "ARS",
                "strength": 4,
                "team_division": None,
                "unavailable": False,
                "win": 0,
                "strength_overall_home": 1230,
                "strength_overall_away": 1285,
                "strength_attack_home": 1250,
                "strength_attack_away": 1250,
                "strength_defence_home": 1210,
                "strength_defence_away": 1320,
                "pulse_id": 1,
            },
            {
                "code": 7,
                "draw": 0,
                "form": None,
                "id": 2,
                "loss": 0,
                "name": "Aston Villa",
                "played": 0,
                "points": 0,
                "position": 0,
                "short_name": "AVL",
                "strength": 3,
                "team_division": None,
                "unavailable": False,
                "win": 0,
                "strength_overall_home": 1115,
                "strength_overall_away": 1175,
                "strength_attack_home": 1130,
                "strength_attack_away": 1190,
                "strength_defence_home": 1100,
                "strength_defence_away": 1160,
                "pulse_id": 2,
            },
        ]

    monkeypatch.setattr("custom.teams.get_teams", mock_get_teams)

    async def mock_get_fdr():
        return {"Arsenal": {"all": {"H": 4.380170195923214, "A": 4.18487113008998}}, "Aston Villa": {"all": {"H": 2.10799358574808, "A": 5.0}}}

    monkeypatch.setattr("custom.teams.get_fdr", mock_get_fdr)

    teams = builder()
    assert teams == {1: {"short_name": "ARS", "FDR_H": 4.38, "FDR_A": 4.18}, 2: {"short_name": "AVL", "FDR_H": 2.11, "FDR_A": 5.0}}
