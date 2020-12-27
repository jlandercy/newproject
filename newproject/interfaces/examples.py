"""
Module :py:mod:`newproject.interfaces.examples` provides implemented interfaces examples.
Classes defined in this module are used in test suites to check Generic Interface and
implemented interface properties (see :py:mod:`newproject.tests.test_interfaces_generic`
module for details).
"""

import sys
from typing import Any
import datetime

from newproject.interfaces.generic import GenericInterface


class SimpleCase(GenericInterface):
    """
    This class shows a simple case of :class:`GenericInterface` implementation with no serializer.
    """

    def __init__(self, value: Any = None) -> None:
        """
        Initialization method takes a single argument called value and store it into the object.
        """
        self.value = value

    def to_dict(self) -> dict:
        """
        Return the object configuration as a dictionary.
        """
        return {"value": self.value}


class SimpleCaseWithSerializer(SimpleCase):
    """
    This class shows a simple case of :class:`GenericInterface` implementation with serializer.
    It inherits from :class:`SimpleCase` and override the :meth:`serializer` method in order to
    provide the missing helper for :class:`datetime.datetime` object.
    """

    @staticmethod
    def serializer(instance: Any) -> Any:
        """
        Provides an helper for :class:`datetime.datetime` object as it is not JSON serializable.
        Returns the result of parent serializer in any other cases.
        """
        if isinstance(instance, datetime.datetime):
            return instance.isoformat()
        else:
            return super().serializer(instance)


def main():
    """
    Module entrypoint
    """
    sys.exit(0)


if __name__ == "__main__":
    main()
