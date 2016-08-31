import unittest
import card
import cardlist
import evaluator
import pokerhands


class TestEvaluator(unittest.TestCase):
    """
    Tests for is_valid_hand(cards)
    """
    def test_is_validhand_4cards_returnsFalse(self):
        h = pokerhands.dealhand(4)
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_5cards_returnsTrue(self):
        h = pokerhands.dealhand(5)
        expected = True
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_6cards_returnsFalse(self):
        h = pokerhands.dealhand(6)
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_duplicateCards_returnsFalse(self):
        h = pokerhands.deal_duplicates()
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
        rd = cardlist.rank_list(cards)
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
