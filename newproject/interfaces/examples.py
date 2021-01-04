"""
Module :py:mod:`newproject.interfaces.examples` provides implemented interfaces examples.
Classes defined in this module are used in test suites to check generic and
implemented interfaces properties (see :py:mod:`newproject.tests.test_interfaces`
and :py:mod:`newproject.tests.test_interfaces_examples` modules for operational details).
"""

import datetime
from typing import Any

from newproject.interfaces.generic import GenericInterface


class SimpleCase(GenericInterface):
    """
    This class shows a simple case of :class:`newproject.interfaces.generic.GenericInterface`
    implementation with no serializer.

    A basic example of :class:`newproject.interfaces.examples.SimpleCase` is shown below.
    It illustrates native capabilities of such a class:

    .. code-block:: python

        a = SimpleCase(value="dummy")
        a.to_dict()  # returns: {"value": "dummy"}
        a.to_json()  # returns: '{"value": "dummy"}'
        b = SimpleCase(**a.to_dict())
        a.to_dict() == b.to_dict()  # returns: True

    The purpose of :meth:`to_dict` is to export instance configuration and be able
    to recreate an equal object from it. Of course it should be JSON serializable as
    well in order to safely exchange configurations.
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

    .. code-block:: python

        import datetime

        t = datetime.datetime(2021, 1, 1)
        c = SimpleCaseWithSerializer(value=t)
        c.to_dict()  # returns: {"value": datetime.datetime(2021, 1, 1, 0, 0)}
        c.to_json()  # returns: '{"value": "2021-01-01T00:00:00"}'

    """

    @staticmethod
    def serializer(instance: Any) -> Any:
        """
        Provides an helper for :class:`datetime.datetime` object as it is not JSON serializable.
        Returns the result of parent serializer in any other cases.
        """
        if isinstance(instance, datetime.datetime):
            return instance.isoformat()
        return super().serializer(instance)
