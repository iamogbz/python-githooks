import os
import sys
import argparse

from .constants import AVAILABLE_HOOKS, CONFIG_FILENAME, GITHOOKS_RELATIVE_DIR
from .helpers import (
    create_config_file,
    create_git_hooks,
    delete_git_hooks,
    execute_git_hook,
)

__BASE_DIR__ = os.getcwd()
__GITHOOKS_BASE_DIR__ = os.path.join(__BASE_DIR__, GITHOOKS_RELATIVE_DIR)
__GITHOOKS_CONFIGFILE_PATH__ = os.path.join(__BASE_DIR__, CONFIG_FILENAME)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Shim git hooks for easier configuration"
    )
    parser.add_argument(
        "hook",
        metavar="git.hook",
        type=str,
        nargs="?",
        choices=AVAILABLE_HOOKS,
        help="name of git hook to execute",
    )
    parser.add_argument(
        "--activate",
        default=True,
        action="store_true",
        help="activates python_githooks shimming",
    )
    parser.add_argument(
        "--deactivate",
        default=False,
        action="store_true",
        help="deactivates python_githooks shimming",
    )
    return parser.parse_args(sys.argv[1:])


def main():
    if os.path.isdir(__GITHOOKS_BASE_DIR__):
        args = parse_args()
        if args.hook:
            return execute_git_hook(
                hook_name=args.hook.strip(),
                configfile_path=__GITHOOKS_CONFIGFILE_PATH__,
            )
        elif args.deactivate:
            return delete_git_hooks(
                configfile_path=__GITHOOKS_CONFIGFILE_PATH__,
                githooks_dir=__GITHOOKS_BASE_DIR__,
            )
        elif args.activate:
            if not os.path.isfile(__GITHOOKS_CONFIGFILE_PATH__):
                print("Creating sample configuration")
                create_config_file(configfile_path=__GITHOOKS_CONFIGFILE_PATH__)
            else:
                print("Found configuration file")

            print("Installing githooks...\n")
            return create_git_hooks(
                configfile_path=__GITHOOKS_CONFIGFILE_PATH__,
                githooks_dir=__GITHOOKS_BASE_DIR__,
            )
    else:
        message = """
        Sorry, this is not a GIT repository.
        Please, run 'git init' before trying to install the hooks.
        """
        print(message)
        sys.exit(1)


if __name__ == "__main__":
    main()
