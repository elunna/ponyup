import pytest
from ..src import cardlist
from ..src import playingcard as pc


@pytest.fixture
def full_deck():
    d = pc.std_deck()
    return cardlist.CardList(d)


@pytest.fixture
def test_cl():
    return cardlist.CardList()


@pytest.fixture
def ace_spades():
    return pc.PlayingCard(rank='A', suit='s')


def test_len_newcardlist_size0(test_cl):
    assert len(test_cl) == 0


def test_len_1card_len1(ace_spades):
    cl = cardlist.CardList([ace_spades])
    assert len(cl) == 1


def test_len_fulldeck_len52(full_deck):
    assert len(full_deck) == 52


def test_str_1card(ace_spades):
    cl = cardlist.CardList([ace_spades])
    cl.toggle_hidden(False)
    assert str(cl) == 'As'


def test_contains_AceSpadesinStandardDeck_returnsTrue(ace_spades):
    cl = cardlist.CardList([ace_spades])
    assert ace_spades in cl.cards


def test_contains_JokerinStandardDeck_returnsFalse(test_cl):
    c = pc.Joker()
    assert c not in test_cl.cards


def test_isempty_hasacard_returnFalse(ace_spades):
    cl = cardlist.CardList([ace_spades])
    assert cl.is_empty() is False


def test_isempty_emptydeck_returnTrue(test_cl):
    assert test_cl.is_empty()


def test_remove_existingcard_size0(ace_spades):
    cl = cardlist.CardList([ace_spades])
    cl.remove(ace_spades)
    assert len(cl) == 0


def test_remove_cardnotindeck_returnsNone(test_cl):
    c = pc.PlayingCard('Z', 's')
    assert test_cl.remove(c) == None


def test_togglehidden_1card_hidden(ace_spades):
    cl = cardlist.CardList([ace_spades])
    cl.toggle_hidden(False)
    assert cl.cards[0].hidden is False


def test_togglehidden_1card_nothidden(ace_spades):
    cl = cardlist.CardList([ace_spades])
    cl.toggle_hidden(True)
    assert cl.cards[0].hidden


def test_sort_2cards_deuceisfirst(test_cl):
    c1 = pc.PlayingCard('A', 's')
    c2 = pc.PlayingCard('2', 's')
    test_cl.cards = [c1, c2]
    test_cl.sort()
    assert test_cl.cards[0].rank == '2'


def test_sort_3cards_deuceisfirst(test_cl):
    c1 = pc.PlayingCard('A', 's')
    c2 = pc.PlayingCard('2', 's')
    c3 = pc.PlayingCard('7', 's')
    test_cl.cards = [c1, c2, c3]
    test_cl.sort()
    assert test_cl.cards[0].rank == '2'
