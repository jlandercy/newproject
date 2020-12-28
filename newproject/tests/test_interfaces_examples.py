"""
Module :mod:`newproject.tests.test_interfaces_examples` implements test suite using
class :class:`newproject.tests.test_interfaces.TestGenericInterfaceImplementation`
and interface examples defined in module :mod:`newproject.interfaces.examples`.
"""

import unittest
import datetime

from newproject.tests.test_interfaces import TestGenericInterfaceImplementation
from newproject.interfaces.examples import SimpleCase, SimpleCaseWithSerializer


class TestSimpleCase(TestGenericInterfaceImplementation, unittest.TestCase):

    factory = SimpleCase
    dict_configuration = {"value": "Hello World!"}
    json_configuration = """{"value": "Hello World!"}"""


class TestSimpleCaseWithNoSerializer(TestGenericInterfaceImplementation, unittest.TestCase):

    factory = SimpleCase
    dict_configuration = {"value": datetime.datetime(2020, 1, 1)}
    json_configuration = None

    def test_serializer(self) -> None:
        pass

    def test_to_json_configuration(self) -> None:
        with self.assertRaises(AttributeError) as context:
            super().test_to_json_configuration()


class TestSimpleCaseWithSerializer(TestGenericInterfaceImplementation, unittest.TestCase):

    factory = SimpleCaseWithSerializer
    dict_configuration = {"value": datetime.datetime(2020, 1, 1)}
    json_configuration = """{"value": "2020-01-01T00:00:00"}"""

