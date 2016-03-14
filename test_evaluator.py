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
    Tests for is_flush(cards)
    """

    """
    Tests for is_straight(cards)
    """

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
    def test_gettype_negativevalue_raiseEx(self):
        self.assertRaises(ValueError, evaluator.get_type, -1)

    def test_gettype_1000000000000_raiseEx(self):
        self.assertRaises(ValueError, evaluator.get_type, 1000000000000)

    """
    Tests for get_value(cards)
    """

    """
    Tests for get_description(value, cards)
    """

    """
    Tests for process_nonpairhands(cards, sortedranks):
    """

    """
    Tests for def process_pairhands(sortedranks):
    """

    """
    Tests for find_best_hand(cards)
    """

    #  def test_findbesthand_7cardstraightflush_returnsROYALFLUSH(self):
    # besthand = ev.find_best_hand(group)
