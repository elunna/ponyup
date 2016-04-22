import unittest
import blinds


class TestTable(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        self.b = blinds.Blinds(blinds.limit)

    """
    Tests for __init__
    """

    # trying to use a limit outside out the bounds of the blind_dictionary, raise exception
    def test_init_level0_raiseException(self):
        self.assertRaises(ValueError, blinds.Blinds, blinds.limit, 0)

    def test_init_level100_raiseException(self):
        self.assertRaises(ValueError, blinds.Blinds, blinds.limit, 1000)

    def test_setlevel_limit1_hascorrectblinds(self):
        self.assertEqual(self.b.SB, 1)
        self.assertEqual(self.b.BB, 2)
        self.assertEqual(self.b.ANTE, 0)

    def test_sbtoanteratio_sb150_ante25_returns6(self):
        self.b = blinds.Blinds(blinds.WSOP, 4)
        expected = 6
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    def test_sbtoanteratio_sb1000_ante300_returns3_3(self):
        self.b = blinds.Blinds(blinds.WSOP, 12)
        expected = 3.3
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    def test_stakes_noAnte_returnsString(self):
        expected = '$2/$4'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    def test_stakes_Ante_returnsStringWithAnte(self):
        self.b.set_level(2)
        expected = '$3/$6, Ante: $1'
        result = self.b.stakes()
        self.assertEqual(expected, result)
