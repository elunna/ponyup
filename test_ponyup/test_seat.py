"""
  " Tests for seat.py
  """
import unittest
from ponyup import card
from ponyup import player
from ponyup import seat


class TestSeat(unittest.TestCase):
    """ Function tests for seat.py """

    def setUp(self):
        self.s = seat.Seat(1)
        self.p = player.Player("Erik")
        self.p.bank = 1000

    def test_init_newseat_playerNone(self):
        expected = None
        result = self.s.player
        self.assertEqual(expected, result)

    # Test that the players name shows up
    def test_str_playersitting_returnsName(self):
        self.s.sitdown(self.p)
        expected = 'Erik'
        result = str(self.s)
        self.assertEqual(expected, result)

    # If no player is sitting, returns 'Open Seat'
    def test_str_empty_returnsOpenSeat(self):
        expected = 'Open Seat'
        result = str(self.s)
        self.assertEqual(expected, result)

    # Same seat, no player, are equal
    def test_eq_sameseat_noplayer_returnsTrue(self):
        seatcopy = self.s
        expected = True
        result = self.s == seatcopy
        self.assertEqual(expected, result)

    # Different seats, not equal
    def test_eq_different_returnsFalse(self):
        s2 = seat.Seat(2)
        expected = False
        result = self.s == s2
        self.assertEqual(expected, result)

    # Different seats, same players, not equal
    def test_eq_diffseats_sameplayers_returnsFalse(self):
        s2 = seat.Seat(2)
        self.s.sitdown(self.p)
        s2.sitdown(self.p)
        expected = False
        result = self.s == s2
        self.assertEqual(expected, result)

    # Same seats, same players, equal
    def test_eq_sameseats_sameplayers_returnsTrue(self):
        s2 = seat.Seat(1)
        self.s.sitdown(self.p)
        s2.sitdown(self.p)
        expected = True
        result = self.s == s2
        self.assertEqual(expected, result)

    def test_eq_sameplayers_diffstacks_returnsFalse(self):
        """ Same seats, same players, diff stacks, not equal """
        s2 = seat.Seat(1)
        self.s.sitdown(self.p)
        s2.sitdown(self.p)
        self.s.buy_chips(100)
        s2.buy_chips(300)

        expected = False
        result = self.s == s2
        self.assertEqual(expected, result)

    def test_sitdown_player_isnotEmpty(self):
        self.s.sitdown(self.p)
        expected = False
        result = self.s.vacant()
        self.assertEqual(expected, result)

    def test_sitdown_player_matchesSeatPlayer(self):
        self.s.sitdown(self.p)
        expected = self.p
        result = self.s.player
        self.assertEqual(expected, result)

    def test_sitdown_dupeplayer_attable_raiseException(self):
        pass

    def test_standup_existingplayer_isempty(self):
        self.s.sitdown(self.p)
        self.s.standup()
        expected = True
        result = self.s.vacant()
        self.assertEqual(expected, result)

    def test_standup_playerwithchips_0chips(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        self.s.standup()
        expected = 0
        result = self.s.stack
        self.assertEqual(expected, result)

    def test_standup_playersitting_returnsPlayer(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        expected = self.p
        result = self.s.standup()
        self.assertEqual(expected, result)

    def test_vacant_emptyseat_returnsTrue(self):
        self.assertTrue(self.s.vacant())

    def test_occupied_emptyseat_returnsFalse(self):
        expected = False
        result = self.s.occupied()
        self.assertEqual(expected, result)

    def test_occupied_filledseat_returnsTrue(self):
        self.s.sitdown(self.p)
        expected = True
        result = self.s.occupied()
        self.assertEqual(expected, result)

    def test_hashand_emptyseat_returnsFalse(self):
        self.assertFalse(self.s.has_hand())

    def test_hashand_filledseat_returnsFalse(self):
        # Has a player, but still no hand
        self.s.sitdown(self.p)
        self.assertFalse(self.s.has_hand())

    def test_hashand_1card_returnsTrue(self):
        self.s.sitdown(self.p)
        self.s.hand.add(card.Card('A', 's'))
        expected = True
        result = self.s.has_hand()
        self.assertEqual(expected, result)

    def test_haschips_playerboughtchips_returnsTrue(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        expected = True
        result = self.s.has_chips()
        self.assertEqual(expected, result)

    def test_haschips_playerdidnotbuychips_returnsFalse(self):
        self.s.sitdown(self.p)
        expected = False
        result = self.s.has_chips()
        self.assertEqual(expected, result)

    def test_buychips_emptyseat_raiseException(self):
        self.assertRaises(Exception, self.s.buy_chips)

    def test_buychips_negamount_raiseException(self):
        self.s.sitdown(self.p)
        self.assertRaises(ValueError, self.s.buy_chips, -1)

    def test_buychips_exceedsplayerbank_raiseException(self):
        self.s.sitdown(self.p)
        self.assertRaises(ValueError, self.s.buy_chips, 100000000)

    def test_buychips_100_returns100(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        expected = 100
        result = self.s.stack
        self.assertEqual(expected, result)

    def test_buychips_buy100twice_returns200(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        self.s.buy_chips(100)
        expected = 200
        result = self.s.stack
        self.assertEqual(expected, result)

    def test_win_negamount_raiseException(self):
        self.s.sitdown(self.p)
        self.assertRaises(ValueError, self.s.win, -1)

    def test_win_100_stackis100(self):
        self.s.sitdown(self.p)
        expected = 100
        self.s.win(100)
        result = self.s.stack
        self.assertEqual(expected, result)

    def test_bet_stack100_bets10_returns10(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        expected = 10
        result = self.s.bet(10)
        self.assertEqual(expected, result)

    def test_bet_stack100_bets10_stack90(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        expected = 90
        self.s.bet(10)
        result = self.s.stack
        self.assertEqual(expected, result)

    #  def test_bet_broke_raiseException(self):
        #  self.s.sitdown(self.p)
        #  self.assertRaises(ValueError, self.s.bet, 10)

    def test_bet_stack100_bets100_return100(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        expected = 100
        result = self.s.bet(100)
        self.assertEqual(expected, result)

    def test_bet_overstack_returnsStack(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        expected = 100
        result = self.s.bet(1000)
        self.assertEqual(expected, result)

    def test_bet_stack100_bets0_raiseException(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        self.assertRaises(ValueError, self.s.bet, 0)

    def test_bet_stack100_betsNegative_raiseException(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        self.assertRaises(ValueError, self.s.bet, -1)

    # Folding 1 card. Player has no cards
    def test_fold_1card_handisempty(self):
        c = card.Card('A', 's')
        self.s.hand.add(c)
        self.s.fold()
        expected = 0
        result = len(self.s.hand)
        self.assertEqual(expected, result)

    # Folding 1 card. Returns 1 card.
    def test_fold_1card_return1card(self):
        c = card.Card('A', 's')
        self.s.hand.add(c)
        h = self.s.fold()
        expected = 1
        result = len(h)
        self.assertEqual(expected, result)

    # Folding 0 cards, Returns empty list.
    def test_fold_0cards_returnEmptyList(self):
        h = self.s.fold()
        expected = 0
        result = len(h)
        self.assertEqual(expected, result)
