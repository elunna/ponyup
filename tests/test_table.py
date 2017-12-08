"""
  " Tests for table.py
  """
import pytest
from ..src import player
from ..src import table


@pytest.fixture
def tbl():
    return table.Table(size=6)


def custom_tbl(players=6):
    """ Setup a table filled with generic players for testing. """
    t = table.Table(players)

    for i, seat in enumerate(t):
        name = 'bob{}'.format(i)
        p = player.Player(name)
        seat.sitdown(p)

    return t


def test_init_invalidtablesize1_throwException():
    with pytest.raises(ValueError):
        table.Table('1')


def test_init_invalidtablesize11_throwException():
    with pytest.raises(ValueError):
        table.Table('11')


def test_len_newTable_returns6(tbl):
    assert len(tbl) == 6


def test_next_newTable_getsseat0():
    # Test that the table iterates through seats in order, full table
    t = custom_tbl()
    iterator = t.__iter__()
    nextplayer = next(iterator)
    # Test seat # instead
    assert str(nextplayer) == 'bob0'


def test_next2_newTable_getsseat1():
    # Test that it goes to the next player.
    t = custom_tbl()
    iterator = t.__iter__()
    next(iterator)
    assert str(next(iterator)) == 'bob1'


def test_iternext_removedseat0_getsseat0():
    # Iter should NOT skip over an empty seat
    t = custom_tbl()
    t.pop(0)
    iterator = t.__iter__()
    assert next(iterator).NUM == 0


def test_addplayer_EmptyTable_1player(tbl):
    tbl.add_player(0, player.Player('bob0', 'CPU'))
    assert len(tbl.get_occupied_seats()) == 1


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
    p = player.Player('bob0', 'CPU')
    tbl.add_player(0, p)
    tbl.pop(0)
    assert tbl.seats[0].vacant()


def test_pop_seat0_returnsPlayer():
    t = custom_tbl()
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


def test_getfreeseats_0players(tbl):
    assert len(tbl.get_free_seats()) == 6


def test_getoccupiedseats_0players(tbl):
    assert tbl.get_occupied_seats() == []
