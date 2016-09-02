import unittest
import stud
import testtools


class TestStud(unittest.TestCase):
    """
    Tests for bring(table, gametype):
    """
    # stud5: 6 players, seat 5 has lowest card, 9
    def test_bringin_seat6islow_returns6(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 0)
        expected = 5
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # 2 players have the same rank, clubs gets it.
    def test_bringin_tiedcards_seat1haslowersuit_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 2)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # 3 players have the same rank, clubs gets it.
    # 4 players have the same rank, clubs gets it.
