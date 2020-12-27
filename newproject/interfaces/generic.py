"""
Module :py:mod:`newproject.interafces.generic` defines the class :class:`GenericInterface`
on which any other interfaces must inherit from. This class exposes generic abstract methods
all interfaces must implement.
"""

import sys
import abc
import json


class GenericInterface(abc.ABC):
    """
    Generic Interface (Abstract Base Class) for all object of the package.
    This class must be subclassed by any other interfaces.
    """

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """
        Returns the configuration of the object as a dictionary.
        This configuration must be self-contained and sufficient to recreate a new object from it
        using dict unpacking to feed the `__init__` method of the class.
        This configuration must be JSON serializable as well, see method :meth:`to_json` and
        override :meth:`serializer` to add JSON serialization helpers for specific objects.
        """

    @staticmethod
    def serializer(o) -> object:
        """
        JSON Serializer for any configuration object
        """
        return o

    def to_json(self) -> str:
        """
        Returns the configuration of the object as a JSON string.
        """
        return json.dumps(self.to_dict(), default=self.serializer)


def main():
    """
    Module entrypoint
    """
    sys.exit(0)


if __name__ == "__main__":
    main()
