import unittest
import game


class TestGame(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        pass

    """
    Tests for __init__ and table construction
    """
    # initialized with invalid seat count(less than 2)
    def test_raiseException(self):
        pass
        #  self.assertRaises(ValueError, table.Table, '1')

    # a Test
    def test_(self):
        pass
