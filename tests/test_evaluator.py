"""
  " Tests for evaluator.py
  """
import pytest
from ponyup import card
from ponyup import evaluator
from ponyup import tools


def test_is_validhand_4cards_returnsFalse():
    h = tools.get_cards(4)
    assert evaluator.is_validhand(h) is False


def test_is_validhand_5cards_returnsTrue():
    h = tools.get_cards(5)
    assert evaluator.is_validhand(h)


def test_is_validhand_6cards_returnsFalse():
    h = tools.get_cards(6)
    assert evaluator.is_validhand(h) is False


def test_is_validhand_duplicateCards_returnsFalse():
    h = tools.make('dupes')
    assert evaluator.is_validhand(h) is False


def test_is_validhand_royalflush_returnsTrue():
    h = tools.make('royalflush')
    assert evaluator.is_validhand(h)


def test_dominantsuit_1card_returnssuit():
    cards = [card.Card('A', 's')]
    assert evaluator.dominant_suit(cards) == 's'


def test_dominantsuit_2diffranks_returnshigherrank():
    cards = tools.convert_to_cards(['As', 'Kc'])
    assert evaluator.dominant_suit(cards) == 's'


def test_dominantsuit_3diffranks_returnshigherrank():
    cards = tools.convert_to_cards(['Kc', 'As', 'Qh'])
    assert evaluator.dominant_suit(cards) == 's'


def test_dominantsuit_4diffranks_returnshigherrank():
    cards = tools.convert_to_cards(['Kc', 'As', 'Jd', 'Qh'])
    assert evaluator.dominant_suit(cards) == 's'


def test_dominantsuit_3cards2suitedSpades_returnsSpades():
    cards = tools.convert_to_cards(['Kc', 'As', 'Qs'])
    assert evaluator.dominant_suit(cards) == 's'


def test_dominantsuit_HigherSpades_returnsSpades():
    cards = tools.convert_to_cards(['Ac', 'Ks', 'As', 'Qc'])
    assert evaluator.dominant_suit(cards) == 's'


def test_issuited_1card_returnsTrue():
    cards = [card.Card('A', 's')]
    assert evaluator.is_suited(cards)


def test_issuited_2suitedcards_returnsTrue():
    cards = tools.convert_to_cards(['As', '2s'])
    assert evaluator.is_suited(cards)


def test_issuited_2unsuitedcard_returnsFalse():
    cards = tools.convert_to_cards(['As', 'Ad'])
    assert evaluator.is_suited(cards) is False


# Test a low straight hand
def test_isstraight_lowstraight_returns5():
    hand = tools.make('straight_low')
    assert evaluator.is_straight(hand) == 5


# Test a mid straight hand
def test_isstraight_midstraight_returnsPostiveNum():
    hand = tools.make('straight_mid')
    assert evaluator.is_straight(hand) > 0


# Test a high straight hand
def test_isstraight_highstraight_returnsA():
    hand = tools.make('straight_high')
    assert evaluator.is_straight(hand) == 14


# Test a non-straight hand
def test_isstraight_nonstraight_returns0():
    hand = tools.make('wheeldraw')
    assert evaluator.is_straight(hand) == 0


def test_scoreranklist_A_return14():
    cards = [card.Card('A', 's')]
    expected = 14 * evaluator.MULTIPLIERS[0]
    rd = evaluator.rank_list(cards)
    assert evaluator.score_ranklist(rd) == expected


def test_scorecardlist_A_returns14():
    cards = [card.Card('A', 's')]
    assert evaluator.score_cardlist(cards) == 14


def test_scorecardlist_AK_returns1413():
    cards = tools.convert_to_cards(['As', 'Ks'])
    assert evaluator.score_cardlist(cards) == 1413


def test_scorecardlist_AKQ_returns141312():
    cards = tools.convert_to_cards(['As', 'Ks', 'Qs'])
    assert evaluator.score_cardlist(cards) == 141312


def test_gettype_negativevalue_returnsINVALID():
    assert evaluator.get_type(-1) == 'INVALID'


