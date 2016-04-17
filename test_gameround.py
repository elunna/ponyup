import unittest
import gameround


class TestGameRound(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        pass

    """
    Tests for __init__ and table construction
    """
    # initialized with invalid seat count(less than 2)
    def test_raiseException(self):
        pass
        #  self.assertRaises(ValueError, table.Table, '1')

    # a Test
    def test_(self):
        pass

    """
    Tests for __str__()
    """

    """
    Tests for cheat_check()
    """

    """
    Tests for deal_cards(qty, faceup=False)
    """

    """
    Tests for muck_all_cards()
    """

    """
    Tests for verify_muck()
    """

    """
    Tests for remove_broke_players()
    """

    """
    Tests for get_valueplayer_list()
    """

    """
    Tests for showdown()
    """

    """
    Tests for process_sidepots(handlist)
    """

    """
    Tests for determine_eligibility(handlist, pot, stack)
    """

    """
    Tests for process_allins()
    """

    """
    Tests for make_sidepot(stacksize)
    """

    """
    Tests for award_pot(winners, amt)
    """

    """
    Tests for post_antes()
    """

    """
    Tests for post_blinds()
    """

    """
    Tests for setup_betting()
    """

    """
    Tests for betting()
    """

    """
    Tests for process_option(option)
    """

    """
    Tests for menu(options=None)
    """

    """
    Tests for get_options(cost)
    """

    """
    Tests for determine_bringin(gametype)
    """

################################################################
# Not in the round class

    """
    Tests for calc_odds(bet, pot)
    """

    """
    Tests for
    """
