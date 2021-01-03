"""
Interfaces are the core of any objects, they define a standardized way for
object creation and manipulation.
Interfaces are used to enforce consistency among objects by specifying
a clear and strict API. Interfaces are:

  * Either Abstract Base Classes, then they are prefixed by the :attr:`Generic` keyword
    to recall they are abstract.
  * Or concrete classes when all abstract methods have been implemented.

Developers are asked to provide or subclass from an interface when implementing new objects.
Any interface must inherit either from :class:`newproject.interfaces.generic.GenericInterface`
or one of its subclasses.
"""

from newproject.interfaces.examples import *
from newproject.interfaces.generic import *
