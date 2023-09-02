import pytest

from custom.user import User


def test_get_user_with_mock(monkeypatch):
    async def mock_get_user(self):
        return {
            "player_first_name": "Fábio",
            "player_last_name": "Borges",
            "name": "Clichy's Cleansheets",
        }

    monkeypatch.setattr(User, "get_user", mock_get_user)

    user = User(user_id=4305040)

    assert user.name == "Fábio, Borges"
    assert user.team_name == "Clichy's Cleansheets"


def test_get_picks_with_mock(monkeypatch):
    async def mock_get_picks(self):
        return {
            4: [
                {
                    "element": 101,
                    "position": 1,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 203,
                    "position": 2,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 20,
                    "position": 3,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 195,
                    "position": 4,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 373,
                    "position": 5,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 108,
                    "position": 6,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 143,
                    "position": 7,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 308,
                    "position": 8,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": True,
                },
                {
                    "element": 396,
                    "position": 9,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 211,
                    "position": 10,
                    "multiplier": 1,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 355,
                    "position": 11,
                    "multiplier": 2,
                    "is_captain": True,
                    "is_vice_captain": False,
                },
                {
                    "element": 28,
                    "position": 12,
                    "multiplier": 0,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 473,
                    "position": 13,
                    "multiplier": 0,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 316,
                    "position": 14,
                    "multiplier": 0,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
                {
                    "element": 490,
                    "position": 15,
                    "multiplier": 0,
                    "is_captain": False,
                    "is_vice_captain": False,
                },
            ]
        }

    monkeypatch.setattr(User, "get_picks", mock_get_picks)

    user = User(user_id=4305040)

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
