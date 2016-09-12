import unittest
import blinds
import tourneys


class TestBlinds(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self, level=1):
        # Setup the standard no-ante blind structure
        self.b = blinds.Blinds(level, structure=tourneys.WSOP)
        # Level 1 of WSOP is 50/100 blinds.

    """
    Tests for __init__()
    """
    def test_init_shouldbelevel1(self):
        expected = 1
        result = self.b.level
        self.assertEqual(expected, result)

    """
    Tests for __str__()
    """
    def test_str_level1_returns_SB50_BB100(self):
        self.setUp(level=1)
        expected = 'SB: $50, BB: $100\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    def test_str_level5_returns_Antes50_SB200_BB400(self):
        self.setUp(level=5)
        expected = 'Ante: $50\nSB: $200, BB: $400\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    """
    Tests for set_level()
    """
    # trying to use a limit outside out the bounds of the blind_dictionary, raise exception
    def test_setlevel_level0_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 0)

    def test_setlevel_level100_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 1000)

    def test_setlevel_level2_SB100_BB200(self):
        self.setUp(level=2)
        self.assertEqual(self.b.SB, 100)
        self.assertEqual(self.b.BB, 200)

    """
    Tests for stakes():
    """
    def test_str_level1_returns50_100_stakes(self):
        self.setUp(level=1)
        expected = '$100/$200'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    def test_str_level5_returns200_400_stakes(self):
        self.setUp(level=5)
        expected = '$400/$800'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    """
    Tests for big_blinds(stack)
    """
    # 50/100 blinds
    def test_bigblinds_BB100_stack100_returns1(self):
        stack = 100
        expected = 1
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    # 50/100 blinds
    def test_bigblinds_BB100_stack1000_returns10(self):
        stack = 1000
        expected = 10
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    # 50/100 blinds
    def test_bigblinds_BB100_stack1050_returns11(self):
        stack = 1050
        expected = 11
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    def test_bigblinds_BB100_stack1070_returns11(self):
        stack = 1070
        expected = 11
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    # 200/400 blinds with 50 ante.
    def test_bigblinds_BB400_stack4000_returns10(self):
        self.setUp(level=5)
        stack = 4000
        expected = 10
        result = self.b.big_blinds(stack)
        self.assertEqual(expected, result)

    """
    Tests for eff_big_blinds(self, players):
    """
    # 50/100 blinds with no ante. No change from regular BB
    def test_trueBB_lev1_returns100(self):
        self.setUp(level=1)
        expected = self.b.BB
        result = self.b.trueBB(players=8)
        self.assertEqual(expected, result)

    # 150/300 blinds with 25 ante.
    def test_trueBB_lev4_8players_returns429(self):
        self.setUp(level=4)
        expected = 429
        result = self.b.trueBB(players=8)
        self.assertEqual(expected, result)

    # 200/400 blinds with 50 ante.
    def test_trueBB_lev5_8players_returns660(self):
        self.setUp(level=5)
        expected = 660
        result = self.b.trueBB(players=8)
        self.assertEqual(expected, result)

    """
    Tests for def effective_big_blinds(self, stack, players):
    """
    # 150/300 blinds with 25 ante.
    def test_effectiveBB_lev4_10000stack_8players_returns23(self):
        self.setUp(level=4)
        stack = 10000
        expected = 23
        result = self.b.effectiveBB(stack, players=8)
        self.assertEqual(expected, result)

    # 200/400 blinds with 50 ante.
    def test_effectiveBB_lev5_10000stack_8players_returns15(self):
        self.setUp(level=5)
        stack = 10000
        expected = 15
        result = self.b.effectiveBB(stack, players=8)
        self.assertEqual(expected, result)

    # 200/400 blinds with 50 ante.
    def test_effectiveBB_lev5_10500stack_8players_returns16(self):
        self.setUp(level=5)
        stack = 10500
        expected = 16
        result = self.b.effectiveBB(stack, players=8)
        self.assertEqual(expected, result)

    """
    Tests for sb_to_ante_ratio()
    """
    # lev1: ante=0.25, SB=1
    def test_sbtoanteratio_lev1_returns4(self):
        self.b = blinds.BlindsAnte(level=1)
        expected = 4
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    # lev5: ante=1, SB=5
    def test_sbtoanteratio_lev5_returns5(self):
        self.b = blinds.BlindsAnte(level=5)
        expected = 4
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    """
    Tests for tuple_to_level(lev):
    """
    # Tuple size 0 - raise exception
    def test_tupletolevel_size0_raisesException(self):
        t = tuple()
        self.assertRaises(ValueError, blinds.tuple_to_level, t)

    # Tuple size 1 - raise exception
    def test_tupletolevel_size1_raisesException(self):
        t = (0, )
        self.assertRaises(ValueError, blinds.tuple_to_level, t)

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
