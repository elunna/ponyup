import pytest
from ..src import cardlist
from ..src import deck
from ..src import joker
from ..src import card


@pytest.fixture
def full_deck():
    d = deck.std_deck()
    return cardlist.CardList(d)


@pytest.fixture
def test_cl():
    return cardlist.CardList()


def test_len_newcardlist_size0(test_cl):
    assert len(test_cl) == 0


def test_len_1card_len1():
    c = card.Card('As')
    cl = cardlist.CardList([c])
    assert len(cl) == 1


def test_len_fulldeck_len52(full_deck):
    assert len(full_deck) == 52


def test_str_1card():
    c = card.Card('As')
    cl = cardlist.CardList([c])
    cl.toggle_hidden(False)
    assert str(cl) == 'As'


def test_contains_AceSpadesinStandardDeck_returnsTrue():
    c = card.Card('As')
    cl = cardlist.CardList([c])
    assert c in cl.cards


def test_contains_JokerinStandardDeck_returnsFalse(test_cl):
    c = joker.Joker()
    assert c not in test_cl.cards


def test_isempty_hasacard_returnFalse():
    c = card.Card('As')
    cl = cardlist.CardList([c])
    assert cl.is_empty() is False


def test_isempty_emptydeck_returnTrue(test_cl):
    assert test_cl.is_empty()


def test_remove_existingcard_size0():
    c = card.Card('As')
    cl = cardlist.CardList([c])
    cl.remove(c)
    assert len(cl) == 0


def test_remove_cardnotindeck_returnsNone(test_cl):
    c = card.Card('Zs')
    assert test_cl.remove(c) == None


def test_togglehidden_1card_hidden():
    c = card.Card('As')
    cl = cardlist.CardList([c])
    cl.toggle_hidden(False)
    assert cl.cards[0].hidden is False


def test_togglehidden_1card_nothidden():
    c = card.Card('As')
    cl = cardlist.CardList([c])
    cl.toggle_hidden(True)
    assert cl.cards[0].hidden