def test_gettype_1000000000000_raiseEx():
    with pytest.raises(ValueError):
        evaluator.get_type(1000000000000)


# Test the value of 1 Ace
def test_scorepairhands_A_returns1400000000():
    cards = [card.Card('A', 's')]
    assert evaluator.score_pair_hands(cards) == 1400000000


# Test the value of 2 Aces
def test_scorepairhands_AA_returns21400000000():
    cards = tools.convert_to_cards(['As', 'Ah'])
    assert evaluator.score_pair_hands(cards) == 21400000000


# Test the value of 3 Aces
def test_scorepairhands_AAA_returns41400000000():
    cards = tools.convert_to_cards(['As', 'Ah', 'Ac'])
    assert evaluator.score_pair_hands(cards) == 41400000000


# Test the value of 4 Aces
def test_scorepairhands_AAAA_returns81400000000():
    cards = tools.convert_to_cards(['As', 'Ah', 'Ac', 'Ad'])
    assert evaluator.score_pair_hands(cards) == 81400000000


# Test the value of 2 pair: AAKK
def test_scorepairhands_AAKK_returns31413000000():
    cards = tools.convert_to_cards(['As', 'Ah', 'Kc', 'Kd'])
    assert evaluator.score_pair_hands(cards) == 31413000000


def test_findbesthand_pair_returnsPAIR():
    cards = tools.convert_to_cards(['2c', '3c', '5s', '7s', 'Kc', 'Ac', 'As'])
    besthand = evaluator.find_best_hand(cards)
    val = evaluator.get_value(besthand)
    assert evaluator.get_type(val) == 'PAIR'


def test_findbesthand_fullhouse_returnsFULLHOUSE():
    cards = tools.convert_to_cards(['7c', '7s', 'Ks', 'Kc', 'Ah', 'Ac', 'As'])
    besthand = evaluator.find_best_hand(cards)
    val = evaluator.get_value(besthand)
    assert evaluator.get_type(val) == 'FULL HOUSE'


def test_findbesthand_straightflush_returnsSTRAIGHTFLUSH():
    cards = tools.convert_to_cards(['4s', '5s', '6s', '7s', '8s', 'Ks', 'As'])
    besthand = evaluator.find_best_hand(cards)
    val = evaluator.get_value(besthand)
    assert evaluator.get_type(val) == 'STRAIGHT FLUSH'


def test_findbesthand_quads_returnsQUADS():
    cards = tools.convert_to_cards(['Kc', 'Kd', 'Ks', 'Ac', 'Kd', 'Ah', 'As'])
    besthand = evaluator.find_best_hand(cards)
    val = evaluator.get_value(besthand)
    assert evaluator.get_type(val) == 'QUADS'


def test_findbesthand_straight_returnsSTRAIGHT():
    cards = tools.convert_to_cards(['Ac', 'As', '2c', '3s', '4h', '5s', '5h'])
    besthand = evaluator.find_best_hand(cards)
    val = evaluator.get_value(besthand)
    assert evaluator.get_type(val) == 'STRAIGHT'


def test_findbesthand_flush_returnsFLUSH():
    cards = tools.convert_to_cards(['8s', '9s', 'Tc', 'Js', 'Qs', 'Ks', 'Ac'])
    besthand = evaluator.find_best_hand(cards)
    val = evaluator.get_value(besthand)
    assert evaluator.get_type(val) == 'FLUSH'


def test_is_set_royalflush_returnsTrue():
    h = tools.make('royalflush')
    assert evaluator.is_set(h)


def test_is_set_handwithdupes_returnsFalse():
    h = tools.make('dupes')
    assert evaluator.is_set(h) is False


def test_is_set_1card_returnsTrue():
    h = [card.Card('A', 's')]
    assert evaluator.is_set(h)


def test_is_set_2As_returnsFalse():
    c = card.Card('A', 's')
    h = [c, c]
    assert evaluator.is_set(h) is False


def test_rankdict_0Ace_counts0():
    cards = tools.convert_to_cards(['Kc', '2s'])
    rankdict = evaluator.rank_dict(cards)
    # 0 is the default in case there are no Aces
    assert rankdict.get('A', 0) == 0


