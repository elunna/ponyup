"""
  " Tests for sessions.py
  """
import unittest
from ponyup import factory


class TestSessions(unittest.TestCase):
    """ Function tests for sessions.py """
    def test_clearbrokeplayers(self):
        s = factory.session_factory(seats=6, game='FIVE CARD DRAW', level=1)
        p = s.table.seats[0]
        p.stack = 0
        expected = []
        s.clear_broke_players()
        result = s.table.get_broke_players()
        self.assertEqual(expected, result)
