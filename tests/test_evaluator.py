"""
  " Tests for evaluator.py
  """
import pytest
from ..src import playingcard as pc
from ..src import evaluator as ev
from . import tools


@pytest.fixture
def ace():
    return pc.PlayingCard('A', 's')


def test_chkstraightdraw_2card_0gap_275Q6K_returnsQK():
    qty, gap = 2, 0
    cards = tools.to_cards(['2c', '7s', '5h', 'Qd', '6s', 'Kh'])
    expected = tools.to_cards(['Qd', 'Kh'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_2card_0gap_2A5Q6_returns56():
    qty, gap = 2, 0
    cards = tools.to_cards(['2c', 'As', '5h', 'Qd', '6s'])
    expected = tools.to_cards(['5h', '6s'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_0gap_AK_raisesException():
    qty, gap = 3, 0
    cards = tools.to_cards(['As', 'Kc'])
    with pytest.raises(ValueError):
        ev.chk_straight_draw(cards, qty, gap)


def test_chkstraightdraw_3card_0gap_AKQ_returnsQKA():
    qty, gap = 3, 0
    cards = tools.to_cards(['As', 'Kc', 'Qd'])
    expected = tools.to_cards(['Qd', 'Kc', 'As'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_0gap_AK9_returnsNone():
    qty, gap = 3, 0
    cards = tools.to_cards(['As', 'Kc', '9d'])
    assert ev.chk_straight_draw(cards, qty, gap) is None


def test_chkstraightdraw_3card_0gap_AKQJ_returnsQKA():
    qty, gap = 3, 0
    cards = tools.to_cards(['As', 'Kc', 'Qd', 'Jd'])
    expected = tools.to_cards(['Qd', 'Kc', 'As'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_0gap_27J3KA_returns23A():
    qty, gap = 3, 0
    cards = tools.to_cards(['2d', '7h', 'Js', '3s', 'Ks', 'As'])
    expected = tools.to_cards(['2d', '3s', 'As'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_1gap_27T4KA_returns24A():
    qty, gap = 3, 1
    cards = tools.to_cards(['2d', '7h', 'Ts', '4s', 'Ks', 'As'])
    expected = tools.to_cards(['2d', '4s', 'As'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_1gap_JA5Q6_returnsJQA():
    qty, gap = 3, 1
    cards = tools.to_cards(['Jd', 'As', '5h', 'Qd', '6s'])
    expected = tools.to_cards(['Jd', 'Qd', 'As'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_1gap_JA596_returnsNone():
    qty, gap = 3, 1
    cards = tools.to_cards(['Jd', 'As', '5h', '9d', '6s'])
    assert ev.chk_straight_draw(cards, qty, gap) is None


def test_chkstraightdraw_4card_0gap_2J5Q6K_returnsNone():
    qty, gap = 4, 0
    cards = tools.to_cards(['2c', 'Js', '5h', 'Qd', '6s', 'Kh'])
    assert ev.chk_straight_draw(cards, qty, gap) is None


def test_chkstraightdraw_4card_0gap_A2234_returns234A():
    qty, gap = 4, 0
    cards = tools.to_cards(['Ah', '2h', '2c', '3d', '4h'])
    expected = tools.to_cards(['2h', '3d', '4h', 'Ah'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_4card_1gap_43674_returns3467():
    qty, gap = 4, 1
    cards = tools.to_cards(['4c', '3c', '6h', '7d', '4d'])
    expected = tools.to_cards(['3c', '4c', '6h', '7d'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_4card_1gap_34589A_returnsA345():
    qty, gap = 4, 1
    cards = tools.to_cards(['3h', '4s', '5d', '8h', '9d', 'Ad'])
    expected = tools.to_cards(['3h', '4s', '5d', 'Ad'])
    assert ev.chk_straight_draw(cards, qty, gap) == expected


def test_chkwheel_A_returnsTrue():
    cards = tools.to_cards(['As'])
    assert ev.chk_wheel(cards)


def test_chkwheel_A2_returnsTrue():
    cards = tools.to_cards(['As', '2c'])
    assert ev.chk_wheel(cards)


def test_chkwheel_A23_returnsTrue():
    cards = tools.to_cards(['As', '2c', '3d'])
    assert ev.chk_wheel(cards)


def test_chkwheel_A234_returnsTrue():
    cards = tools.to_cards(['As', '2c', '3d', '4d'])
    assert ev.chk_wheel(cards)


def test_chkwheel_A2345_returnsTrue():
    cards = tools.to_cards(['As', '2c', '3d', '4d', '5h'])
    ev.chk_wheel(cards)


def test_chkwheel_AA23_returnsFalse():
    cards = tools.to_cards(['As', 'Ah', '2c', '3d'])
    assert ev.chk_wheel(cards) is False


def test_chkwheel_A223_returnsFalse():
    cards = tools.to_cards(['As', '2h', '2c', '3d'])
    assert ev.chk_wheel(cards) is False


def test_chkwheel_AKQJ_returnsFalse():
    cards = tools.to_cards(['As', 'Kc', 'Qd', 'Jd'])
    assert ev.chk_wheel(cards) is False


def test_chkwheel_2345_returnsFalse():
    cards = tools.to_cards(['2c', '3d', '4d', '5h'])
    assert ev.chk_wheel(cards) is False


def test_dominantsuit_1card_returnssuit():
    cards = [pc.PlayingCard('A', 's')]
    assert ev.dominant_suit(cards) == 's'


def test_dominantsuit_2diffranks_returnshigherrank():
    cards = tools.to_cards(['As', 'Kc'])
    assert ev.dominant_suit(cards) == 's'


def test_dominantsuit_3diffranks_returnshigherrank():
    cards = tools.to_cards(['Kc', 'As', 'Qh'])
    assert ev.dominant_suit(cards) == 's'


def test_dominantsuit_4diffranks_returnshigherrank():
    cards = tools.to_cards(['Kc', 'As', 'Jd', 'Qh'])
    assert ev.dominant_suit(cards) == 's'


def test_dominantsuit_3cards2suitedSpades_returnsSpades():
    cards = tools.to_cards(['Kc', 'As', 'Qs'])
    assert ev.dominant_suit(cards) == 's'


def test_dominantsuit_HigherSpades_returnsSpades():
    cards = tools.to_cards(['Ac', 'Ks', 'As', 'Qc'])
    assert ev.dominant_suit(cards) == 's'


def test_isset_0cards_returnsFalse():
    assert ev.is_set([])


def test_isset_1card_returnsTrue(ace):
    assert ev.is_set([ace])


def test_isset_dupes_returnsFalse(ace):
    assert ev.is_set([ace, ace]) is False


def test_isstraight_lowstraight_returns5():
    hand = tools.make('straight_low')
    assert ev.is_straight(hand) == 5


def test_isstraight_midstraight_returnsPostiveNum():
    hand = tools.make('straight_mid')
    assert ev.is_straight(hand) > 0


def test_isstraight_highstraight_returnsA():
    hand = tools.make('straight_high')
    assert ev.is_straight(hand) == 14


def test_isstraight_nonstraight_returns0():
    hand = tools.make('wheeldraw')
    assert ev.is_straight(hand) == 0


def test_issuited_1card_returnsTrue(ace):
    assert ev.is_suited([ace])


def test_issuited_2suitedcards_returnsTrue():
    cl = tools.to_cards(['As', '2s'])
    assert ev.is_suited(cl)


def test_issuited_2unsuitedcard_returnsFalse():
    cl = tools.to_cards(['As', 'Ad'])
    assert ev.is_suited(cl) is False


def test_isvalidhand_4cards_returnsFalse():
    h = tools.get_cards(4)
    assert ev.is_validhand(h) is False


def test_isvalidhand_5cards_returnsTrue():
    h = tools.get_cards(5)
    assert ev.is_validhand(h)


def test_isvalidhand_6cards_returnsFalse():
    h = tools.get_cards(6)
    assert ev.is_validhand(h) is False


def test_isvalidhand_duplicateCards_returnsFalse():
    h = tools.make('dupes')
    assert ev.is_validhand(h) is False


def test_isvalidhand_royalflush_returnsTrue():
    h = tools.make('royalflush')
    assert ev.is_validhand(h)


def test_findbesthand_pair_returnsPAIR():
    cards = tools.to_cards(['2c', '3c', '5s', '7s', 'Kc', 'Ac', 'As'])
    besthand = ev.find_best_hand(cards)
    val = ev.get_value(besthand)
    assert ev.get_type(val) == 'PAIR'


def test_findbesthand_fullhouse_returnsFULLHOUSE():
    cards = tools.to_cards(['7c', '7s', 'Ks', 'Kc', 'Ah', 'Ac', 'As'])
    besthand = ev.find_best_hand(cards)
    val = ev.get_value(besthand)
    assert ev.get_type(val) == 'FULL HOUSE'


def test_findbesthand_straightflush_returnsSTRAIGHTFLUSH():
    cards = tools.to_cards(['4s', '5s', '6s', '7s', '8s', 'Ks', 'As'])
    besthand = ev.find_best_hand(cards)
    val = ev.get_value(besthand)
    assert ev.get_type(val) == 'STRAIGHT FLUSH'


def test_findbesthand_quads_returnsQUADS():
    cards = tools.to_cards(['Kc', 'Kd', 'Ks', 'Ac', 'Kd', 'Ah', 'As'])
    besthand = ev.find_best_hand(cards)
    val = ev.get_value(besthand)
    assert ev.get_type(val) == 'QUADS'


def test_findbesthand_straight_returnsSTRAIGHT():
    cards = tools.to_cards(['Ac', 'As', '2c', '3s', '4h', '5s', '5h'])
    besthand = ev.find_best_hand(cards)
    val = ev.get_value(besthand)
    assert ev.get_type(val) == 'STRAIGHT'


def test_findbesthand_flush_returnsFLUSH():
    cards = tools.to_cards(['8s', '9s', 'Tc', 'Js', 'Qs', 'Ks', 'Ac'])
    besthand = ev.find_best_hand(cards)
    val = ev.get_value(besthand)
    assert ev.get_type(val) == 'FLUSH'


def test_getallgaps_1card_returns0():
    cards = tools.to_cards(['Kc', 'As'])
    assert ev.get_allgaps(cards) == 0


def test_getallgaps_2connected_returns0():
    cards = tools.to_cards(['Kc', 'As'])
    assert ev.get_allgaps(cards) == 0


def test_getallgaps_2cards1gap_returns1():
    cards = tools.to_cards(['Qc', 'As'])
    assert ev.get_allgaps(cards) == 1


def test_getallgaps_3cards1gap_returns1():
    cards = tools.to_cards(['Tc', 'Js', 'Ks'])
    assert ev.get_allgaps(cards) == 1


def test_getgap_23_returns0():
    c1 = pc.PlayingCard('2', 's')
    c2 = pc.PlayingCard('3', 's')
    assert ev.get_gap(c1, c2) == 0


def test_getgap_32_returns0():
    c1 = pc.PlayingCard('2', 's')
    c2 = pc.PlayingCard('3', 's')
    assert ev.get_gap(c2, c1) == 0


def test_getgap_24_returns1():
    c1 = pc.PlayingCard('2', 's')
    c2 = pc.PlayingCard('4', 's')
    assert ev.get_gap(c2, c1) == 1


def test_getgap_2A_returns11():
    c1 = pc.PlayingCard('2', 's')
    c2 = pc.PlayingCard('A', 's')
    assert ev.get_gap(c1, c2) == 11


def test_getgap_22_returnsNeg1():
    c1 = pc.PlayingCard('2', 's')
    c2 = pc.PlayingCard('2', 'c')
    assert ev.get_gap(c1, c2) == -1


def test_gettype_negativevalue_returnsINVALID():
    assert ev.get_type(-1) == 'INVALID'


def test_gettype_1000000000000_raiseEx():
    with pytest.raises(ValueError):
        ev.get_type(1000000000000)


def test_rankdict_0K_counts0(ace):
    rankdict = ev.rank_dict([ace])
    # 0 is the default in case there are no Aces
    assert rankdict.get('K', 0) == 0


def test_rankdict_1Ace_counts1():
    cl = tools.to_cards(['As', '2s'])
    rankdict = ev.rank_dict(cl)
    assert rankdict.get('A') == 1


def test_rankdict_2Aces_counts2():
    cl = tools.to_cards(['As', 'Ah', 'Kc'])
    rankdict = ev.rank_dict(cl)
    assert rankdict.get('A') == 2


def test_ranklist_1Ace_lenEquals1(ace):
    ranklist = ev.rank_list([ace])
    assert len(ranklist) == 1


def test_ranklist_1Ace_1AceCounted(ace):
    ranklist = ev.rank_list([ace])
    print(ranklist)
    assert ranklist[0][0] == 1
    assert ranklist[0][1] == 'A'


def test_ranklist_2Aces_lenEquals1():
    cl = tools.to_cards(['Ah', 'As'])
    ranklist = ev.rank_list(cl)
    assert len(ranklist) == 1


def test_ranklist_2Aces_2AcesCounted():
    cl = tools.to_cards(['Ah', 'As'])
    ranklist = ev.rank_list(cl)
    assert ranklist[0][0] == 2
    assert ranklist[0][1] == 'A'


def test_ranklist_AK_lenEquals2():
    cl = tools.to_cards(['Kh', 'As'])
    ranklist = ev.rank_list(cl)
    assert len(ranklist) == 2


def test_removepairs_22_returns2():
    cl = tools.to_cards(['2c', '2d'])
    assert ev.remove_pairs(cl).pop().rank == '2'

    # assert cl.remove_pairs() == ['2c']


def test_removepairs_2345_returns2345():
    cards = tools.to_cards(['2c', '3d', '4d', '5h'])
    assert ev.remove_pairs(cards) == cards


def test_removepairs_A223_returns23A():
    # Keep the first 2
    cl = tools.to_cards(['As', '2h', '2c', '3d'])
    expected = tools.to_cards(['2h', '3d', 'As'])
    assert ev.remove_pairs(cl) == expected


def test_scoreranklist_A_return14():
    cards = [pc.PlayingCard('A', 's')]
    expected = 14 * ev.MULTIPLIERS[0]
    rd = ev.rank_list(cards)
    assert ev.score_ranklist(rd) == expected


def test_scorecardlist_A_returns14():
    cards = [pc.PlayingCard('A', 's')]
    assert ev.score_cardlist(cards) == 14


def test_scorecardlist_AK_returns1413():
    cards = tools.to_cards(['As', 'Ks'])
    assert ev.score_cardlist(cards) == 1413


def test_scorecardlist_AKQ_returns141312():
    cards = tools.to_cards(['As', 'Ks', 'Qs'])
    assert ev.score_cardlist(cards) == 141312


def test_scorepairhands_1Ace_returns1400000000():
    cards = [pc.PlayingCard('A', 's')]
    assert ev.score_pair_hands(cards) == 1400000000


def test_scorepairhands_2Aces_returns21400000000():
    cards = tools.to_cards(['As', 'Ah'])
    assert ev.score_pair_hands(cards) == 21400000000


def test_scorepairhands_3Aces_returns41400000000():
    cards = tools.to_cards(['As', 'Ah', 'Ac'])
    assert ev.score_pair_hands(cards) == 41400000000


def test_scorepairhands_4Aces_returns81400000000():
    cards = tools.to_cards(['As', 'Ah', 'Ac', 'Ad'])
    assert ev.score_pair_hands(cards) == 81400000000


def test_scorepairhands_AAKK_returns31413000000():
    cards = tools.to_cards(['As', 'Ah', 'Kc', 'Kd'])
    assert ev.score_pair_hands(cards) == 31413000000


def test_suitdict_0Spades_counts0():
    cl = tools.to_cards(['Kc', '2h'])
    suitdict = ev.suit_dict(cl)
    # 0 is the default in case there are no Aces
    assert suitdict.get('s', 0) == 0


def test_suitdict_0Spade_counts0():
    cl = tools.to_cards(['Kc', 'Ah'])
    suitdict = ev.suit_dict(cl)
    assert suitdict.get('s', 0) == 0


def test_suitdict_1Spade_counts1():
    cl = tools.to_cards(['Kc', 'As'])
    suitdict = ev.suit_dict(cl)
    assert suitdict.get('s') == 1


def test_suitdict_2Spade_counts2():
    cl = tools.to_cards(['Kc', '2s', 'As'])
    suitdict = ev.suit_dict(cl)
    assert suitdict.get('s') == 2


def test_suitedcarddict_0Spades_listlenEquals0():
    cl = tools.to_cards(['2h', 'Kc'])
    suitdict = ev.suitedcard_dict(cl)
    # Empty list is the default in case there are no Aces
    assert len(suitdict.get('s', [])) == 0


def test_suitedcarddict_1Spade_listlenEquals1():
    cl = tools.to_cards(['As', 'Kc'])
    suitdict = ev.suitedcard_dict(cl)
    # Empty list is the default in case there are no Aces
    assert len(suitdict.get('s', [])) == 1
