import unittest
import deck
import card


class TestDeck(unittest.TestCase):
    """
    Tests for __init__ and Deck construction.
    """
    def test_init_nocards_stddeckwithsize52(self):
        d = deck.Deck()
        expected = 52
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_2cards_haslen2(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('K', 's'))
        d = deck.Deck(cards)
        expected = 2
        result = len(d)
        self.assertEqual(expected, result)

    """
    Tests for __str__
    """

    """
    Tests for __len__
    """

    """
    Tests for contains(card)
    """
    def test_contains_AceSpadesinStandardDeck_returnsTrue(self):
        d = deck.Deck()
        c = card.Card('A', 's')
        expected = True
        #  result = d.contains(c)
        result = c in d
        self.assertEqual(expected, result)

    def test_contains_JokerinStandardDeck_returnsFalse(self):
        d = deck.Deck()
        c = card.Card('Z', 's')
        expected = False
        #  result = d.contains(c)
        result = c in d
        self.assertEqual(expected, result)

    """
    Tests for shuffle()
    """

    """
    Tests for sort()
    """
    def test_sort_2cards_deuceisfirst(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('2', 's'))
        d = deck.Deck(cards)
        d.sort()
        expected = '2'
        result = d.cards[0].rank
        self.assertEqual(expected, result)

    def test_sort_3cards_deuceisfirst(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('7', 's'))
        cards.append(card.Card('2', 's'))
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
    Tests for unhide()
    """
