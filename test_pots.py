import unittest
import evaluator
import pots
import table_factory
import tools


class TestPots(unittest.TestCase):
    """
    Tests for invested(player)
    """
    def setUp(self, level=2, players=6):
        # Make a 6 player table
        self.t = table_factory.factory(seats=players)
        self.p = pots.Pot(self.t)
        # Deal cards to all players
        tools.deal_random_cards(self.t, 2)

    def setup_allins(self, _seats):
        self.t = table_factory.factory(seats=_seats, stepstacks=True)
        self.p = pots.Pot(self.t)

        # Deal cards to all players
        tools.deal_random_cards(self.t, 2)

    def everybody_bet(self, bet):
        for s in self.t:
            self.p += s.bet(bet)

    def get_generic_table(self, seats=6):
        return table_factory.factory(
                seats=seats, heroname='octavia', stepstacks=True
        )

    """
    Tests for __add__(amt)
    """
    def test_add_10tonewpot_potequals10(self):
        bet = 10
        expected = 10
        self.p = self.p + bet
        result = self.p
        self.assertEqual(expected, result)

    # Cannot add a negative amount
    def test_add_neg10_raisesException(self):
        bet = -10
        self.assertRaises(ValueError, self.p.__add__, bet)

    """
    Tests for __iadd__(amt)
    """
    def test_iadd_10tonewpot_potequals10(self):
        bet = 10
        expected = 10
        self.p += bet
        result = self.p
        self.assertEqual(expected, result)

    # Cannot add a negative amount
    def test_iadd_neg10_raisesException(self):
        bet = -10
        self.assertRaises(ValueError, self.p.__iadd__, bet)

    """
    Tests for invested(self, seat):
    """
    # New table - player has invested nothing.
    def test_invested_nobets_returns0(self):
        expected = 0
        result = self.p.invested(self.t.seats[0])
        self.assertEqual(expected, result)

    # After betting 100 - player invested 100.
    def test_invested_bet100_returns100(self):
        expected = 100
        self.t.seats[0].bet(100)
        result = self.p.invested(self.t.seats[0])
        self.assertEqual(expected, result)

    """
    Tests for allin_stacks()
    """
    # 2 players, 1 allin
    def test_allinstacks_2plyr_1allin_returns1(self):
        self.setup_allins(2)
        self.everybody_bet(100)
        expected = 1
        result = len(self.p.allin_stacks())
        self.assertEqual(expected, result)

    # 3 players, 1 allin
    def test_allinstacks_3plyr_1allin_returns1(self):
        self.setup_allins(3)
        self.everybody_bet(100)
        expected = 1
        result = len(self.p.allin_stacks())
        self.assertEqual(expected, result)

    # 3 players, 2 allins
    def test_allinstacks_3plyr_2allin_returns2(self):
        self.setup_allins(3)
        self.everybody_bet(200)
        expected = 2
        result = len(self.p.allin_stacks())
        self.assertEqual(expected, result)

    # 4 players, 3 allins
    def test_allinstacks_4plyr_3allin_returns3(self):
        self.setup_allins(4)
        self.everybody_bet(300)
        expected = 3
        result = len(self.p.allin_stacks())
        self.assertEqual(expected, result)

    """
    Tests for make_sidepots(self, _stacks):
    """
    # 2 players, 1 allin
    def test_makesidepots_2plyr_1allin_returns1sidepot(self):
        self.setup_allins(2)
        expected = {100: 200}
        self.everybody_bet(100)
        result = self.p.make_sidepots()
        self.assertEqual(expected, result)

    # 3 players, 1 allin
    def test_makesidepots_3plyr_1allin_returns1sidepot(self):
        self.setup_allins(3)
        expected = {100: 300}
        self.everybody_bet(100)
        result = self.p.make_sidepots()
        self.assertEqual(expected, result)

    # 3 players, 2 allins
    def test_makesidepots_3plyr_2allin_returns2sidepot(self):
        self.setup_allins(3)
        expected = {100: 300, 200: 200}
        self.everybody_bet(200)
        result = self.p.make_sidepots()
        self.assertEqual(expected, result)

    # 4 players, 3 allins
    def test_makesidepots_4plyr_3allin_returns3sidepot(self):
        self.setup_allins(4)
        expected = {100: 400, 200: 300, 300: 200}
        self.everybody_bet(300)
        result = self.p.make_sidepots()
        self.assertEqual(expected, result)

    # 5 players, 2 allins, challenge stack sizes.
    def test_makesidepots_4plyr_2allin_returns2sidepot(self):
        # Setup a problem situation
        self.t = self.get_generic_table(4)
        stacks = [1000, 1000, 225, 100]
        for s in self.t:
            s.stack = stacks.pop(0)

        self.p = pots.Pot(self.t)
        tools.deal_random_cards(self.t)
        self.everybody_bet(300)

        expected = {100: 400, 225: 375}
        result = self.p.make_sidepots()
        self.assertEqual(expected, result)

    """
    Tests for calc_sidepot(stacksize):
    """
    # 2 players, 1 allin
    def test_calcsidepot_2plyr_allinfor100_returns200(self):
        self.setup_allins(2)
        expected = 200
        self.everybody_bet(100)
        result = self.p.calc_sidepot(100)
        self.assertEqual(expected, result)

    # 3 players, 1 allin
    def test_calcsidepot_3plyr_allinfor100_returns300(self):
        self.setup_allins(3)
        expected = 300
        self.everybody_bet(100)
        result = self.p.calc_sidepot(100)
        self.assertEqual(expected, result)

    # 3 players, 2 allin
    def test_calcsidepot_3plyr_allinfor200_returns500(self):
        self.setup_allins(3)
        expected = 500
        self.everybody_bet(200)
        result = self.p.calc_sidepot(200)
        self.assertEqual(expected, result)

    """
    Tests for process_sidepots(sidepots)
    """
    # 2 players, 2 allins.
    def test_processsidepots_2players(self):
        self.setup_allins(2)
        tools.deal_ranked_hands(self.t)
        self.everybody_bet(200)
        sidepots = self.p.make_sidepots()

        expected = {200: [0], 100: [1]}
        result = self.p.process_sidepots(sidepots)
        self.assertEqual(expected, result)

    # 3 players, 3 allins.
    def test_processsidepots_3players(self):
        self.setup_allins(3)
        tools.deal_ranked_hands(self.t)
        self.everybody_bet(300)
        # seat 0 gets strongest hand, 1 gets middle, 2 gets lowest.
        sidepots = self.p.make_sidepots()

        expected = {300: [0], 200: [1], 100: [2]}
        result = self.p.process_sidepots(sidepots)
        self.assertEqual(expected, result)

    # If noone has cards, raise an exception.

    """
    Tests for eligible(self, stack_req):
    """
    def test_geteligible_3players_req100_returns3players(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 100
        expected = 3
        result = len(self.p.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req200_returns2players(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 200
        expected = 2
        result = len(self.p.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req300_returns1player(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 300
        expected = 1
        result = len(self.p.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req300_correctplayer(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 300
        expected = [self.t.seats[2]]
        result = self.p.get_eligible(required_stack)
        self.assertEqual(expected, result)

    """
    Tests for eligible_for_pot(self, stack_required):
    """

    """
    Tests for split_pot(winners, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    def test_splitpot_100to1player_awardis100(self):
        p = self.t.seats[0]
        pot = 100
        expected = {0: 100}
        result = self.p.split_pot([p.NUM], pot)
        self.assertEqual(expected, result)

    # Award 2 players 100 chips. Each stack goes up 50
    def test_splitpot_100to2player_awardeach50(self):
        p1 = self.t.seats[0]
        p2 = self.t.seats[1]
        pot = 100
        expected = {0: 50, 1: 50}
        result = self.p.split_pot([p1.NUM, p2.NUM], pot)
        self.assertEqual(expected, result)

    def test_splitpot_101to2player_awardeach50(self):
        self.t.move_button()
        p1 = self.t.seats[0]
        p2 = self.t.seats[1]
        self.assertEqual(self.t.TOKENS['D'], 0)
        pot = 101
        expected = {0: 50, 1: 51}
        result = self.p.split_pot([p1.NUM, p2.NUM], pot)
        self.assertEqual(expected, result)

    # Award 2 players -100 chips. Raise exception.
    def test_splitpot_neg100_raisesException(self):
        p1 = self.t.seats[0]
        p2 = self.t.seats[1]
        pot = -100
        self.assertRaises(ValueError, self.p.split_pot, [p1.NUM, p2.NUM], pot)

    """
    Tests for process_awards(self, award_dict):
    """

    """
    Tests for valid_sidepots(self, sidepots):
    """

################################
# Independent Functions
    """
    Tests for award_pot(player, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    def test_awardpot_100to1player_stackincreases100(self):
        p = self.t.seats[0]
        expected = 100
        p_stack = p.stack
        pots.award_pot(p, expected)
        result = p.stack - p_stack
        self.assertEqual(expected, result)

    # Try awarding -100. Should raise an exception.
    def test_awardpot_neg100_raisesException(self):
        p = self.t.seats[0]
        award = -100
        self.assertRaises(ValueError, pots.award_pot, p, award)

    # Try awarding a player with no cards. Should raise an exception.
    def test_awardpot_playerhasnocards_raisesException(self):
        p = self.t.seats[0]
        p.fold()
        self.assertRaises(ValueError, pots.award_pot, p, 100)

    """
    Tests for best_hand_val()
    # Note we'll use the table with the hand values reversed,
    # so that 0 has the lowest hand, 1 has better, 2 beats 1, etc.
    """

    # 2 players: should be pair_low
    def test_besthandval_2players_lowpair(self):
        self.setup_allins(2)
        tools.deal_ranked_hands(self.t, _rev=True)
        players = self.t.get_players(hascards=True)

        expected = evaluator.get_value(tools.make('pair_low'))
        result = pots.best_hand_val(players)
        self.assertEqual(expected, result)

    # 3 players: should be pair_high
    def test_besthandval_3players_highpair(self):
        self.setup_allins(3)
        tools.deal_ranked_hands(self.t, _rev=True)
        players = self.t.get_players(hascards=True)

        expected = evaluator.get_value(tools.make('pair_high'))
        result = pots.best_hand_val(players)
        self.assertEqual(expected, result)

    # 4 players: should be two pair
    def test_besthandval_4players_twopair(self):
        self.setup_allins(4)
        tools.deal_ranked_hands(self.t, _rev=True)
        players = self.t.get_players(hascards=True)

        expected = evaluator.get_value(tools.make('twopair_high'))
        result = pots.best_hand_val(players)
        self.assertEqual(expected, result)

    # 5 players: should be trips
    def test_besthandval_5players_trips(self):
        self.setup_allins(5)
        tools.deal_ranked_hands(self.t, _rev=True)
        players = self.t.get_players(hascards=True)

        expected = evaluator.get_value(tools.make('trips_high'))
        result = pots.best_hand_val(players)
        self.assertEqual(expected, result)

    # 5 players: should be straight
    def test_besthandval_6players_straight(self):
        self.setup_allins(6)
        tools.deal_ranked_hands(self.t, _rev=True)
        players = self.t.get_players(hascards=True)

        expected = evaluator.get_value(tools.make('straight_high'))
        result = pots.best_hand_val(players)
        self.assertEqual(expected, result)

    """
    Tests for calc_odds(bet ,pot)
    """
    # bet cannot be negative
    def test_calcodds_negbet_raiseEx(self):
        self.assertRaises(ValueError, pots.calc_odds, -10, 10)

    # pot cannot be negative
    def test_calcodds_negpot_raiseEx(self):
        self.assertRaises(ValueError, pots.calc_odds, 10, -10)

    # bet = 5, pot = 10, we are getting 2-to-1 odds.
    def test_calcodds_pot10_bet5_returns2(self):
        expected = 2.0
        result = pots.calc_odds(5, 10)
        self.assertEqual(expected, result)
