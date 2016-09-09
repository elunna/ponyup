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
        result = p.withdraw(0)
        self.assertEqual(expected, result)

    # If a player has 0 and bets 1, it returns 0
    def test_bet_has0chipsbets1_returns0(self):
        p = player.Player('Erik')
        expected = 0
        result = p.withdraw(1)
        self.assertEqual(expected, result)

    # If a player has 1 and bets 1, it returns 1
    def test_bet_has1chipbets1_returns1(self):
        p = player.Player('Erik')
        p.deposit(1)
        expected = 1
        result = p.withdraw(1)
        self.assertEqual(expected, result)

    # If a player has 1 and bets 1, they have 0 chips.
    def test_bet_has1chipbets1_has0chips(self):
        p = player.Player('Erik')
        p.deposit(1)
        p.withdraw(1)
        expected = 0
        result = p.chips
        self.assertEqual(expected, result)

    # If a player has 1 and bets 1, they have 0 chips.
    def test_bet_negativebet_raisesException(self):
        p = player.Player('Erik')
        p.deposit(1)
        self.assertRaises(ValueError, p.withdraw, -1)

    """
    Tests for add_chips(amt)
    """
    # Adding 1 chip results in their stack being 1. Starting with 1.
    def test_addchips_newplayer_add1chip_has1chip(self):
        p = player.Player('Erik')
        p.deposit(1)
        expected = 1
        result = p.chips
        self.assertEqual(expected, result)

    # Adding 0 chips results in no chips added.
    def test_addchips_newplayer_add0chips_has0chip(self):
        p = player.Player('Erik')
        p.deposit(0)
        expected = 0
        result = p.chips
        self.assertEqual(expected, result)

    # Cannot add negative chips!
    def test_addchips_negativechips_raisesException(self):
        p = player.Player('Erik')
        self.assertRaises(Exception, p.deposit, -100)

    """
    Tests for makeplay(options, street)
    """
    # Where to start with this?
