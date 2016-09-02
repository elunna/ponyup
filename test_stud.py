import unittest
import stud
import testtools


class TestStud(unittest.TestCase):
    """
    Tests for bring(table, gametype):
    """
    # Stud5 deal: seat 5 has lowest card, 9
    def test_bringin_stud5_no_ties_returns6(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 0)
        expected = 5
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # Stud5 deal: 2 Tied ranks
    def test_bringin_stud5_2tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 2)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # Stud5 deal: 3 Tied ranks
    def test_bringin_stud5_3tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 3)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # Stud5 deal: 4 Tied ranks
    def test_bringin_stud5_4tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 4)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # Stud7 deal: seat 5 has lowest card, 9
    def test_bringin_stud7_no_ties_returns6(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 0)
        expected = 5
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # Stud7 deal: 2 Tied ranks
    def test_bringin_stud7_2tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 2)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # Stud7 deal: 3 Tied ranks
    def test_bringin_stud7_3tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 3)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)

    # Stud7 deal: 4 Tied ranks
    def test_bringin_stud7_4tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 4)
        expected = 1
        result = t.get_index(stud.bringin(t))
        self.assertEqual(expected, result)
