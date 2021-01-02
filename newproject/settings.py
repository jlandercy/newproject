"""
Settings module
"""

import json
import logging.config
import os
import pathlib
import sys
import uuid
from types import SimpleNamespace

# Settings Namespace:
settings = SimpleNamespace()

# Directories:
settings.home = pathlib.Path.home()
settings.package = pathlib.Path(__file__).parent
settings.resources = settings.package / "resources"
settings.name = settings.package.parts[-1]
settings.user = settings.home / settings.name
settings.user.mkdir(exist_ok=True)

# Logger:
settings.logger = logging.getLogger(settings.name)
with (settings.resources / "logging.json").open("r") as fh:
    data = json.load(fh)
    data["loggers"][settings.name] = data["loggers"]["default"]
    logging.config.dictConfig(data)

# Application Settings:
settings.database = os.environ.get("DATABASE", "sqlite://")
settings.secretkey = os.environ.get("SECRETKEY", os.urandom(64))
settings.uuid4 = uuid.uuid4()


def main():
    """
    Module entrypoint
    """
    settings.logger.info(settings.__dict__)
    sys.exit(0)


if __name__ == "__main__":
    main()
