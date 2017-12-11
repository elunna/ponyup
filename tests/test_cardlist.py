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
    cl.toggle_hidden(False)
    assert str(cl) == 'As'


def test_contains_AceSpadesinStandardDeck_returnsTrue(ace):
    cl = cardlist.CardList([ace])
    assert ace in cl.cards


def test_contains_JokerinStandardDeck_returnsFalse():
    cl = cardlist.CardList()
    c = pc.Joker()
    assert c not in cl.cards


def test_isempty_hasacard_returnFalse(ace):
    cl = cardlist.CardList([ace])
    assert cl.is_empty() is False


def test_isempty_emptydeck_returnTrue():
    cl = cardlist.CardList()
    assert cl.is_empty()


def test_remove_existingcard_size0(ace):
    cl = cardlist.CardList([ace])
    cl.remove(ace)
    assert len(cl) == 0


def test_remove_cardnotindeck_returnsNone():
    cl = cardlist.CardList(tools.convert_to_cards(['Zs']))
    c = pc.PlayingCard('Z', 's')
    assert cl.remove(c) == None


def test_togglehidden_1card_hidden(ace):
    cl = cardlist.CardList([ace])
    cl.toggle_hidden(False)
    assert cl.cards[0].hidden is False


def test_togglehidden_1card_nothidden(ace):
    cl = cardlist.CardList([ace])
    cl.toggle_hidden(True)
    assert cl.cards[0].hidden


def test_sort_2cards_deuceisfirst():
    cl = cardlist.CardList(tools.convert_to_cards(['As', '2s']))
    cl.sort()
    assert cl.cards[0].rank == '2'


def test_sort_3cards_deuceisfirst():
    cl = cardlist.CardList(tools.convert_to_cards(['As', '2s', '7s']))
    cl.sort()
    assert cl.cards[0].rank == '2'


def test_isset_0cards_returnsFalse():
    cl = cardlist.CardList()
    assert cl.is_set()


def test_isset_1card_returnsTrue(ace):
    cl = cardlist.CardList([ace])
    assert cl.is_set()


def test_isset_dupes_returnsFalse(ace):
    cl = cardlist.CardList([ace, ace])
    assert cl.is_set() is False


def test_is_set_two_As_returnsFalse():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'As']))
    assert cl.is_set() is False


def test_rankdict_0K_counts0(ace):
    cl = cardlist.CardList([ace])
    rankdict = cl.rank_dict()
    # 0 is the default in case there are no Aces
    assert rankdict.get('K', 0) == 0


def test_rankdict_1Ace_counts1():
    cl = cardlist.CardList(tools.convert_to_cards(['As', '2s']))
    rankdict = cl.rank_dict()
    assert rankdict.get('A') == 1


def test_rankdict_2Aces_counts2():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Ah', 'Kc']))
    rankdict = cl.rank_dict()
    assert rankdict.get('A') == 2


def test_ranklist_1Ace_lenEquals1(ace):
    cl = cardlist.CardList([ace])
    ranklist = cl.rank_list()
    assert len(ranklist) == 1


def test_ranklist_1Ace_1AceCounted(ace):
    cl = cardlist.CardList([ace])
    ranklist = cl.rank_list()
    print(ranklist)
    assert ranklist[0][0] == 1
    assert ranklist[0][1] == 'A'


def test_ranklist_2Aces_lenEquals1():
    cl = cardlist.CardList(tools.convert_to_cards(['Ah', 'As']))
    ranklist = cl.rank_list()
    assert len(ranklist) == 1


def test_ranklist_2Aces_2AcesCounted():
    cl = cardlist.CardList(tools.convert_to_cards(['Ah', 'As']))
    ranklist = cl.rank_list()
    assert ranklist[0][0] == 2
    assert ranklist[0][1] == 'A'


def test_ranklist_AK_lenEquals2():
    cl = cardlist.CardList(tools.convert_to_cards(['Kh', 'As']))
    ranklist = cl.rank_list()
    assert len(ranklist) == 2


def test_suitdict_0Spades_counts0():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc', '2h']))
    suitdict = cl.suit_dict()
    # 0 is the default in case there are no Aces
    assert suitdict.get('s', 0) == 0


def test_suitdict_0Spade_counts0():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc', 'Ah']))
    suitdict = cl.suit_dict()
    assert suitdict.get('s', 0) == 0


def test_suitdict_1Spade_counts1():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc', 'As']))
    suitdict = cl.suit_dict()
    assert suitdict.get('s') == 1


def test_suitdict_2Spade_counts2():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc', '2s', 'As']))
    suitdict = cl.suit_dict()
    assert suitdict.get('s') == 2


def test_countsuit_nospade_returns0():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc']))
    assert cl.count_suit('s') == 0


def test_countsuit_1spade_returns1():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc', 'As']))
    assert cl.count_suit('s') == 1


def test_countrank_1K_returns1():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc']))
    assert cl.count_rank('K') == 1


def test_countrank_0A_returns():
    cl = cardlist.CardList(tools.convert_to_cards(['Kc']))
    assert cl.count_rank('A') == 0


def test_countrank_1Kin2cards_returns1():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Kc']))
    assert cl.count_rank('K') == 1


def test_suitedcarddict_0Spades_listlenEquals0():
    cl = cardlist.CardList(tools.convert_to_cards(['2h', 'Kc']))
    suitdict = cl.suitedcard_dict()
    # Empty list is the default in case there are no Aces
    assert len(suitdict.get('s', [])) == 0


def test_suitedcarddict_1Spade_listlenEquals1():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Kc']))
    suitdict = cl.suitedcard_dict()
    # Empty list is the default in case there are no Aces
    assert len(suitdict.get('s', [])) == 1


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


def test_removepairs_22_returns2():
    cl = cardlist.CardList(tools.convert_to_cards(['2c', '2d']))
    assert cl.remove_pairs().pop().rank == '2'

    # assert cl.remove_pairs() == ['2c']


def test_removepairs_2345_returns2345():
    cards = tools.convert_to_cards(['2c', '3d', '4d', '5h'])
    cl = cardlist.CardList(cards)
    assert cl.remove_pairs() == cards


def test_removepairs_A223_returns23A():
    # Keep the first 2
    cl = cardlist.CardList(tools.convert_to_cards(['As', '2h', '2c', '3d']))
    expected = tools.convert_to_cards(['2h', '3d', 'As'])
    assert cl.remove_pairs() == expected


def test_issuited_1card_returnsTrue(ace):
    cl = cardlist.CardList([ace])
    assert cl.is_suited()


def test_issuited_2suitedcards_returnsTrue():
    cl = cardlist.CardList(tools.convert_to_cards(['As', '2s']))
    assert cl.is_suited()


def test_issuited_2unsuitedcard_returnsFalse():
    cl = cardlist.CardList(tools.convert_to_cards(['As', 'Ad']))
    assert cl.is_suited() is False
