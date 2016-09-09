import unittest
import holdem
import pokerhands


class TestHoldem(unittest.TestCase):
    """
    Test for valid_holecards(cards):
    """
    # 1 card - raises exception
    def test_validholecards_1card_returnsFalse(self):
        cards = pokerhands.make('A')
        expected = False
        result = holdem.valid_holecards(cards)
        self.assertEqual(expected, result)

    def test_cards2text_JTQ_returnsFalse(self):
        cards = pokerhands.make('JTQ')
        expected = False
        result = holdem.valid_holecards(cards)
        self.assertEqual(expected, result)

    def test_cards2text_2unique_returnsTrue(self):
        cards = pokerhands.make('AKo')
        expected = True
        result = holdem.valid_holecards(cards)
        self.assertEqual(expected, result)

    def test_cards2text_2dupes_returnsFalse(self):
        cards = pokerhands.make('KK_dupes')
        expected = False
        result = holdem.valid_holecards(cards)
        self.assertEqual(expected, result)

    """
    Tests for card2text(cards):
    """

    # 1 card - raises exception
    def test_cards2text_As_raiseException(self):
        cards = pokerhands.make('A')
        self.assertRaises(ValueError, holdem.card2text, cards)

    # 3 cards- raises exception
    def test_cards2text_JTQ_raiseException(self):
        cards = pokerhands.make('JTQ')
        self.assertRaises(ValueError, holdem.card2text, cards)

    # AsKd - returns AKo
    def test_cards2text_AsKd_returnsAKo(self):
        cards = pokerhands.make('AKo')
        expected = 'AKo'
        result = holdem.card2text(cards)
        self.assertEqual(expected, result)

    # AsKs - returns AKs
    def test_cards2text_AcKc_returnsAKs(self):
        cards = pokerhands.make('AKs')
        expected = 'AKs'
        result = holdem.card2text(cards)
        self.assertEqual(expected, result)

    # AsAc - returns AA
    def test_cards2text_AcAh_returnsAA(self):
        cards = pokerhands.make('AA')
        expected = 'AA'
        result = holdem.card2text(cards)
        self.assertEqual(expected, result)
