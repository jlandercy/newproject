"""
Generic Interface Test Suite
"""

import sys
import unittest
import datetime

from newproject.interfaces import GenericInterface
from newproject.interfaces.examples import SimpleCase, SimpleCaseWithSerializer


class TestGenericInterface(unittest.TestCase):

    def test_abstract_class(self) -> None:

        with self.assertRaises(TypeError) as context:
            instance = GenericInterface()
            self.assertTrue("Can't instantiate abstract class" in context.exception)


class TestGenericInterfaceImplementation:

    factory = object
    dict_configuration = dict()
    json_configuration = ""

    def setUp(self) -> None:
        self.instance = self.factory(**self.dict_configuration)

    def test_to_dict_configuration(self) -> None:
        self.assertEqual(self.dict_configuration, self.instance.to_dict())

    def test_to_json_configuration(self) -> None:
        self.assertEqual(self.json_configuration, self.instance.to_json())


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
