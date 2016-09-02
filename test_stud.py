import unittest
import pokerhands
import stud
import testtools

HANDS_3CARD = {
    0: pokerhands.convert_to_cards(['2s', 'As', 'Ah']),
    1: pokerhands.convert_to_cards(['2h', 'Ks', 'Kh']),
    2: pokerhands.convert_to_cards(['2c', 'Qs', 'Qh']),
}

HANDS_4CARD = {
    0: pokerhands.convert_to_cards(['Qs', 'Kh', 'As']),
    1: pokerhands.convert_to_cards(['Jh', 'Ts', 'Qh']),
    2: pokerhands.convert_to_cards(['8c', '9s', 'Js']),
    2: pokerhands.convert_to_cards(['5c', '6s', '7s']),
}


def get_dealt_table(hands):
    t = testtools.test_table(len(hands))
    for k, v in hands.items():
        t.seats[k]._hand = v
    return t


class TestStud(unittest.TestCase):
    """
    Tests for bring(table, gametype):
    """
    # Stud5 deal: seat 5 has lowest card, 9
    def test_bringin_stud5_no_ties_returns6(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 0)
        expected = 5
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 2 Tied ranks
    def test_bringin_stud5_2tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 2)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 3 Tied ranks
    def test_bringin_stud5_3tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 3)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 4 Tied ranks
    def test_bringin_stud5_4tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 2, 4)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: seat 5 has lowest card, 9
    def test_bringin_stud7_no_ties_returns6(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 0)
        expected = 5
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 2 Tied ranks
    def test_bringin_stud7_2tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 2)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 3 Tied ranks
    def test_bringin_stud7_3tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 3)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 4 Tied ranks
    def test_bringin_stud7_4tied_returns1(self):
        t = testtools.test_table(6)
        testtools.deal_stud(t, 3, 4)
        expected = 1
        result = stud.bringin(t)
        self.assertEqual(expected, result)

    """
    Tests for highhand(table)
    """
    def test_highhand_3cards_pairAces_return0(self):
        t = get_dealt_table(HANDS_3CARD)
        expected = 0
        result = stud.highhand(t)
        self.assertEqual(expected, result)

    def test_highhand_4cards_AceHigh_return0(self):
        t = get_dealt_table(HANDS_4CARD)
        expected = 0
        result = stud.highhand(t)
        self.assertEqual(expected, result)
