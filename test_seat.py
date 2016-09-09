import unittest
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
    Tests for has_chips(self):
    """

    """
    Tests for buy_chips(self, amount):
    """

    """
    Tests for bet(self, amount):
    """

    """
    Tests for add_card(self, c):
    """

    """
    Tests for remove_card(self, c):
    """

    """
    Tests for fold(self, c):
    """