def test_rankdict_1Ace_counts1():
    cards = tools.convert_to_cards(['Kc', 'As'])
    rankdict = evaluator.rank_dict(cards)
    assert rankdict.get('A') == 1


def test_rankdict_2Aces_counts2():
    cards = tools.convert_to_cards(['Ah', 'Kc', 'As'])
    rankdict = evaluator.rank_dict(cards)
    assert rankdict.get('A') == 2


def test_ranklist_1Ace_lenEquals1():
    cards = [card.Card('A', 's')]
    ranklist = evaluator.rank_list(cards)
    assert len(ranklist) == 1


def test_ranklist_1Ace_1AceCounted():
    cards = [card.Card('A', 's')]
    ranklist = evaluator.rank_list(cards)
    assert ranklist[0][0] == 1
    assert ranklist[0][1] == 'A'


def test_ranklist_2Aces_lenEquals1():
    cards = tools.convert_to_cards(['As', 'Ah'])
    ranklist = evaluator.rank_list(cards)
    assert len(ranklist) == 1


def test_ranklist_2Aces_2AcesCounted():
    cards = tools.convert_to_cards(['As', 'Ah'])
    ranklist = evaluator.rank_list(cards)
    assert ranklist[0][0] == 2
    assert ranklist[0][1] == 'A'


def test_ranklist_AK_lenEquals2():
    cards = tools.convert_to_cards(['As', 'Kh'])
    ranklist = evaluator.rank_list(cards)
    assert len(ranklist) == 2


def test_suitdict_0Spades_counts0():
    cards = tools.convert_to_cards(['Kc', '2h'])
    suitdict = evaluator.suit_dict(cards)
    # 0 is the default in case there are no Aces
    assert suitdict.get('s', 0) == 0


def test_suitdict_0Spade_counts0():
    cards = tools.convert_to_cards(['Kc', 'Ah'])
    suitdict = evaluator.suit_dict(cards)
    assert suitdict.get('s', 0) == 0


def test_suitdict_1Spade_counts1():
    cards = tools.convert_to_cards(['Kc', 'As'])
    suitdict = evaluator.suit_dict(cards)
    assert suitdict.get('s') == 1


def test_suitdict_2Spade_counts2():
    cards = tools.convert_to_cards(['Kc', '2s', 'As'])
    suitdict = evaluator.suit_dict(cards)
    assert suitdict.get('s') == 2


def test_suitedcarddict_0Spades_listlenEquals0():
    cards = tools.convert_to_cards(['Kc', '2h'])
    suitdict = evaluator.suitedcard_dict(cards)
    # Empty list is the default in case there are no Aces
    assert len(suitdict.get('s', [])) == 0


def test_suitedcarddict_1Spade_listlenEquals1():
    cards = tools.convert_to_cards(['Kc', 'As'])
    suitdict = evaluator.suitedcard_dict(cards)
    # Empty list is the default in case there are no Aces
    assert len(suitdict.get('s', [])) == 1


def test_countsuit_nospade_returns0():
    cards = [card.Card('K', 'c')]
    assert evaluator.count_suit(cards, 's') == 0


def test_countsuit_1spade_returns1():
    cards = tools.convert_to_cards(['Kc', 'As'])
    assert evaluator.count_suit(cards, 's') == 1


def test_getgap_23_returns0():
    c1 = card.Card('2', 's')
    c2 = card.Card('3', 's')
    assert evaluator.get_gap(c1, c2) == 0


def test_getgap_32_returns0():
    c1 = card.Card('2', 's')
    c2 = card.Card('3', 's')
    assert evaluator.get_gap(c2, c1) == 0


def test_getgap_24_returns1():
    c1 = card.Card('2', 's')
    c2 = card.Card('4', 's')
    assert evaluator.get_gap(c2, c1) == 1


def test_getgap_2A_returns11():
    c1 = card.Card('2', 's')
    c2 = card.Card('A', 's')
    assert evaluator.get_gap(c1, c2) == 11


