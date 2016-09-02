import unittest
import blinds
import card
import draw5
import evaluator
import poker
import pokerhands
import testtools

STAKES = blinds.Blinds()


class TestPoker(unittest.TestCase):
    """
    poker.Session #############################################
    """

    """
    poker.Round   #############################################
    """

    """
    Setup a session and round, with a table filled with 6 players.
    """
    def setUp(self):
        self.g = draw5.Draw5Session('FIVE CARD DRAW', STAKES, 6)
        self.g._table = testtools.test_table(6)
        self.r = poker.Round(self.g)

    def allin_table(self, seats, REVERSED_HANDS=False):
        self.g._table = testtools.allin_table(seats, REVERSED_HANDS)
        self.r = poker.Round(self.g)

    def allin_situation1(self, seats, REVERSED_HANDS=False):
        self.r = poker.Round(g)

    def everybody_bet(self, bet):
        for p in self.r._table:
            self.r.pot += p.bet(bet)

    # New round - pot = 0
    def test_newround_potis0(self):
        expected = 0
        result = self.r.pot
        self.assertEqual(expected, result)

    """
    Tests for __str__()
    """
    # None yet.

    """
    Tests for deal_cards(qty, faceup=False)
    """
    # 6 players, deal 1 - should be 6 cardholders
    def test_dealcards_deal1to6players_6cardholders(self):
        self.r._table.move_button()
        self.r.deal_cards(1)
        expected = 6
        result = len(self.r._table.get_players(hascards=True))
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
    Tests show_cards()
    """
    # Deal cards to 2 players, should be able to see CPU cards

    """
    Tests for sortcards()
    """
    # deal highcards1():
    #  h = [('A', 'd'), ('4', 's'), ('Q', 's'), ('7', 's'), ('K', 'h')]
    def test_sortcards_humandealt_sorted(self):
        h = pokerhands.make('highcards')
        self.r._table.seats[0]._hand.cards = h[:]
        expected = sorted(h)
        self.r.sortcards()
        result = self.r._table.seats[0]._hand.cards
        self.assertEqual(expected, result)

    """
    Tests for muck_all_cards()
    """
    # 6 players, deal 1 - no cardholders after running
    def test_muckallcards_cardsmucked_nocardholders(self):
        self.r._table.move_button()
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r._table.get_players(hascards=True))
        self.assertEqual(expected, result)

    # 6 players, deal 1 - verify_muck is True after running
    def test_muckallcards_cardsmucked_verifymuckreturnsTrue(self):
        self.r._table.move_button()
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = True
        result = self.r.check_integrity_post()
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
    Tests for post_antes()
    """
    # 6 players ante 1. Pot == 6.
    def test_postantes_6players_potequals60(self):
        STAKES = blinds.Blinds(level=2)
        g = draw5.Draw5Session('FIVE CARD DRAW', STAKES, 6, 'HUMAN')
        g._table = testtools.test_table(6)
        self.r = poker.Round(g)
        self.r.post_antes()
        expected = 6
        result = self.r.pot
        self.assertEqual(expected, result)

    # Initial stacks=1000. Ante=1. After ante are 999.
    def test_postantes_6players_stacksequal999(self):
        STAKES = blinds.Blinds(level=2)
        g = draw5.Draw5Session('FIVE CARD DRAW', STAKES, 6, 'HUMAN')
        g._table = testtools.test_table(6)
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
        self.r._table.move_button()
        self.assertEqual(self.r._table.TOKENS['D'], 0)  # verify the button is 0
        self.r.post_blinds()
        self.assertEqual(self.r._table.seats[1].chips, 999)
        self.assertEqual(self.r._table.seats[2].chips, 998)
        self.assertEqual(self.r.pot, 3)

    # 6 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_6players_returnsString(self):
        self.r._table.move_button()
        self.assertEqual(self.r._table.TOKENS['D'], 0)  # verify the button is 0
        expected = 'bob1 posts $1\nbob2 posts $2\n'
        result = self.r.post_blinds()
        self.assertEqual(expected, result)

    """
    Tests for invested(player)
    """
    # New table - player has invested nothing.
    def test_invested_nobets_returns0(self):
        expected = 0
        result = self.r.invested(self.r._table.seats[0])
        self.assertEqual(expected, result)

    # After betting 100 - player invested 100.
    def test_invested_bet100_returns100(self):
        expected = 100
        self.r._table.seats[0].bet(100)
        result = self.r.invested(self.r._table.seats[0])
        self.assertEqual(expected, result)

    """
    Tests for get_allin_stacks()
    """
    # No allins, returns empty list
    def test_getallins_none_returnsemptylist(self):
        expected = []
        result = self.r.get_allins()
        self.assertEqual(expected, result)

    # 1 allin, returns list with 1 stack size.
    def test_getallins_1allin_returns1stack(self):
        expected = [1000]
        self.r._table.seats[0].bet(1000)
        result = self.r.get_allins()
        self.assertEqual(expected, result)

    # 2 allins, returns list with 2 stack sizes.
    def test_getallins_2allin_returns2stacks(self):
        expected = [1000, 1000]
        self.r._table.seats[0].bet(1000)
        self.r._table.seats[1].bet(1000)
        result = self.r.get_allins()
        self.assertEqual(expected, result)

    """
    Tests for make_sidepots(self, _stacks):
    """
    # 2 players, 1 allin
    def test_makesidepots_2plyr_1allin_returns1sidepot(self):
        self.allin_table(2)
        expected = {100: 200}
        self.everybody_bet(100)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    # 3 players, 1 allin
    def test_makesidepots_3plyr_1allin_returns1sidepot(self):
        self.allin_table(3)
        expected = {100: 300}
        self.everybody_bet(100)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    # 3 players, 2 allins
    def test_makesidepots_3plyr_2allin_returns2sidepot(self):
        self.allin_table(3)
        expected = {100: 300, 200: 200}
        self.everybody_bet(200)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    # 4 players, 3 allins
    def test_makesidepots_4plyr_3allin_returns3sidepot(self):
        self.allin_table(4)
        expected = {100: 400, 200: 300, 300: 200}
        self.everybody_bet(300)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    """
    Tests for calc_sidepot(stacksize):
    """
    # 2 players, 1 allin
    def test_calcsidepot_2plyr_allinfor100_returns200(self):
        self.allin_table(2)
        expected = 200
        self.everybody_bet(100)
        result = self.r.calc_sidepot(100)
        self.assertEqual(expected, result)

    # 3 players, 1 allin
    def test_calcsidepot_3plyr_allinfor100_returns300(self):
        self.allin_table(3)
        expected = 300
        self.everybody_bet(100)
        result = self.r.calc_sidepot(100)
        self.assertEqual(expected, result)

    # 3 players, 2 allin
    def test_calcsidepot_3plyr_allinfor200_returns500(self):
        self.allin_table(3)
        expected = 500
        self.everybody_bet(200)
        result = self.r.calc_sidepot(200)
        self.assertEqual(expected, result)

    """
    Tests for process_sidepots(sidepots)
    """
    # 2 players, 2 allins.
    def test_processsidepots_2plyr_besthand_biggeststack_getswholepot(self):
        seats = 2
        self.allin_table(seats)
        p0, p1 = [p for p in self.r._table.seats]
        expected = {200: [p0], 100: [p1]}
        self.everybody_bet(200)
        sidepots = self.r.make_sidepots(self.r.get_allins())
        result = self.r.process_sidepots(sidepots)
        self.assertEqual(expected, result)

    # 3 players, 3 allins.
    def test_processsidepots_3plyr_besthand_biggeststack_getswholepot(self):
        seats = 3
        self.allin_table(seats)
        p0, p1, p2 = [p for p in self.r._table.seats]
        self.everybody_bet(300)
        sidepots = self.r.make_sidepots(self.r.get_allins())
        expected = {300: [p0], 200: [p1], 100: [p2]}
        result = self.r.process_sidepots(sidepots)
        self.assertEqual(expected, result)

    """
    Tests for eligible(self, stack_req):
    """
    def test_geteligible_3players_req100_returns3players(self):
        required_stack = 100
        seats = 3
        self.allin_table(seats)
        expected = 3
        result = len(self.r.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req200_returns2players(self):
        required_stack = 200
        seats = 3
        self.allin_table(seats)
        expected = 2
        result = len(self.r.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req300_returns1player(self):
        required_stack = 300
        seats = 3
        self.allin_table(seats)
        expected = 1
        result = len(self.r.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req300_correctplayer(self):
        required_stack = 300
        seats = 3
        self.allin_table(seats)
        expected = [self.r._table.seats[2]]
        result = self.r.get_eligible(required_stack)
        self.assertEqual(expected, result)

    """
    Tests for best_hand_val()
    # Note we'll use the table with the hand values reversed,
    # so that 0 has the lowest hand, 1 has better, 2 beats 1, etc.
    """
    # Out of 2 players, should have a straight
    def test_besthandval_2players_straight(self):
        seats = 2
        self.allin_table(seats, REVERSED_HANDS=True)
        players = self.r._table.get_players(hascards=True)
        expected = evaluator.get_value(pokerhands.make('straight_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # Out of 3 players, should have a flush

    def test_besthandval_3players_flush(self):
        seats = 3
        self.allin_table(seats, REVERSED_HANDS=True)
        players = self.r._table.get_players(hascards=True)
        expected = evaluator.get_value(pokerhands.make('flush_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # Out of 4 players, should have a boat
    def test_besthandval_4players_fullhouse(self):
        seats = 4
        self.allin_table(seats, REVERSED_HANDS=True)
        players = self.r._table.get_players(hascards=True)
        expected = evaluator.get_value(pokerhands.make('fullhouse_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # Out of 5 players, should have a straightflush
    def test_besthandval_5players_straightflush(self):
        seats = 5
        self.allin_table(seats, REVERSED_HANDS=True)
        players = self.r._table.get_players(hascards=True)
        expected = evaluator.get_value(pokerhands.make('straightflush_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # Out of 6 players, should have a royalflush
    def test_besthandval_6players_royalflush(self):
        seats = 6
        self.allin_table(seats, REVERSED_HANDS=True)
        players = self.r._table.get_players(hascards=True)
        expected = evaluator.get_value(pokerhands.make('royalflush'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    """
    Tests for split_pot(winners, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    # Award 2 players 100 chips. Each stack goes up 50
    # Award 2 players -100 chips. Raise exception.

    """
    Tests for showdown()
    """

    """
    Tests for award_pot(player, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    # Try awarding -100. Should raise an exception.
    # Try awarding a player with no cards. Should raise an exception.

    """
    Tests for next_street()
    """
    def test_nextstreet_street0_streetIs1(self):
        self.r.next_street()
        expected = 1
        result = self.r.street
        self.assertEqual(expected, result)

    def test_nextstreet_draw5_street2_raisesException(self):
        self.r.next_street()
        self.r.next_street()
        self.assertRaises(Exception, self.r.next_street)

    """
    Tests for check_integrity_post(self):
    """
    # All cards mucked, but 1 card in deck, returns False
    def test_checkintegritypost_1cardindeck_returnsFalse(self):
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r.d.cards.append(c)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # All cards mucked, but 1 player w cards, returns False
    def test_checkintegritypost_1playerwithcards_returnsFalse(self):
        self.r._table.move_button()
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r._table.seats[0].add_card(c)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # All cards mucked, but card in muck deleted, returns False
    def test_checkintegritypost_1poppedfrommuck_returnsFalse(self):
        self.r.muck_all_cards()
        self.r.muck.pop(0)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    """
    Tests for cleanup()
    """
    # After cleanup, there should be no broke players.
