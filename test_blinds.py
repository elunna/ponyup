import unittest
import blinds


class TestTable(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        self.b = blinds.Blinds()

    """
    Tests for __init__
    """

    """
    Tests for set_level(level)
    """
    def test_setlevel_limit1_hascorrectblinds(self):
        self.assertEqual(self.b.SB, 1)
        self.assertEqual(self.b.BB, 2)
        self.assertEqual(self.b.ANTE, 0)

    # trying to use a limit outside out the bounds of the blind_dictionary, raise exception
    def test_setlevel_level0_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 0)

    def test_setlevel_level100_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 1000)

    """
    Tests for sb_to_ante_ratio()
    """
    def test_sbtoanteratio_sb1_ante0_returns0(self):
        self.b = blinds.Blinds(level=1)
        expected = 0
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    def test_sbtoanteratio_sb1_ante1_returns1(self):
        self.b = blinds.Blinds(level=2)
        expected = 1
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    def test_sbtoanteratio_sb2_ante1_returns2(self):
        self.b = blinds.Blinds(level=3)
        expected = 2
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    def test_sbtoanteratio_sb3_ante2_returns1pt5(self):
        self.b = blinds.Blinds(level=6)
        expected = 1.7
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    """
    Tests for stakes()
    """
    def test_stakes_noAnte_returnsString(self):
        expected = '$2/$4'
        result = self.b.__str__()
        self.assertEqual(expected, result)

    def test_stakes_Ante_returnsStringWithAnte(self):
        self.b.set_level(2)
        expected = '$3/$6, Ante: $1'
        result = self.b.__str__()
        self.assertEqual(expected, result)
