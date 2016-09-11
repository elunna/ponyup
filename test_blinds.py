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

    """
    Tests for __str__()
    """

    """
    Tests for set_level()
    """
    # trying to use a limit outside out the bounds of the blind_dictionary, raise exception
    def test_setlevel_level0_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 0)

    def test_setlevel_level100_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 1000)

    """
    Tests for stakes():
    """

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
    Tests for eff_big_blinds(self, stack, players):
    """

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
