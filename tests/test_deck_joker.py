"""
  " Tests for Deck1Joker
  """
from ..src import deck_joker as dj
from ..src import joker


def test_1Joker_containsJoker():
    d = dj.DeckJoker(jokers=1)
    joker1 = joker.Joker()
    assert joker1 in d.cards


def test_1Joker_size53():
    d = dj.DeckJoker(jokers=1)
    assert len(d) == 53


def test_2Joker_size54():
    d = dj.DeckJoker(jokers=2)
    assert len(d) == 54


def test_1Joker_contains1Joker():
    d = dj.DeckJoker(jokers=1)
    count = sum(1 for c in d.cards if isinstance(c, joker.Joker))
    assert count == 1


def test_2Joker_contains2Jokers():
    d = dj.DeckJoker(jokers=2)
    count = sum(1 for c in d.cards if isinstance(c, joker.Joker))
    assert count == 2
