import unittest
from ponyup import deck
from ponyup import card
from ponyup import tools


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
        c = card.JOKER1
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


class TestDeck1Joker(unittest.TestCase):
    """
    Tests for subclasses
    """
    def test_init_Deck1Joker_size53(self):
        d = deck.Deck1Joker()
        expected = 53
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_Deck1Joker_containsZs(self):
        d = deck.Deck1Joker()
        joker = card.Card('Z', 's')
        expected = True
        #  result = d.contains(joker)
        result = joker in d
        self.assertEqual(expected, result)


class TestDeck2Joker(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_Deck2Joker_size54(self):
        d = deck.Deck2Joker()
        expected = 54
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_Deck2Joker_containsZsZc(self):
        d = deck.Deck2Joker()
        joker1 = card.Card('Z', 's')
        joker2 = card.Card('Z', 'c')
        expected = True
        #  result = d.contains(joker1) and d.contains(joker2)
        result = joker1 in d and joker2 in d
        self.assertEqual(expected, result)


class TestPiquetDeck(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_PiquetDeck_size32(self):
        d = deck.PiquetDeck()
        expected = 32
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_PiquetDeck_4Aces(self):
        d = deck.PiquetDeck()
        expected = 4
        result = 0
        for c in d.cards:
            if c.rank == 'A':
                result += 1
        self.assertEqual(expected, result)

    def test_init_PiquetDeck_1AceSpades(self):
        d = deck.PiquetDeck()
        c = card.Card('A', 's')
        expected = 1
        result = d.cards.count(c)
        self.assertEqual(expected, result)


class TestPinochleDeck(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_PinochleDeck_size48(self):
        d = deck.PinochleDeck()
        expected = 48
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_PinochleDeck_8Aces(self):
        d = deck.PinochleDeck()
        expected = 8
        result = 0
        for c in d.cards:
            if c.rank == 'A':
                result += 1
        self.assertEqual(expected, result)

    def test_init_PinochleDeck_2AceSpades(self):
        c = card.Card('A', 's')
        d = deck.PinochleDeck()
        expected = 2
        result = d.cards.count(c)
        self.assertEqual(expected, result)


class TestBlackjackDeck(unittest.TestCase):
    """
    Tests for __init__
    """
    def test_init_0shoes_raiseException(self):
        self.assertRaises(ValueError, deck.BlackjackDeck, 0)

    def test_init_negshoes_raiseException(self):
        self.assertRaises(ValueError, deck.BlackjackDeck, -1)

    def test_init_4shoes_208cards(self):
        d = deck.BlackjackDeck(4)
        expected = 208
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_4shoes_4AceSpaces(self):
        d = deck.BlackjackDeck(4)
        c = card.Card('A', 's')
        expected = 4
        result = d.cards.count(c)
        self.assertEqual(expected, result)

    def test_init_6shoes_312cards(self):
        d = deck.BlackjackDeck(6)
        expected = 312
        result = len(d)
        self.assertEqual(expected, result)
