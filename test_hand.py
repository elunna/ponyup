import unittest
import card
import hand


class TestHand(unittest.TestCase):
    def test_init_invalidboth_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 's', 'A')

    """
    Tests for __init__
    """
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

    """
    Tests for __len__()
    """
    # See add and discard tests

    """
    Tests for __str__
    """
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
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('K', 's'))
        h = hand.Hand(cards)
        h.unhide()
        expected = 'As Ks'
        result = str(h)
        self.assertEqual(expected, result)

    """
    Tests for add(card)
    """
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

    """
    Tests for discard(card)
    """
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

    """
    Tests for unhide()
    """
    # Unhide a 1 card hand, the card is up
    def test_unhide_1card_cardIsUp(self):
        c = card.Card('A', 's')
        h = hand.Hand([c])
        h.unhide()

        expected = False
        result = h.cards[0].hidden
        self.assertEqual(expected, result)

    # Unhide a 2 card hand, both cards are up
    def test_unhide_2cards_bothcardsUp(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('K', 's')
        h = hand.Hand()
        h.add(c1)
        h.add(c2)
        h.unhide()

        result = h.cards[0].hidden is False and h.cards[1].hidden is False
        self.assertTrue(result)

    """
    Tests for sort()
    """
    # Takes in a 564 hand and after it is 456
    def test_sort_unsortedhand_sortedafter(self):
        c1, c2, c3 = card.Card('5', 's'), card.Card('6', 's'), card.Card('4', 's')
        h = hand.Hand([c1, c2, c3])
        h.sort()
        expected = [c3, c1, c2]
        result = h.cards
        self.assertTrue(expected, result)

    """
    Tests for value()
    """

    """
    Tests for rank()
    """

    """
    Tests for desc()
    """

    """
    Tests for get_upcards()
    """
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
        c1 = card.Card('A', 's')
        c2 = card.Card('K', 's')
        c1.hidden = False
        h = hand.Hand([c1, c2])

        expected = 1
        result = len(h.get_upcards())
        self.assertEqual(expected, result)
