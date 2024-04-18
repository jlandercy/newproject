"""
Module :mod:`newproject.tests.test_interfaces` implements test suite for the
class :class:`newproject.interfaces.generic.GenericInterface` and its children.
"""

import json
import unittest

from newproject.interfaces import GenericInterface


class TestGenericInterface(unittest.TestCase):
    def test_abstract_class(self) -> None:
        with self.assertRaises(TypeError) as context:
            instance = GenericInterface()
            self.assertTrue("Can't instantiate abstract class" in context.exception)


class TestGenericInterfaceImplementation:
    """
    Reusable class for interface implementation tests.
    Subsequent test classes must inherit both from this class and :class:`unittest.TestCase`.
    Use class members :attr:`factory`, :attr:`dict_configuration` and :attr:`json_configuration`
    to setup the defined test mechanic.
    """

    factory = None
    dict_configuration = None
    json_configuration = None

    def setUp(self) -> None:
        """
        Create instance of interface using :attr:`factory` initialized
        with :attr:`dict_configuration`.
        """
        self.instance = self.factory(**self.dict_configuration)

    def test_to_dict_configuration(self) -> None:
        """
        Test configuration returned as a dict is equal to original
        defined by :attr:`dict_configuration`.
        """
        self.assertEqual(self.dict_configuration, self.instance.to_dict())

    def test_serializer(self) -> None:
        """
        Test all :attr:`dict_configuration` values serialiazed are equal to expected values
        defined in :attr:`json_configuration`.
        """
        reference = json.loads(self.json_configuration)
        for key, value in self.dict_configuration.items():
            serialized = self.instance.serializer(value)
            self.assertEqual(reference[key], serialized)

    def test_to_json_configuration(self) -> None:
        """
        Test configuration returned as a dict is equal to expected JSON
        defined in :attr:`json_configuration`.
        """
        self.assertEqual(self.json_configuration, self.instance.to_json())

    def test_creation_from_dict_configuration(self) -> None:
        """
        Test new instance created with object configuration returns same configuration object.
        """
        instance = self.factory(**self.instance.to_dict())
        self.assertEqual(self.instance.to_dict(), instance.to_dict())
