import unittest
import war


class TestWar(unittest.TestCase):
    def testgetwin_tie_returns0(self):
        p = [[], []]
        expected = 0
        result = war.getwin(p)
        self.assertEqual(expected, result)

    def testgetwin_player2nocards_returns1(self):
        p = war.get_players()
        p[1] = []
        expected = 1
        result = war.getwin(p)
        self.assertEqual(expected, result)

    def testgetwin_player1nocards_returns2(self):
        p = war.get_players()
        p[0] = []
        expected = 2
        result = war.getwin(p)
        self.assertEqual(expected, result)

    def testgetwin_bothhavecards_returnsNeg1(self):
        p = war.get_players()
        expected = -1
        result = war.getwin(p)
        self.assertEqual(expected, result)

    def test_getPlayers_sizesAreEqual(self):
        p = war.get_players()
        expected = True
        result = len(p[0]) == len(p[1])
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
