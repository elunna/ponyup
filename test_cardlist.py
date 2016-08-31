import unittest
import card
import cardlist
import pokerhands


class TestCardList(unittest.TestCase):
    """
    Tests for is_set(cards)
    """
    def test_is_set_royalflush_returnsTrue(self):
        h = pokerhands.royalflush()
        expected = True
        result = cardlist.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_handwithdupes_returnsFalse(self):
        h = pokerhands.dupes()
        expected = False
        result = cardlist.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_1card_returnsTrue(self):
        c = card.Card('A', 's')
        h = [c]
        expected = True
        result = cardlist.is_set(h)
        self.assertEqual(expected, result)

    def test_is_set_2As_returnsFalse(self):
        c = card.Card('A', 's')
        h = [c, c]
        expected = False
        result = cardlist.is_set(h)
        self.assertEqual(expected, result)

    """
    Tests for rank_dict(cards)
    """
    def test_rankdict_0Ace_counts0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 's'))
        expected = 0
        rankdict = cardlist.rank_dict(cards)
        # 0 is the default in case there are no Aces
        result = rankdict.get('A', 0)
        self.assertEqual(expected, result)

    def test_rankdict_1Ace_counts1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        rankdict = cardlist.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    def test_rankdict_2Aces_counts2(self):
        cards = []
        cards.append(card.Card('A', 'h'))
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 2
        rankdict = cardlist.rank_dict(cards)
        result = rankdict.get('A')
        self.assertEqual(expected, result)

    def test_suitdict_0Spades_counts0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 'h'))
        expected = 0
        suitdict = cardlist.suit_dict(cards)
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
        ranklist = cardlist.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    def test_ranklist_1Ace_1AceCounted(self):
        cards = []
        cards.append(card.Card('A', 's'))
        ranklist = cardlist.rank_list(cards)
        expected_qty = ranklist[0][0]
        expected_rank = ranklist[0][1]
        self.assertTrue(
            expected_qty == 1, expected_rank == 'A')

    def test_ranklist_2Aces_lenEquals1(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('A', 'h'))
        expected = 1
        ranklist = cardlist.rank_list(cards)
        result = len(ranklist)
        self.assertEqual(expected, result)

    def test_ranklist_2Aces_2AcesCounted(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('A', 'h'))
        ranklist = cardlist.rank_list(cards)
        expected_qty = ranklist[0][0]
        expected_rank = ranklist[0][1]
        self.assertTrue(
            expected_qty == 2, expected_rank == 'A')

    def test_ranklist_AK_lenEquals2(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('K', 'h'))
        expected = 2
        ranklist = cardlist.rank_list(cards)
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
        suitdict = cardlist.suit_dict(cards)
        result = suitdict.get('s', 0)
        self.assertEqual(expected, result)

    def test_suitdict_1Spade_counts1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        suitdict = cardlist.suit_dict(cards)
        result = suitdict.get('s')
        self.assertEqual(expected, result)

    def test_suitdict_2Spade_counts2(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('2', 's'))
        cards.append(card.Card('A', 's'))
        expected = 2
        suitdict = cardlist.suit_dict(cards)
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
        suitdict = cardlist.suitedcard_dict(cards)
        # Empty list is the default in case there are no Aces
        result = len(suitdict.get('s', []))
        self.assertEqual(expected, result)

    def test_suitedcarddict_1Spade_listlenEquals1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        suitdict = cardlist.suitedcard_dict(cards)
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
        result = cardlist.count_suit(cards, 's')
        self.assertEqual(expected, result)

    def test_countsuit_1spade_returns1(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        result = cardlist.count_suit(cards, 's')
        self.assertEqual(expected, result)

    """
    Tests for get_gap(card1, card2)
    """
    def test_getgap_23_returns0(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('3', 's')
        expected = 0
        result = cardlist.get_gap(c1, c2)
        self.assertEqual(expected, result)

    def test_getgap_32_returns0(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('3', 's')
        expected = 0
        result = cardlist.get_gap(c2, c1)
        self.assertEqual(expected, result)

    def test_getgap_24_returns1(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('4', 's')
        expected = 1
        result = cardlist.get_gap(c2, c1)
        self.assertEqual(expected, result)

    def test_getgap_2A_returns11(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('A', 's')
        expected = 11
        result = cardlist.get_gap(c1, c2)
        self.assertEqual(expected, result)

    def test_getgap_22_returnsNeg1(self):
        c1 = card.Card('2', 's')
        c2 = card.Card('2', 'c')
        expected = -1
        result = cardlist.get_gap(c1, c2)
        self.assertEqual(expected, result)

    """
    Tests for get_allgaps(cards)
    """
    def test_getallgaps_1card_returns0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 0
        result = cardlist.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_2connected_returns0(self):
        cards = []
        cards.append(card.Card('K', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 0
        result = cardlist.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_2cards1gap_returns1(self):
        cards = []
        cards.append(card.Card('Q', 'c'))
        cards.append(card.Card('A', 's'))
        expected = 1
        result = cardlist.get_allgaps(cards)
        self.assertEqual(expected, result)

    def test_getallgaps_3cards1gap_returns1(self):
        cards = []
        cards.append(card.Card('T', 'c'))
        cards.append(card.Card('J', 's'))
        cards.append(card.Card('K', 's'))
        expected = 1
        result = cardlist.get_allgaps(cards)
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
        result = ace in cardlist.strip_ranks(cards, ['A'])
        self.assertEqual(expected, result)

    def test_stripranks_stripAcesAndKings_containsNothing(self):
        cards = []
        ace = card.Card('A', 's')
        king = card.Card('K', 'c')
        cards.append(ace)
        cards.append(king)
        expected = []
        result = cardlist.strip_ranks(cards, ['A', 'K'])
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
        cards = cardlist.strip_suits(cards, 's')
        expected = 0
        result = cardlist.count_suit(cards, 's')
        self.assertEqual(expected, result)

    def test_stripsuits_stripMultipleSuits_allSuitsWereStripped(self):
        cards = []
        ace = card.Card('A', 's')
        king = card.Card('K', 'c')
        queen = card.Card('Q', 'd')
        cards.append(ace)
        cards.append(king)
        cards.append(queen)
        cards = cardlist.strip_suits(cards, ['s', 'c'])
        expected = 0
        result = cardlist.count_suit(cards, 's') + cardlist.count_suit(cards, 'c')
        self.assertEqual(expected, result)