def test_getgap_22_returnsNeg1():
    c1 = card.Card('2', 's')
    c2 = card.Card('2', 'c')
    assert evaluator.get_gap(c1, c2) == -1


def test_getallgaps_1card_returns0():
    cards = tools.convert_to_cards(['Kc', 'As'])
    assert evaluator.get_allgaps(cards) == 0


def test_getallgaps_2connected_returns0():
    cards = tools.convert_to_cards(['Kc', 'As'])
    assert evaluator.get_allgaps(cards) == 0


def test_getallgaps_2cards1gap_returns1():
    cards = tools.convert_to_cards(['Qc', 'As'])
    assert evaluator.get_allgaps(cards) == 1


def test_getallgaps_3cards1gap_returns1():
    cards = tools.convert_to_cards(['Tc', 'Js', 'Ks'])
    assert evaluator.get_allgaps(cards) == 1


def test_stripranks_stripAces_containsNoAces():
    ace = card.Card('A', 's')
    king = card.Card('K', 'c')
    cards = [ace, king]
    assert ace not in evaluator.strip_ranks(cards, ['A'])


def test_stripranks_stripAcesAndKings_containsNothing():
    cards = tools.convert_to_cards(['As', 'Kc'])
    assert evaluator.strip_ranks(cards, ['A', 'K']) == []


def test_stripsuits_stripSpades_containsNoSpades():
    cards = tools.convert_to_cards(['As', 'Kc'])
    cards = evaluator.strip_suits(cards, 's')
    assert evaluator.count_suit(cards, 's') == 0


def test_stripsuits_stripMultipleSuits_allSuitsWereStripped():
    cards = tools.convert_to_cards(['As', 'Kc', 'Qd'])
    cards = evaluator.strip_suits(cards, ['s', 'c'])
    assert evaluator.count_suit(cards, 's') == 0
    assert evaluator.count_suit(cards, 'c') == 0


def test_chkwheel_A_returnsTrue():
    cards = tools.convert_to_cards(['As'])
    assert evaluator.chk_wheel(cards)


def test_chkwheel_A2_returnsTrue():
    cards = tools.convert_to_cards(['As', '2c'])
    assert evaluator.chk_wheel(cards)


def test_chkwheel_A23_returnsTrue():
    cards = tools.convert_to_cards(['As', '2c', '3d'])
    assert evaluator.chk_wheel(cards)


def test_chkwheel_A234_returnsTrue():
    cards = tools.convert_to_cards(['As', '2c', '3d', '4d'])
    assert evaluator.chk_wheel(cards)


def test_chkwheel_A2345_returnsTrue():
    cards = tools.convert_to_cards(['As', '2c', '3d', '4d', '5h'])
    evaluator.chk_wheel(cards)


def test_chkwheel_AA23_returnsFalse():
    cards = tools.convert_to_cards(['As', 'Ah', '2c', '3d'])
    assert evaluator.chk_wheel(cards) is False


def test_chkwheel_A223_returnsFalse():
    cards = tools.convert_to_cards(['As', '2h', '2c', '3d'])
    assert evaluator.chk_wheel(cards) is False


def test_chkwheel_AKQJ_returnsFalse():
    cards = tools.convert_to_cards(['As', 'Kc', 'Qd', 'Jd'])
    assert evaluator.chk_wheel(cards) is False


def test_chkwheel_2345_returnsFalse():
    cards = tools.convert_to_cards(['2c', '3d', '4d', '5h'])
    assert evaluator.chk_wheel(cards) is False


