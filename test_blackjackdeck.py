import unittest
import blackjack_deck
import card


class TestBlackjackDeck(unittest.TestCase):
    """
    Tests for __init__
    """
    def test_init_0shoes_raiseException(self):
        self.assertRaises(ValueError, blackjack_deck.BlackjackDeck, 0)

    def test_init_negshoes_raiseException(self):
        self.assertRaises(ValueError, blackjack_deck.BlackjackDeck, -1)

    def test_init_4shoes_208cards(self):
        d = blackjack_deck.BlackjackDeck(4)
        expected = 208
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_4shoes_4AceSpaces(self):
        d = blackjack_deck.BlackjackDeck(4)
        c = card.Card('A', 's')
        expected = 4
        result = d.cards.count(c)
        self.assertEqual(expected, result)

    def test_init_6shoes_312cards(self):
        d = blackjack_deck.BlackjackDeck(6)
        expected = 312
        result = len(d)
        self.assertEqual(expected, result)
