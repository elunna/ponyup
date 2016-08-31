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
        h = pokerhands.dupes()
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_royalflush_returnsTrue(self):
        h = pokerhands.royalflush()
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
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('K', 'c'))
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_3diffranks_returnshigherrank(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('Q', 'h'))
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_4diffranks_returnshigherrank(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('J', 'd'))
        cards.append(card.Card('Q', 'h'))
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_3cards2suitedSpades_returnsSpades(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('Q', 's'))
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    def test_dominantsuit_HigherSpades_returnsSpades(self):
        cards = []
        cards.append(card.Card('A', 'c'))
        cards.append(card.Card('K', 's'))
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('Q', 'c'))
        expected = 's'
        result = evaluator.dominant_suit(cards)
        self.assertEqual(expected, result)

    """
    Tests for is_suited(cards)
    """
    def test_issuited_1card_returnsTrue(self):
        cards = []
        cards.append(card.Card('A', 's'))
        expected = True
        result = evaluator.is_suited(cards)
        self.assertEqual(expected, result)

    def test_issuited_2suitedcards_returnsTrue(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('2', 's'))
        expected = True
        result = evaluator.is_suited(cards)
        self.assertEqual(expected, result)

    def test_issuited_2unsuitedcard_returnsFalse(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('A', 'd'))
        expected = False
        result = evaluator.is_suited(cards)
        self.assertEqual(expected, result)

    """
    Tests for is_straight(cards)
    """
    # Test a low straight hand
    def test_isstraight_lowstraight_returnsTrue(self):
        hand = pokerhands.straight_low()
        expected = True
        result = evaluator.is_straight(hand)
        self.assertEqual(expected, result)

    # Test a mid straight hand
    def test_isstraight_midstraight_returnsTrue(self):
        hand = pokerhands.straight_mid()
        expected = True
        result = evaluator.is_straight(hand)
        self.assertEqual(expected, result)

    # Test a high straight hand
    def test_isstraight_highstraight_returnsTrue(self):
        hand = pokerhands.straight_high()
        expected = True
        result = evaluator.is_straight(hand)
        self.assertEqual(expected, result)

    # Test a non-straight hand
    def test_isstraight_nonstraight_returnsFalse(self):
        hand = pokerhands.wheeldraw()
        expected = False
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
        cards = [card.Card('A', 's'), card.Card('K', 's')]
        expected = 1413
        result = evaluator.score_cardlist(cards)
        self.assertEqual(expected, result)

    def test_scorecardlist_AKQ_returns141312(self):
        cards = [card.Card('A', 's'), card.Card('K', 's'), card.Card('Q', 's')]
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
    Tests for get_value(cards)
    """
    # Test the value of 1 Ace
    def test_get_value_A_returns1400000000(self):
        cards = [card.Card('A', 's')]
        expected = 1400000000
        result = evaluator.get_value(cards)
        self.assertEqual(expected, result)

    # Test the value of 2 Aces
    def test_get_value_AA_returns21400000000(self):
        cards = [
            card.Card('A', 's'),
            card.Card('A', 'h'),
        ]
        expected = 21400000000
        result = evaluator.get_value(cards)
        self.assertEqual(expected, result)

    # Test the value of 3 Aces
    def test_get_value_AAA_returns41400000000(self):
        cards = [
            card.Card('A', 's'),
            card.Card('A', 'h'),
            card.Card('A', 'c'),
        ]
        expected = 41400000000
        result = evaluator.get_value(cards)
        self.assertEqual(expected, result)

    # Test the value of 4 Aces
    def test_get_value_AAAA_returns81400000000(self):
        cards = [
            card.Card('A', 's'),
            card.Card('A', 'h'),
            card.Card('A', 'c'),
            card.Card('A', 'd'),
        ]
        expected = 81400000000
        result = evaluator.get_value(cards)
        self.assertEqual(expected, result)

    """
    Tests for get_description(value, cards)
    """

    """
    Tests for process_nonpairhands(cards, sortedranks):
    """

    """
    Tests for process_pairhands(sortedranks):
    """

    """
    Tests for find_best_hand(cards)
    """

    def test_findbesthand_pair_returnsPAIR(self):
        cards = [
            card.Card('2', 'c'),
            card.Card('3', 'c'),
            card.Card('5', 's'),
            card.Card('7', 's'),
            card.Card('K', 'c'),
            card.Card('A', 'c'),
            card.Card('A', 's'),
        ]
        besthand = evaluator.find_best_hand(cards)
        expected = 'PAIR'
        result = besthand.rank()
        self.assertEqual(expected, result)

    def test_findbesthand_fullhouse_returnsFULLHOUSE(self):
        cards = [
            card.Card('7', 'c'),
            card.Card('7', 's'),
            card.Card('K', 's'),
            card.Card('K', 'c'),
            card.Card('A', 'h'),
            card.Card('A', 'c'),
            card.Card('A', 's'),
        ]
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'FULL HOUSE'
        self.assertEqual(expected, result)

    def test_findbesthand_straightflush_returnsSTRAIGHTFLUSH(self):
        cards = [
            card.Card('4', 's'),
            card.Card('5', 's'),
            card.Card('6', 's'),
            card.Card('7', 's'),
            card.Card('8', 's'),
            card.Card('K', 's'),
            card.Card('A', 's'),
        ]
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'STRAIGHT FLUSH'
        self.assertEqual(expected, result)

    def test_findbesthand_quads_returnsQUADS(self):
        cards = [
            card.Card('K', 'c'),
            card.Card('K', 'd'),
            card.Card('K', 's'),
            card.Card('A', 'c'),
            card.Card('K', 'd'),
            card.Card('A', 'h'),
            card.Card('A', 's'),
        ]
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'QUADS'
        self.assertEqual(expected, result)

    def test_findbesthand_straight_returnsSTRAIGHT(self):
        cards = [
            card.Card('A', 'c'),
            card.Card('A', 's'),
            card.Card('2', 'c'),
            card.Card('3', 's'),
            card.Card('4', 'h'),
            card.Card('5', 's'),
            card.Card('5', 'h'),
        ]
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'STRAIGHT'
        self.assertEqual(expected, result)

    def test_findbesthand_flush_returnsFLUSH(self):
        cards = [
            card.Card('8', 's'),
            card.Card('9', 's'),
            card.Card('T', 'c'),
            card.Card('J', 's'),
            card.Card('Q', 's'),
            card.Card('K', 's'),
            card.Card('A', 'c'),
        ]
        besthand = evaluator.find_best_hand(cards)
        result = besthand.rank()
        expected = 'FLUSH'
        self.assertEqual(expected, result)

    # besthand = ev.find_best_hand(group)

    """
    Tests for is_set(cards)
    """
    def test_is_set_royalflush_returnsTrue(self):
        h = pokerhands.royalflush()
        expected = True
        result = evaluator.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_handwithdupes_returnsFalse(self):
        h = pokerhands.dupes()
        expected = False
        result = evaluator.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_1card_returnsTrue(self):
        c = card.Card('A', 's')
        h = [c]
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
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 's'))
        expected = 0
        rankdict = evaluator.rank_dict(cards)
        # 0 is the default in case there are no Aces
        result = rankdict.get('A', 0)
        self.assertEqual(expected, result)

    def test_rankdict_1Ace_counts1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        rankdict = evaluator.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    def test_rankdict_2Aces_counts2(self):
        cards = []
        cards.append(card.Card('A', 'h'))
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 2
        rankdict = evaluator.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    def test_suitdict_0Spades_counts0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 'h'))
        expected = 0
        suitdict = evaluator.suit_dict(cards)
        # 0 is the default in case there are no Aces
        result = suitdict.get('s', 0)
        self.assertEqual(expected, result)

    """
    Tests for rank_list(cards)
    """
    def test_ranklist_1Ace_lenEquals1(self):
        cards = []
        cards.append(card.Card('A', 's'))
        expected = 1
        ranklist = evaluator.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    def test_ranklist_1Ace_1AceCounted(self):
        cards = []
        cards.append(card.Card('A', 's'))
        ranklist = evaluator.rank_list(cards)
        expected_qty = ranklist[0][0]
        expected_rank = ranklist[0][1]
        self.assertTrue(
            expected_qty == 1, expected_rank == 'A')

    def test_ranklist_2Aces_lenEquals1(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('A', 'h'))
        expected = 1
        ranklist = evaluator.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    def test_ranklist_2Aces_2AcesCounted(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('A', 'h'))
        ranklist = evaluator.rank_list(cards)
        expected_qty = ranklist[0][0]
        expected_rank = ranklist[0][1]
        self.assertTrue(
            expected_qty == 2, expected_rank == 'A')

    def test_ranklist_AK_lenEquals2(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('K', 'h'))
        expected = 2
        ranklist = evaluator.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    """
    Tests for suit_dict(cards)
    """
    def test_suitdict_0Spade_counts0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 'h'))
        expected = 0
        suitdict = evaluator.suit_dict(cards)
        result = suitdict.get('s', 0)
        self.assertEqual(expected, result)

    def test_suitdict_1Spade_counts1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        suitdict = evaluator.suit_dict(cards)
        result = suitdict.get('s')
        self.assertEqual(expected, result)

    def test_suitdict_2Spade_counts2(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 's'))
        cards.append(card.Card('A', 's'))
        expected = 2
        suitdict = evaluator.suit_dict(cards)
        result = suitdict.get('s')
        self.assertEqual(expected, result)

    """
    Tests for suitedcard_dict(cards)
    """
    def test_suitedcarddict_0Spades_listlenEquals0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 'h'))
        expected = 0
        suitdict = evaluator.suitedcard_dict(cards)
        # Empty list is the default in case there are no Aces
        result = len(suitdict.get('s', []))
        self.assertEqual(expected, result)

    def test_suitedcarddict_1Spade_listlenEquals1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        suitdict = evaluator.suitedcard_dict(cards)
        # Empty list is the default in case there are no Aces
        result = len(suitdict.get('s', []))
        self.assertEqual(expected, result)

    """
    Tests for count_suit(cards, suit)
    """
    def test_countsuit_nospade_returns0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        expected = 0
        result = evaluator.count_suit(cards, 's')
        self.assertEqual(expected, result)

    def test_countsuit_1spade_returns1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
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
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 0
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_2connected_returns0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 0
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_2cards1gap_returns1(self):
        cards = []
        cards.append(card.Card('Q', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_3cards1gap_returns1(self):
        cards = []
        cards.append(card.Card('T', 'c'))
        cards.append(card.Card('J', 's'))
        cards.append(card.Card('K', 's'))
        expected = 1
        result = evaluator.get_allgaps(cards)
        self.assertEqual(expected, result)

    """
    Tests for strip_ranks(cards, ranks)
    """
    def test_stripranks_stripAces_containsNoAces(self):
        cards = []
        ace = card.Card('A', 's')
        king = card.Card('K', 'c')
        cards.append(ace)
        cards.append(king)
        expected = False
        result = ace in evaluator.strip_ranks(cards, ['A'])
        self.assertEqual(expected, result)

    def test_stripranks_stripAcesAndKings_containsNothing(self):
        cards = []
        ace = card.Card('A', 's')
        king = card.Card('K', 'c')
        cards.append(ace)
        cards.append(king)
        expected = []
        result = evaluator.strip_ranks(cards, ['A', 'K'])
        self.assertEqual(expected, result)

    """
    Tests for strip_suits(cards, suit)
    """
    def test_stripsuits_stripSpades_containsNoSpades(self):
        cards = []
        ace = card.Card('A', 's')
        king = card.Card('K', 'c')
        cards.append(ace)
        cards.append(king)
        cards = evaluator.strip_suits(cards, 's')
        expected = 0
        result = evaluator.count_suit(cards, 's')
        self.assertEqual(expected, result)

    def test_stripsuits_stripMultipleSuits_allSuitsWereStripped(self):
        cards = []
        ace = card.Card('A', 's')
        king = card.Card('K', 'c')
        queen = card.Card('Q', 'd')
        cards.append(ace)
        cards.append(king)
        cards.append(queen)
        cards = evaluator.strip_suits(cards, ['s', 'c'])
        expected = 0
        result = evaluator.count_suit(cards, 's') + evaluator.count_suit(cards, 'c')
        self.assertEqual(expected, result)
