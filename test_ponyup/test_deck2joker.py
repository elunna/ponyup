import unittest
from ponyup import deck2joker
from ponyup import card


class TestDeck2Joker(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_Deck2Joker_size54(self):
        d = deck2joker.Deck2Joker()
        expected = 54
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_Deck2Joker_containsZsZc(self):
        d = deck2joker.Deck2Joker()
        joker1 = card.Card('Z', 's')
        joker2 = card.Card('Z', 'c')
        expected = True
        #  result = d.contains(joker1) and d.contains(joker2)
        result = joker1 in d and joker2 in d
        self.assertEqual(expected, result)
