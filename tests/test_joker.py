"""
  " Tests for joker.py
  """
from ..src import card
from ..src import joker
from ..src import tools


def test_pickjoker_89TJrainbow_returnsQ():
    h = tools.make('OESD 4card')
    j = joker.pick_joker(h)
    assert j.rank == 'Q'


def test_pickjoker_spadeflushdraw_returnsAs():
    h = tools.make('flushdraw 4card')
    expected = card.Card('A', 's')
    assert joker.pick_joker(h) == expected


def test_pickjoker_straightflushdraw_returnsAs():
    h = tools.make('straightflush 4card')
    expected = card.Card('A', 's')
    assert joker.pick_joker(h) == expected


def test_pickjoker_2AA_returnsA():
    h = tools.make('2AA_v1')
    j = joker.pick_joker(h)
    assert j.rank == 'A'
