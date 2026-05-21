import unittest

from config import AppConfig


class TestAppConfig(unittest.TestCase):
    def test_singleton_returns_same_instance(self):
        first = AppConfig()
        second = AppConfig()
        self.assertIs(first, second)
