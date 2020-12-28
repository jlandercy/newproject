"""
Module :py:mod:`newproject.errors` defines all package exceptions.
"""


class GenericException(Exception):
    """
    Generic Exception, all other exceptions must inherit from it.
    """


class InvalidParameter(GenericException):
    """
    Invalid Parameter Exception
    """
