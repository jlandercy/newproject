import sys
import abc

import newproject
from newproject.settings import settings


class GenericInterface(abc.ABC):
    """
    Generic Interface for all object of the package
    """

    @abc.abstractmethod
    def configuration(self) -> dict:
        """
        Return the configuration of the object as a dictionary
        """
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
