import unittest
import deck


class TestDeck(unittest.TestCase):
    def testinit_nocards_stddeckwithsize52(self):
        d = deck.Deck()
        expected = 52
        result = len(d)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
