import unittest
import table_factory


class TestTableFactory(unittest.TestCase):

    """
    Tests BobTable
    """
    def test_bobtable_2seats_len2(self):
        t = table_factory.BobTable(2)
        expected = 2
        result = len(t)
        self.assertEqual(expected, result)

    def test_bobtable_2seats_1000chips(self):
        t = table_factory.BobTable(2)
        expected = 1000
        result = t.seats[0].chips
        self.assertEqual(expected, result)

    def test_bobtable_2seats_bob0_in_seat0(self):
        t = table_factory.BobTable(2)
        expected = 'bob0'
        result = str(t.seats[0])
        self.assertEqual(expected, result)
