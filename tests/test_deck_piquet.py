"""
  " Tests for PiquetDeck
  """
from ..src import deck_piquet as dpiq
from ..src import playingcard as pc


def test_init_PiquetDeck_size32():
    d = dpiq.PiquetDeck()
    assert len(d) == 32


def test_init_PiquetDeck_4Aces():
    d = dpiq.PiquetDeck()
    result = sum(1 for c in d.cards if c.rank == 'A')
    assert result == 4


def test_init_PiquetDeck_1AceSpades():
    d = dpiq.PiquetDeck()
    c = pc.PlayingCard('A', 's')
    assert d.cards.count(c) == 1
