"""
  " Tests for table.py
  """
import pytest
from ..src import card
from ..src import player
from ..src import table
from ..src import tools


@pytest.fixture
def tbl():
    return table.Table(size=6)


def test_table(players=6, rm=None, btn_moved=1, setblinds=False):
    """ Setup a table filled with generic players for testing. """
    t = table.Table(players)
    # t = factory.table_factory(seats=players, remove=rm)

    for _ in range(btn_moved):
        t.move_button()

    if setblinds:
        t.set_blinds()

    return t


def check_btn(t, b):
    t.move_button()
    assert t.TOKENS['D'] == b


def test_init_invalidtablesize1_throwException():
    with pytest.raises(ValueError):
        table.Table('1')


def test_init_invalidtablesize11_throwException():
    with pytest.raises(ValueError):
        table.Table('11')


def test_init_Dtoken_returnsNeg1(tbl):
    assert tbl.TOKENS['D'] == -1


def test_init_SBtoken_returnsNeg1(tbl):
    assert tbl.TOKENS['SB'] == -1


def test_init_BBtoken_returnsNeg1(tbl):
    assert tbl.TOKENS['BB'] == -1

# Test that table displays correctly?
# 08/28/16 - putting this off, display changes too much.


def test_len_newTable_returns6(tbl):
    assert len(tbl) == 6


def test_next_newTable_getsseat0(tbl):
    # Test that the table iterates through seats in order, full table
    iterator = tbl.__iter__()
    nextplayer = next(iterator)
    # Test seat # instead
    assert str(nextplayer) == 'bob0'


def test_next2_newTable_getsseat1(tbl):
    # Test that it goes to the next player.
    iterator = tbl.__iter__()
    next(iterator)
    assert str(next(iterator)) == 'bob1'


def test_iternext_removedseat0_getsseat0():
    # Iter should NOT skip over an empty seat
    t = test_table(rm=0)
    iterator = t.__iter__()
    assert next(iterator).NUM == 0


def test_addplayer_EmptyTable_1player(tbl):
    tbl.add_player(0, player.Player('bob0', 'CPU'))
    assert len(tbl.get_players()) == 1


def test_addplayer_EmptyTable_returnsTrue(tbl):
    assert tbl.add_player(0, player.Player('bob0', 'CPU'))


def test_addplayer_EmptyTable_containsPlayer(tbl):
    p = player.Player('bob0', 'CPU')
    tbl.add_player(0, p)
    assert p in tbl


def test_addplayer_occupied_returnsFalse(tbl):
    p1 = player.Player('bob0', 'CPU')
    p2 = player.Player('bob1', 'CPU')
    tbl.add_player(0, p1)
    assert tbl.add_player(0, p2) is False


def test_addplayer_duplicate_returnFalse(tbl):
    p1 = player.Player('bob0', 'CPU')
    p2 = player.Player('bob1', 'CPU')
    p3 = player.Player('bob1', 'CPU')
    tbl.add_player(0, p1)
    tbl.add_player(1, p2)
    assert tbl.add_player(3, p3) is False


def test_pop_seat0_playernotattable(tbl):
    p = player.Player('bob0', 'CPU')
    tbl.add_player(0, p)
    tbl.pop(0)
    assert p not in tbl


def test_pop_seat0_seat0isEmpty(tbl):
    tbl.pop(0)
    assert tbl.seats[0].vacant()


def test_pop_seat0_returnsPlayer():
    t = test_table()
    expected = t.seats[0].player
    assert t.pop(0) == expected


def test_pop_emptyseat_raisesException(tbl):
    assert tbl.seats[0].vacant()
    with pytest.raises(ValueError):
        tbl.pop(0)


def test_getindex_playerinseat0_returns0(tbl):
    p = player.Player('bob0', 'CPU')
    tbl.add_player(0, p)
    assert tbl.get_index(p) == 0


def test_getindex_absent_player_returnsNeg1(tbl):
    p = player.Player('bob0', 'CPU')
    p2 = player.Player('bob1', 'CPU')
    tbl.add_player(0, p)
    assert tbl.get_index(p2) == -1


def test_getplayers_6players_returnslistsize6(tbl):
    assert len(tbl.get_players()) == 6


def test_getplayers_1player_returnslistsize1(tbl):
    p1 = player.Player('bob0', 'CPU')
    tbl.add_player(0, p1)
    assert len(tbl.get_players()) == 1


def test_getplayers_1player_listcontainsplayer(tbl):
    p1 = player.Player('bob0', 'CPU')
    tbl.add_player(0, p1)
    assert tbl.get_players()[0].player == p1


