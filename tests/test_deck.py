"""
  " Tests for deck.py
  """
import pytest
from ..src import deck
from ..src import playingcard as pc
from ..src import joker
from ..src import tools


def test_str_2cards_returnsAsKsinParentheses():
    cards = tools.convert_to_cards(['As', 'Ks'])
    d = deck.Deck(cards)
    d.unhide()  # They are hidden by default
    assert str(d) == 'As Ks'


def test_len_size52():
    d = deck.Deck()
    assert len(d) == 52


def test_len_2cards_haslen2():
    cards = tools.convert_to_cards(['As', 'Ks'])
    d = deck.Deck(cards)
    assert len(d) == 2


def test_contains_AceSpadesinStandardDeck_returnsTrue():
    d = deck.Deck()
    c = pc.PlayingCard('A', 's')
    assert c in d


def test_contains_JokerinStandardDeck_returnsFalse():
    d = deck.Deck()
    c = joker.Joker()
    assert c not in d


def test_sort_2cards_deuceisfirst():
    cards = tools.convert_to_cards(['As', '2s'])
    d = deck.Deck(cards)
    d.sort()
    assert d.cards[0].rank == '2'


def test_sort_3cards_deuceisfirst():
    cards = tools.convert_to_cards(['As', '7s', '2s'])
    d = deck.Deck(cards)
    d.sort()
    assert d.cards[0].rank == '2'


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


def test_isempty_fulldeck_returnFalse():
    d = deck.Deck()
    assert not d.is_empty()


def test_isempty_emptydeck_returnTrue():
    d = deck.Deck([])
    assert d.is_empty()


def test_remove_removeAs_sizeIs51():
    d = deck.Deck()
    c = pc.PlayingCard('A', 's')
    d.remove(c)
    assert len(d) == 51


def test_remove_cardnotindeck_returnsNone():
    d = deck.Deck()
    c = pc.PlayingCard('Z', 's')
    assert d.remove(c) == None


def test_removecards_removeAs_sizeIs51():
    d = deck.Deck()
    c = pc.PlayingCard('A', 's')
    d.remove_cards([c])
    assert len(d) == 51


def test_removecards_removeAs_containsIsFalse():
    d = deck.Deck()
    c = pc.PlayingCard('A', 's')
    d.remove_cards([c])
    assert c not in d


def test_removecards_removeAsKs_containsNeither():
    d = deck.Deck()
    cards = tools.convert_to_cards(['As', 'Ks'])
    d.remove_cards(cards)
    assert cards[0] not in d
    assert cards[1] not in d


# All cards in deck are faceup
def test_unhide_2cards_bothfaceup():
    cards = tools.convert_to_cards(['As', 'Ks'])
    d = deck.Deck(cards)
    d.unhide()
    assert d.cards[0].hidden is False
    assert d.cards[1].hidden is False
