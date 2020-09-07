from unittest import TestCase
from applocker.policy import AppLockerPolicy
from applocker.utils import dumps, loads


class TestUtils(TestCase):
    def test_dumps(self):
        policy = AppLockerPolicy()
        self.assertEqual(dumps(policy), '<AppLockerPolicy Version="1" />')

    def test_loads(self):
        policy = loads('<AppLockerPolicy Version="1" />')
        self.assertIsInstance(policy, AppLockerPolicy)
