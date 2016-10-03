import unittest
from ponyup import combos
from ponyup import deck
from ponyup import tools


class TestCombos(unittest.TestCase):
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
    """
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

    """
    Tests for get_allcombos(cards)
    """
    def test_getallcombos_emptylist_returns0(self):
        allcombos = combos.get_allcombos([])
        expected = 0
        result = len(allcombos)
        self.assertEqual(expected, result)

    def test_getallcombos_1card_returns1(self):
        cards = tools.convert_to_cards(['As'])
        allcombos = combos.get_allcombos(cards)
        expected = 1
        result = len(allcombos)
        self.assertEqual(expected, result)

    def test_getallcombos_2cards_returns3(self):
        cards = tools.convert_to_cards(['As', 'Ks'])
        allcombos = combos.get_allcombos(cards)
        expected = 3
        result = len(allcombos)
        self.assertEqual(expected, result)

    def test_getallcombos_3cards_returns7(self):
        cards = tools.convert_to_cards(['As', 'Ks', 'Qs'])
        allcombos = combos.get_allcombos(cards)
        expected = 7
        result = len(allcombos)
        self.assertEqual(expected, result)
