"""
Generic Interface Test Suite
"""

import sys
import unittest
from typing import Any
import datetime

from newproject.interfaces import GenericInterface


class TestGenericInterface(unittest.TestCase):
    """
    Test Generic Interface
    """

    def test_abstract_class(self) -> None:
        """
        Test Abstract Class
        """
        with self.assertRaises(TypeError) as context:
            instance = GenericInterface()
            self.assertTrue("Can't instantiate abstract class" in context.exception)


class TestGenericInterfaceImplementation:
    """
    Test helper for Generic Interface implementations
    """

    factory = object
    dict_configuration = dict()
    json_configuration = ""

    def setUp(self) -> None:
        self.instance = self.factory(**self.dict_configuration)

    def test_to_dict_configuration(self) -> None:
        self.assertEqual(self.dict_configuration, self.instance.to_dict())

    def test_to_json_configuration(self) -> None:
        self.assertEqual(self.json_configuration, self.instance.to_json())


class SimpleCase(GenericInterface):

    def __init__(self, value: Any = None) -> None:
        self.value = value

    def to_dict(self) -> dict:
        return {"value": self.value}


class TestSimpleCase(TestGenericInterfaceImplementation, unittest.TestCase):

    factory = SimpleCase
    dict_configuration = {"value": "Hello World!"}
    json_configuration = """{"value": "Hello World!"}"""


class TestSimpleCaseWithNoSerializer(TestGenericInterfaceImplementation, unittest.TestCase):

    factory = SimpleCase
    dict_configuration = {"value": datetime.datetime(2020, 1, 1)}
    json_configuration = None

    def test_to_json_configuration(self) -> None:
        with self.assertRaises(AttributeError) as context:
            self.assertEqual(self.json_configuration, self.instance.to_json())


class SimpleCaseWithSerializer(SimpleCase):

    @staticmethod
    def serializer(instance: Any) -> Any:
        if isinstance(instance, datetime.datetime):
            return instance.isoformat()
        else:
            return super().serializer(instance)


class TestSimpleCaseWithSerializer(TestGenericInterfaceImplementation, unittest.TestCase):

    factory = SimpleCaseWithSerializer
    dict_configuration = {"value": datetime.datetime(2020, 1, 1)}
    json_configuration = """{"value": "2020-01-01T00:00:00"}"""


def main():
    """
    Module entrypoint
    """
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
