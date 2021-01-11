"""
Service module
"""

import sys

from newproject.settings import settings


def main():
    """
    Service entrypoint
    """

    import argparse

    # CLI Arguments:
    cli_parser = argparse.ArgumentParser(
        description="Service Command Line",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    cli_parser.add_argument("--verbose", type=int, default=40,
                            help="Logger Verbose Level")
    cli_parser.add_argument("--config", type=str, default=str(settings.file),
                            help='Configuration path')
    cli_parameters = cli_parser.parse_args()

    # Set Logger Level
    settings.logger.setLevel(cli_parameters.verbose)

    sys.exit(0)


if __name__ == "__main__":
    main()
