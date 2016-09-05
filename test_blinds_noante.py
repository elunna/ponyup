import unittest
from blinds import Level
import blinds_noante


class TestBlindsNoAnte(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        # Setup the standard no-ante blind structure
        self.b = blinds_noante.BlindsNoAnte()

    """
    Tests for __init__
    """
    def test_init_ante_defaultlevel1(self):
        self.assertEqual(self.b.level, 1)
    """
    Tests for __str__()
    """
    # Assume level 1
    def test_str_showsBlinds(self):
        expected = 'SB: $1, BB: $2\n'
        result = str(self.b)
        self.assertEqual(expected, result)

    """
    Tests for stakes()
    """
    # Assume level 1
    def test_stakes_lev1_returns1_2(self):
        expected = '$2/$4'
        result = self.b.stakes()
        self.assertEqual(expected, result)

    """
    Tests for set_level(level)
    """
    def test_setlevel_lev1_hascorrectblinds(self):
        self.assertEqual(self.b.SB, 1)
        self.assertEqual(self.b.BB, 2)
        self.assertEqual(self.b.ANTE, 0)

    def test_setlevel_lev1_noantes(self):
        self.assertEqual(self.b.ANTE, 0)
        self.assertEqual(self.b.BRINGIN, 0)

    """
    Tests for noante_level(sb, bb)
    """
    def test_noantelevel_BB2_SB1_returnsCorrectLevel(self):
        self.b.set_level(2)
        blind_tuple = (2, 1)
        expected = Level(2, 1, 0, 0)
        result = blinds_noante.noante_level(*blind_tuple)
        self.assertEqual(expected, result)

    def test_blind_sizes(self):
        for level in blinds_noante.no_ante.values():
            self.assertTrue(level.SB < level.BB)
