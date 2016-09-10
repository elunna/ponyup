import unittest
import poker
import pokerhands
import stud
import testtools
import table_factory


class TestStud(unittest.TestCase):
    # Level 2: Ante $0.50, Bringin $1, Small bet $2
    def setUp(self, level=2, players=6):
        self.g = testtools.stud5_session(level, players)
        self.r = poker.Round(self.g)

    def givehand(self, seat, hand):
        self.r._table.seats[seat].hand.cards = pokerhands.make(hand)
        # Hide the 1st card
        self.r._table.seats[seat].hand.cards[0].hidden = True

    """
    Tests for bring(table, gametype):
    """
    # Stud5 deal: seat 5 has lowest card, 9
    def test_bringin_stud5_no_ties_returns5(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=0)
        expected = 5
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 2 Tied ranks
    def test_bringin_stud5_2tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=2)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 3 Tied ranks
    def test_bringin_stud5_3tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=3)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 4 Tied ranks
    def test_bringin_stud5_4tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=4)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: seat 5 has lowest card, 9
    def test_bringin_stud7_no_ties_returns6(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=0)
        expected = 5
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 2 Tied ranks
    def test_bringin_stud7_2tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=2)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 3 Tied ranks
    def test_bringin_stud7_3tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=3)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 4 Tied ranks
    def test_bringin_stud7_4tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=4)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    """
    Tests for highhand(table)
    """
    # Throw in an empty seat for testing.
    # Throw in a player without cards for testing.

    # Stud5:
    def test_highhand_3cards_pairAces_return0(self):
        self.setUp(players=3)
        self.givehand(0, '2AA_v1')
        self.givehand(1, '2KK')
        self.givehand(2, '2QQ')
        self.r._table.set_bringin(2)
        expected = 0
        result = stud.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_AceHigh_return0(self):
        self.setUp(players=4)
        self.givehand(0, 'QKA_v1')
        self.givehand(1, 'JTQ')
        self.givehand(2, '89J')
        self.givehand(3, '567')
        self.r._table.set_bringin(3)
        expected = 0
        result = stud.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_3cards_2tied_return02(self):
        self.setUp(players=3)
        self.givehand(0, '2AA_v1')
        self.givehand(1, '2KK')
        self.givehand(2, '2AA_v2')  # Ad is bringin; dealt first
        self.r._table.set_bringin(2)
        expected = 2
        result = stud.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_2tied_return02(self):
        self.setUp(players=4)
        self.givehand(0, 'QKA_v1')  # Dealt first on 4th street
        self.givehand(1, 'JTQ')
        self.givehand(2, 'QKA_v2')
        self.givehand(3, '567')     # Bringin
        self.r._table.set_bringin(3)
        expected = 0
        result = stud.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_3cards_3tied_return023(self):
        self.setUp(players=6)
        self.givehand(0, '3AK_v1')  # Dealt first on 4th street
        self.givehand(1, '3AK_v2')
        self.givehand(2, '3AK_v3')
        self.givehand(3, '345')
        self.givehand(4, '234')     # Bringin
        self.givehand(5, '245')
        self.r._table.set_bringin(4)
        expected = 0
        result = stud.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    """
    Tests for post_bringin():
    """
    # Initial stacks=1000.
    # Seat 0
    def test_postbringin_seat5_has2chipsless(self):
        testtools.deal_stud5(self.r._table, matchingranks=0)
        BI = stud.bringin(self.r._table)
        seat = self.r._table.seats[BI]
        stack = seat.stack
        stud.post_bringin(self.r)
        expected = 1
        result = stack - seat.stack
        self.assertEqual(expected, result)

    def test_postbringin_seat5_returnsString(self):
        testtools.deal_stud5(self.r._table, matchingranks=0)
        expected = 'bob5 brings it in for $1\n'
        result = stud.post_bringin(self.r)
        self.assertEqual(expected, result)
