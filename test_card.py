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

    def testEquals_EqualCards_returnsTrue(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('A', 'c')
        expected = 0
        result = c1 ==c2
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
