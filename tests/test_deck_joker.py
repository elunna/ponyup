"""
  " Tests for Deck1Joker
  """
from ..src import deck_joker as dj
from ..src import playingcard as pc

# Test deck constructor


def test_mkjokerdeck_1Joker_containsJoker():
    d = dj.mk_joker_deck(jokers=1)
    joker1 = pc.Joker()
    assert joker1 in d


def test_mkjokerdeck_1Joker_size53():
    d = dj.mk_joker_deck(jokers=1)
    assert len(d) == 53


def test_mkjokerdeck_2Joker_size54():
    d = dj.mk_joker_deck(jokers=2)
    assert len(d) == 54


def test_mkjokerdeck_1Joker_contains1Joker():
    d = dj.mk_joker_deck(jokers=1)
    count = sum(1 for c in d if isinstance(c, pc.Joker))
    assert count == 1


def test_mkjokerdeck_2Joker_contains2Jokers():
    d = dj.mk_joker_deck(jokers=2)
    count = sum(1 for c in d if isinstance(c, pc.Joker))
    assert count == 2


# Test Joker class
