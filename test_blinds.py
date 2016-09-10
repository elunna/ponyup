import unittest
import blinds
import tourneys


class TestBlinds(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        # Setup the standard no-ante blind structure
        self.b = blinds.Blinds(structure=tourneys.WSOP)
        # Level 1 of WSOP is 50/100 blinds.

    # trying to use a limit outside out the bounds of the blind_dictionary, raise exception
    def test_setlevel_level0_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 0)

    def test_setlevel_level100_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 1000)

    def test_bigblinds_BB100_stack100_returns1(self):
        stack = 100
        expected = 1
        result = self.b.big_blinds(stack)
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
