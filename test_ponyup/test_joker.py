"""
  " Tests for joker.py
  """
import unittest
from ponyup import card
from ponyup import joker
from ponyup import tools


class TestJoker(unittest.TestCase):
    """ Function tests for joker.py """

    def test_pickjoker_89TJrainbow_returnsQ(self):
        h = tools.make('OESD 4card')
        j = joker.pick_joker(h)
        expected = 'Q'
        result = j.rank
        self.assertEqual(expected, result)

    def test_pickjoker_spadeflushdraw_returnsAs(self):
        h = tools.make('flushdraw 4card')
        expected = card.Card('A', 's')
        result = joker.pick_joker(h)
        self.assertEqual(expected, result)

    def test_pickjoker_straightflushdraw_returnsAs(self):
        h = tools.make('straightflush 4card')
        expected = card.Card('A', 's')
        result = joker.pick_joker(h)
        self.assertEqual(expected, result)

    def test_pickjoker_2AA_returnsA(self):
        h = tools.make('2AA_v1')
        j = joker.pick_joker(h)
        expected = 'A'
        result = j.rank
        self.assertEqual(expected, result)
