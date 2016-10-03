import unittest
from ponyup import deck1joker
from ponyup import card


class TestDeck1Joker(unittest.TestCase):
    """
    Tests for subclasses
    """
    def test_init_Deck1Joker_size53(self):
        d = deck1joker.Deck1Joker()
        expected = 53
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_Deck1Joker_containsZs(self):
        d = deck1joker.Deck1Joker()
        joker = card.Card('Z', 's')
        expected = True
        #  result = d.contains(joker)
        result = joker in d
        self.assertEqual(expected, result)
