import unittest
import war
import card


class TestWar(unittest.TestCase):
    def testgetGameState_tie_returns0(self):
        p = [[], []]
        expected = 0
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    def testgetGameState_player2nocards_returns1(self):
        p = war.get_players()
        p[1] = []
        expected = 1
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    def testgetGameState_player1nocards_returns2(self):
        p = war.get_players()
        p[0] = []
        expected = 2
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    def testgetGameState_bothhavecards_returnsNeg1(self):
        p = war.get_players()
        expected = -1
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    def test_getPlayers_sizesAreEqual(self):
        p = war.get_players()
        expected = True
        result = len(p[0]) == len(p[1])
        self.assertEqual(expected, result)

    def testGetWinner_player1win_return1(self):
        hi = card.Card('A', 's')
        lo = card.Card('2', 's')
        p = [[hi], [lo]]
        expected = 1
        result = war.get_winner(p)
        self.assertEqual(expected, result)

    def testGetWinner_player2win_return2(self):
        hi = card.Card('A', 's')
        lo = card.Card('2', 's')
        p = [[lo], [hi]]
        expected = 2
        result = war.get_winner(p)
        self.assertEqual(expected, result)

    def testGetWinner_tie_return0(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('A', 'c')
        p = [[c1], [c2]]
        expected = 0
        result = war.get_winner(p)
        self.assertEqual(expected, result)

    #  def testAwardSpoils_As_player1containsAs(self):
    #  def testGetSpoils_0qty_returnEmptyList(self):
    #  def testGetSpoils_playerHasLessThanQty_raiseException(self):
    #  def testDisplayCards_As_showAs(self):

if __name__ == "__main__":
    unittest.main()
