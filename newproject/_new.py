"""
New module
"""

import sys

import newproject
from newproject.settings import settings


def main():
    """
    Module entrypoint
    """
    settings.logger.info("New package {}".format(newproject.__version__))
    sys.exit(0)


if __name__ == "__main__":
    main()
