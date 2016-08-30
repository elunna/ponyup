import unittest
import betting
import draw5
import setup_table


class TestBetting(unittest.TestCase):
    """
    Setup a session and round, with a table filled with 6 players.
    """
    def setUp(self, seats=6):
        g = draw5.Draw5Session('FIVE CARD DRAW', tablesize=6)
        g._table = setup_table.test_table(seats)
        g._table.move_button()
        self.assertEqual(g._table.TOKENS['D'], 0)  # verify the button is 0
        self.r = g.new_round()
        self.br = betting.BettingRound(self.r)

    """
    Tests for BettingRound initialization
    """
    # Export the invested variable to betting.has_invested(player)
    # Export the cost variable.

    """
    Tests for setup_betting()
    """
    # 2 players. SB and BTN should be together.
    # 2 players. BB is not BTN.

    """
    Tests for play()
    """

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

    """
    Tests for get_options(cost)
    """

    """
    Tests for get_bettor()
    """
    # 6 players, new table. Preflop. BTN=0, SB=1, BB=2. bettor should be 3.
    def test_getbettor_6plyr_preflop_returns3(self):
        self.setUp(6)
        expected = self.r._table.seats[3]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    # 6 players, new table. Postflop. BTN=0, SB=1, BB=2. bettor should be 1.
    # 2 players, new table. Preflop. BTN/SB=0, BB=1. bettor should be 0.
    # 2 players, new table. Postflop. BTN/SB=0, BB=1. bettor should be 1.

    """
    Tests for get_closer()
    """
    # 6 players, new table. Preflop. BTN=0, SB=1, BB=2. closer should be 2.
    # 6 players, new table. Postflop. BTN=0, SB=1, BB=2. bettor should be 0.

    # 2 players, new table. Preflop. BTN/SB=0, BB=1. closer should be 1.
    # 2 players, new table. Postflop. BTN/SB=0, BB=1. bettor should be 0.

################################################################################
    """
    Tests for calc_odds(bet ,pot)
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
    Tests for menu()
    """

    """
    Tests for allin_option()
    """

    """
    Tests for spacing()
    """
