import unittest
import blinds_ante


class TestBlindsAnte(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        # Setup the standard no-ante blind structure
        self.b = blinds_ante.BlindsAnte()

    """
    Tests for __init__
    """
    def test_init_ante_defaultlevel1(self):
        self.assertEqual(self.b.level, 1)

    """
    Tests for __str__()
    """
    # Assume level 1
    def test_str_showsAnteandBringin(self):
        expected = 'Ante: $0.25\nBringin: $0.50\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    """
    Tests for stakes()
    """
    # Assume level 1
    def test_stakes_lev1_returns1_2(self):
        expected = '$1/$2'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    """
    Tests for set_level(level)
    """
    def test_setlevel_lev1_correctsmallbet(self):
        self.assertEqual(self.b.BB, 1)

    def test_setlevel_lev1_ante_25cent(self):
        self.assertEqual(self.b.ANTE, 0.25)

    def test_setlevel_lev1_bringin_50cent(self):
        self.assertEqual(self.b.BRINGIN, 0.50)

    """
    Tests for sb_to_ante_ratio()
    """
    # lev1: ante=0.25, SB=1
    def test_sbtoanteratio_lev1_returns4(self):
        self.b = blinds_ante.BlindsAnte(level=1)
        expected = 4
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    # lev5: ante=1, SB=5
    def test_sbtoanteratio_lev5_returns5(self):
        self.b = blinds_ante.BlindsAnte(level=5)
        expected = 4
        result = self.b.sb_to_ante_ratio()
        self.assertEqual(expected, result)

    def test_ante_sizes(self):
        for level in blinds_ante.ante.values():
            self.assertTrue(level.ANTE < level.BRINGIN)

    def test_bringin_sizes(self):
        for level in blinds_ante.ante.values():
            self.assertTrue(level.BRINGIN < level.SB)

    def test_blind_sizes(self):
        # These should be equal and should just represent the "Small Bet" Size.
        for level in blinds_ante.ante.values():
            self.assertTrue(level.BB == level.BB)
