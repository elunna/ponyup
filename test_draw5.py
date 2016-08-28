import unittest
import draw5
import hand
import pokerhands


class TestDraw5(unittest.TestCase):
    #  def test_(self):
        #  self.assertRaises(ValueError, )

    """
    Tests for auto_discard(hand):
    """

    # Royal flush - no discards
    def test_autodiscard_royalflush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.royalflush())
        expected = []
        result = draw5.auto_discard(h)
        self.assertEqual(expected, result)

    # Straight flush - no discards
    def test_autodiscard_straightflush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.straightflush_high())
        expected = []
        result = draw5.auto_discard(h)
        self.assertEqual(expected, result)

    # Full house - no discards
    def test_autodiscard_fullhouse_returnsEmptyList(self):
        h = hand.Hand(pokerhands.boat_high())
        expected = []
        result = draw5.auto_discard(h)
        self.assertEqual(expected, result)

    # Flush - no discards
    def test_autodiscard_flush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.flush_low())
        expected = []
        result = draw5.auto_discard(h)
        self.assertEqual(expected, result)

    # Straight - no discards
    def test_autodiscard_straight_returnsEmptyList(self):
        h = hand.Hand(pokerhands.straight_mid())
        expected = []
        result = draw5.auto_discard(h)
        self.assertEqual(expected, result)

    # No cards pass, length = 0
