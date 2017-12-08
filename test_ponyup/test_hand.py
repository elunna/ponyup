"""
  " Tests for hand.py
  """
import unittest
from ponyup import card
from ponyup import hand
from ponyup import tools


class TestHand(unittest.TestCase):
    """ Function tests for hand.py """

    def test_init_invalidboth_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 's', 'A')

    # No cards pass, length = 0
    def test_init_0cardspassed_length0(self):
        h = hand.Hand()
        expected = 0
        result = len(h)
        self.assertEqual(expected, result)

    # 1 card passed, length = 1
    def test_init_1cardpassed_length1(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        expected = 1
        result = len(h)
        self.assertEqual(expected, result)

    # 1 card passed, contains the card
    def test_init_1cardpassed_containsCard(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        expected = True
        result = c in h.cards
        self.assertEqual(expected, result)

    # No cards pass, displays nothing
    def test_str_0cardspassed_returnsNothing(self):
        h = hand.Hand()
        expected = ''
        result = str(h)
        self.assertEqual(expected, result)

    # 1 card passed, displays the hidden card as "Xx"
    def test_str_1card_hidden_returnsAs(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        expected = 'Xx'
        result = str(h)
        self.assertEqual(expected, result)

    # 1 card passed, displays the hidden card as "Xx"
    def test_str_1card_unhidden_returnsAs(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        h.unhide()
        expected = 'As'
        result = str(h)
        self.assertEqual(expected, result)

    # 1 card passed, displays the hidden card as "Xx"
    def test_str_2cards_unhidden_returnsAs_Ks(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        h = hand.Hand(cards)
        h.unhide()
        expected = 'As Ks'
        result = str(h)
        self.assertEqual(expected, result)

    # Empty hand, adding 1 card, size = 1
    def test_add_1card_length1(self):
        c = card.Card('A', 's')
        h = hand.Hand()
        h.add(c)
        expected = 1
        result = len(h)
        self.assertEqual(expected, result)

    # Empty hand, adding 1 card, contains the card
    def test_add_1card_containsCard(self):
        c = card.Card('A', 's')
        h = hand.Hand()
        h.add(c)
        expected = True
        result = c in h.cards
        self.assertEqual(expected, result)

    # Discarding the only card in the hand, size = 0
    def test_discard_1card_length0(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        h.discard(c)
        expected = 0
        result = len(h)
        self.assertEqual(expected, result)

    # Discarding the only card in the hand, returns the card
    def test_discard_1card_returnsCard(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        expected = c
        result = h.discard(c)
        self.assertEqual(expected, result)

    # Discarding a card not in the hand, raise exception
    def test_discard_cardNotInHand_raiseException(self):
        c = card.Card('A', 's')
        h = hand.Hand()
        self.assertRaises(ValueError, h.discard, c)

    # Unhide a 1 card hand, the card is up
    def test_unhide_1card_cardIsUp(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        h.unhide()

        expected = False
        result = h.cards[0].hidden
        self.assertEqual(expected, result)

    def test_unhide_2cards_bothcardsUp(self):
        """ Unhide a 2 card hand, both cards are up """
        c1 = card.Card('A', 's')
        c2 = card.Card('K', 's')
        h = hand.Hand()
        h.add(c1)
        h.add(c2)
        h.unhide()

        result = h.cards[0].hidden is False and h.cards[1].hidden is False
        self.assertTrue(result)

    # Takes in a 564 hand and after it is 456
    def test_sort_unsortedhand_sortedafter(self):
        cards = tools.convert_to_cards(['5s', '6s', '4s'])
        h = hand.Hand(cards)
        h.sort()
        expected = [cards[2], cards[1], cards[0]]
        result = h.cards
        self.assertTrue(expected, result)

    def test_value_royalflush_returns100000000000(self):
        h = hand.Hand(tools.make('royalflush'))
        expected = 100000000000
        result = h.value()
        self.assertTrue(expected, result)

    def test_rank_royalflush_returnsROYALFLUSH(self):
        h = hand.Hand(tools.make('royalflush'))
        expected = 'ROYAL FLUSH'
        result = h.rank()
        self.assertTrue(expected, result)

    def test_desc_royalflush_AceHigh(self):
        h = hand.Hand(tools.make('royalflush'))
        expected = 'A high'
        result = h.rank()
        self.assertTrue(expected, result)

    # 1 card hand that is hidden - return empty list
    def test_getupcards_1downcard_returnsEmptyList(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        expected = []
        result = h.get_upcards()
        self.assertEqual(expected, result)

    # 1 card hand that is up - return card
    def test_getupcards_1upcard_returnsUpCard(self):
        c = card.Card('A', 's')
        c.hidden = False
        h = hand.Hand([c])
        expected = [c]
        result = h.get_upcards()
        self.assertEqual(expected, result)

    # 2 card hand - 1 up, 1 down - returns the up card
    def test_getupcards_1up1down_returns1up(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        cards[0].hidden = False
        h = hand.Hand(cards)

        expected = 1
        result = len(h.get_upcards())
        self.assertEqual(expected, result)

    def test_peek_AsKs_returnslist(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        h = hand.Hand(cards)
        expected = ['As ', 'Ks ']
        result = h.peek()
        self.assertEqual(expected, result)

    def test_peek_AsKs_stillhidden(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        h = hand.Hand(cards)
        h.peek()
        result = h.cards[0].hidden is True and h.cards[1].hidden is True
        self.assertTrue(result)
