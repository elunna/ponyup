
"""
  " Tests for playingcard.py
  """
import pytest
from ..src import playingcard
PlayingCard = playingcard.PlayingCard


def test_init_invalidsuit_raiseEx():
    with pytest.raises(ValueError):
        PlayingCard('A', 'a')


def test_init_invalidrank_raiseEx():
    with pytest.raises(ValueError):
        PlayingCard('Y', 's')


def test_init_invalidboth_raiseEx():
    with pytest.raises(ValueError):
        PlayingCard('s', 'A')


def test_init_uppercaseSuit_suitIsLowercase():
    c = PlayingCard('A', 'S')
    assert c.suit == 's'


def test_init_default_hiddenIsTrue():
    c = PlayingCard('A', 's')
    assert c.hidden is True


def test_str_hiddenCard_returnsXx():
    c = PlayingCard('A', 's')
    assert str(c) == 'Xx'


def test_str_As_returnsAs():
    c = PlayingCard('A', 's')
    c.hidden = False
    assert str(c) == 'As'


def test_repr_hiddenCard_returnsXx():
    c = PlayingCard('A', 's')
    assert repr(c) == 'Xx'


def test_repr_FaceupAs_returnsAs():
    c = PlayingCard('A', 's')
    c.hidden = False
    assert repr(c) == 'As'


def test_gt_HighToLow_returnsFalse():
    high = PlayingCard('A', 's')
    low = PlayingCard('K', 's')
    assert high > low


def test_gt_LowToHigh_returnsTrue():
    high = PlayingCard('A', 's')
    low = PlayingCard('K', 's')
    assert not low > high


def test_gt_SameRanks_returnsFalse():
    c1 = PlayingCard('K', 's')
    c2 = PlayingCard('K', 'c')
    assert not c2 > c1


def test_lt_HighToLow_returnsFalse():
    high = PlayingCard('A', 's')
    low = PlayingCard('K', 's')
    assert not high < low


def test_lt_LowToHigh_returnsTrue():
    high = PlayingCard('A', 's')
    low = PlayingCard('K', 's')
    assert low < high


def test_lt_SameRanks_returnsFalse():
    c1 = PlayingCard('K', 's')
    c2 = PlayingCard('K', 'c')
    assert not c2 < c1


def test_val_A_returns14():
    c = PlayingCard('A', 's')
    assert c.val() == 14


def test_val_K_returns13():
    instance = PlayingCard('K', 's')
    assert instance.val() == 13


def test_val_Q_returns12():
    instance = PlayingCard('Q', 's')
    assert instance.val() == 12


def test_val_J_returns11():
    instance = PlayingCard('J', 's')
    assert instance.val() == 11


def test_val_T_returns10():
    instance = PlayingCard('T', 's')
    assert instance.val() == 10


def test_val_9_returns9():
    instance = PlayingCard('9', 's')
    assert instance.val() == 9


def test_val_8_returns8():
    instance = PlayingCard('8', 's')
    assert instance.val() == 8


def test_val_7_returns7():
    instance = PlayingCard('7', 's')
    assert instance.val() == 7


def test_val_6_returns6():
    instance = PlayingCard('6', 's')
    assert instance.val() == 6


def test_val_5_returns5():
    instance = PlayingCard('5', 's')
    assert instance.val() == 5


def test_val_4_returns4():
    instance = PlayingCard('4', 's')
    assert instance.val() == 4


def test_val_3_returns3():
    instance = PlayingCard('3', 's')
    assert instance.val() == 3


def test_val_2_returns2():
    instance = PlayingCard('2', 's')
    assert instance.val() == 2


def test_val_JOKER_Z_returns15():
    c = PlayingCard('Z', 's')
    assert c.val() == 15
