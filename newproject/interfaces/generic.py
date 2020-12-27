"""
Module :py:mod:`newproject.interafces.generic` defines the class :class:`GenericInterface`
on which any other interfaces must inherit from. This class exposes generic abstract methods
all interfaces must implement.
"""

import sys
import abc
import json
from typing import Any


class GenericInterface(abc.ABC):
    """
    Generic Interface (Abstract Base Class) for all object of the package.
    This class must be subclassed by any other interfaces.
    """

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """
        Returns the object configuration as a dictionary.
        This configuration must be self-contained and sufficient to recreate a new object from it
        using dict unpacking to feed the `__init__` method of the class.
        This configuration must be JSON serializable as well, see method :meth:`to_json`.
        Override :meth:`serializer` method to add JSON serialization helpers if needed.
        """

    @staticmethod
    def serializer(instance: Any) -> Any:
        """
        JSON Serializer provided as default to :meth:`to_json` method when serializing
        object configuration.
        This method must provide missing serialization helpers in order to allow
        valid JSON export and object reconstruction.
        """
        return instance.__dict__

    def to_json(self) -> str:
        """
        Returns the object configuration as a JSON string.
        """
        return json.dumps(self.to_dict(), default=self.serializer)


def main():
    """
    Module entrypoint
    """
    sys.exit(0)


if __name__ == "__main__":
    main()
