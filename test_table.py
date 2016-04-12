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
    def test_str_newtable_correctDisplay(self):
        expected = ''
        expected += '#  Tokens Player         Chips     Hand      \n'
        expected += '--------------------------------------------------\n'
        expected += '0         bob0           $1000     \n'
        expected += '1         bob1           $1000     \n'
        expected += '2         bob2           $1000     \n'
        expected += '3         bob3           $1000     \n'
        expected += '4         bob4           $1000     \n'
        expected += '5         bob5           $1000     \n'

        result = str(self.t)
        self.assertEqual(expected, result)

    """
    Tests for __iter__(), __next__() # needed?
    """
    # Test that the table iterates through few players in order, full table
    def test_next_setUpTable_getsseat0(self):
        expected = 'bob0'
        iterator = self.t.__iter__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    # Test that it goes to the next player.
    def test_next2_setUpTable_getsseat1(self):
        expected = 'bob1'
        iterator = self.t.__iter__()
        iterator.__next__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    # Iter should skip over an empty seat
    def test_next_removedseat0_getsseat1(self):
        self.t.remove_player(0)
        expected = 'bob1'
        iterator = self.t.__iter__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    """
    Tests for btn(), move_button()
    """
    # A new table should have the button set to -1
    def test_btn_setUpTable_returnsNeg1(self):
        expected = -1
        result = self.t.btn()
        self.assertEqual(expected, result)

    # New table, moving button once should go from -1 to 0.
    def test_movebutton_setUpTable_returns0(self):
        expected = 0
        self.t.move_button()
        result = self.t.btn()
        self.assertEqual(expected, result)

    # New table(without seat 0), moving button once should go from -1 to 1
    def test_movebutton_seat0removed_returns1(self):
        expected = 1
        self.t.remove_player(0)
        self.t.move_button()
        result = self.t.btn()
        self.assertEqual(expected, result)

    # New table: Button at 0, sb should be at 1
    def test_movebutton_setUpTable_SBat1(self):
        expected = 1
        self.t.move_button()
        result = self.t.get_sb()
        self.assertEqual(expected, result)

    # New table(seat 1 removed): Button at 0, sb should be at 2
    def test_movebutton_seat1removed_SBat2(self):
        expected = 2
        self.t.remove_player(1)
        self.t.move_button()
        result = self.t.get_sb()
        self.assertEqual(expected, result)

    # New table: Button at 0, bb should be at 2
    def test_movebutton_setUpTable_BBat2(self):
        expected = 2
        self.t.move_button()
        result = self.t.get_bb()
        self.assertEqual(expected, result)

    # New table(seat 2 removed): Button at 0, bb should be at 3
    def test_movebutton_seat2removed_BBat3(self):
        expected = 3
        self.t.remove_player(2)
        self.t.move_button()
        result = self.t.get_bb()
        self.assertEqual(expected, result)

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
