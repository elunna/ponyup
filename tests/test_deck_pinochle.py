"""
  " Tests for PinochleDeck
  """
from ..src import deck_pinochle as dpiq
from ..src import playingcard as pc


def test_init_PinochleDeck_size48():
    d = dpiq.PinochleDeck()
    assert len(d) == 48


def test_init_PinochleDeck_8Aces():
    d = dpiq.PinochleDeck()
    result = sum(1 for c in d.cards if c.rank == 'A')
    assert result == 8


def test_init_PinochleDeck_2AceSpades():
    c = pc.PlayingCard('A', 's')
    d = dpiq.PinochleDeck()
    assert d.cards.count(c) == 2
