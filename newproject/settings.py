"""
Settings module manages all package settings (system and user).
User can adapt the default package settings using the `settings.json` file
stored in user home directory **~/newproject**.

If the settings file is missing, a fresh copy of default settings file is created
in this directory before the package loads settings.

Update of the settings file is not taken into account until package is restarted.

Settings also hold package logger as well and are available in Python as follow:

.. code-block:: python

   from newproject.settings import settings
   settings.logger("Settings: %s", settings.__dict__)

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

# Settings file:
filename = "settings.json"
settings.file = settings.user / filename
if not settings.file.exists():
    settings.file.write_bytes((settings.resources / filename).read_bytes())
settings.settings = json.loads(settings.file.read_bytes())

# Application Settings:
settings.database = os.environ.get("DATABASE", "sqlite://")
settings.secretkey = os.environ.get("SECRETKEY", os.urandom(64))
settings.uuid4 = uuid.uuid4()


def main():
    """
    Settings entrypoint
    """
    settings.logger.info("Settings: %s", settings.__dict__)
    sys.exit(0)


if __name__ == "__main__":
    main()