def test_getplayers_hascards_0withcards_returns0():
    t.randomize_button()
    assert len(t.get_players(hascards=True)) == 0


def test_getplayers_cardsandchips_1card_returns1():
    t.randomize_button()
    c = card.Card('A', 's')
    t.seats[0].hand.add(c)
    assert len(t.get_players(hascards=True, haschips=True)) == 1


def test_getplayers_1withcards_negbutton_raiseException(self):
    # 1 player with cards. Button is -1. Raises Exception
    self.setUp(setblinds=True)
    c = card.Card('A', 's')
    self.t.seats[0].hand.add(c)
    with pytest.raises(Exception):
        self.t.get_players(hascards=True)


def test_getplayers_withcards_btn0_seat0hascards_returnsPlayer():
    # 1 player with cards. Button moved to 0. Returns the player
    self.setUp(setblinds=True)
    assert t.TOKENS['D'] == 0
    c = card.Card('A', 's')
    t.seats[0].hand.add(c)
    expected = [t.seats[0]]
    assert t.get_players(hascards=True) == expected


def test_getplayers_withcards_btn0_seat0and1hascards_return0():
    """ 2 player with cards. Button moved to 0. Returns the player.
        Since it's heads up, the sb/btn(0) should be first in the returned list.
    """
    self.setUp(players=2, setblinds=True)
    assert t.TOKENS['D'] == 0  # Make sure the btn is at 0
    assert t.TOKENS['SB'] == 0  # Make sure the sb is at 0.

    tools.deal_random_cards(t)
    # SB should be first
    assert t.get_players(hascards=True)[0] == t.seats[1]


def test_getplayers_withcards_btn1_seat0and1hascards_return1():
    """ 2 player with cards. Button moved to 0. Returns the player
        Since it's heads up, the sb/btn(0) should be first in the returned list.
    """
    self.setUp(players=2, btn_moved=2, setblinds=True)
    assert t.TOKENS['D'] == 1
    assert t.TOKENS['SB'] == 1
    tools.deal_random_cards(t)

    # BB will act first and be first in the list
    assert t.get_players(hascards=True)[0] == t.seats[0]


def test_getplayers_withcards_6havecards_btn0_seat1first():
    # 6 players with cards, Button at 0. Returns list with seat 1 first.
    self.setUp(setblinds=True)
    assert t.TOKENS['D'] == 0
    tools.deal_random_cards(t)

    expected = t.seats[1]
    assert t.get_players(hascards=True)[0] == expected


def test_getplayers_withcards_6havecards_btn5_seat0first():
    """ 6 players with cards, Button at 5. Returns list with seat 0 first. """
    self.setUp()
    t.TOKENS['D'] = 5
    t.set_blinds()

    tools.deal_random_cards(t)
    assert t.get_players(hascards=True)[0] == t.seats[0]


def test_getplayers_withcards_6havecards_lengthis6():
    # 6 players with cards, Button at 0. Returns list that's size 6.
    self.setUp(setblinds=True)
    tools.deal_random_cards(t)
    players = t.get_players(hascards=True)
    assert len(players) == 6


def test_nextplayer_outofboundsseat100_raiseException(tbl):
    # New setUp table, user supplies from_seat out of list index range. Should raise exception.
    seat = 100
    with pytest.raises(ValueError):
        tbl.next_player(seat)


def test_nextplayer_outofboundsseatneg2_raiseException(tbl):
    # Less than -1 is an error. -1 is the starting point for the button and other tokens.
    seat = -2
    with pytest.raises(ValueError):
        tbl.next_player(seat)


def test_nextplayer_setUptable_returnSeat0():
    # New setUp table, from_seat 0, returns 1
    seat = 0
    assert t.next_player(seat) == 1


def test_nextplayer_from0_seat1empty_return2(self):
    # Empty seat between 0 and 2, returns 1
    self.setUp(rm=1)
    seat = 0
    assert t.next_player(seat) == 2

# setUp table, negative step, from_seat 0, returns 5
def test_nextplayer_negativestep_from0_returnSeat5(self):
    seat = 0
    assert t.next_player(seat, -1) == 5

# Empty seat between 4 and 0, returns 5
def test_nextplayer_negativestep_seat5empty_from0_returnSeat5(self):
    self.setUp(rm=5)
    seat = 0
    assert t.next_player(seat, -1) == 4

def test_nextplayer_noplayers_returnsNeg1(tbl):
    seat = 0
    with pytest.raises(Exception):
        tbl.next_player(seat)

