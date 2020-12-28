"""
Module :py:mod:`newproject.errors` defines package exceptions.
"""


class GenericException(Exception):
    """
    :class:`GenericException` inherits from PSL :class:`Exception`.
    This exception is not intended to be raised.
    This exception must be inherited by any other exceptions instead.
    """


class InvalidParameter(GenericException):
    """
    :class:`InvalidParameter` stands for any error occuring with function parameters.
    It is usually raised when invalid parameter is passed to :meth:`__init__`.
    """
