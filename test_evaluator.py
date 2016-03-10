import unittest
import evaluator
import pokerhands


class TestEvaluator(unittest.TestCase):
    def test_is_validhand_4cards_returnsFalse(self):
        h = pokerhands.dealhand(4)
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_5cards_returnsTrue(self):
        h = pokerhands.dealhand(5)
        expected = True
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_6cards_returnsFalse(self):
        h = pokerhands.dealhand(6)
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_duplicateCards_returnsFalse(self):
        h = pokerhands.deal_duplicates()
        expected = False
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_is_validhand_royalflush_returnsTrue(self):
        h = pokerhands.royalflush()
        expected = True
        result = evaluator.is_validhand(h)
        self.assertEqual(expected, result)

    def test_gettype_negativevalue_raiseEx(self):
        self.assertRaises(ValueError, evaluator.get_type, -1)

    def test_gettype_1000000000000_raiseEx(self):
        self.assertRaises(ValueError, evaluator.get_type, 1000000000000)



    #  def test_get_description_(self):

    #  def test_findbesthand_7cardstraightflush_returnsROYALFLUSH(self):
        # besthand = ev.find_best_hand(group)

        # Test description?