def test_nextplayer_negstep_noplayers_returnsNeg1(tbl):
    seat = 0
    with pytest.raises(Exception):
        tbl.next_player(seat)


def test_nextplayer_from0_returns1(self):
    assert t.next_player(0) == 1


def test_nextplayer_from1_returns2(self):
    assert t.next_player(1) == 2


def test_nextplayer_from2_returns3(self):
    assert t.next_player(2) == 3


def test_nextplayer_from3_returns4(self):
    assert t.next_player(3) == 4


def test_nextplayer_from4_returns5(self):
    assert t.next_player(4) == 5


def test_nextplayer_from5_returns0(self):
    assert t.next_player(5) == 0


def test_nextplayer_withcards_from0_seat0hascards_return0(self):
    # 6 seat table, seat 0 has cards - from 0, returns 0
    c = card.Card('A', 's')
    t.seats[0].hand.add(c)
    from_seat = 0
    assert t.next_player(from_seat, hascards=True) == 0


def test_nextplayer_withcards_from1_seat0hascards_return0(self):
    # 6 seat table, seat 0 has cards - from 1, returns 0
    c = card.Card('A', 's')
    t.seats[0].hand.add(c)
    from_seat = 1
    assert t.next_player(from_seat, hascards=True) == 0


def test_nextplayer_withcards_nocards_return0(self):
    # 6 seat table, no cards - raise exception
    from_seat = 0
    with pytest.raises(Exception):
        t.next_player(from_seat, hascards=True)


def test_nextplayer_withcards_fulltable_from0_return1(self):
    # Full table - all w cards. btn at 0. From 0 returns 1.
    assert self.t.TOKENS['D'] == 0
    tools.deal_random_cards(self.t, qty=1)
    from_seat = 0
    assert t.next_player(from_seat, hascards=True) == 1


def test_nextplayer_withcards_seat3hascards_from0_return3(self):
    # Full table - seat 3 has cards. btn at 0. From 0 returns 3.
    c = card.Card('A', 's')
    t.seats[3].hand.add(c)
    from_seat = 0
    assert t.next_player(from_seat, hascards=True) == 3


def test_nextplayer_withcards_fulltable_negstep_from0_return5(self):
    # Full table - all w cards. btn at 0. From 0 returns 5. Negative step
    assert t.TOKENS['D'] == 0
    tools.deal_random_cards(t, qty=1)
    from_seat = 0
    assert t.next_player(from_seat, -1, hascards=True) == 5


def test_nextplayer_withcards_4hascards_negstep_from0_return4(self):
    # Full table - seat 3 has cards. btn at 0. negative step. From 0 returns 4.
    c = card.Card('A', 's')
    t.seats[4].hand.add(c)
    from_seat = 0
    assert t.next_player(from_seat, -1, hascards=True) == 4


def test_getbrokeplayers_6playerswithchips_returnemptylist(self):
    assert t.get_broke_players() == []


def test_getbrokeplayers_1brokeplayer_returnsplayer(self):
    s = t.seats[0]
    s.stack = 0
    assert t.get_broke_players() == [s]


def test_getbrokeplayers_2broke_returnsboth(self):
    s1, s2 = t.seats[0], t.seats[1]
    s1.stack, s2.stack = 0, 0
    assert t.get_broke_players() == [s1, s2]


def test_getplayerdict_noplayers_returns_emptydict(tbl):
    assert len(tbl.get_playerdict()) == 0


def test_getplayerdict_1player_returnsDictsize1(tbl):
    tbl.add_player(0, player.Player('bob0', 'CPU'))
    assert len(tbl.get_playerdict()) == 1


def test_getplayerdict_6players_returnsDictsize6(self):
    assert len(self.t.get_playerdict()) == 6


def test_stackdict_2players(self):
    self.setUp(players=2)
    assert t.stackdict() == {0: 1000, 1: 1000}


def test_stacklist_6players_returns4stacks(self):
    t = factory.table_factory(seats=6, stepstacks=True)
    assert t.stacklist() == [100, 200, 300, 400, 500, 600]


def test_playerlisting_1player2seats(self):
    self.setUp(players=2)
    t.pop(1)
    assert t.player_listing() == 'Seat #0: bob0($1000)\nSeat #1:\n'


def test_playerlisting_2players(self):
    self.setUp(players=2)
    assert t.player_listing() == 'Seat #0: bob0($1000)\nSeat #1: bob1($1000)\n'


def test_movebutton_newTable_returns0(self):
    # New table, moving button once should go from -1 to 0.
    assert t.TOKENS['D'] == 0


