import unittest
import player
import seat


class TestSeat(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_newseat_playerNone(self):
        s = seat.Seat()
        expected = None
        result = s.player
        self.assertEqual(expected, result)

    """
    Tests for sitdown(self, player):
    """
    def test_sitdown_player_isnotEmpty(self):
        p = player.Player("Erik")
        s = seat.Seat()
        s.sitdown(p)
        expected = False
        result = s.is_empty()
        self.assertEqual(expected, result)

    def test_sitdown_player_matchesSeatPlayer(self):
        p = player.Player("Erik")
        s = seat.Seat()
        s.sitdown(p)
        expected = p
        result = s.player
        self.assertEqual(expected, result)

    """
    Tests for standup(self, player):
    """

    """
    Tests for is_empty(self):
    """

    """
    Tests for has_hand(self):
    """

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
