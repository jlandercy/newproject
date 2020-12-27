"""
Module :mod:`newproject.tests.test_interfaces_generic` implements test suite for the
:class:`newproject.interfaces.generic.GenericInterface` using examples defined in
module :mod:`newproject.tests.test_interfaces_generic`.
"""

import sys
import unittest
import datetime
import json

from newproject.interfaces import GenericInterface
from newproject.interfaces.examples import SimpleCase, SimpleCaseWithSerializer


class TestGenericInterface(unittest.TestCase):

    def test_abstract_class(self) -> None:

        with self.assertRaises(TypeError) as context:
            instance = GenericInterface()
            self.assertTrue("Can't instantiate abstract class" in context.exception)


class TestGenericInterfaceImplementation:
    """
    Reusable class for Generic Interface implementation tests.
    Test class must inherit both from this class and :class:`unittest.TestCase`.
    Use class members `factory` and `configuration` to bind tested class.
    """

    factory = None
    dict_configuration = None
    json_configuration = None

    def setUp(self) -> None:
        """
        Create instance of class with configuration using factory
        """
        self.instance = self.factory(**self.dict_configuration)

    def test_to_dict_configuration(self) -> None:
        """
        Test whether configuration returned as a dict is equal to original configuration
        """
        self.assertEqual(self.dict_configuration, self.instance.to_dict())

    def test_to_json_configuration(self) -> None:
        """
        Test whether configuration returned as a dict is equal to expected JSON configuration
        """
        self.assertEqual(self.json_configuration, self.instance.to_json())

    def test_creation_from_dict_configuration(self) -> None:
        """
        Test whether new instance created with object configuration return same configuration object
        """
        instance = self.factory(**self.instance.to_dict())
        self.assertEqual(self.instance.to_dict(), instance.to_dict())


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
