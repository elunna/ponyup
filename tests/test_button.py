from . import test_table

# def test_movebutton_newTable_returns0(self):
# def test_movebutton_seat0removed_returns1(self):
# def test_movebutton_2x_returns1(self):


def test_randomizebutton_2seats_inrange0to1(self):
    # Randomize button on table size 2, button is in range 0-1
    seats = 2
    t = test_table.custom_tbl(players=seats)
    t.randomize_button()
    assert t.TOKENS['D'] >= 0
    assert t.TOKENS['D'] < seats


def test_randomizebutton_6seats_validbtn(self):
    seats = 6
    t = test_table.custom_tbl(players=seats)
    t.randomize_button()
    assert t.TOKENS['D'] >= 0
    assert t.TOKENS['D'] < seats


def test_randomizebutton_9seats_inrange0to8(self):
    # Randomize button on table size 9, button is in range 0-8
    seats = 9
    t = test_table.custom_tbl(players=seats)
    t.randomize_button()
    assert t.TOKENS['D'] >= 0
    assert t.TOKENS['D'] < seats

def test_randomizebutton_noplayers_raisesException(self):
    # Randomize button on table size 9, but no players
    seats = 9
    t = table.Table(seats)
    with pytest.raises(Exception):
        t.randomize_button()
