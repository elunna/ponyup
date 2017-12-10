"""
  " Tests for BlackjackDeck
  """
import pytest
from ..src import deck_blackjack as bj
from ..src import playingcard as pc


def test_mkblackjackdeck_raiseException():
    with pytest.raises(ValueError):
        bj.mk_blackjack_deck(0)


def test_mkblackjackdeck_negshoes_raiseException():
    with pytest.raises(ValueError):
        bj.mk_blackjack_deck(-1)


def test_init_2shoes_104cards():
    d = bj.mk_blackjack_deck(2)
    assert len(d) == 104


def test_init_4shoes_208cards():
    d = bj.mk_blackjack_deck(4)
    assert len(d) == 208


def test_init_4shoes_4AceSpaces():
    d = bj.mk_blackjack_deck(4)
    c = pc.PlayingCard('A', 's')
    assert d.count(c) == 4
