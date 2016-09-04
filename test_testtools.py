import unittest
import testtools


class TestTestTools(unittest.TestCase):

    """
    Tests BobTable
    """
    def test_bobtable_2seats_len2(self):
        t = testtools.BobTable(2)
        expected = 2
        result = len(t)
        self.assertEqual(expected, result)

    def test_bobtable_2seats_1000chips(self):
        t = testtools.BobTable(2)
        expected = 1000
        result = t.seats[0].chips
        self.assertEqual(expected, result)

    def test_bobtable_2seats_bob0_in_seat0(self):
        t = testtools.BobTable(2)
        expected = 'bob0'
        result = str(t.seats[0])
        self.assertEqual(expected, result)

    """
    Tests SteppedStackTable
    """
    def test_steppedstacktable_seat0_100chips(self):
        t = testtools.SteppedStackTable(2)
        expected = 100
        result = t.seats[0].chips
        self.assertEqual(expected, result)

    def test_steppedstacktable_seat1_200chips(self):
        t = testtools.SteppedStackTable(2)
        expected = 200
        result = t.seats[1].chips
        self.assertEqual(expected, result)
