import unittest
import card
import blinds
import draw5
import gameround
import test_table


class TestGameRound(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        STAKES = blinds.limit['50/100']
        g = draw5.Draw5Game('FIVE CARD DRAW', STAKES, 6, 'HUMAN')
        g._table = test_table.make_table(6)
        g._table.randomize_button()
        self.r = gameround.Round(g)

    """
    Tests for __init__ and table construction
    """

    """
    Tests for __str__()
    """
    # New round - pot displayed as $0
    def test_str_newround_returns0(self):
        expected = 'Pot: $0'
        result = str(self.r)
        self.assertEqual(expected, result)

    """
    Tests for do_players_have_cards():
    """
    # Players have no cards, returns False
    def test_doplayershavecards_nocards_returnsFalse(self):
        expected = False
        result = self.r.do_players_have_cards()
        self.assertEqual(expected, result)

    # 1 player has cards, returns True
    def test_doplayershavecards_allhavecards_returnsTrue(self):
        self.r.deal_cards(1)
        expected = True
        result = self.r.do_players_have_cards()
        self.assertEqual(expected, result)

    """
    Tests for deal_cards(qty, faceup=False)
    """
    # 6 players, deal 1 - should be 6 cardholders
    def test_dealcards_deal1to6players_6cardholders(self):
        self.r.deal_cards(1)
        expected = 6
        result = len(self.r.tbl.get_cardholders())
        self.assertEqual(expected, result)

    # 6 players, deal 1 - decksize == 48
    def test_dealcards_deal1to6players_decksize48(self):
        self.r.deal_cards(1)
        expected = 46
        result = len(self.r.d)
        self.assertEqual(expected, result)

    # 6 players, deal 1 (no keyword arg) - cards are hidden
    def test_dealcards_deal1to6players_cardsarehidden(self):
        self.r.deal_cards(1)
        for s in self.r.tbl:
            expected = 0
            result = len(s.get_upcards())
            self.assertEqual(expected, result)

    # 6 players, deal 1 (faceup=True) - cards are faceup
    def test_dealcards_deal1to6players_faceup_cardsarenothidden(self):
        self.r.deal_cards(1, faceup=True)
        for s in self.r.tbl:
            self.assertFalse(s._hand.cards[0].hidden)

    """
    Tests for muck_all_cards()
    """
    # 6 players, deal 1 - no cardholders after running
    def test_muckallcards_cardsmucked_nocardholders(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r.tbl.get_cardholders())
        self.assertEqual(expected, result)

    # 6 players, deal 1 - verify_muck is True after running
    def test_muckallcards_cardsmucked_verifymuckreturnsTrue(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = True
        result = self.r.verify_muck()
        self.assertEqual(expected, result)

    # 6 players, deal 1 - decksize == 0 after running
    def test_muckallcards_cardsmucked_decksize0(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r.d)
        self.assertEqual(expected, result)

    # 6 players, deal 1 - muck size == 52 after running
    def test_muckallcards_cardsmucked_mucksize52(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 52
        result = len(self.r.muck)
        self.assertEqual(expected, result)

    # 6 players, deal 1 - do_players_have_cards == False after running
    def test_muckallcards_cardsmucked_playersdonothavecards(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = False
        result = self.r.do_players_have_cards()
        self.assertEqual(expected, result)

    """
    Tests for verify_muck()
    """
    # All cards mucked, but 1 card in deck, returns False
    def test_verifymuck_1cardindeck_returnsFalse(self):
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r.d.cards.append(c)
        expected = False
        result = self.r.verify_muck()
        self.assertEqual(expected, result)

    # All cards mucked, but 1 player w cards, returns False
    def test_verifymuck_1playerwithcards_returnsFalse(self):
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r.tbl.seats[0].add_card(c)
        expected = False
        result = self.r.verify_muck()
        self.assertEqual(expected, result)

    # All cards mucked, but card in muck deleted, returns False
    def test_verifymuck_1poppedfrommuck_returnsFalse(self):
        self.r.muck_all_cards()
        self.r.muck.pop(0)
        expected = False
        result = self.r.verify_muck()
        self.assertEqual(expected, result)

    """
    Tests for remove_broke_players()
    """
    # 6 players, all with chips, returns empty list
    # 1 broke player, returns the player in a list
    # 6 players, all broke, table is empty.

    """
    Tests for get_valueplayer_list()
    """

    """
    Tests for showdown()
    """

    """
    Tests for process_sidepots(handlist)
    """

    """
    Tests for determine_eligibility(handlist, pot, stack)
    """

    """
    Tests for process_allins()
    """

    """
    Tests for make_sidepot(stacksize)
    """

    """
    Tests for award_pot(winners, amt)
    """

    """
    Tests for post_antes()
    """

    """
    Tests for post_blinds()
    """

    """
    Tests for setup_betting()
    """

    """
    Tests for betting()
    """

    """
    Tests for process_option(option)
    """

    """
    Tests for menu(options=None)
    """

    """
    Tests for get_options(cost)
    """

    """
    Tests for determine_bringin(gametype)
    """

################################################################
# Not in the round class

    """
    Tests for calc_odds(bet, pot)
    """

    """
    Tests for
    """
