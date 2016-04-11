import unittest
import table
import player


class TestTable(unittest.TestCase):

    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        self.t = table.Table(6)
        self.t.add_player(0, player.Player('bob0', 'CPU'))
        self.t.add_player(1, player.Player('bob1', 'CPU'))
        self.t.add_player(2, player.Player('bob2', 'CPU'))
        self.t.add_player(3, player.Player('bob3', 'CPU'))
        self.t.add_player(4, player.Player('bob4', 'CPU'))
        self.t.add_player(5, player.Player('bob5', 'CPU'))

        for p in self.t:
            p.add_chips(1000)

    """
    Tests for __init__ and table construction
    """
    # initialized with invalid seat count(less than 2)
    def test_init_invalidtablesize1_throwException(self):
        self.assertRaises(ValueError, table.Table, '1')

    # initialized with invalid seat count(more than 10)
    def test_init_invalidtablesize11_throwException(self):
        self.assertRaises(ValueError, table.Table, '11')

    # initialized with valid seat count
    def test_init_validtablesize_validSize(self):
        t = table.Table(6)
        expected = 6
        result = len(t)
        self.assertEqual(expected, result)

    """
    Tests for __len__()
    """
    # Also tested in the init and add/remove player tests.
    def test_len_lenOfSetupTable_returns6(self):
        expected = 6
        result = len(self.t)
        self.assertEqual(expected, result)

    """
    Tests for __str__()
    """
    # Test that table displays correctly?

    """
    Tests for __iter__() # needed?
    """
    # Test that the table iterates through all the players
    # Test that it goes to the next player.

    """
    Tests for __next__() # needed?
    """

    """
    Tests for btn()
    """

    """
    Tests for get_sb()
    """

    """
    Tests for get_bb()
    """

    """
    Tests for add_player()
    """

    """
    Tests for player_index()
    """

    """
    Tests for remove_player()
    """

    """
    Tests for get_players()
    """

    """
    Tests for valid_bettors()
    """

    """
    Tests for next(from_seat, hascards=False)
    """

    """
    Tests for prev(from_seat, hascards=False)
    """

    """
    Tests for move_button()
    """

    """
    Tests for get_playerdict()
    """

    """
    Tests for randomize_button()
    """

    """
    Tests for get_cardholders()
    """

    """
    Tests for has_cards(s)
    """

#########################

# Test setup_table(num, hero=None, gametype="DRAW5")
