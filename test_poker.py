import unittest
import blinds
import draw5
import card
import poker
import setup_table


class TestGame(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        STAKES = blinds.Blinds()
        g = draw5.Draw5Session('FIVE CARD DRAW', STAKES, 6)
        g._table = setup_table.test_table(6)
        self.r = poker.Round(g)

    """
    Tests for __str__()
    """
    # New round - pot = 0
    def test_newround_potis0(self):
        expected = 0
        result = self.r.pot
        self.assertEqual(expected, result)

    """
    Tests for deal_cards(qty, faceup=False)
    """
    # 6 players, deal 1 - should be 6 cardholders
    def test_dealcards_deal1to6players_6cardholders(self):
        self.r._table.move_button()
        self.r.deal_cards(1)
        expected = 6
        result = len(self.r._table.get_players(CARDS=True))
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
        for s in self.r._table:
            expected = 0
            result = len(s.get_upcards())
            self.assertEqual(expected, result)

    # 6 players, deal 1 (faceup=True) - cards are faceup
    def test_dealcards_deal1to6players_faceup_cardsarenothidden(self):
        self.r.deal_cards(1, faceup=True)
        for s in self.r._table:
            self.assertFalse(s._hand.cards[0].hidden)

    """
    Tests for sortcards()
    """

    """
    Tests for muck_all_cards()
    """
    # 6 players, deal 1 - no cardholders after running
    def test_muckallcards_cardsmucked_nocardholders(self):
        self.r._table.move_button()
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r._table.get_players(CARDS=True))
        self.assertEqual(expected, result)

    # 6 players, deal 1 - verify_muck is True after running
    def test_muckallcards_cardsmucked_verifymuckreturnsTrue(self):
        self.r._table.move_button()
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
        self.r._table.move_button()
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r._table.seats[0].add_card(c)
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
    Tests for post_antes()
    """
    # 6 players ante 1. Pot == 6.
    def test_postantes_6players_potequals60(self):
        STAKES = blinds.Blinds(level=2)
        g = draw5.Draw5Session('FIVE CARD DRAW', STAKES, 6, 'HUMAN')
        g._table = setup_table.test_table(6)
        self.r = poker.Round(g)
        self.r.post_antes()
        expected = 6
        result = self.r.pot
        self.assertEqual(expected, result)

    # Initial stacks=1000. Ante=1. After ante are 999.
    def test_postantes_6players_stacksequal999(self):
        STAKES = blinds.Blinds(level=2)
        g = draw5.Draw5Session('FIVE CARD DRAW', STAKES, 6, 'HUMAN')
        g._table = setup_table.test_table(6)
        self.r = poker.Round(g)
        self.r.post_antes()
        expected = 999
        for p in self.r._table:
            result = p.chips
            self.assertEqual(expected, result)

    """
    Tests for post_blinds()
    """
    # If the button(and blinds haven't been set, raise an exception.)
    def test_postblinds_btnnotset_raiseException(self):
        self.assertEqual(self.r._table.TOKENS['D'], -1, 'Button should be -1!')
        self.assertRaises(Exception, self.r.post_blinds)

    # 2 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_2players_pot3(self):
        for i in [1, 2, 4, 5]:
            self.r._table.remove_player(i)
        self.r._table.move_button()  # verify the button is 0
        self.assertEqual(self.r._table.TOKENS['D'], 0)
        self.r.post_blinds()
        self.assertEqual(self.r._table.seats[0].chips, 999)
        self.assertEqual(self.r._table.seats[3].chips, 998)
        self.assertEqual(self.r.pot, 3)

    # 3 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_3players_pot3(self):
        for i in [1, 3, 5]:
            self.r._table.remove_player(i)
        self.r._table.move_button()  # verify the button is 0
        self.assertEqual(self.r._table.TOKENS['D'], 0)
        self.r.post_blinds()
        self.assertEqual(self.r._table.seats[2].chips, 999)
        self.assertEqual(self.r._table.seats[4].chips, 998)
        self.assertEqual(self.r.pot, 3)

    # 6 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_6players_pot3(self):
        self.r._table.move_button()  # verify the button is 0
        self.assertEqual(self.r._table.TOKENS['D'], 0)
        self.r.post_blinds()
        self.assertEqual(self.r._table.seats[1].chips, 999)
        self.assertEqual(self.r._table.seats[2].chips, 998)
        self.assertEqual(self.r.pot, 3)

    # 6 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_6players_returnsString(self):
        self.r._table.move_button()  # verify the button is 0
        expected = 'bob1 posts $1\nbob2 posts $2\n'
        result = self.r.post_blinds()
        self.assertEqual(expected, result)

    """
    Tests for setup_betting()
    """
    # 2 players. SB and BTN should be together.
    # 2 players. BB is not BTN.

    """
    Tests for process_sidepots(handlist)
    """

    """
    Tests for eligible_for_pot(handlist, pot, stack)
    """

    """
    Tests for get_allin_stacks()
    """
    # No allins, returns empty list
    # 1 allin, returns list with 1 stack size.
    # 2 allins, returns list with 2 stack sizes.

    """
    Tests for process_allins()
    """

    """
    Tests for make_sidepot(stacksize)
    """

    """
    Tests for split_pot(winners, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    # Award 2 players 100 chips. Each stack goes up 50
    # Award 2 players -100 chips. Raise exception.

    """
    Tests for betting_round()
    """
    # Export the invested variable to betting.has_invested(player)
    # Export the cost variable.

    """
    Tests for process_option(option)
    """
    # CHECK - bet level is same
    # CHECK - Players chips stay the same
    # FOLD - player doesn't have cards
    # FOLD - Players chips stay the same
    # BET - bet level is raised by one
    # BET - Players chips are diminished by the bet amount
    # RAISE - bet level is raised by one
    # RAISE - Players chips are diminished by the raiseamount
    # CHECK - bet level is same
    # COMPLETE - Players chips are diminished by the bet amount

    """
    Tests show_cards()
    """
    # Deal cards to 2 players, should be able to see CPU cards

    """
    Tests for showdown()
    """
