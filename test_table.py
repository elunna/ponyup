import unittest
import card
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
    # Adding 1 player to an empty table, size should be 1.
    def test_addplayer_toEmptyTable_1player(self):
        t = table.Table(6)
        t.add_player(0, player.Player('bob0', 'CPU'))
        expected = 1
        result = len(t.get_players())
        self.assertEqual(expected, result)

    # Adding 1 player to an empty table, contains the added player
    def test_addplayer_toEmptyTable_containsPlayer(self):
        t = table.Table(6)
        p = player.Player('bob0', 'CPU')
        t.add_player(0, p)
        expected = 1
        result = p in t
        self.assertEqual(expected, result)

    # Adding 1 player to an occupied spot,
    def test_addplayer_tooccupiedspot_raiseException(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        t.add_player(0, p1)
        self.assertRaises(ValueError, t.add_player, 0, p2)

    # Adding a duplicate player to the table, should raise exception.
    def test_addplayer_duplicateplayer_raiseException(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        p3 = player.Player('bob1', 'CPU')
        t.add_player(0, p1)
        t.add_player(1, p2)
        self.assertRaises(ValueError, t.add_player, 3, p3)

    """
    Tests for indexof
    """
    # Add a player to seat 0, indexof returns 0
    def test_indexof_playerinseat0_returns0(self):
        t = table.Table(6)
        p = player.Player('bob0', 'CPU')
        t.add_player(0, p)
        expected = 0
        result = t.get_index(p)
        self.assertEqual(expected, result)

    # indexof a player not in the table, returns -1
    def test_indexof_nonpresentplayer_returnsNeg1(self):
        t = table.Table(6)
        p = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        t.add_player(0, p)
        expected = -1
        result = t.get_index(p2)
        self.assertEqual(expected, result)

    """
    Tests for remove_player()
    """
    # Remove player 0, table doesn't contain the player at seat 0.
    def test_removeplayer_removeseat0_doesntcontainseat0(self):
        p = player.Player('bob0', 'CPU')
        self.t.remove_player(0)
        expected = False
        result = p in self.t
        self.assertEqual(expected, result)

    # Remove player 0, seat 0 is None
    def test_removeplayer_removeseat0_seat0isNone(self):
        self.t.remove_player(0)
        expected = True
        result = self.t.seats[0] is None
        self.assertEqual(expected, result)

    """
    Tests for get_players()
    """
    # From the setUp table, gets an array size 6.
    def test_getplayers_6players_returnslistsize6(self):
        expected = 6
        result = len(self.t.get_players())
        self.assertEqual(expected, result)

    # From a table of 1, gets an array of size 1.
    def test_getplayers_1player_returnslistsize1(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        t.add_player(0, p1)
        expected = 1
        result = len(t.get_players())
        self.assertEqual(expected, result)

    # From a table of one, gets the player at the table.
    def test_getplayers_1player_listcontainsplayer(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        t.add_player(0, p1)
        expected = True
        result = p1 in t
        self.assertEqual(expected, result)

    """
    Tests for valid_bettors()
    """
    # 0 players holding cards, gets an array size 0
    def test_validbettors_0withcards_returns0(self):
        expected = 0
        result = self.t.valid_bettors()
        self.assertEqual(expected, result)

    # 1 players holding cards, gets an array size 1
    def test_validbettors_1withcards_returns1(self):
        expected = 1
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        result = self.t.valid_bettors()
        self.assertEqual(expected, result)

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
