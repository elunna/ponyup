import unittest
import blinds


class TestBlindsNoAnte(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        # Setup the standard no-ante blind structure
        self.b = blinds.BlindsNoAnte(level=2)

    """
    Tests for __init__
    """
    def test_init_ante_defaultlevel1(self):
        self.b = blinds.BlindsNoAnte()
        self.assertEqual(self.b.level, 1)
    """
    Tests for __str__()
    """
    # Assume level 2
    def test_str_showsBlinds(self):
        expected = 'SB: $1, BB: $2\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    """
    Tests for stakes()
    """
    # Assume level 2
    def test_stakes_lev1_returns1_2(self):
        expected = '$2/$4'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    """
    Tests for set_level(level)
    """
    def test_setlevel_lev2_hascorrectblinds(self):
        self.assertEqual(self.b.SB, 1)
        self.assertEqual(self.b.BB, 2)
        self.assertEqual(self.b.ANTE, 0)

    def test_setlevel_lev2_noantes(self):
        self.assertEqual(self.b.ANTE, 0)
        self.assertEqual(self.b.BRINGIN, 0)
