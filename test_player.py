import unittest
import card
import player
import pokerhands


class TestPlayer(unittest.TestCase):

    """
    Tests for __init__
    """
    # valid name, player name is ok
    def test_init_validname_namematches(self):
        p = player.Player('Erik')
        expected = 'Erik'
        result = p.name
        self.assertEqual(expected, result)

    # name too short - raise ex
    def test_init_nametooshort_raiseException_(self):
        self.assertRaises(ValueError, player.Player, 'ab')

    # name too long - raise ex
    def test_init_nametoolong_raiseException_(self):
        self.assertRaises(ValueError, player.Player, 'EEEErrrriiiikkkk')

    # playertype isn't valid - raise ex
    def test_init_invalidplayertype_raiseException_(self):
        self.assertRaises(ValueError, player.Player, 'Erik', 'ROBOT')

    # new player - chips == 0
    def test_init_validname_has0chips(self):
        p = player.Player('Erik')
        expected = 0
        result = p.chips
        self.assertEqual(expected, result)

    # new player - hand is empty
    def test_init_validname_emptyhand(self):
        p = player.Player('Erik')
        expected = 0
        result = len(p._hand)
        self.assertEqual(expected, result)

    # new player - strategy is None
    def test_init_validname_strategyisNone(self):
        p = player.Player('Erik')
        expected = None
        result = p.strategy
        self.assertEqual(expected, result)

    def test_init__(self):
        self.assertRaises(ValueError, player.Player, 'ab')

    """
    Tests for __str__
    """
    # Return players name
    def test_str_validname_returnsName(self):
        p = player.Player('Erik')
        expected = 'Erik'
        result = str(p)
        self.assertEqual(expected, result)

    """
    Tests for __repr__
    """
    # Return players name
    def test_repr_validname_returnsName(self):
        p = player.Player('Erik')
        expected = 'Erik'
        result = p.__repr__()
        self.assertEqual(expected, result)

    """
    Tests for bet(amt)
    """
    # If a player has 0 and bets 0, it returns 0
    def test_bet_has0chipsbets0_returns0(self):
        p = player.Player('Erik')
        expected = 0
        result = p.bet(0)
        self.assertEqual(expected, result)

    # If a player has 0 and bets 1, it returns 0
    def test_bet_has0chipsbets1_returns0(self):
        p = player.Player('Erik')
        expected = 0
        result = p.bet(1)
        self.assertEqual(expected, result)

    # If a player has 1 and bets 1, it returns 1
    def test_bet_has1chipbets1_returns1(self):
        p = player.Player('Erik')
        p.add_chips(1)
        expected = 1
        result = p.bet(1)
        self.assertEqual(expected, result)

    # If a player has 1 and bets 1, they have 0 chips.
    def test_bet_has1chipbets1_has0chips(self):
        p = player.Player('Erik')
        p.add_chips(1)
        p.bet(1)
        expected = 0
        result = p.chips
        self.assertEqual(expected, result)

    """
    Tests for add_chips(amt)
    """
    # Adding 1 chip results in their stack being 1. Starting with 1.
    def test_addchips_newplayer_add1chip_has1chip(self):
        p = player.Player('Erik')
        p.add_chips(1)
        expected = 1
        result = p.chips
        self.assertEqual(expected, result)

    # Adding 0 chips results in no chips added.
    def test_addchips_newplayer_add0chips_has0chip(self):
        p = player.Player('Erik')
        p.add_chips(0)
        expected = 0
        result = p.chips
        self.assertEqual(expected, result)

    """
    Tests for showhand()
    """
    # A single hidden card is now not hidden.
    def test_showhand_has1card_cardisup(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        p.add_card(c)
        p.showhand()
        expected = False
        result = p._hand.cards[0].hidden
        self.assertEqual(expected, result)

    # A five card hand is not not hidden
    def test_showhand_has5cards_allareup(self):
        p = player.Player('Erik')
        for c in pokerhands.royalflush():
            p.add_card(c)
        p.showhand()
        expected = True
        allup = True
        for c in p._hand.cards:
            if c.hidden is True:
                allup = False
                break
        self.assertEqual(expected, allup)

    """
    Tests for fold()
    """
    # Folding 1 card. Player has no cards
    def test_fold_1card_handisempty(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        p.add_card(c)
        p.fold()
        expected = 0
        result = len(p._hand)
        self.assertEqual(expected, result)

    # Folding 1 card. Returns 1 card.
    def test_fold_1card_return1card(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        p.add_card(c)
        h = p.fold()
        expected = 1
        result = len(h)
        self.assertEqual(expected, result)

    # Folding 0 cards, Returns empty list.
    def test_fold_0cards_returnEmptyList(self):
        p = player.Player('Erik')
        h = p.fold()
        expected = 0
        result = len(h)
        self.assertEqual(expected, result)

    """
    Tests for add_card(card)
    """
    # Add 1 card to empty hand. Size = 1
    def test_addcard_1card_sizeequals1(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        p.add_card(c)
        expected = 1
        result = len(p._hand)
        self.assertEqual(expected, result)

    """
    Tests for discard(card)
    """
    # Discard a card not in player's hand- throw exception.
    def test_discard_cardnotinhand_raiseEx(self):
        p = player.Player('Erik')
        c1 = card.Card('A', 's')
        c2 = card.Card('K', 's')
        p.add_card(c1)
        self.assertRaises(ValueError, p.discard, c2)

    # Discard 1 from 1 card hand - returns the card
    def test_discard_1cardhand_returnsCard(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        p.add_card(c)
        result = p.discard(c)
        self.assertEqual(c, result)

    # Discard 1 from 1 card hand - hand is empty
    def test_discard_1cardhand_sizeequals0(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        p.add_card(c)
        p.discard(c)
        expected = 0
        result = len(p._hand)
        self.assertEqual(expected, result)

    """
    Tests for get_upcards()
    """
    # 1 card hand that is hidden - return empty list
    def test_getupcards_1downcard_returnsEmptyList(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        p.add_card(c)
        expected = []
        result = p.get_upcards()
        self.assertEqual(expected, result)

    # 1 card hand that is up - return card
    def test_getupcards_1upcard_returnsUpCard(self):
        p = player.Player('Erik')
        c = card.Card('A', 's')
        c.hidden = False
        p.add_card(c)
        expected = [c]
        result = p.get_upcards()
        self.assertEqual(expected, result)

    # 2 card hand - 1 up, 1 down - returns the up card
    def test_getupcards_1up1down_returns1up(self):
        p = player.Player('Erik')
        c1 = card.Card('A', 's')
        c2 = card.Card('K', 's')
        c1.hidden = False
        p.add_card(c1)
        p.add_card(c2)

        expected = 1
        result = len(p.get_upcards())
        self.assertEqual(expected, result)

    """
    Tests for makeplay(options, street)
    """
    # Where to start with this?
