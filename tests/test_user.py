import pytest

from custom.user import User


def test_init_with_mock(monkeypatch):
    async def mock_get_user(self):
        return {
            "player_first_name": "Fábio",
            "player_last_name": "Borges",
            "name": "Clichy's Cleansheets",
        }

    monkeypatch.setattr(User, "get_user", mock_get_user)

    async def mock_get_picks(self):
        return {
            4: [
                {
                    "element": 101,
                },
                {
                    "element": 203,
                },
                {
                    "element": 20,
                },
                {
                    "element": 195,
                },
                {
                    "element": 373,
                },
                {
                    "element": 108,
                },
                {
                    "element": 143,
                },
                {
                    "element": 308,
                },
                {
                    "element": 396,
                },
                {
                    "element": 211,
                },
                {
                    "element": 355,
                },
                {
                    "element": 28,
                },
                {
                    "element": 473,
                },
                {
                    "element": 316,
                },
                {
                    "element": 490,
                },
            ]
        }

    monkeypatch.setattr(User, "get_picks", mock_get_picks)

    user = User(user_id=4305040)
    assert user.log_in == None
    assert user.user_id == 4305040
    assert user.name == "Fábio, Borges"
    assert user.team_name == "Clichy's Cleansheets"
    assert user.in_the_bank == "This is only available through login"
    assert user.team == [
        101,
        203,
        20,
        195,
        373,
        108,
        143,
        308,
        396,
        211,
        355,
        28,
        473,
        316,
        490,
    ]
