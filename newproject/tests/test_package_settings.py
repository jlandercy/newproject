"""
Module for settings tests
"""

import sys
import unittest

from newproject import settings


class TestSettings(unittest.TestCase):
    """
    Package settings tests
    """

    def test_namespace(self):
        """
        Test namespace type
        """
        self.assertIsInstance(settings.settings, settings.SimpleNamespace)

    def test_required_keys(self):
        """
        Test namespace keys
        """
        self.assertTrue({"package", "user", "resources", "uuid4"}
                        .issubset(settings.settings.__dict__))


def main():
    """
    Module entrypoint
    """
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
