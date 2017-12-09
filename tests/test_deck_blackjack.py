"""
  " Tests for BlackjackDeck
  """
import pytest
from ..src import deck_blackjack as bj
from ..src import playingcard as pc


def test_init_0shoes_raiseException():
    with pytest.raises(ValueError):
        bj.BlackjackDeck(0)


def test_init_negshoes_raiseException():
    with pytest.raises(ValueError):
        bj.BlackjackDeck(-1)


def test_init_4shoes_208cards():
    d = bj.BlackjackDeck(4)
    assert len(d) == 208


def test_init_4shoes_4AceSpaces():
    d = bj.BlackjackDeck(4)
    c = pc.PlayingCard('A', 's')
    assert d.cards.count(c) == 4


def test_init_6shoes_312cards():
    d = bj.BlackjackDeck(6)
    assert len(d) == 312
