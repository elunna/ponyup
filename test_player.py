import unittest
import player


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
    # Adding 0 chips results in no chips added.

    """
    Tests for showhand()
    """
    # A single hidden card is now not hidden.
    # A five card hand is not not hidden

    """
    Tests for fold()
    """
    # Folding 1 card. Player has no cards
    # Folding 1 card. Returns 1 card.
    # Folding 0 cards, Returns empty list.

    """
    Tests for add_card(card)
    """
    # Add 1 card to empty hand. Size = 1

    """
    Tests for discard(card)
    """
    # Discard 1 from empty hand - throw exception.
    # Discard 1 from 1 card hand - returns the card
    # Discard 1 from 1 card hand - hand is empty

    """
    Tests for makeplay(options, street)
    """
    # Where to start with this?

    """
    Tests for get_upcards()
    """
    # 1 card hand that is hidden - return empty list
    # 1 card hand that is up - return card
    # 2 card hand - 1 up, 1 down - returns the up card
