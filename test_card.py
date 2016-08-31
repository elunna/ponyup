import unittest
import card


class TestCards(unittest.TestCase):

    """
    Tests for __init__ and card construction
    """
    def test_init_invalidsuit_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 'A', 'a')
        # failUnlessRaises is deprecated!
        # self.failUnlessRaises(ValueError, card.Card, 'A', 'a')

    def test_init_invalidrank_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 'Y', 's')
        # failUnlessRaises is deprecated!
        # self.failUnlessRaises(ValueError, card.Card, 'Y', 's')

    def test_init_invalidboth_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 's', 'A')

    def test_init_uppercaseSuit_suitIsLowercase(self):
        c = card.Card('A', 'S')
        expected = 's'
        result = c.suit
        self.assertEqual(expected, result)

    def test_init_default_hiddenIsTrue(self):
        c = card.Card('A', 's')
        expected = True
        result = c.hidden
        self.assertEqual(expected, result)

    """
    Tests for val()
    """
    def test_val_JOKER_Z_returns15(self):
        c = card.Card('Z', 's')
        expected = 15
        result = c.val()
        self.assertEqual(expected, result)

    def test_val_A_returns14(self):
        c = card.Card('A', 's')
        expected = 14
        result = c.val()
        self.assertEqual(expected, result)

    def test_val_K_returns13(self):
        instance = card.Card('K', 's')
        expected = 13
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_Q_returns12(self):
        instance = card.Card('Q', 's')
        expected = 12
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_J_returns11(self):
        instance = card.Card('J', 's')
        expected = 11
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_T_returns10(self):
        instance = card.Card('T', 's')
        expected = 10
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_9_returns9(self):
        instance = card.Card('9', 's')
        expected = 9
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_8_returns8(self):
        instance = card.Card('8', 's')
        expected = 8
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_7_returns7(self):
        instance = card.Card('7', 's')
        expected = 7
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_6_returns6(self):
        instance = card.Card('6', 's')
        expected = 6
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_5_returns5(self):
        instance = card.Card('5', 's')
        expected = 5
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_4_returns4(self):
        instance = card.Card('4', 's')
        expected = 4
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_3_returns3(self):
        instance = card.Card('3', 's')
        expected = 3
        result = instance.val()
        self.assertEqual(expected, result)

    def test_val_2_returns2(self):
        instance = card.Card('2', 's')
        expected = 2
        result = instance.val()
        self.assertEqual(expected, result)

    """
    Tests for str()
    """
    def test_str_hiddenCard_returnsXx(self):
        c = card.Card('A', 's')
        #  expected = 'Xx'
        expected = '\x1b[1;40;40mXx\x1b[0m'
        result = str(c)
        self.assertEqual(expected, result)

    def test_str_FaceupAs_returnsAs(self):
        c = card.Card('A', 's')
        c.hidden = False
        #  expected = 'As'
        expected = '\x1b[1;37;40mAs\x1b[0m'
        result = str(c)
        self.assertEqual(expected, result)

    """
    Tests for __repr__()
    * Currently this just calls str so no tests are required.
    """
    def test_repr_hiddenCard_returnsXx(self):
        c = card.Card('A', 's')
        expected = 'Xx'
        result = repr(c)
        self.assertEqual(expected, result)

    def test_repr_FaceupAs_returnsAs(self):
        c = card.Card('A', 's')
        c.hidden = False
        expected = 'As'
        result = repr(c)
        self.assertEqual(expected, result)

    """
    Tests for __eq__()
    """
    def test_Equals_SameCard_returnsTrue(self):
        """ __equals__ tests that the two cards have exactly the same suit and rank."""
        c1 = card.Card('A', 's')
        c2 = card.Card('A', 's')
        expected = True
        result = c1 == c2
        self.assertEqual(expected, result)

    def test_Equals_DiffSuits_returnsFalse(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('A', 'c')
        expected = False
        result = c1 == c2
        self.assertEqual(expected, result)

    """
    Tests for __gt__
    """
    def test_Greaterthan_HighToLow_returnsFalse(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = True
        result = high > low
        self.assertEqual(expected, result)

    def test_Greaterthan_LowToHigh_returnsTrue(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = False
        result = low > high
        self.assertEqual(expected, result)

    def test_Greaterthan_SameRanks_returnsFalse(self):
        c1 = card.Card('K', 's')
        c2 = card.Card('K', 'c')
        expected = False
        result = c2 > c1
        self.assertEqual(expected, result)

    """
    Tests for __lt__
    """
    def test_Lessthan_HighToLow_returnsFalse(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = False
        result = high < low
        self.assertEqual(expected, result)

    def test_Lessthan_LowToHigh_returnsTrue(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = True
        result = low < high
        self.assertEqual(expected, result)

    def test_Lessthan_SameRanks_returnsFalse(self):
        c1 = card.Card('K', 's')
        c2 = card.Card('K', 'c')
        expected = False
        result = c2 < c1
        self.assertEqual(expected, result)

    """
    Tests for to_card(string)
    """

    def test_tocard_As_returnsAs(self):
        string = 'As'
        rank = 'A'
        suit = 's'
        result = card.to_card(string)
        self.assertEqual(rank, result.rank)
        self.assertEqual(suit, result.suit)

    def test_tocard_AA_returnsAs(self):
        string = 'AA'
        self.assertRaises(Exception, card.to_card, string)
