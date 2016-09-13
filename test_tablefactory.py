import unittest
import table_factory


class TestTableFactory(unittest.TestCase):
    """
    Tests for factory(**new_config)
    """
    def test_factory_2seat_Tablehas2seats(self):
        t = table_factory.factory(seats=2)
        expected = 2
        result = len(t)
        self.assertEqual(expected, result)