def test_chkstraightdraw_2card_0gap_275Q6K_returnsQK():
    qty, gap = 2, 0
    cards = tools.convert_to_cards(['2c', '7s', '5h', 'Qd', '6s', 'Kh'])
    expected = tools.convert_to_cards(['Qd', 'Kh'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_2card_0gap_2A5Q6_returns56():
    qty, gap = 2, 0
    cards = tools.convert_to_cards(['2c', 'As', '5h', 'Qd', '6s'])
    expected = tools.convert_to_cards(['5h', '6s'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_0gap_AK_raisesException():
    qty, gap = 3, 0
    cards = tools.convert_to_cards(['As', 'Kc'])
    with pytest.reaises(ValueError):
        evaluator.chk_straight_draw(cards, qty, gap)


def test_chkstraightdraw_3card_0gap_AKQ_returnsQKA():
    qty, gap = 3, 0
    cards = tools.convert_to_cards(['As', 'Kc', 'Qd'])
    expected = tools.convert_to_cards(['Qd', 'Kc', 'As'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_0gap_AK9_returnsNone():
    qty, gap = 3, 0
    cards = tools.convert_to_cards(['As', 'Kc', '9d'])
    assert evaluator.chk_straight_draw(cards, qty, gap) is None


def test_chkstraightdraw_3card_0gap_AKQJ_returnsQKA():
    qty, gap = 3, 0
    cards = tools.convert_to_cards(['As', 'Kc', 'Qd', 'Jd'])
    expected = tools.convert_to_cards(['Qd', 'Kc', 'As'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


# 3 card wheel draw
def test_chkstraightdraw_3card_0gap_27J3KA_returns23A():
    qty, gap = 3, 0
    cards = tools.convert_to_cards(['2d', '7h', 'Js', '3s', 'Ks', 'As'])
    expected = tools.convert_to_cards(['2d', '3s', 'As'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_1gap_27T4KA_returns24A():
    qty, gap = 3, 1
    cards = tools.convert_to_cards(['2d', '7h', 'Ts', '4s', 'Ks', 'As'])
    expected = tools.convert_to_cards(['2d', '4s', 'As'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_1gap_JA5Q6_returnsJQA():
    qty, gap = 3, 1
    cards = tools.convert_to_cards(['Jd', 'As', '5h', 'Qd', '6s'])
    expected = tools.convert_to_cards(['Jd', 'Qd', 'As'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_3card_1gap_JA596_returnsNone():
    qty, gap = 3, 1
    cards = tools.convert_to_cards(['Jd', 'As', '5h', '9d', '6s'])
    assert evaluator.chk_straight_draw(cards, qty, gap) is None


def test_chkstraightdraw_4card_0gap_2J5Q6K_returnsNone():
    qty, gap = 4, 0
    cards = tools.convert_to_cards(['2c', 'Js', '5h', 'Qd', '6s', 'Kh'])
    assert evaluator.chk_straight_draw(cards, qty, gap) is None


def test_chkstraightdraw_4card_0gap_A2234_returns234A():
    qty, gap = 4, 0
    cards = tools.convert_to_cards(['Ah', '2h', '2c', '3d', '4h'])
    expected = tools.convert_to_cards(['2h', '3d', '4h', 'Ah'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_4card_1gap_43674_returns3467():
    qty, gap = 4, 1
    cards = tools.convert_to_cards(['4c', '3c', '6h', '7d', '4d'])
    expected = tools.convert_to_cards(['3c', '4c', '6h', '7d'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_chkstraightdraw_4card_1gap_34589A_returnsA345():
    qty, gap = 4, 1
    cards = tools.convert_to_cards(['3h', '4s', '5d', '8h', '9d', 'Ad'])
    expected = tools.convert_to_cards(['3h', '4s', '5d', 'Ad'])
    assert evaluator.chk_straight_draw(cards, qty, gap) == expected


def test_removepairs_22_returns2():
    cards = tools.convert_to_cards(['2c', '2d'])
    expected = [card.Card('2', 'c')]
    assert evaluator.remove_pairs(cards) == expected


def test_removepairs_2345_returns2345():
    cards = tools.convert_to_cards(['2c', '3d', '4d', '5h'])
    assert evaluator.remove_pairs(cards) == cards


def test_removepairs_A223_returns23A():
    # Keep the first 2
    cards = tools.convert_to_cards(['As', '2h', '2c', '3d'])
    expected = tools.convert_to_cards(['2h', '3d', 'As'])
    assert evaluator.remove_pairs(cards) == expected
