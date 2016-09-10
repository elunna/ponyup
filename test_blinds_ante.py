import unittest
import blinds


class TestBlindsAnte(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        # Setup the standard no-ante blind structure
        self.b = blinds.BlindsAnte()

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

    def test_ante_sizes(self):
        for level in blinds.ante.values():
            self.assertTrue(level[3] < level[2])

    def test_bringin_sizes(self):
        for level in blinds.ante.values():
            self.assertTrue(level[2] < level[1])

    def test_blind_sizes(self):
        # These should be equal and should just represent the "Small Bet" Size.
        for level in blinds.ante.values():
            self.assertTrue(level[1] == level[0])
