import unittest
import war
import card


class TestWar(unittest.TestCase):

    def setUp(self):
        self.w = war.War()
    """
    Tests for __init__()
    """
    # Make sure the decks are shuffled???

    # make sure both players start with 27 cards
    def test_init_player1_has27cards(self):
        expected = 27
        result = len(self.w.plyr[1])
        self.assertEqual(expected, result)

    def test_init_player2_has27cards(self):
        expected = 27
        result = len(self.w.plyr[2])
        self.assertEqual(expected, result)

    # Make sure both players have equal decks
    def test_init_bothareequalsize(self):
        expected = True
        result = len(self.w.plyr[1]) == len(self.w.plyr[2])
        self.assertEqual(expected, result)

    """
    Tests for get_gamestate(players)
    """
    def test_get_gamestate_tie_returns0(self):
        p = [[], []]
        expected = 0
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    def test_get_gamestate_player2nocards_returns1(self):
        p = war.get_players()
        p[1] = []
        expected = 1
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    def test_get_gamestate_player1nocards_returns2(self):
        p = war.get_players()
        p[0] = []
        expected = 2
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    def test_get_gamestate_bothhavecards_returnsneg1(self):
        p = war.get_players()
        expected = -1
        result = war.get_gamestate(p)
        self.assertEqual(expected, result)

    """
    Tests for get_winner(players)
    """
    def test_GetWinner_player1win_return1(self):
        hi = card.Card('A', 's')
        lo = card.Card('2', 's')
        p = [[hi], [lo]]
        expected = 1
        result = war.get_winner(p)
        self.assertEqual(expected, result)

    def test_GetWinner_player2win_return2(self):
        hi = card.Card('A', 's')
        lo = card.Card('2', 's')
        p = [[lo], [hi]]
        expected = 2
        result = war.get_winner(p)
        self.assertEqual(expected, result)

    def test_GetWinner_tie_return0(self):
        c1 = card.Card('A', 's')
        c2 = card.Card('A', 'c')
        p = [[c1], [c2]]
        expected = 0
        result = war.get_winner(p)
        self.assertEqual(expected, result)

    """
    Tests for display_cards(cardlist)
    """
    # Try displaying an empty list, returns empty string.
    # Passing As card, returns 'As'
    # Passing As, Ks, returns 'As Ks'

    """
    Tests for show_topcards(players)
    # No players have cards. Exception?
    # As vs Ks, returns 'As vs Ks'
    """

    """
    Tests for award_cards(plyr, spoils)
    """
    # Award a pile of 1 card - players pile increases by 1.
    # Award a pile of 1 card - players pile contains the card.

    """
    Tests for get_spoils(players, qty)
    """

    """
    Tests for playround(players, warlevel)
    """

    """
    Tests for def get_wartext(level)
    """

    """
    Tests for war(players, level, spoils)
    """

    """
    Tests for gameloop(players)
    """


if __name__ == "__main__":
    unittest.main()
