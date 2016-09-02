import unittest
import stud
import testtools


class TestStud(unittest.TestCase):
    """
    Tests for bring(table, gametype):
    """
    # 6 players, seat 5 has lowest card, 9
    def test_bringin_seat6islow_returns6(self):
        t = testtools.test_table(6)
        testtools.deal_stud5_table(t)
        expected = 5
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    def test_bringin_tiedcards_seat1haslowersuit_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud5_table2(t)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)
