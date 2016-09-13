import unittest
import deck
import card
import joker
import tools


class TestDeck(unittest.TestCase):
    """
    Tests for __str__()
    """
    def test_str_2cards_returnsAsKsinParentheses(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        d = deck.Deck(cards)
        d.unhide()  # They are hidden by default
        expected = 'As Ks'
        result = str(d)
        self.assertEqual(expected, result)

    """
    Tests for __len__()
    """
    def test_len_size52(self):
        d = deck.Deck()
        expected = 52
        result = len(d)
        self.assertEqual(expected, result)

    def test_len_2cards_haslen2(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        d = deck.Deck(cards)
        expected = 2
        result = len(d)
        self.assertEqual(expected, result)

    """
    Tests for contains(card)
    """
    def test_contains_AceSpadesinStandardDeck_returnsTrue(self):
        d = deck.Deck()
        c = card.Card('A', 's')
        expected = True
        result = c in d
        self.assertEqual(expected, result)

    def test_contains_JokerinStandardDeck_returnsFalse(self):
        d = deck.Deck()
        c = joker.JOKER1
        expected = False
        result = c in d
        self.assertEqual(expected, result)

    """
    Tests for shuffle()
    """

    """
    Tests for sort()
    """
    def test_sort_2cards_deuceisfirst(self):
        cards = tools.convert_to_cards(['As', '2s'])
        d = deck.Deck(cards)
        d.sort()
        expected = '2'
        result = d.cards[0].rank
        self.assertEqual(expected, result)

    def test_sort_3cards_deuceisfirst(self):
        cards = tools.convert_to_cards(['As', '7s', '2s'])
        d = deck.Deck(cards)
        d.sort()
        expected = '2'
        result = d.cards[0].rank
        self.assertEqual(expected, result)

    """
    Tests for deal()
    """
    def test_deal_stddeck_sizeIs51(self):
        d = deck.Deck()
        d.deal()
        expected = 51
        result = len(d)
        self.assertEqual(expected, result)

    def test_deal_As_returnsCard(self):
        c = card.Card('A', 's')
        d = deck.Deck([c])
        expected = c
        result = d.deal()
        self.assertEqual(expected, result)

    def test_deal_emptydeck_raiseException(self):
        d = deck.Deck([])
        self.assertEqual(len(d), 0)
        self.assertRaises(Exception, d.deal)

    """
    Tests for is_empty()
    """
    def test_isempty_fulldeck_returnFalse(self):
        d = deck.Deck()
        expected = False
        result = d.is_empty()
        self.assertEqual(expected, result)

    def test_isempty_emptydeck_returnTrue(self):
        d = deck.Deck([])
        expected = True
        result = d.is_empty()
        self.assertEqual(expected, result)

    """
    Tests for remove(card)
    """
    def test_remove_removeAs_sizeIs51(self):
        d = deck.Deck()
        c = card.Card('A', 's')
        d.remove(c)
        expected = 51
        result = len(d)
        self.assertEqual(expected, result)

    def test_remove_cardnotindeck_returnsNone(self):
        d = deck.Deck()
        c = card.Card('Z', 's')
        expected = None
        result = d.remove(c)
        self.assertEqual(expected, result)

    """
    Tests for remove_cards(cards)
    """
    def test_removecards_removeAs_sizeIs51(self):
        d = deck.Deck()
        c = card.Card('A', 's')
        d.remove_cards([c])
        expected = 51
        result = len(d)
        self.assertEqual(expected, result)

    def test_removecards_removeAs_containsIsFalse(self):
        d = deck.Deck()
        c = card.Card('A', 's')
        d.remove_cards([c])
        expected = False
        result = c in d
        self.assertEqual(expected, result)

    def test_removecards_removeAsKs_containsNeither(self):
        d = deck.Deck()
        cards = tools.convert_to_cards(['As', 'Ks'])
        d.remove_cards(cards)
        self.assertFalse(cards[0] in d)
        self.assertFalse(cards[1] in d)

    """
    Tests for unhide()
    """
    # All cards in deck are faceup
    def test_unhide_2cards_bothfaceup(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        d = deck.Deck(cards)
        d.unhide()
        self.assertTrue(d.cards[0].hidden is False)
        self.assertTrue(d.cards[1].hidden is False)
