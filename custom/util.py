from os import mkdir
import argparse


class MkdirOutput:
    def create_output_dir():
        try:
            mkdir("output")
        except (FileExistsError):
            pass


class AnalTeamArg:
    def set_attr():
        parser = argparse.ArgumentParser(description="analyse FPL team")
        required_args = parser.add_argument_group("access method arguments")
        required_args.add_argument("-id", "--user_id", type=int, help="user ID")
        required_args.add_argument(
            "-l",
            "--log_in",
            type=bool,
            help='pass "True" to enable login',
        )
        args = parser.parse_args()
        if not any(vars(args).values()):
            parser.error("no access method arg is parsed.")
        return {"log_in": args.log_in, "user_id": args.user_id}

    log_in, user_id = set_attr().values()
