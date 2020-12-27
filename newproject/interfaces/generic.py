"""
Generic Interface module
"""

import sys
import abc


class GenericInterface(abc.ABC):
    """
    Generic Interface for all object of the package
    """

    @abc.abstractmethod
    def configuration(self) -> dict:
        """
        Return the configuration of the object as a dictionary
        """


def main():
    """
    Module entrypoint
    """
    sys.exit(0)


if __name__ == "__main__":
    main()
