"""
  " Tests for card.py
  """
import pytest
from ..src import card


def test_init_invalidsuit_raiseEx():
    with pytest.raises(ValueError):
        card.Card('A', 'a')


def test_init_invalidrank_raiseEx():
    with pytest.raises(ValueError):
        card.Card('Y', 's')


def test_init_invalidboth_raiseEx():
    with pytest.raises(ValueError):
        card.Card('s', 'A')


def test_init_uppercaseSuit_suitIsLowercase():
    c = card.Card('A', 'S')
    assert c.suit == 's'


def test_init_default_hiddenIsTrue():
    c = card.Card('A', 's')
    assert c.hidden is True


def test_str_hiddenCard_returnsXx():
    c = card.Card('A', 's')
    assert str(c) == 'Xx'


def test_str_As_returnsAs():
    c = card.Card('A', 's')
    c.hidden = False
    assert str(c) == 'As'


def test_repr_hiddenCard_returnsXx():
    c = card.Card('A', 's')
    assert repr(c) == 'Xx'


def test_repr_FaceupAs_returnsAs():
    c = card.Card('A', 's')
    c.hidden = False
    assert repr(c) == 'As'


def test_eq_SameCard_returnsTrue():
    """ __equals__ tests that the two cards have exactly the same suit and rank."""
    c1 = card.Card('A', 's')
    c2 = card.Card('A', 's')
    assert c1 == c2


def test_eq_DiffSuits_returnsFalse():
    c1 = card.Card('A', 's')
    c2 = card.Card('A', 'c')
    assert c1 != c2


def test_gt_HighToLow_returnsFalse():
    high = card.Card('A', 's')
    low = card.Card('K', 's')
    assert high > low


def test_gt_LowToHigh_returnsTrue():
    high = card.Card('A', 's')
    low = card.Card('K', 's')
    assert not low > high


def test_gt_SameRanks_returnsFalse():
    c1 = card.Card('K', 's')
    c2 = card.Card('K', 'c')
    assert not c2 > c1


def test_lt_HighToLow_returnsFalse():
    high = card.Card('A', 's')
    low = card.Card('K', 's')
    assert not high < low


def test_lt_LowToHigh_returnsTrue():
    high = card.Card('A', 's')
    low = card.Card('K', 's')
    assert low < high


def test_lt_SameRanks_returnsFalse():
    c1 = card.Card('K', 's')
    c2 = card.Card('K', 'c')
    assert not c2 < c1


def test_val_JOKER_Z_returns15():
    c = card.Card('Z', 's')
    assert c.val() == 15


def test_val_A_returns14():
    c = card.Card('A', 's')
    assert c.val() == 14


def test_val_K_returns13():
    instance = card.Card('K', 's')
    assert instance.val() == 13


def test_val_Q_returns12():
    instance = card.Card('Q', 's')
    assert instance.val() == 12


def test_val_J_returns11():
    instance = card.Card('J', 's')
    assert instance.val() == 11


def test_val_T_returns10():
    instance = card.Card('T', 's')
    assert instance.val() == 10


def test_val_9_returns9():
    instance = card.Card('9', 's')
    assert instance.val() == 9


def test_val_8_returns8():
    instance = card.Card('8', 's')
    assert instance.val() == 8


def test_val_7_returns7():
    instance = card.Card('7', 's')
    assert instance.val() == 7


def test_val_6_returns6():
    instance = card.Card('6', 's')
    assert instance.val() == 6


def test_val_5_returns5():
    instance = card.Card('5', 's')
    assert instance.val() == 5


def test_val_4_returns4():
    instance = card.Card('4', 's')
    assert instance.val() == 4


def test_val_3_returns3():
    instance = card.Card('3', 's')
    assert instance.val() == 3


def test_val_2_returns2():
    instance = card.Card('2', 's')
    assert instance.val() == 2
