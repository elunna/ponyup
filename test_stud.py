import unittest
import poker
import tools
import session_factory
import stud


class TestStud(unittest.TestCase):
    # Level 2: Ante $0.50, Bringin $1, Small bet $2
    def setUp(self, level=2, players=6):
        self.g = session_factory.factory(seats=players, game="FIVE CARD STUD", blindlvl=level)
        self.r = poker.Round(self.g)

    def givehand(self, seat, hand):
        self.r._table.seats[seat].hand.cards = tools.make(hand)
        # Hide the 1st card
        self.r._table.seats[seat].hand.cards[0].hidden = True

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
        self.r._table.set_bringin()
        expected = 0
        result = stud.highhand(self.r._table)
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_AceHigh_return0(self):
        self.setUp(players=4)
        self.givehand(0, 'QKA_v1')
        self.givehand(1, 'JTQ')
        self.givehand(2, '89J')
        self.givehand(3, '567')
        self.r._table.set_bringin()
        expected = 0
        result = stud.highhand(self.r._table)
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_3cards_2tied_return02(self):
        self.setUp(players=3)
        self.givehand(0, '2AA_v1')
        self.givehand(1, '2KK')
        self.givehand(2, '2AA_v2')  # Ad is bringin; dealt first
        self.r._table.set_bringin()
        expected = 2
        result = stud.highhand(self.r._table)
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_2tied_return02(self):
        self.setUp(players=4)
        self.givehand(0, 'QKA_v1')  # Dealt first on 4th street
        self.givehand(1, 'JTQ')
        self.givehand(2, 'QKA_v2')
        self.givehand(3, '567')     # Bringin
        self.r._table.set_bringin()
        expected = 0
        result = stud.highhand(self.r._table)
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
        self.r._table.set_bringin()
        expected = 0
        result = stud.highhand(self.r._table)
        self.assertEqual(expected, result)
