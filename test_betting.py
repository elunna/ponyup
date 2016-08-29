import unittest
import betting


class TestBetting(unittest.TestCase):
    """
    Tests for calc_odds(bet, pot):
    """

    # bet cannot be negative
    def test_calcodds_negbet_raiseEx(self):
        self.assertRaises(ValueError, betting.calc_odds, -10, 10)

    # pot cannot be negative
    def test_calcodds_negpot_raiseEx(self):
        self.assertRaises(ValueError, betting.calc_odds, 10, -10)

    # bet = 5, pot = 10, we are getting 2-to-1 odds.
    def test_init_0cardspassed_length0(self):
        expected = 2.0
        result = betting.calc_odds(5, 10)
        self.assertEqual(expected, result)

    """
    Tests for award_pot(player, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    # Try awarding -100. Should raise an exception.
    # Try awarding a player with no cards. Should raise an exception.
