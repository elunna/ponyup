import card
import unittest
import evaluator
import pokerhands


class TestEvaluator(unittest.TestCase):
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

    def test_gettype_negativevalue_raiseEx(self):
        self.assertRaises(ValueError, evaluator.get_type, -1)

    def test_gettype_1000000000000_raiseEx(self):
        self.assertRaises(ValueError, evaluator.get_type, 1000000000000)

    def test_is_set_royalflush_returnsTrue(self):
        h = pokerhands.royalflush()
        expected = True
        result = evaluator.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_handwithdupes_returnsFalse(self):
        h = pokerhands.deal_duplicates()
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

    def test_rank_dict_0Ace_counts0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 's'))
        expected = 0
        rankdict = evaluator.rank_dict(cards)
        # 0 is the default in case there are no Aces
        result = rankdict.get('A', 0)
        self.assertEqual(expected, result)

    def test_rank_dict_1Ace_counts1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        rankdict = evaluator.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    def test_rank_dict_2Aces_counts2(self):
        cards = []
        cards.append(card.Card('A', 'h'))
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 2
        rankdict = evaluator.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    #  def test_sortedranks_tolist

    def test_suitdict_0Spades_counts0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 'h'))
        expected = 0
        suitdict = evaluator.suit_dict(cards)
        # 0 is the default in case there are no Aces
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

    def test_score_unsortedlist_A_returns14(self):
        cards = [card.Card('A', 's')]
        expected = 14
        result = evaluator.score_unsortedlist(cards)
        self.assertEqual(expected, result)

    def test_score_unsortedlist_AK_returns1413(self):
        cards = [card.Card('A', 's'), card.Card('K', 's')]
        expected = 1413
        result = evaluator.score_unsortedlist(cards)
        self.assertEqual(expected, result)

    def test_score_unsortedlist_AKQ_returns141312(self):
        cards = [card.Card('A', 's'), card.Card('K', 's'), card.Card('Q', 's')]
        expected = 141312
        result = evaluator.score_unsortedlist(cards)
        self.assertEqual(expected, result)

    #  score

    # get_value
    # get_gap
    # get_allgaps
    # find_best_hand
    # pop_ranks
    # pop_suits

    # is_flush
    # is_straight

    #  def test_findbesthand_7cardstraightflush_returnsROYALFLUSH(self):
    # besthand = ev.find_best_hand(group)

    # Test description?
