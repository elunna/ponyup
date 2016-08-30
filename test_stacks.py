import unittest
import setup_table
import stacks


class TestStacks(unittest.TestCase):
    """
    Tests for def test_largest(table):
    """
    # For 4 players, 100, 200, 300, 400.
    def test_largest_4players_returns400(self):
        seats = 4
        t = setup_table.allin_table(seats)
        expected = 400
        result = stacks.largest(t)
        self.assertEqual(expected, result)

    """
    Tests for def test_smallest(table):
    """
    # For 4 players, 100, 200, 300, 400.
    def test_smallest_4players_returns400(self):
        seats = 4
        t = setup_table.allin_table(seats)
        expected = 100
        result = stacks.smallest(t)
        self.assertEqual(expected, result)

    """
    Tests for def test_average(table):
    """
    def test_average_4players_returns400(self):
        seats = 4
        t = setup_table.allin_table(seats)
        expected = 250
        result = stacks.average(t)
        self.assertEqual(expected, result)

    """
    Tests for def test_effective(table):
    """

    """
    Tests for stacklist(table)
    """
    def test_average_4players_returns4stacks(self):
        seats = 4
        t = setup_table.allin_table(seats)
        expected = [100, 200, 300, 400]
        result = stacks.stacklist(t)
        self.assertEqual(expected, result)
