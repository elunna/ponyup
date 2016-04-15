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
    Tests for next(from_seat)
    """
    # New setUp table, user supplies from_seat out of list index range. Should raise exception.
    def test_next_outofboundsseat100_raiseException(self):
        seat = 100
        self.assertRaises(ValueError, self.t.next, seat)

    # Less than -1 is an error. -1 is the starting point for the button and other tokens.
    def test_next_outofboundsseatneg2_raiseException(self):
        seat = -2
        self.assertRaises(ValueError, self.t.next, seat)

    # New setUp table, from_seat 0, returns 1
    def test_next_setUptable_returnSeat0(self):
        seat = 0
        expected = 1
        result = self.t.next(seat)
        self.assertEqual(expected, result)

    # Empty seat between 0 and 2, returns 1
    def test_next_from0_seat1empty_return2(self):
        seat = 0
        self.t.remove_player(1)
        expected = 2
        result = self.t.next(seat)
        self.assertEqual(expected, result)

    # setUp table, negative step, from_seat 0, returns 5
    def test_next_negativestep_from0_returnSeat5(self):
        seat = 0
        expected = 5
        result = self.t.next(seat, -1)
        self.assertEqual(expected, result)

    # Empty seat between 4 and 0, returns 5
    def test_next_negativestep_seat5empty_from0_returnSeat5(self):
        seat = 0
        self.t.remove_player(5)
        expected = 4
        result = self.t.next(seat, -1)
        self.assertEqual(expected, result)

    # No players, return -1
    def test_next_noplayers_returnsNeg1(self):
        t = table.Table(6)
        seat = 0
        self.assertRaises(Exception, t.next, seat)

    # No players, negative step, return -1
    def test_next_negativestep_noplayers_returnsNeg1(self):
        t = table.Table(6)
        seat = 0
        self.assertRaises(Exception, t.next, seat)

    """
    Tests for next_player_w_cards(from_seat, step=1)
    """
    # 6 seat table, seat 0 has cards - from 0, returns 0
    def test_nextplayerwcards_from0_seat0hascards_return0(self):
        t = table.Table(6)
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        seat = 0
        self.assertRaises(Exception, t.next_player_w_cards, seat)

    # 6 seat table, seat 0 has cards - from 1, returns 0
    def test_nextplayerwcards_from1_seat0hascards_return0(self):
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        expected = 0
        result = self.t.next_player_w_cards(1)
        self.assertEqual(expected, result)

    # 6 seat table, no cards - raise exception
    def test_nextplayerwcards_nocards_return0(self):
        from_seat = 0
        self.assertRaises(Exception, self.t.next_player_w_cards, from_seat)

    # Full table - all w cards. btn at 0. From 0 returns 1.
    def test_nextplayerwcards_fulltable_from0_return1(self):
        # Button should be at -1 for self.t
        self.t.move_button()
        # Button should be at 0 after move.

        # Give everyone cards
        c = card.Card('A', 's')
        for seat in self.t:
            seat.add_card(c)
        from_seat = 0
        expected = 1
        result = self.t.next_player_w_cards(from_seat)
        self.assertEqual(expected, result)

    # Full table - seat 3 has cards. btn at 0. From 0 returns 3.
    def test_nextplayerwcards_seat3hascards_from0_return3(self):
        self.t.move_button()
        c = card.Card('A', 's')
        self.t.seats[3].add_card(c)
        from_seat = 0
        expected = 3
        result = self.t.next_player_w_cards(from_seat)
        self.assertEqual(expected, result)

    # Full table - all w cards. btn at 0. From 0 returns 5. Negative step
    def test_nextplayerwcards_fulltable_negstep_from0_return5(self):
        # Button should be at -1 for self.t
        self.t.move_button()
        # Button should be at 0 after move.

        # Give everyone cards
        c = card.Card('A', 's')
        for seat in self.t:
            seat.add_card(c)
        from_seat = 0
        expected = 5
        result = self.t.next_player_w_cards(from_seat, -1)
        self.assertEqual(expected, result)

    # Full table - seat 3 has cards. btn at 0. negative step. From 0 returns 4.
    def test_nextplayerwcards_seat4hascards_negstep_from0_return4(self):
        self.t.move_button()
        c = card.Card('A', 's')
        self.t.seats[4].add_card(c)
        from_seat = 0
        expected = 4
        result = self.t.next_player_w_cards(from_seat, -1)
        self.assertEqual(expected, result)

    """
    Tests for get_playerdict()
    """
    # No players at table returns empty dict
    def test_getplayerdict_noplayer_returnsDictsize0(self):
        t = table.Table(6)
        expected = 0
        result = len(t.get_playerdict())
        self.assertEqual(expected, result)

    # 1 player at table, returns dict size 1
    def test_getplayerdict_1player_returnsDictsize1(self):
        t = table.Table(6)
        t.add_player(0, player.Player('bob0', 'CPU'))
        expected = 1
        result = len(t.get_playerdict())
        self.assertEqual(expected, result)

    # 6 players returns dict size 6
    def test_getplayerdict_6players_returnsDictsize6(self):
        expected = 6
        result = len(self.t.get_playerdict())
        self.assertEqual(expected, result)

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
