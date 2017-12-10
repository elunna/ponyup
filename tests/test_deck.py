"""
  " Tests for deck.py
  """
import pytest
from ..src import deck
from ..src import playingcard as pc


def test_stddeck_size52():
    d = deck.std_deck()
    assert len(d) == 52


def test_stddeck_allunique():
    d = deck.std_deck()
    assert len(set(d)) == 52


def test_deal_stddeck_sizeIs51():
    d = deck.Deck()
    d.deal()
    assert len(d) == 51


def test_deal_As_returnsCard():
    c = pc.PlayingCard('A', 's')
    d = deck.Deck([c])
    assert d.deal() == c


def test_deal_emptydeck_raiseException():
    d = deck.Deck([])
    assert len(d) == 0
    with pytest.raises(Exception):
        d.deal()
