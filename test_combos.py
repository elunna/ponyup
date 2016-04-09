import unittest
import card
import combos
import deck


class TestCombos(unittest.TestCase):
    #  def __init__(self):
        #  super(TestCombos, self).__init__()
        #  d = deck.Deck()
        #  self.combosof5 = combos.get_combolist(d.cards, 5)
        #  self.type_count = combos.typecount_dict(combosof5)

    """
    Tests for n_choose_k(n, k)
    """
    def test_nchoosek_0pick1_raiseException(self):
        self.assertRaises(ValueError, combos.n_choose_k, 0, 1)

    def test_nchoosek_1pick0_raiseException(self):
        self.assertRaises(ValueError, combos.n_choose_k, 1, 0)

    def test_nchoosek_neg1pick1_raiseException(self):
        self.assertRaises(ValueError, combos.n_choose_k, -1, 1)

    def test_nchoosek_1pickneg1_raiseException(self):
        self.assertRaises(ValueError, combos.n_choose_k, 1, -1)

    # K larger than N
    def test_nchoosek_1pick2_raiseException(self):
        self.assertRaises(ValueError, combos.n_choose_k, 1, 2)

    def test_nchoosek_1pick1_returns1(self):
        expected = 1
        result = combos.n_choose_k(1, 1)
        self.assertEqual(expected, result)

    def test_nchoosek_2pick1_returns1(self):
        expected = 2
        result = combos.n_choose_k(2, 1)
        self.assertEqual(expected, result)

    def test_nchoosek_3pick2_returns3(self):
        expected = 3
        result = combos.n_choose_k(3, 2)
        self.assertEqual(expected, result)

    """
    Tests for get_combolist(source, n)
    """
    def test_getcombos_of1withfullDeck_52combos(self):
        d = deck.Deck()
        combosof1 = combos.get_combolist(d.cards, 1)
        expected = 52
        result = len(combosof1)
        self.assertEqual(expected, result)

    def test_getcombos_of2withfullDeck_1326combos(self):
        d = deck.Deck()
        combosof2 = combos.get_combolist(d.cards, 2)
        expected = 1326
        result = len(combosof2)
        self.assertEqual(expected, result)

    def test_getcombos_of3withfullDeck_22100combos(self):
        d = deck.Deck()
        combosof3 = combos.get_combolist(d.cards, 3)
        expected = 22100
        result = len(combosof3)
        self.assertEqual(expected, result)

    def test_getcombos_of4withfullDeck_combos270725(self):
        d = deck.Deck()
        combosof4 = combos.get_combolist(d.cards, 4)
        expected = 270725
        result = len(combosof4)
        self.assertEqual(expected, result)

    def test_getcombos_of5withfullDeck_2598960combos(self):
        d = deck.Deck()
        combosof5 = combos.get_combolist(d.cards, 5)
        expected = 2598960
        result = len(combosof5)
        self.assertEqual(expected, result)

    """
    Tests for get_allcombos(cards)
    """
    def test_getallcombos_emptylist_returns0(self):
        allcombos = combos.get_allcombos([])
        expected = 0
        result = len(allcombos)
        self.assertEqual(expected, result)

    def test_getallcombos_1card_returns1(self):
        c = card.Card('A', 's')
        cards = [c]
        allcombos = combos.get_allcombos(cards)
        expected = 1
        result = len(allcombos)
        self.assertEqual(expected, result)

    def test_getallcombos_2cards_returns3(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('K', 's')
        cards = []
        cards.append(c1)
        cards.append(c2)

        allcombos = combos.get_allcombos(cards)
        expected = 3
        result = len(allcombos)
        self.assertEqual(expected, result)

    def test_getallcombos_3cards_returns7(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('K', 's')
        c3 = card.Card('Q', 's')
        cards = []
        cards.append(c1)
        cards.append(c2)
        cards.append(c3)

        allcombos = combos.get_allcombos(cards)
        expected = 7
        result = len(allcombos)
        self.assertEqual(expected, result)

    """
    Tests for typecount_dict(handlist)
    """
    # Since this dict is VERY LARGE, We will call all the tests from this constructor method.
    # DISABLED TEMPARILY FOR FASTER TESTING - THIS TAKES ~30 seconds.
    """
    def test_typecountdict_fulldeck(self):
        d = deck.Deck()
        combosof5 = combos.get_combolist(d.cards, 5)
        type_count = combos.typecount_dict(combosof5)

        # Run individual tests
        self.typecountdict_fulldeck_10keys(type_count)
        self.typecountdict_fulldeck_4royalflush(type_count)
        self.typecountdict_fulldeck_40straightflush(type_count)
        self.typecountdict_fulldeck_624quads(type_count)
        self.typecountdict_fulldeck_3744fullhouse(type_count)
    """
    def typecountdict_fulldeck_10keys(self, type_count):
        expected = 10
        result = len(type_count.keys())
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_4royalflush(self, type_count):
        expected = 4
        result = type_count['ROYAL FLUSH']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_40straightflush(self, type_count):
        expected = 36
        result = type_count['STRAIGHT FLUSH']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_624quads(self, type_count):
        expected = 624
        result = type_count['QUADS']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_3744fullhouse(self, type_count):
        expected = 3744
        result = type_count['FULL HOUSE']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_5108flush(self, type_count):
        expected = 5108
        result = type_count['FLUSH']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_10200straight(self, type_count):
        expected = 10200
        result = type_count['STRAIGHT']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_54912sets(self, type_count):
        expected = 54912
        result = type_count['SET']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_123552twopair(self, type_count):
        expected = 123552
        result = type_count['TWO PAIR']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_1098240pairs(self, type_count):
        expected = 1098240
        result = type_count['PAIR']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_1302540(self, type_count):
        expected = 1302540
        result = type_count['HIGH CARD']
        self.assertEqual(expected, result)

    """
    Tests for get_unique_5cardhands()
    """

    """
    Tests for sort_handslist(handdict)
    """

    """
    Tests for print_unique_5cardhands(handlist)
    """
    # No tests needed, only displays results.

    """
    Tests for count_all_handtypes(combolist)
    """

    """
    Tests for enumerate_unique_5cardhands(combolist)
    """
