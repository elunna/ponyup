import unittest
import table_factory
import testtools


class TestTestTools(unittest.TestCase):

    """
    Tests for deal_ranked_hands(table, reversed=False):
    """
    def test_dealrankedhands_seat0_hasRoyalFlush(self):
        t = table_factory.BobTable(2)
        testtools.deal_ranked_hands(t)
        expected = "ROYAL FLUSH"
        result = t.seats[0].hand.rank()
        self.assertEqual(expected, result)
