import unittest
from ponyup import piquet_deck
from ponyup import card


class TestPiquetDeck(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_PiquetDeck_size32(self):
        d = piquet_deck.PiquetDeck()
        expected = 32
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_PiquetDeck_4Aces(self):
        d = piquet_deck.PiquetDeck()
        expected = 4
        result = 0
        for c in d.cards:
            if c.rank == 'A':
                result += 1
        self.assertEqual(expected, result)

    def test_init_PiquetDeck_1AceSpades(self):
        d = piquet_deck.PiquetDeck()
        c = card.Card('A', 's')
        expected = 1
        result = d.cards.count(c)
        self.assertEqual(expected, result)
