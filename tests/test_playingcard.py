
"""
  " Tests for playingcard.py
  """
import pytest
from ..src import playingcard as pc

# Test the standard 52-card deck constructor


def test_stddeck_size52():
    d = pc.std_deck()
    assert len(d) == 52


def test_stddeck_allunique():
    d = pc.std_deck()
    assert len(set(d)) == 52


# Tests for PlayingCard

def test_init_invalidsuit_raiseEx():
    with pytest.raises(ValueError):
        pc.PlayingCard('A', 'a')


def test_init_invalidrank_raiseEx():
    with pytest.raises(ValueError):
        pc.PlayingCard('Y', 's')


def test_init_invalidboth_raiseEx():
    with pytest.raises(ValueError):
        pc.PlayingCard('s', 'A')


def test_init_uppercaseSuit_raiseException():
    with pytest.raises(ValueError):
        pc.PlayingCard('A', 'S')


def test_init_default_hiddenIsTrue():
    c = pc.PlayingCard('A', 's')
    assert c.hidden is True


def test_str_hiddenCard_returnsXx():
    c = pc.PlayingCard('A', 's')
    assert str(c) == 'Xx'


def test_str_As_returnsAs():
    c = pc.PlayingCard('A', 's')
    c.hidden = False
    assert str(c) == 'As'


def test_repr_hiddenCard_returnsXx():
    c = pc.PlayingCard('A', 's')
    assert repr(c) == 'Xx'


def test_repr_FaceupAs_returnsAs():
    c = pc.PlayingCard('A', 's')
    c.hidden = False
    assert repr(c) == 'As'


def test_gt_HighToLow_returnsFalse():
    high = pc.PlayingCard('A', 's')
    low = pc.PlayingCard('K', 's')
    assert high > low


def test_gt_LowToHigh_returnsTrue():
    high = pc.PlayingCard('A', 's')
    low = pc.PlayingCard('K', 's')
    assert not low > high


def test_gt_SameRanks_returnsFalse():
    c1 = pc.PlayingCard('K', 's')
    c2 = pc.PlayingCard('K', 'c')
    assert not c2 > c1


def test_lt_HighToLow_returnsFalse():
    high = pc.PlayingCard('A', 's')
    low = pc.PlayingCard('K', 's')
    assert not high < low


def test_lt_LowToHigh_returnsTrue():
    high = pc.PlayingCard('A', 's')
    low = pc.PlayingCard('K', 's')
    assert low < high


def test_lt_SameRanks_returnsFalse():
    c1 = pc.PlayingCard('K', 's')
    c2 = pc.PlayingCard('K', 'c')
    assert not c2 < c1


def test_val_A_returns14():
    c = pc.PlayingCard('A', 's')
    assert c.val() == 14


def test_val_K_returns13():
    instance = pc.PlayingCard('K', 's')
    assert instance.val() == 13


def test_val_Q_returns12():
    instance = pc.PlayingCard('Q', 's')
    assert instance.val() == 12


def test_val_J_returns11():
    instance = pc.PlayingCard('J', 's')
    assert instance.val() == 11


def test_val_T_returns10():
    instance = pc.PlayingCard('T', 's')
    assert instance.val() == 10


def test_val_9_returns9():
    instance = pc.PlayingCard('9', 's')
    assert instance.val() == 9


def test_val_8_returns8():
    instance = pc.PlayingCard('8', 's')
    assert instance.val() == 8


def test_val_7_returns7():
    instance = pc.PlayingCard('7', 's')
    assert instance.val() == 7


def test_val_6_returns6():
    instance = pc.PlayingCard('6', 's')
    assert instance.val() == 6


def test_val_5_returns5():
    instance = pc.PlayingCard('5', 's')
    assert instance.val() == 5


def test_val_4_returns4():
    instance = pc.PlayingCard('4', 's')
    assert instance.val() == 4


def test_val_3_returns3():
    instance = pc.PlayingCard('3', 's')
    assert instance.val() == 3


def test_val_2_returns2():
    instance = pc.PlayingCard('2', 's')
    assert instance.val() == 2


# Tests for Joker

def test_val_JOKER_Z_returns15():
    c = pc.Joker()
    assert c.val() == 15


def test_joker_gt_Ace_returnTrue():
    ace = pc.PlayingCard('A', 's')
    j = pc.Joker()
    assert j > ace


def test_joker_lt_Ace_returnFalse():
    ace = pc.PlayingCard('A', 's')
    j = pc.Joker()
    assert not j < ace
