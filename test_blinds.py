import unittest
import blinds
from blinds import Level
import blinds_noante


class TestBlinds(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        # Setup the standard no-ante blind structure
        self.b = blinds_noante.BlindsNoAnte()

    def setUp_ante(self):
        # Setup the standard no-ante blind structure
        pass


    # trying to use a limit outside out the bounds of the blind_dictionary, raise exception
    def test_setlevel_level0_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 0)

    def test_setlevel_level100_raiseException(self):
        self.assertRaises(ValueError, self.b.set_level, 1000)


