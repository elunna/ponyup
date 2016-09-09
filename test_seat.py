import unittest
import player
import seat
import table


class TestSeat(unittest.TestCase):

    def setUp(self):
        t = table.Table(6)
        self.s = seat.Seat(t)
        self.p = player.Player("Erik")
        self.p.chips = 1000

    """
    Tests for __init__()
    """
    def test_init_newseat_playerNone(self):
        expected = None
        result = self.s.player
        self.assertEqual(expected, result)

    """
    Tests for sitdown(self, player):
    """
    def test_sitdown_player_isnotEmpty(self):
        self.s.sitdown(self.p)
        expected = False
        result = self.s.is_empty()
        self.assertEqual(expected, result)

    def test_sitdown_player_matchesSeatPlayer(self):
        self.s.sitdown(self.p)
        expected = self.p
        result = self.s.player
        self.assertEqual(expected, result)

    def test_sitdown_dupeplayer_attable_raiseException(self):
        pass

    """
    Tests for standup(self, player):
    """
    def test_standup_existingplayer_isempty(self):
        self.s.sitdown(self.p)
        self.s.standup()
        expected = True
        result = self.s.is_empty()
        self.assertEqual(expected, result)

    def test_standup_empty_raisesException(self):
        self.assertRaises(Exception, self.s.standup)

    def test_standup_playerwithchips_0chips(self):
        self.s.sitdown(self.p)
        self.s.buy_chips(100)
        self.s.standup()
        expected = 0
        result = self.s.chips
        self.assertEqual(expected, result)

    """
    Tests for is_empty(self):
    """
    def test_isempty_emptyseat_returnsTrue(self):
        self.assertTrue(self.s.is_empty())

    """
    Tests for has_hand(self):
    """
    def test_hashand_emptyseat_returnsFalse(self):
        self.assertFalse(self.s.has_hand())

    def test_hashand_filledseat_returnsFalse(self):
        # Has a player, but still no hand
        self.s.sitdown(self.p)
        self.assertFalse(self.s.has_hand())


    """
    Tests for show_hand(self):
    """

    """
    Tests for has_chips(self):
    """

    """
    Tests for buy_chips(self, amount):
    """

    """
    Tests for bet(self, amount):
    """

    """
    Tests for is_allin():
    """

    """
    Tests for fold(self, c):
    """
