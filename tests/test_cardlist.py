from ..src import cardlist
from ..src import deck
from ..src import joker
from ..src import playingcard as pc
from ..src import tools


def test_len_newcardlist_size0():
    cl = cardlist.CardList()
    assert len(cl) == 0


def test_len_2cards_len2():
    cards = tools.convert_to_cards(['As', 'Ks'])
    cl = cardlist.CardList(cards)
    assert len(cl) == 2


def test_len_fulldeck_len52():
    cl = cardlist.CardList(deck.std_deck())
    assert len(cl) == 52


def test_str_1card():
    c = pc.PlayingCard('A', 's')
    cl = cardlist.CardList([c])
    cl.toggle_hidden(False)
    assert str(cl) == 'As'


def test_contains_AceSpadesinStandardDeck_returnsTrue():
    c = pc.PlayingCard('A', 's')
    cl = cardlist.CardList([c])
    assert c in cl.cards


def test_contains_JokerinStandardDeck_returnsFalse():
    cl = cardlist.CardList()
    c = joker.Joker()
    assert c not in cl.cards


def test_isempty_hasacard_returnFalse():
    c = pc.PlayingCard('A', 's')
    cl = cardlist.CardList([c])
    assert cl.is_empty() is False


def test_isempty_emptydeck_returnTrue():
    cl = cardlist.CardList()
    assert cl.is_empty()


def test_remove_existingcard_size0():
    c = pc.PlayingCard('A', 's')
    cl = cardlist.CardList([c])
    cl.remove(c)
    assert len(cl) == 0


def test_remove_cardnotindeck_returnsNone():
    cl = cardlist.CardList()
    c = pc.PlayingCard('Z', 's')
    assert cl.remove(c) == None


def test_togglehidden_1card_hidden():
    c = pc.PlayingCard('A', 's')
    cl = cardlist.CardList([c])
    cl.toggle_hidden(False)
    assert cl.cards[0].hidden is False


def test_togglehidden_1card_nothidden():
    c = pc.PlayingCard('A', 's')
    cl = cardlist.CardList([c])
    cl.toggle_hidden(True)
    assert cl.cards[0].hidden
