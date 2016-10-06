import unittest
from ponyup import blinds


class TestBlinds(unittest.TestCase):
    """
    Tests for __init__()
    """
    def test_init_shouldbelevel1(self):
        self.b = blinds.Blinds()
        expected = 1
        result = self.b.level
        self.assertEqual(expected, result)

    # Can use blinds and antes
    # Can use bringin and antes
    # Can't use both blinds and bringin.

    """
    Tests for __str__()
    """
    def test_str_level1_returns_SB1_BB2(self):
        self.b = blinds.Blinds(1)
        expected = 'SB: $1, BB: $2\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    def test_str_level5_returns_SB15_BB30(self):
        self.b = blinds.Blinds(5)
        expected = 'SB: $15, BB: $30\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    def test_str_level5_withantes__returns_SB30_BB60_ante15(self):
        self.b = blinds.Blinds(5, antes=True)
        expected = 'Ante: $7.50, SB: $15, BB: $30\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    # Test antes, bringin

    """
    Tests for set_level()
    """
    # trying to use a limit outside out the bounds of the blind_dictionary, raise exception
    def test_setlevel_level0_raiseException(self):
        self.b = blinds.Blinds()
        self.assertRaises(ValueError, self.b.set_level, 0)

    def test_setlevel_level1000_raiseException(self):
        self.b = blinds.Blinds()
        self.assertRaises(ValueError, self.b.set_level, 1000)

    def test_setlevel_level1_SB1_BB2(self):
        self.b = blinds.Blinds()
        self.assertEqual(self.b.SB, 1)
        self.assertEqual(self.b.BB, 2)

    """
    Tests for stakes():
    """
    def test_str_level1_returns2_4_stakes(self):
        self.b = blinds.Blinds()
        expected = '$2-$4'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    def test_str_level5_returns30_60_stakes(self):
        self.b = blinds.Blinds(5)
        expected = '$30-$60'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    """
    Tests for big_blinds(stack)
    """
    # 50/100 blinds
    def test_bigblinds_BB2_stack100_returns50(self):
        self.b = blinds.Blinds(1)
        stack = 100
        expected = 50
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    # 50/100 blinds
    def test_bigblinds_BB100_stack1000_returns10(self):
        self.b = blinds.Blinds(7)
        stack = 1000
        expected = 10
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    # 50/100 blinds
    def test_bigblinds_BB100_stack1050_returns11(self):
        self.b = blinds.Blinds(7)
        stack = 1050
        expected = 11
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    def test_bigblinds_BB100_stack1070_returns11(self):
        self.b = blinds.Blinds(7)
        stack = 1070
        expected = 11
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    def test_bigblinds_BB100_antes_stack1000_returns10(self):
        self.b = blinds.Blinds(7, antes=True)
        stack = 1000
        expected = 10
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    """
    Tests for eff_big_blinds(self, players):
    """
    # 50/100 blinds with no ante. No change from regular BB
    def test_trueBB_BB100_returns100(self):
        self.b = blinds.Blinds(7)
        expected = self.b.BB
        result = self.b.trueBB(players=8)
        self.assertEqual(expected, result)

    # 50/100 blinds w ante
    def test_trueBB_BB100_8players_returns429(self):
        self.b = blinds.Blinds(7, antes=True)
        expected = 231
        result = self.b.trueBB(players=8)
        self.assertEqual(expected, result)

    # 100/200 blinds with 25 ante.
    def test_trueBB_BB200_8players_returns660(self):
        self.b = blinds.Blinds(8, antes=True)
        expected = 462
        result = self.b.trueBB(players=8)
        self.assertEqual(expected, result)

    """
    Tests for def effective_big_blinds(self, stack, players):
    """
    # 100/200 blinds with 50 ante.
    def test_effectiveBB_BB200_10000stack_8players_returns30(self):
        self.b = blinds.Blinds(8, antes=True)
        stack = 10000
        expected = 22
        result = self.b.effectiveBB(stack, players=8)
        self.assertEqual(expected, result)

    # 100/200 blinds with 50 ante.
    def test_effectiveBB_BB200_10500stack_8players_returns32(self):
        self.b = blinds.Blinds(8, antes=True)
        stack = 10500
        expected = 23
        result = self.b.effectiveBB(stack, players=8)
        self.assertEqual(expected, result)

    # 100/200 blinds with 25 ante.
    def test_effectiveBB_BB200_10350stack_8players_returns31(self):
        self.b = blinds.Blinds(8, antes=True)
        stack = 10350
        expected = 22
        result = self.b.effectiveBB(stack, players=8)
        self.assertEqual(expected, result)

    """
    Tests for sb_to_ante_ratio()
    """
    # lev1: SB=1, Ante=.50
    def test_sbtoanteratio_lev1_returns2(self):
        self.b = blinds.Blinds(level=1, antes=True)
        expected = 2
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    # lev5: SB=15, ante=7.50
    def test_sbtoanteratio_lev5_returns2(self):
        self.b = blinds.Blinds(level=5, antes=True)
        expected = 2
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    """
    Tests for round_number(num)
    """
    def test_roundnumber_10pt5_returns11(self):
        num = 10.5
        expected = 11
        result = blinds.round_number(num)
        self.assertEqual(expected, result)

    def test_roundnumber_10pt4_returns10(self):
        num = 10.4
        expected = 10
        result = blinds.round_number(num)
        self.assertEqual(expected, result)

    def test_roundnumber_1_returns1(self):
        num = 1
        expected = 1
        result = blinds.round_number(num)
        self.assertEqual(expected, result)
