import unittest
import deck
import card


class TestDeck(unittest.TestCase):
    def testinit_nocards_stddeckwithsize52(self):
        d = deck.Deck()
        expected = 52
        result = len(d)
        self.assertEqual(expected, result)

    def testinit_2cards_haslen2(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('K', 's'))
        d = deck.Deck(cards)
        expected = 2
        result = len(d)
        self.assertEqual(expected, result)

    def testsort_2cards_deuceisfirst(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('2', 's'))
        d = deck.Deck(cards)
        d.sort()
        expected = '2'
        result = d.cards[0].rank
        self.assertEqual(expected, result)

    def testdeal_stddeck_sizeIs51(self):
        d = deck.Deck()
        d.deal()
        expected = 51
        result = len(d)
        self.assertEqual(expected, result)

    def testremove_rmAs_sizeIs51(self):
        d = deck.Deck()
        c = card.Card('A', 's')
        d.remove(c)
        expected = 51
        result = len(d)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
