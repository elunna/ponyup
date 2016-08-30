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
    Tests for process_option(option)
    """
    # CHECK - bet level is same
    # CHECK - Players chips stay the same
    # FOLD - player doesn't have cards
    # FOLD - Players chips stay the same
    # BET - bet level is raised by one
    # BET - Players chips are diminished by the bet amount
    # RAISE - bet level is raised by one
    # RAISE - Players chips are diminished by the raiseamount
    # CHECK - bet level is same
    # COMPLETE - Players chips are diminished by the bet amount
