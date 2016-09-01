import unittest
import card
import evaluator
import pokerhands
import testtools


class TestEvaluator(unittest.TestCase):
    """
    Tests for is_valid_hand(cards)
    """
    def test_is_validhand_4cards_returnsFalse(self):
        h = testtools.get_cards(4)
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_5cards_returnsTrue(self):
        h = testtools.get_cards(5)
        expected = True
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_6cards_returnsFalse(self):
        h = testtools.get_cards(6)
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_duplicateCards_returnsFalse(self):
        h = pokerhands.make('dupes')
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_royalflush_returnsTrue(self):
        h = pokerhands.make('royalflush')
        expected = True
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    """
    Tests for dominant_suit(cards)
    """
    def test_dominantsuit_1card_returnssuit(self):
        cards = [card.Card('A', 's')]
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_2diffranks_returnshigherrank(self):
        cards = pokerhands.convert_to_cards(['As', 'Kc'])
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_3diffranks_returnshigherrank(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As', 'Qh'])
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_4diffranks_returnshigherrank(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As', 'Jd', 'Qh'])
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_3cards2suitedSpades_returnsSpades(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As', 'Qs'])
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_HigherSpades_returnsSpades(self):
        cards = pokerhands.convert_to_cards(['Ac', 'Ks', 'As', 'Qc'])
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    """
    Tests for is_suited(cards)
    """
    def test_issuited_1card_returnsTrue(self):
        cards = [card.Card('A', 's')]
        expected = True
        result = evaluator.is_suited(cards)
        self.assertEqual(expected, result)

    def test_issuited_2suitedcards_returnsTrue(self):
        cards = pokerhands.convert_to_cards(['As', '2s'])
        expected = True
        result = evaluator.is_suited(cards)
        self.assertEqual(expected, result)

    def test_issuited_2unsuitedcard_returnsFalse(self):
        cards = pokerhands.convert_to_cards(['As', 'Ad'])
        expected = False
        result = evaluator.is_suited(cards)
        self.assertEqual(expected, result)

    """
    Tests for is_straight(cards)
    """
    # Test a low straight hand
    def test_isstraight_lowstraight_returns5(self):
        hand = pokerhands.make('straight_low')
        expected = 5
        result = evaluator.is_straight(hand)
        self.assertEqual(expected, result)

    # Test a mid straight hand
    def test_isstraight_midstraight_returnsPostiveNum(self):
        hand = pokerhands.make('straight_mid')
        expected = True
        result = evaluator.is_straight(hand) > 0
        self.assertEqual(expected, result)

    # Test a high straight hand
    def test_isstraight_highstraight_returnsA(self):
        hand = pokerhands.make('straight_high')
        expected = 14
        result = evaluator.is_straight(hand)
        self.assertEqual(expected, result)

    # Test a non-straight hand
    def test_isstraight_nonstraight_returns0(self):
        hand = pokerhands.make('wheeldraw')
        expected = 0
        result = evaluator.is_straight(hand)
        self.assertEqual(expected, result)

    """
    Tests for score_ranklist(ranklist)
    """
    def test_scoreranklist_A_return14(self):
        cards = [card.Card('A', 's')]
        expected = 14 * evaluator.MULTIPLIERS[0]
        rd = evaluator.rank_list(cards)
        result = evaluator.score_ranklist(rd)
        self.assertEqual(expected, result)

    """
    Tests for score_cardlist(cards)
    """
    def test_scorecardlist_A_returns14(self):
        cards = [card.Card('A', 's')]
        expected = 14
        result = evaluator.score_cardlist(cards)
        self.assertEqual(expected, result)

    def test_scorecardlist_AK_returns1413(self):
        cards = pokerhands.convert_to_cards(['As', 'Ks'])
        expected = 1413
        result = evaluator.score_cardlist(cards)
        self.assertEqual(expected, result)

    def test_scorecardlist_AKQ_returns141312(self):
        cards = pokerhands.convert_to_cards(['As', 'Ks', 'Qs'])
        expected = 141312
        result = evaluator.score_cardlist(cards)
        self.assertEqual(expected, result)

    """
    Tests for get_type(cards)
    """

    def test_gettype_negativevalue_returnsINVALID(self):
        expected = 'INVALID'
        result = evaluator.get_type(-1)
        self.assertEqual(expected, result)

    def test_gettype_1000000000000_raiseEx(self):
        self.assertRaises(ValueError, evaluator.get_type, 1000000000000)

    """
    Tests for score_pair_hands(ranklist)
    """

    # Test the value of 1 Ace
    def test_scorepairhands_A_returns1400000000(self):
        cards = [card.Card('A', 's')]
        expected = 1400000000
        result = evaluator.score_pair_hands(cards)
        self.assertEqual(expected, result)

    # Test the value of 2 Aces
    def test_scorepairhands_AA_returns21400000000(self):
        cards = pokerhands.convert_to_cards(['As', 'Ah'])
        expected = 21400000000
        result = evaluator.score_pair_hands(cards)
        self.assertEqual(expected, result)

    # Test the value of 3 Aces
    def test_scorepairhands_AAA_returns41400000000(self):
        cards = pokerhands.convert_to_cards(['As', 'Ah', 'Ac'])
        expected = 41400000000
        result = evaluator.score_pair_hands(cards)
        self.assertEqual(expected, result)

    # Test the value of 4 Aces
    def test_scorepairhands_AAAA_returns81400000000(self):
        cards = pokerhands.convert_to_cards(['As', 'Ah', 'Ac', 'Ad'])
        expected = 81400000000
        result = evaluator.score_pair_hands(cards)
        self.assertEqual(expected, result)

    # Test the value of 2 pair: AAKK
    def test_scorepairhands_AAKK_returns31413000000(self):
        cards = pokerhands.convert_to_cards(['As', 'Ah', 'Kc', 'Kd'])
        expected = 31413000000
        result = evaluator.score_pair_hands(cards)
        self.assertEqual(expected, result)

    """
    Tests for get_description(value, cards)
    """
    # See test_pokerhands.py for extensive tests of get_description.

    """
    Tests for find_best_hand(cards)
    """
    def test_findbesthand_pair_returnsPAIR(self):
        cards = pokerhands.convert_to_cards(['2c', '3c', '5s', '7s', 'Kc', 'Ac', 'As'])
        besthand = evaluator.find_best_hand(cards)
        expected = 'PAIR'
        result = besthand.rank()
        self.assertEqual(expected, result)

    def test_findbesthand_fullhouse_returnsFULLHOUSE(self):
        cards = pokerhands.convert_to_cards(['7c', '7s', 'Ks', 'Kc', 'Ah', 'Ac', 'As'])
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'FULL HOUSE'
        self.assertEqual(expected, result)

    def test_findbesthand_straightflush_returnsSTRAIGHTFLUSH(self):
        cards = pokerhands.convert_to_cards(['4s', '5s', '6s', '7s', '8s', 'Ks', 'As'])
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'STRAIGHT FLUSH'
        self.assertEqual(expected, result)

    def test_findbesthand_quads_returnsQUADS(self):
        cards = pokerhands.convert_to_cards(['Kc', 'Kd', 'Ks', 'Ac', 'Kd', 'Ah', 'As'])
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'QUADS'
        self.assertEqual(expected, result)

    def test_findbesthand_straight_returnsSTRAIGHT(self):
        cards = pokerhands.convert_to_cards(['Ac', 'As', '2c', '3s', '4h', '5s', '5h'])
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'STRAIGHT'
        self.assertEqual(expected, result)

    def test_findbesthand_flush_returnsFLUSH(self):
        cards = pokerhands.convert_to_cards(['8s', '9s', 'Tc', 'Js', 'Qs', 'Ks', 'Ac'])
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'FLUSH'
        self.assertEqual(expected, result)

    """
    Tests for is_set(cards)
    """
    def test_is_set_royalflush_returnsTrue(self):
        h = pokerhands.make('royalflush')
        expected = True
        result = evaluator.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_handwithdupes_returnsFalse(self):
        h = pokerhands.make('dupes')
        expected = False
        result = evaluator.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_1card_returnsTrue(self):
        h = [card.Card('A', 's')]
        expected = True
        result = evaluator.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_2As_returnsFalse(self):
        c = card.Card('A', 's')
        h = [c, c]
        expected = False
        result = evaluator.is_set(h)
        self.assertEqual(expected, result)

    """
    Tests for rank_dict(cards)
    """
    def test_rankdict_0Ace_counts0(self):
        cards = pokerhands.convert_to_cards(['Kc', '2s'])
        expected = 0
        rankdict = evaluator.rank_dict(cards)
        # 0 is the default in case there are no Aces
        result = rankdict.get('A', 0)
        self.assertEqual(expected, result)

    def test_rankdict_1Ace_counts1(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As'])
        expected = 1
        rankdict = evaluator.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    def test_rankdict_2Aces_counts2(self):
        cards = pokerhands.convert_to_cards(['Ah', 'Kc', 'As'])
        expected = 2
        rankdict = evaluator.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    """
    Tests for rank_list(cards)
    """
    def test_ranklist_1Ace_lenEquals1(self):
        cards = [card.Card('A', 's')]
        expected = 1
        ranklist = evaluator.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    def test_ranklist_1Ace_1AceCounted(self):
        cards = [card.Card('A', 's')]
        ranklist = evaluator.rank_list(cards)
        expected_qty = ranklist[0][0]
        expected_rank = ranklist[0][1]
        self.assertTrue(
            expected_qty == 1, expected_rank == 'A')

    def test_ranklist_2Aces_lenEquals1(self):
        cards = pokerhands.convert_to_cards(['As', 'Ah'])
        expected = 1
        ranklist = evaluator.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    def test_ranklist_2Aces_2AcesCounted(self):
        cards = pokerhands.convert_to_cards(['As', 'Ah'])
        ranklist = evaluator.rank_list(cards)
        expected_qty = ranklist[0][0]
        expected_rank = ranklist[0][1]
        self.assertTrue(
            expected_qty == 2, expected_rank == 'A')

    def test_ranklist_AK_lenEquals2(self):
        cards = pokerhands.convert_to_cards(['As', 'Kh'])
        expected = 2
        ranklist = evaluator.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    """
    Tests for suit_dict(cards)
    """
    def test_suitdict_0Spades_counts0(self):
        cards = pokerhands.convert_to_cards(['Kc', '2h'])
        expected = 0
        suitdict = evaluator.suit_dict(cards)
        # 0 is the default in case there are no Aces
        result = suitdict.get('s', 0)
        self.assertEqual(expected, result)

    def test_suitdict_0Spade_counts0(self):
        cards = pokerhands.convert_to_cards(['Kc', 'Ah'])
        expected = 0
        suitdict = evaluator.suit_dict(cards)
        result = suitdict.get('s', 0)
        self.assertEqual(expected, result)

    def test_suitdict_1Spade_counts1(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As'])
        expected = 1
        suitdict = evaluator.suit_dict(cards)
        result = suitdict.get('s')
        self.assertEqual(expected, result)

    def test_suitdict_2Spade_counts2(self):
        cards = pokerhands.convert_to_cards(['Kc', '2s', 'As'])
        expected = 2
        suitdict = evaluator.suit_dict(cards)
        result = suitdict.get('s')
        self.assertEqual(expected, result)

    """
    Tests for suitedcard_dict(cards)
    """
    def test_suitedcarddict_0Spades_listlenEquals0(self):
        cards = pokerhands.convert_to_cards(['Kc', '2h'])
        expected = 0
        suitdict = evaluator.suitedcard_dict(cards)
        # Empty list is the default in case there are no Aces
        result = len(suitdict.get('s', []))
        self.assertEqual(expected, result)

    def test_suitedcarddict_1Spade_listlenEquals1(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As'])
        expected = 1
        suitdict = evaluator.suitedcard_dict(cards)
        # Empty list is the default in case there are no Aces
        result = len(suitdict.get('s', []))
        self.assertEqual(expected, result)

    """
    Tests for count_suit(cards, suit)
    """
    def test_countsuit_nospade_returns0(self):
        cards = [card.Card('K', 'c')]
        expected = 0
        result = evaluator.count_suit(cards, 's')
        self.assertEqual(expected, result)

    def test_countsuit_1spade_returns1(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As'])
        expected = 1
        result = evaluator.count_suit(cards, 's')
        self.assertEqual(expected, result)

    """
    Tests for get_gap(card1, card2)
    """
    def test_getgap_23_returns0(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('3', 's')
        expected = 0
        result = evaluator.get_gap(c1, c2)
        self.assertEqual(expected, result)

    def test_getgap_32_returns0(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('3', 's')
        expected = 0
        result = evaluator.get_gap(c2, c1)
        self.assertEqual(expected, result)

    def test_getgap_24_returns1(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('4', 's')
        expected = 1
        result = evaluator.get_gap(c2, c1)
        self.assertEqual(expected, result)

    def test_getgap_2A_returns11(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('A', 's')
        expected = 11
        result = evaluator.get_gap(c1, c2)
        self.assertEqual(expected, result)

    def test_getgap_22_returnsNeg1(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('2', 'c')
        expected = -1
        result = evaluator.get_gap(c1, c2)
        self.assertEqual(expected, result)

    """
    Tests for get_allgaps(cards)
    """
    def test_getallgaps_1card_returns0(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As'])
        expected = 0
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_2connected_returns0(self):
        cards = pokerhands.convert_to_cards(['Kc', 'As'])
        expected = 0
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_2cards1gap_returns1(self):
        cards = pokerhands.convert_to_cards(['Qc', 'As'])
        expected = 1
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_3cards1gap_returns1(self):
        cards = pokerhands.convert_to_cards(['Tc', 'Js', 'Ks'])
        expected = 1
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    """
    Tests for strip_ranks(cards, ranks)
    """
    def test_stripranks_stripAces_containsNoAces(self):
        ace = card.Card('A', 's')
        king = card.Card('K', 'c')
        cards = [ace, king]
        expected = False
        result = ace in evaluator.strip_ranks(cards, ['A'])
        self.assertEqual(expected, result)

    def test_stripranks_stripAcesAndKings_containsNothing(self):
        cards = pokerhands.convert_to_cards(['As', 'Kc'])
        expected = []
        result = evaluator.strip_ranks(cards, ['A', 'K'])
        self.assertEqual(expected, result)

    """
    Tests for strip_suits(cards, suit)
    """
    def test_stripsuits_stripSpades_containsNoSpades(self):
        cards = pokerhands.convert_to_cards(['As', 'Kc'])
        cards = evaluator.strip_suits(cards, 's')
        expected = 0
        result = evaluator.count_suit(cards, 's')
        self.assertEqual(expected, result)

    def test_stripsuits_stripMultipleSuits_allSuitsWereStripped(self):
        cards = pokerhands.convert_to_cards(['As', 'Kc', 'Qd'])
        cards = evaluator.strip_suits(cards, ['s', 'c'])
        expected = 0
        result = evaluator.count_suit(cards, 's') + evaluator.count_suit(cards, 'c')
        self.assertEqual(expected, result)

    """
    Tests for is_integer(num)
    """
    # Pass an integer 10. Returns True.
    def test_isinteger_10_returnsTrue(self):
        expected = True
        result = evaluator.is_integer(10)
        self.assertEqual(expected, result)

    # Pass a string. Returns False.
    def test_isinteger_string_returnsFalse(self):
        expected = False
        result = evaluator.is_integer('string')
        self.assertEqual(expected, result)

    # Pass a float 10.5. Returns False.
    def test_isinteger_float_returnsFalse(self):
        expected = False
        result = evaluator.is_integer(10.5)
        self.assertEqual(expected, result)

    """
    Tests for chk_straight_draw(cards, qty, gap):
    """
    def test_straightdrawchk_2card_0gap_275Q6K_returnsQK(self):
        cards = pokerhands.convert_to_cards(['2c', '7s', '5h', 'Qd', '6s', 'Kh'])
        expected = pokerhands.convert_to_cards(['Qd', 'Kh'])
        result = evaluator.chk_straight_draw(cards, 2, 0)
        self.assertEqual(expected, result)

    def test_straightdrawchk_2card_0gap_2A5Q6_returnsAKQ(self):
        cards = pokerhands.convert_to_cards(['2c', 'As', '5h', 'Qd', '6s'])
        expected = pokerhands.convert_to_cards(['5h', '6s'])
        result = evaluator.chk_straight_draw(cards, 2, 0)
        self.assertEqual(expected, result)

    def test_straightdrawchk_3card_1gap_JA5Q6_returnsAKQ(self):
        cards = pokerhands.convert_to_cards(['Jd', 'As', '5h', 'Qd', '6s'])
        expected = pokerhands.convert_to_cards(['Jd', 'Qd', 'As'])
        result = evaluator.chk_straight_draw(cards, 3, 1)
        self.assertEqual(expected, result)

    def test_straightdrawchk_3card_0gap_AKQ_returnsAKQ(self):
        cards = pokerhands.convert_to_cards(['As', 'Kc', 'Qd'])
        expected = pokerhands.convert_to_cards(['Qd', 'Kc', 'As'])
        result = evaluator.chk_straight_draw(cards, 3, 0)
        self.assertEqual(expected, result)

    def test_straightdrawchk_3card_0gap_AKQJ_returnsAKQ(self):
        cards = pokerhands.convert_to_cards(['As', 'Kc', 'Qd', 'Jd'])
        expected = pokerhands.convert_to_cards(['Qd', 'Kc', 'As'])
        result = evaluator.chk_straight_draw(cards, 3, 0)
        self.assertEqual(expected, result)

    def test_straightdrawchk_4card_0gap_2J5Q6K_returnsAKQ(self):
        cards = pokerhands.convert_to_cards(['2c', 'Js', '5h', 'Qd', '6s', 'Kh'])
        expected = pokerhands.convert_to_cards(['Js', 'Qd', 'Kh'])
        result = evaluator.chk_straight_draw(cards, 3, 0)
        self.assertEqual(expected, result)

    """
    Tests for chk_wheel(cards):
    """
    def test_chkwheel_A_returnsTrue(self):
        cards = pokerhands.convert_to_cards(['As'])
        expected = True
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_A2_returnsTrue(self):
        cards = pokerhands.convert_to_cards(['As', '2c'])
        expected = True
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_A23_returnsTrue(self):
        cards = pokerhands.convert_to_cards(['As', '2c', '3d'])
        expected = True
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_A234_returnsTrue(self):
        cards = pokerhands.convert_to_cards(['As', '2c', '3d', '4d'])
        expected = True
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_A2345_returnsTrue(self):
        cards = pokerhands.convert_to_cards(['As', '2c', '3d', '4d', '5h'])
        expected = True
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_AA23_returnsFalse(self):
        cards = pokerhands.convert_to_cards(['As', 'Ah', '2c', '3d'])
        expected = False
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_A223_returnsFalse(self):
        cards = pokerhands.convert_to_cards(['As', '2h', '2c', '3d'])
        expected = False
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_AKQJ_returnsFalse(self):
        cards = pokerhands.convert_to_cards(['As', 'Kc', 'Qd', 'Jd'])
        expected = False
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    def test_chkwheel_2345_returnsFalse(self):
        cards = pokerhands.convert_to_cards(['2c', '3d', '4d', '5h'])
        expected = False
        result = evaluator.chk_wheel(cards)
        self.assertEqual(expected, result)

    """
    Tests for def extract_discards(cards, keep):
    """
