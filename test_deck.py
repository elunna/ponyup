import unittest
import Deck


class TestDeck(unittest.TestCase):
    def testval_A_returns14(self):
        c = card.Card('A', 's')
        expected = 14
        result = c.val()
        self.assertEqual(expected, result)

    def testGreaterthan_HighToLow_returnsFalse(self):
        high = card.Card('A', 's')
        low = card.Card('K', 's')
        expected = True
        result = high > low
        self.assertEqual(expected, result)

    def testinit_invalidsuit_raiseEx(self):
        self.assertRaises(ValueError, card.Card, 'A', 'a')
        # failUnlessRaises is deprecated!
        # self.failUnlessRaises(ValueError, card.Card, 'A', 'a')


if __name__ == "__main__":
    unittest.main('-v')
