import unittest
import card
import table
import player
import testtools
import table_factory


class TestTable(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self, players=6, removed=None, btn_moved=1, setblinds=False):
        self.t = table_factory.BobTable(players)

        if removed is not None:
            self.t.remove_player(removed)
            self.assertEqual(self.t.seats[removed], None)

        for i in range(btn_moved):
            self.t.move_button()

        if setblinds:
            self.t.set_blinds()

    """
    Tests for __init__ and table construction
    """
    # initialized with invalid seat count(less than 2)
    def test_init_invalidtablesize1_throwException(self):
        self.assertRaises(ValueError, table.Table, '1')

    # initialized with invalid seat count(more than 10)
    def test_init_invalidtablesize11_throwException(self):
        self.assertRaises(ValueError, table.Table, '11')

    def test_Dtoken_newTable_returnsNeg1(self):
        t = table_factory.BobTable(6)
        expected = -1
        result = t.TOKENS['D']
        self.assertEqual(expected, result)

    def test_SBtoken_newTable_returnsNeg1(self):
        expected = -1
        result = self.t.TOKENS['SB']
        self.assertEqual(expected, result)

    def test_BBtoken_newTable_returnsNeg1(self):
        expected = -1
        result = self.t.TOKENS['BB']
        self.assertEqual(expected, result)

    def check_btn(self, b):
        self.t.move_button()
        expected = b
        result = self.t.TOKENS['D']
        self.assertEqual(expected, result)

    """
    Tests for __len__()
    """
    def test_len_newTable_returns6(self):
        expected = 6
        result = len(self.t)
        self.assertEqual(expected, result)

    """
    Tests for __str__()
    """
    # Test that table displays correctly?
    # 08/28/16 - putting this off, display changes too much.

    """
    Tests for __iter__(), __next__() # needed?
    """
    # Test that the table iterates through few players in order, full table
    def test_next_newTable_getsseat0(self):
        expected = 'bob0'
        iterator = self.t.__iter__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    # Test that it goes to the next player.
    def test_next2_newTable_getsseat1(self):
        expected = 'bob1'
        iterator = self.t.__iter__()
        iterator.__next__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    # Iter should skip over an empty seat
    def test_next_removedseat0_getsseat1(self):
        self.setUp(removed=0)
        expected = 'bob1'
        iterator = self.t.__iter__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    """
    Tests for move_button()
    """
    # New table, moving button once should go from -1 to 0.
    def test_movebutton_newTable_returns0(self):
        expected = 0
        result = self.t.TOKENS['D']
        self.assertEqual(expected, result)

    # New table(without seat 0), moving button once should go from -1 to 1
    def test_movebutton_seat0removed_returns1(self):
        self.setUp(removed=0)
        expected = 1
        result = self.t.TOKENS['D']
        self.assertEqual(expected, result)

    def test_movebutton_2x_returns1(self):
        self.setUp(btn_moved=2)
        expected = 1
        result = self.t.TOKENS['D']
        self.assertEqual(expected, result)

    """
    Tests for set_blinds()
    """
    # New table: Button at 0, sb should be at 1
    def test_setblinds_setUpTable_SBat1(self):
        self.setUp(btn_moved=1, setblinds=True)
        expected = 1
        result = self.t.TOKENS['SB']
        self.assertEqual(expected, result)

    # New table(seat 1 removed): Button at 0, sb should be at 2
    def test_setblinds_seat1removed_SBat2(self):
        self.setUp(removed=1, btn_moved=1, setblinds=True)
        self.t.set_blinds()
        expected = 2
        result = self.t.TOKENS['SB']
        self.assertEqual(expected, result)

    # New table: Button at 0, bb should be at 2
    def test_setblinds_setUpTable_BBat2(self):
        self.setUp(setblinds=True)
        expected = 2
        result = self.t.TOKENS['BB']
        self.assertEqual(expected, result)

    # New table(seat 2 removed): Button at 0, bb should be at 3
    def test_setblinds_seat2removed_BBat3(self):
        self.setUp(removed=2, setblinds=True)
        self.assertEqual(self.t.TOKENS['D'], 0, "button ain't right")
        expected = 3
        result = self.t.TOKENS['BB']
        self.assertEqual(expected, result)

    """
    Tests for set_bringin(index)
    """
    # Passed 5, BI token should be 5.
    def test_setbringin_index5_BItokenis5(self):
        self.setUp(players=6, setblinds=False)
        self.t.set_bringin(5)
        self.assertEqual(self.t.TOKENS['BI'], 5)

    # Passed 5, D token should be 4.
    def test_setbringin_index5_Dtokenis4(self):
        self.setUp(players=6, setblinds=False)
        self.t.set_bringin(5)
        self.assertEqual(self.t.TOKENS['D'], 4)

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

    # Adding 1 player to an empty table, returns True
    def test_addplayer_toEmptyTable_returnsTrue(self):
        t = table.Table(6)
        expected = True
        result = t.add_player(0, player.Player('bob0', 'CPU'))
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
    def test_addplayer_tooccupiedspot_returnsFalse(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        expected = False
        t.add_player(0, p1)
        result = t.add_player(0, p2)
        self.assertEqual(expected, result)

    # Adding a duplicate player to the table, should raise exception.
    def test_addplayer_duplicateplayer_raiseException(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        p3 = player.Player('bob1', 'CPU')
        t.add_player(0, p1)
        t.add_player(1, p2)
        expected = False
        result = t.add_player(3, p3)
        self.assertEqual(expected, result)

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

    def test_removeplayer_removeseat0_returnsPlayer(self):
        expected = self.t.seats[0]
        result = self.t.remove_player(0)
        self.assertEqual(expected, result)

    def test_removeplayer_emptyseat_raisesException(self):
        self.t.remove_player(0)
        self.assertTrue(self.t.seats[0] is None)
        self.assertRaises(ValueError, self.t.remove_player, 0)

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

    # 0 players holding cards, gets a list size 0
    def test_getplayers_cardsandchips_0withcards_returns0(self):
        self.t.randomize_button()
        expected = 0
        result = len(self.t.get_players(hascards=True, haschips=True))
        self.assertEqual(expected, result)

    # 1 players holding cards, gets a list size 1
    def test_getplayers_cardsandchips_1withcards_returns1(self):
        self.t.randomize_button()
        expected = 1
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        result = len(self.t.get_players(hascards=True, haschips=True))
        self.assertEqual(expected, result)

    """
    Tests for get_players(hascards=True)
    """
    # 1 player with cards. Button is -1. Raises Exception
    def test_getplayers_withcards_seat0hascards_raiseException(self):
        self.setUp(setblinds=True)
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        self.assertRaises(Exception, self.t.get_players(hascards=True))

    # 1 player with cards. Button moved to 0. Returns the player
    def test_getplayers_withcards_btn0_seat0hascards_returnsPlayer(self):
        self.setUp(setblinds=True)
        self.assertTrue(self.t.TOKENS['D'] == 0)

        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        expected = [self.t.seats[0]]
        result = self.t.get_players(hascards=True)
        self.assertEqual(expected, result)

    # 2 player with cards. Button moved to 0. Returns the player
    # Since it's heads up, the sb/btn(0) should be first in the returned list
    def test_getplayers_withcards_btn0_seat0and1hascards_return0(self):
        self.setUp(players=2, setblinds=True)
        self.assertEqual(self.t.TOKENS['D'], 0)  # Make sure the btn is at 0
        self.assertEqual(self.t.TOKENS['SB'], 0)  # Make sure the sb is at 0.

        testtools.deal_random_cards(self.t)
        expected = self.t.seats[0]
        result = self.t.get_players(hascards=True)[0]
        self.assertEqual(expected, result)

    # 2 player with cards. Button moved to 0. Returns the player
    # Since it's heads up, the sb/btn(0) should be first in the returned list
    def test_getplayers_withcards_btn1_seat0and1hascards_return1(self):
        self.setUp(players=2, btn_moved=2, setblinds=True)
        self.assertEqual(self.t.TOKENS['D'], 1)
        self.assertEqual(self.t.TOKENS['SB'], 1)
        testtools.deal_random_cards(self.t)

        expected = self.t.seats[1]
        result = self.t.get_players(hascards=True)[0]
        self.assertEqual(expected, result)

    # 6 players with cards, Button at 0. Returns list with seat 1 first.
    def test_getplayers_withcards_6havecards_btn0_seat1first(self):
        self.setUp(setblinds=True)
        self.assertEqual(self.t.TOKENS['D'], 0)
        testtools.deal_random_cards(self.t)

        expected = self.t.seats[1]
        result = self.t.get_players(hascards=True)[0]
        self.assertEqual(expected, result)

    # 6 players with cards, Button at 5. Returns list with seat 0 first.
    def test_getplayers_withcards_6havecards_btn5_seat0first(self):
        self.setUp()
        self.t.TOKENS['D'] = 5
        self.t.set_blinds()

        testtools.deal_random_cards(self.t)
        expected = self.t.seats[0]
        result = self.t.get_players(hascards=True)[0]
        self.assertEqual(expected, result)

    # 6 players with cards, Button at 0. Returns list that's size 6.
    def test_getplayers_withcards_6havecards_lengthis6(self):
        self.setUp(setblinds=True)
        testtools.deal_random_cards(self.t)
        expected = 6
        result = len(self.t.get_players(hascards=True))
        self.assertEqual(expected, result)

    """
    Tests for next_player(self, from_seat, step=1, hascards=False):
    """
    # New setUp table, user supplies from_seat out of list index range. Should raise exception.
    def test_nextplayer_outofboundsseat100_raiseException(self):
        seat = 100
        self.assertRaises(ValueError, self.t.next_player, seat)

    # Less than -1 is an error. -1 is the starting point for the button and other tokens.
    def test_nextplayer_outofboundsseatneg2_raiseException(self):
        seat = -2
        self.assertRaises(ValueError, self.t.next_player, seat)

    # New setUp table, from_seat 0, returns 1
    def test_nextplayer_setUptable_returnSeat0(self):
        seat = 0
        expected = 1
        result = self.t.next_player(seat)
        self.assertEqual(expected, result)

    # Empty seat between 0 and 2, returns 1
    def test_nextplayer_from0_seat1empty_return2(self):
        self.setUp(removed=1)
        seat = 0
        expected = 2
        result = self.t.next_player(seat)
        self.assertEqual(expected, result)

    # setUp table, negative step, from_seat 0, returns 5
    def test_nextplayer_negativestep_from0_returnSeat5(self):
        seat = 0
        expected = 5
        result = self.t.next_player(seat, -1)
        self.assertEqual(expected, result)

    # Empty seat between 4 and 0, returns 5
    def test_nextplayer_negativestep_seat5empty_from0_returnSeat5(self):
        self.setUp(removed=5)
        seat = 0
        expected = 4
        result = self.t.next_player(seat, -1)
        self.assertEqual(expected, result)

    # No players, return -1
    def test_nextplayer_noplayers_returnsNeg1(self):
        t = table.Table(6)
        seat = 0
        self.assertRaises(Exception, t.next_player, seat)

    # No players, negative step, return -1
    def test_nextplayer_negativestep_noplayers_returnsNeg1(self):
        t = table.Table(6)
        seat = 0
        self.assertRaises(Exception, t.next_player, seat)

    # Next, 6 players, from 0, returns 1
    def test_nextplayer_from0_returns1(self):
        expected = 1
        result = self.t.next_player(0)
        self.assertEqual(expected, result)

    # Next, 6 players, from 1, returns 2
    def test_nextplayer_from1_returns2(self):
        expected = 2
        result = self.t.next_player(1)
        self.assertEqual(expected, result)

    # Next, 6 players, from 2, returns 3
    def test_nextplayer_from2_returns3(self):
        expected = 3
        result = self.t.next_player(2)
        self.assertEqual(expected, result)

    # Next, 6 players, from 3, returns 4
    def test_nextplayer_from3_returns4(self):
        expected = 4
        result = self.t.next_player(3)
        self.assertEqual(expected, result)

    # Next, 6 players, from 4, returns 5
    def test_nextplayer_from4_returns5(self):
        expected = 5
        result = self.t.next_player(4)
        self.assertEqual(expected, result)

    # Next, 6 players, from 5, returns 0
    def test_nextplayer_from5_returns0(self):
        expected = 0
        result = self.t.next_player(5)
        self.assertEqual(expected, result)

    """
    Tests for nextplayer(from_seat, step=1)
    """
    # 6 seat table, seat 0 has cards - from 0, returns 0
    def test_nextplayer_withcards_from0_seat0hascards_return0(self):
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        from_seat = 0
        expected = 0
        result = self.t.next_player(from_seat, hascards=True)
        self.assertEqual(expected, result)

    # 6 seat table, seat 0 has cards - from 1, returns 0
    def test_nextplayer_withcards_from1_seat0hascards_return0(self):
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        from_seat = 1
        expected = 0
        result = self.t.next_player(from_seat, hascards=True)
        self.assertEqual(expected, result)

    # 6 seat table, no cards - raise exception
    def test_nextplayer_withcards_nocards_return0(self):
        from_seat = 0
        self.assertRaises(Exception, self.t.next_player, from_seat, hascards=True)

    # Full table - all w cards. btn at 0. From 0 returns 1.
    def test_nextplayer_withcards_fulltable_from0_return1(self):
        self.assertEqual(self.t.TOKENS['D'], 0)
        testtools.deal_random_cards(self.t, qty=1)
        from_seat = 0
        expected = 1
        result = self.t.next_player(from_seat, hascards=True)
        self.assertEqual(expected, result)

    # Full table - seat 3 has cards. btn at 0. From 0 returns 3.
    def test_nextplayer_withcards_seat3hascards_from0_return3(self):
        c = card.Card('A', 's')
        self.t.seats[3].add_card(c)
        from_seat = 0
        expected = 3
        result = self.t.next_player(from_seat, hascards=True)
        self.assertEqual(expected, result)

    # Full table - all w cards. btn at 0. From 0 returns 5. Negative step
    def test_nextplayer_withcards_fulltable_negstep_from0_return5(self):
        self.assertEqual(self.t.TOKENS['D'], 0)
        # Give everyone cards
        testtools.deal_random_cards(self.t, qty=1)
        from_seat = 0
        expected = 5
        result = self.t.next_player(from_seat, -1, hascards=True)
        self.assertEqual(expected, result)

    # Full table - seat 3 has cards. btn at 0. negative step. From 0 returns 4.
    def test_nextplayer_withcards_seat4hascards_negstep_from0_return4(self):
        c = card.Card('A', 's')
        self.t.seats[4].add_card(c)
        from_seat = 0
        expected = 4
        result = self.t.next_player(from_seat, -1, hascards=True)
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

    # Randomize button on table size 2, button is in range 0-1
    def test_randomizebutton_2seats_inrange0to1(self):
        seats = 2
        self.setUp(players=seats)
        self.t.randomize_button()
        btn = self.t.TOKENS['D']
        result = (btn >= 0) and (btn < seats)
        self.assertTrue(result)

    # Randomize button on table size 6, button is in range 0-5

    def test_randomizebutton_6seats_inrange0to5(self):
        seats = 6
        self.setUp(players=seats)
        self.t.randomize_button()
        result = self.t.TOKENS['D'] >= 0 and self.t.TOKENS['D'] < seats
        self.assertTrue(result)

    # Randomize button on table size 9, button is in range 0-8
    def test_randomizebutton_9seats_inrange0to8(self):
        seats = 9
        self.setUp(players=seats)
        self.t.randomize_button()
        result = self.t.TOKENS['D'] >= 0 and self.t.TOKENS['D'] < seats
        self.assertTrue(result)

    # Randomize button on table size 9, but no players
    def test_randomizebutton_noplayers_raisesException(self):
        seats = 9
        t = table.Table(seats)
        self.assertRaises(Exception, t.randomize_button)

    """
    Tests for get_broke_players()
    """
    # 6 players, all with chips, returns empty list
    def test_getbrokeplayers_6playerswithchips_returnemptylist(self):
        expected = []
        result = self.t.get_broke_players()
        self.assertEqual(expected, result)

    # 1 broke player, returns the player in a list
    def test_getbrokeplayers_1brokeplayer_returnsplayer(self):
        p = self.t.seats[0]
        p.chips = 0
        expected = [p]
        result = self.t.get_broke_players()
        self.assertEqual(expected, result)

    # 2 broke player, returns the player in a list
    def test_getbrokeplayers_2broke_returnsboth(self):
        p1, p2 = self.t.seats[0], self.t.seats[1]
        p1.chips = 0
        p2.chips = 0
        expected = [p1, p2]
        result = self.t.get_broke_players()
        self.assertEqual(expected, result)
