from custom.user import User

user = User(user_id=10322207)


def test_user():
    assert user.log_in == None
    assert user.user_id == 10322207
    assert user.name == "fplysis, pytest"
    assert user.team_name == "fplysis F.C."
    assert user.team == [
        478,
        516,
        484,
        448,
        109,
        116,
        335,
        311,
        111,
        80,
        318,
        376,
        357,
        7,
        427,
    ]
    assert user.in_the_bank == "This is only available through login"
