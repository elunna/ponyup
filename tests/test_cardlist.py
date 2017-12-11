import pytest
from ..src import cardlist
from ..src import playingcard as pc
from ..src import tools


@pytest.fixture
def full_deck():
    d = pc.std_deck()
    return cardlist.CardList(d)


@pytest.fixture
def ace():
    return pc.PlayingCard('A', 's')


def test_contains_AceSpades_StdDeck_returnsTrue(ace):
    cl = cardlist.CardList([ace])
    assert ace in cl.cards


def test_contains_Jokerin_StdDeck_returnsFalse():
    cl = cardlist.CardList()
    c = pc.Joker()
    assert c not in cl.cards


def test_len_newcardlist_size0():
    cl = cardlist.CardList()
    assert len(cl) == 0


def test_len_1card_len1(ace):
    cl = cardlist.CardList([ace])
    assert len(cl) == 1


def test_len_fulldeck_len52(full_deck):
    assert len(full_deck) == 52


def test_str_1card(ace):
    cl = cardlist.CardList([ace])
    cl.reveal()
    assert str(cl) == 'As'


def test_add_1card_length1(ace):
    cl = cardlist.CardList()
    cl.add(ace)
    assert len(cl) == 1


def test_add_1card_containsCard(ace):
    cl = cardlist.CardList()
    cl.add(ace)
    assert ace in cl.cards


def test_countrank_1K_returns1():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc']))
    assert cl.count_rank('K') == 1


def test_countrank_0A_returns():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc']))
    assert cl.count_rank('A') == 0


def test_countrank_1Kin2cards_returns1():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Kc']))
    assert cl.count_rank('K') == 1


def test_countsuit_nospade_returns0():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc']))
    assert cl.count_suit('s') == 0


def test_countsuit_1spade_returns1():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc', 'As']))
    assert cl.count_suit('s') == 1


def test_discard_1card_length0(ace):
    cl = cardlist.CardList([ace])
    cl.discard(ace)
    assert len(cl) == 0


def test_discard_1card_returnsCard(ace):
    cl = cardlist.CardList([ace])
    assert cl.discard(ace) == ace


def test_discard_cardNotInHand_raiseException(ace):
    cl = cardlist.CardList()
    with pytest.raises(ValueError):
        cl.discard(ace)


def test_getupcards_1downcard_returnsEmptyList(ace):
    cl = cardlist.CardList([ace])
    assert cl.get_upcards() == []


def test_getupcards_1upcard_returnsUpCard(ace):
    ace.hidden = False
    cl = cardlist.CardList([ace])
    assert cl.get_upcards() == [ace]


def test_getupcards_1up1down_returns1up():
    cards = tools.convert_to_cards(['As', 'Ks'])
    cards[0].hidden = False
    cl = cardlist.CardList(cards)
    assert len(cl.get_upcards()) == 1


def test_isempty_hasacard_returnFalse(ace):
    cl = cardlist.CardList([ace])
    assert cl.is_empty() is False


def test_isempty_emptylist_returnTrue():
    cl = cardlist.CardList()
    assert cl.is_empty()


def test_peek_AsKs_returnslist(ace):
    cl = cardlist.CardList([ace])
    assert cl.peek() == ['As']


def test_peek_AsKs_stillhidden():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Ks']))
    cl.peek()
    assert cl.cards[0].hidden is True
    assert cl.cards[1].hidden is True


def test_remove_existingcard_size0(ace):
    cl = cardlist.CardList([ace])
    cl.remove(ace)
    assert len(cl) == 0


def test_remove_cardnotinlist_returnsNone():
    cl = cardlist.CardList(tools.convert_to_cards(['Zs']))
    c = pc.PlayingCard('Z', 's')
    assert cl.remove(c) == None


def test_reveal_1card_cardIsUp(ace):
    cl = cardlist.CardList([ace])
    cl.reveal()
    assert cl.cards[0].hidden is False


def test_reveal_2cards_bothcardsUp():
    """ Unhide a 2 card hand, both cards are up """
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Ks']))
    cl.reveal()

    assert cl.cards[0].hidden is False
    assert cl.cards[1].hidden is False


def test_reveal_1card_faceup(ace):
    cl = cardlist.CardList([ace])
    cl.reveal()
    assert cl.cards[0].hidden is False


def test_sort_2cards_deuceisfirst():
    cl = cardlist.CardList(tools.convert_to_cards(['As', '2s']))
    cl.sort()
    assert cl.cards[0].rank == '2'


def test_sort_3cards_deuceisfirst():
    cl = cardlist.CardList(tools.convert_to_cards(['As', '2s', '7s']))
    cl.sort()
    assert cl.cards[0].rank == '2'


def test_stripranks_stripAces_containsNoAces(ace):
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Kc']))
    assert ace not in cl.strip_ranks(ranks=['A'])


def test_stripranks_stripAcesAndKings_containsNothing():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Kc']))
    assert cl.strip_ranks(ranks=['A', 'K']) == []


def test_stripsuits_stripSpades_containsNoSpades():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Kc']))
    cl.cards = cl.strip_suits('s')
    assert cl.count_suit(suit='s') == 0


def test_stripsuits_stripMultipleSuits_allSuitsWereStripped():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Kc', 'Qd']))
    cl.cards = cl.strip_suits(suits=['s', 'c'])
    assert cl.count_suit('s') == 0
    assert cl.count_suit('c') == 0