def test_movebutton_seat0removed_returns1(self):
    # New table(without seat 0), moving button once should go from -1 to 1
    self.setUp(rm=0)
    assert t.TOKENS['D'] == 1


def test_movebutton_2x_returns1(self):
    self.setUp(btn_moved=2)
    assert t.TOKENS['D'] == 1


def test_setblinds_setUpTable_SBat1(self):
    # New table: Button at 0, sb should be at 1
    self.setUp(btn_moved=1, setblinds=True)
    assert t.TOKENS['SB'] == 1


def test_setblinds_seat1removed_SBat2(self):
    # New table(seat 1 removed): Button at 0, sb should be at 2
    self.setUp(rm=1, btn_moved=1, setblinds=True)
    t.set_blinds()
    assert t.TOKENS['SB'] == 2


def test_setblinds_setUpTable_BBat2(self):
    # New table: Button at 0, bb should be at 2
    self.setUp(setblinds=True)
    assert t.TOKENS['BB'] == 2


def test_setblinds_seat2removed_BBat3(self):
    # New table(seat 2 removed): Button at 0, bb should be at 3
    self.setUp(rm=2, setblinds=True)
    assert t.TOKENS['D'] == 0
    assert t.TOKENS['BB'] == 3


def test_bringin_stud5_no_ties_returns5(self):
    # Stud5 deal: seat 5 has lowest card, 9
    tools.deal_stud5(t, matchingranks=0)
    t.set_bringin()
    assert t.TOKENS['BI'] == 5


def test_bringin_stud5_2tied_returns1(self):
    # Stud5 deal: 2 Tied ranks
    tools.deal_stud5(t, matchingranks=2)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud5_3tied_returns1(self):
    # Stud5 deal: 3 Tied ranks
    tools.deal_stud5(t, matchingranks=3)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud5_4tied_returns1(self):
    # Stud5 deal: 4 Tied ranks
    tools.deal_stud5(t, matchingranks=4)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud7_no_ties_returns6(self):
    # Stud7 deal: seat 5 has lowest card, 9
    tools.deal_stud5(t, matchingranks=0)
    t.set_bringin()
    assert t.TOKENS['BI'] == 5


def test_bringin_stud7_2tied_returns1(self):
    # Stud7 deal: 2 Tied ranks
    tools.deal_stud5(t, matchingranks=2)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud7_3tied_returns1(self):
    # Stud7 deal: 3 Tied ranks
    tools.deal_stud5(t, matchingranks=3)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1


def test_bringin_stud7_4tied_returns1(self):
    # Stud7 deal: 4 Tied ranks
    tools.deal_stud5(t, matchingranks=4)
    t.set_bringin()
    assert t.TOKENS['BI'] == 1

def test_randomizebutton_2seats_inrange0to1(self):
    # Randomize button on table size 2, button is in range 0-1
    seats = 2
    self.setUp(players=seats)
    t.randomize_button()
    assert t.TOKENS['D'] >= 0
    assert t.TOKENS['D'] < seats

def test_randomizebutton_6seats_validbtn(self):
    seats = 6
    self.setUp(players=seats)
    t.randomize_button()
    assert t.TOKENS['D'] >= 0
    assert t.TOKENS['D'] < seats


def test_randomizebutton_9seats_inrange0to8(self):
    # Randomize button on table size 9, button is in range 0-8
    seats = 9
    self.setUp(players=seats)
    t.randomize_button()
    assert t.TOKENS['D'] >= 0
    assert t.TOKENS['D'] < seats

def test_randomizebutton_noplayers_raisesException(self):
    # Randomize button on table size 9, but no players
    seats = 9
    t = table.Table(seats)
    with pytest.raises(Exception):
        t.randomize_button()

# Raise an exception if the button is not set

def test_position_3max_SB_returns2(self):
    self.setUp(players=3)
    SB = t.seats[1]
    assert t.position(SB) == 2

def test_position_3max_BB_returns1(self):
    self.setUp(players=3)
    BB = t.seats[2]
    assert t.position(BB) == 1

def test_position_4max_SB_returns3(self):
    self.setUp(players=4)
    SB = t.seats[1]
    assert t.position(SB) == 3

def test_position_4max_BB_returns2(self):
    self.setUp(players=4)
    BB = t.seats[2]
    assert t.position(BB) == 2


def test_position_6max_EP_returns3(self):
    self.setUp(players=6)
    BB = t.seats[3]
    assert t.position(BB) == 3
