import pytest
from . import test_table
from ..src import table
from ..src import button


def test_movebutton_newTable_returns0():
    t = test_table.custom_tbl(players=6)
    btn = button.Button(t)
    btn.move()
    assert btn.seat == 0


def test_movebutton_seat0removed_returns1():
    t = test_table.custom_tbl(players=6)
    t.pop(0)
    btn = button.Button(t)
    btn.move()
    assert btn.seat == 1


def test_movebutton_2x_returns1():
    t = test_table.custom_tbl(players=6)
    btn = button.Button(t)
    btn.move()
    btn.move()
    assert btn.seat == 1


def test_randomize_2seats_inrange0to1():
    # Randomize button on table size 2, button is in range 0-1
    seats = 2
    t = test_table.custom_tbl(players=seats)
    btn = button.Button(t)
    btn.randomize()
    assert btn.seat >= 0
    assert btn.seat < seats


def test_randomize_6seats_validbtn():
    seats = 6
    t = test_table.custom_tbl(players=seats)
    btn = button.Button(t)
    btn.randomize()
    assert btn.seat >= 0
    assert btn.seat < seats


def test_randomize_9seats_inrange0to8():
    # Randomize button on table size 9, button is in range 0-8
    seats = 9
    t = test_table.custom_tbl(players=seats)
    btn = button.Button(t)
    btn.randomize()
    assert btn.seat >= 0
    assert btn.seat < seats


def test_randomize_noplayers_raisesException():
    # Randomize button on table size 9, but no players
    seats = 9
    t = table.Table(seats)
    btn = button.Button(t)
    with pytest.raises(Exception):
        btn.randomize()
