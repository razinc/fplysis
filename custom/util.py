from os import mkdir
import argparse


class MkdirOutput:
    def create_output_dir():
        try:
            mkdir("output")
        except (FileExistsError):
            pass

    create_output_dir()


class UserAuthArg:
    def set_attr():
        parser = argparse.ArgumentParser(description="make better transfer in FPL")
        parser.add_argument(
            "-id",
            "--user_id",
            type=int,
            help="user ID. only applicable for analysing team, to analyse league: log_in arg must be passed",
        )
        parser.add_argument(
            "-l",
            "--log_in",
            type=bool,
            help='pass "True" to enable login. this is the default arg if no arg is passed',
        )
        args = parser.parse_args()
        if not any(vars(args).values()):
            args.log_in = True
        return {"log_in": args.log_in, "user_id": args.user_id}

    log_in, user_id = set_attr().values()
