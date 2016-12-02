"""
  " Tests for stacks.py
  """
import unittest
from ponyup import factory
from ponyup import stacks
from ponyup import tools


class TestStacks(unittest.TestCase):
    """ Function tests for stacks.py """
    def setUp(self, _seats=6):
        self.t = factory.table_factory(seats=_seats, stepstacks=True)
        tools.deal_random_cards(self.t, 1)

    def test_largest_6players_returns600(self):
        self.setUp(_seats=6)
        expected = 600
        result = stacks.largest(self.t)
        self.assertEqual(expected, result)

    def test_smallest_6players_returns100(self):
        expected = 100
        result = stacks.smallest(self.t)
        self.assertEqual(expected, result)

    def test_average_6players_returns350(self):
        expected = 350
        result = stacks.average(self.t)
        self.assertEqual(expected, result)

    def test_effective_6players_returns350(self):
        self.setUp(_seats=6)
        expected = 350
        result = stacks.effective(self.t)
        self.assertEqual(expected, result)

    def test_effective_2players_returns100(self):
        self.setUp(_seats=2)
        expected = 100
        result = stacks.effective(self.t)
        self.assertEqual(expected, result)
