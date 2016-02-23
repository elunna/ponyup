import unittest
import card


class TestCards(unittest.TestCase):
    """
    def val_JOKER_returns15(self):
        c = card.Card('X', 's')
        expected = 15
        result = c.val()
        self.assertEqual(expected, result)
    """

    def testval_A_returns14(self):
        c = card.Card('A', 's')
        expected = 14
        result = c.val()
        self.assertEqual(expected, result)

    def testval_K_returns13(self):
        instance = card.Card('K', 's')
        expected = 13
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_Q_returns12(self):
        instance = card.Card('Q', 's')
        expected = 12
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_J_returns11(self):
        instance = card.Card('J', 's')
        expected = 11
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_T_returns10(self):
        instance = card.Card('T', 's')
        expected = 10
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_9_returns9(self):
        instance = card.Card('9', 's')
        expected = 9
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_8_returns8(self):
        instance = card.Card('8', 's')
        expected = 8
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_7_returns7(self):
        instance = card.Card('7', 's')
        expected = 7
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_6_returns6(self):
        instance = card.Card('6', 's')
        expected = 6
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_5_returns5(self):
        instance = card.Card('5', 's')
        expected = 5
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_4_returns4(self):
        instance = card.Card('4', 's')
        expected = 4
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_3_returns3(self):
        instance = card.Card('3', 's')
        expected = 3
        result = instance.val()
        self.assertEqual(expected, result)

    def testval_2_returns2(self):
        instance = card.Card('2', 's')
        expected = 2
        result = instance.val()
        self.assertEqual(expected, result)

    def testLessthan_HighToLow_returnsFalse(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = False
        result = high < low
        self.assertEqual(expected, result)

    def testLessthan_LowToHigh_returnsTrue(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = True
        result = low < high
        self.assertEqual(expected, result)

    def testLessthan_SameRanks_returnsFalse(self):
        c1 = card.Card('K', 's')
        c2 = card.Card('K', 'c')
        expected = False
        result = c2 < c1
        self.assertEqual(expected, result)

    def testGreaterthan_HighToLow_returnsFalse(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = True
        result = high > low
        self.assertEqual(expected, result)

    def testGreaterthan_LowToHigh_returnsTrue(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = False
        result = low > high
        self.assertEqual(expected, result)

    def testGreaterthan_SameRanks_returnsFalse(self):
        c1 = card.Card('K', 's')
        c2 = card.Card('K', 'c')
        expected = False
        result = c2 > c1
        self.assertEqual(expected, result)

    def testEquals_SameCard_returnsTrue(self):
        """ __equals__ tests that the two cards have exactly the same suit and rank."""
        c1 = card.Card('A', 's')
        c2 = card.Card('A', 's')
        expected = True
        result = c1 == c2
        self.assertEqual(expected, result)

    def testEquals_DiffSuits_returnsFalse(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('A', 'c')
        expected = False
        result = c1 == c2
        self.assertEqual(expected, result)

    def testinit_invalidsuit_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 'A', 'a')
        # failUnlessRaises is deprecated!
        # self.failUnlessRaises(ValueError, card.Card, 'A', 'a')

    def testinit_invalidrank_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 'Y', 's')
        # failUnlessRaises is deprecated!
        # self.failUnlessRaises(ValueError, card.Card, 'Y', 's')

    def testinit_invalidboth_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 's', 'A')

    def testinit_uppercaseSuit_suitIsLowercase(self):
        c = card.Card('A', 'S')
        expected = 's'
        result = c.suit
        self.assertEqual(expected, result)

    def testinit_default_hiddenIsTrue(self):
        c = card.Card('A', 's')
        expected = True
        result = c.hidden
        self.assertEqual(expected, result)

    def teststr_hiddenCard_returnsXx(self):
        c = card.Card('A', 's')
        expected = 'Xx'
        result = str(c)
        self.assertEqual(expected, result)

    def teststr_FaceupAs_returnsAs(self):
        c = card.Card('A', 's')
        c.hidden = False
        expected = 'As'
        result = str(c)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main('-v')
