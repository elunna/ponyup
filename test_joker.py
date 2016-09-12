import unittest
import card
import joker
import pokerhands


class TestJoker(unittest.TestCase):
    """
    Tests for __str__()
    """
    def test_pickjoker_89TJrainbow_returnsQ(self):
        h = pokerhands.make('OESD 4card')
        j = joker.pick_joker(h)
        expected = 'Q'
        result = j.rank
        self.assertEqual(expected, result)

    def test_pickjoker_spadeflushdraw_returnsAs(self):
        h = pokerhands.make('flushdraw 4card')
        expected = card.Card('A', 's')
        result = joker.pick_joker(h)
        self.assertEqual(expected, result)

    def test_pickjoker_straightflushdraw_returnsAs(self):
        h = pokerhands.make('straightflush 4card')
        expected = card.Card('A', 's')
        result = joker.pick_joker(h)
        self.assertEqual(expected, result)

    def test_pickjoker_2AA_returnsA(self):
        h = pokerhands.make('2AA_v1')
        j = joker.pick_joker(h)
        expected = 'A'
        result = j.rank
        self.assertEqual(expected, result)
