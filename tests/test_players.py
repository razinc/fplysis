from custom.constant import Gameweek
from custom.players import Players


def test_players(monkeypatch):
    monkeypatch.setattr(Gameweek, "CURRENT_GW", 7)
    monkeypatch.setattr(Gameweek, "NO_OF_PREV_GWS", 5)
    monkeypatch.setattr(Gameweek, "PREV_N_GWS", [2, 3, 4, 5, 6])
    monkeypatch.setattr(Gameweek, "NO_OF_NEXT_GWS", 5)

    fpl_id = 427
    players = Players(fpl_ids=[fpl_id])
    
    assert players.stats[fpl_id]["web_name"] == "Kane"
    assert players.stats[fpl_id]["team_short_name"] == "TOT"
    assert players.stats[fpl_id]["pos"] == "FOR"
    assert players.stats[fpl_id]["understat_id"] == 647
    assert players.stats[fpl_id]["pts_prev_n_gw"] == {2: 8, 3: 6, 4: 10, 5: 5, 6: 9}
    assert players.stats[fpl_id]["total_pts_prev_n_gw"] == 38
