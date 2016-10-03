import unittest
from ponyup import pinochle_deck
from ponyup import card


class TestPinochleDeck(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_PinochleDeck_size48(self):
        d = pinochle_deck.PinochleDeck()
        expected = 48
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_PinochleDeck_8Aces(self):
        d = pinochle_deck.PinochleDeck()
        expected = 8
        result = 0
        for c in d.cards:
            if c.rank == 'A':
                result += 1
        self.assertEqual(expected, result)

    def test_init_PinochleDeck_2AceSpades(self):
        c = card.Card('A', 's')
        d = pinochle_deck.PinochleDeck()
        expected = 2
        result = d.cards.count(c)
        self.assertEqual(expected, result)
