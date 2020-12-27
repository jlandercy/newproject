"""
Implemented Interface Examples
"""

import sys
from typing import Any
import datetime

from newproject.interfaces.generic import GenericInterface


class SimpleCase(GenericInterface):

    def __init__(self, value: Any = None) -> None:
        self.value = value

    def to_dict(self) -> dict:
        return {"value": self.value}


class SimpleCaseWithSerializer(SimpleCase):

    @staticmethod
    def serializer(instance: Any) -> Any:
        if isinstance(instance, datetime.datetime):
            return instance.isoformat()
        else:
            return super().serializer(instance)


def main():
    """
    Module entrypoint
    """
    sys.exit(0)


if __name__ == "__main__":
    main()
