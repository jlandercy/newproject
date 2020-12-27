"""
Module :py:mod:`newproject.interfaces.examples` provides implemented interfaces examples.
Classes defined in this module are used in test suites to check generic and
implemented interfaces properties (see :py:mod:`newproject.tests.test_interfaces_generic`
module for operational details).
"""

import sys
from typing import Any
import datetime

from newproject.interfaces.generic import GenericInterface


class SimpleCase(GenericInterface):
    """
    This class shows a simple case of :class:`newproject.interfaces.generic.GenericInterface`
    implementation with no serializer.
    """

    def __init__(self, value: Any = None) -> None:
        """
        Initialization method takes a single argument called value and store it into the object.
        """
        self.value = value

    def to_dict(self) -> dict:
        """
        Returns the object configuration as a dictionary, including user defined value argument.
        """
        return {"value": self.value}


class SimpleCaseWithSerializer(SimpleCase):
    """
    This class shows a simple case inherited from :class:`SimpleCase` with serializer.
    It overrides the :meth:`newproject.interfaces.generic.GenericInterface.serializer`
    method in order to provide the missing helper for :class:`datetime.datetime` object.
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
