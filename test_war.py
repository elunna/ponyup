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
        result = len(self.w.players[1])
        self.assertEqual(expected, result)

    def test_init_player2_has27cards(self):
        expected = 27
        result = len(self.w.players[2])
        self.assertEqual(expected, result)

    # Make sure both players have equal decks
    def test_init_bothareequalsize(self):
        expected = True
        result = len(self.w.players[1]) == len(self.w.players[2])
        self.assertEqual(expected, result)

    """
    Tests for get_gamestate(players)
    """
    """
    Tests for get_winner(players)
    """
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
