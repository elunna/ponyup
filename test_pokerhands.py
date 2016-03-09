import unittest
import evaluator
import pokerhands


class TestPokerHands(unittest.TestCase):
    # Test Values
    def test_getvalue_royalflush_returns100000000000(self):
        h = pokerhands.deal_royalflush()
        expected = 100000000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_royalflush_returnsROYALFLUSH(self):
        h = pokerhands.deal_royalflush()
        val = evaluator.get_value(h)
        expected = 'ROYAL FLUSH'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_straightflush_A_returns90900000000(self):
        h = pokerhands.deal_straightflush_A()
        expected = 90900000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightflushA_returnsSTRAIGHTFLUSH(self):
        h = pokerhands.deal_straightflush_A()
        val = evaluator.get_value(h)
        expected = 'STRAIGHT FLUSH'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_lowstraightflush_returns90000000000(self):
        h = pokerhands.deal_lowstraightflush()
        expected = 90000000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_lowstraightflush_returnsSTRAIGHTFLUSH(self):
        h = pokerhands.deal_lowstraightflush()
        val = evaluator.get_value(h)
        expected = 'STRAIGHT FLUSH'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_4ofakind_A_returns81408000000(self):
        h = pokerhands.deal_4ofakind_A()
        expected = 81408000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_4ofakindA_returnsQUADS(self):
        h = pokerhands.deal_4ofakind_A()
        val = evaluator.get_value(h)
        expected = 'QUADS'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_4ofakind_B_returns80814000000(self):
        h = pokerhands.deal_4ofakind_B()
        expected = 80814000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_4ofakindB_returnsQUADS(self):
        h = pokerhands.deal_4ofakind_B()
        val = evaluator.get_value(h)
        expected = 'QUADS'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_fullhouse_A_returns71413000000(self):
        h = pokerhands.deal_fullhouse_A()
        expected = 71413000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_fullhouseA_returnsFULLHOUSE(self):
        h = pokerhands.deal_fullhouse_A()
        val = evaluator.get_value(h)
        expected = 'FULL HOUSE'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_fullhouse_B_returns71314000000(self):
        h = pokerhands.deal_fullhouse_B()
        expected = 71314000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_fullhouseB_returnsFULLHOUSE(self):
        h = pokerhands.deal_fullhouse_B()
        val = evaluator.get_value(h)
        expected = 'FULL HOUSE'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_flush_returns61409070503(self):
        h = pokerhands.deal_flush()
        expected = 61409070503
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flush_returns(self):
        h = pokerhands.deal_flush()
        val = evaluator.get_value(h)
        expected = 'FLUSH'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_high_straight_returns51413121110(self):
        h = pokerhands.deal_high_straight()
        expected = 51413121110
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_high_straight_returnsSTRAIGHT(self):
        h = pokerhands.deal_high_straight()
        val = evaluator.get_value(h)
        expected = 'STRAIGHT'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_mid_straight_returns51110090807(self):
        h = pokerhands.deal_mid_straight()
        expected = 51110090807
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_mid_straight_returnsSTRAIGHT(self):
        h = pokerhands.deal_mid_straight()
        val = evaluator.get_value(h)
        expected = 'STRAIGHT'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_low_straight_returns50000000000(self):
        h = pokerhands.deal_low_straight()
        expected = 50000000000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_low_straight_returnsSTRAIGHT(self):
        h = pokerhands.deal_low_straight()
        val = evaluator.get_value(h)
        expected = 'STRAIGHT'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_3ofakind_A_returns41413120000(self):
        h = pokerhands.deal_3ofakind_A()
        expected = 41413120000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_3ofakind_A_returnsTRIPS(self):
        h = pokerhands.deal_3ofakind_A()
        val = evaluator.get_value(h)
        expected = 'TRIPS'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_3ofakind_B_returns41314120000(self):
        h = pokerhands.deal_3ofakind_B()
        expected = 41314120000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_3ofakind_B_returnsTRIPS(self):
        h = pokerhands.deal_3ofakind_B()
        val = evaluator.get_value(h)
        expected = 'TRIPS'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_twopairA_returns31413080000(self):
        h = pokerhands.deal_twopair_A()
        expected = 31413080000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_twopairA_returnsTWOPAIR(self):
        h = pokerhands.deal_twopair_A()
        val = evaluator.get_value(h)
        expected = 'TWO PAIR'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_twopairB_returns31308140000(self):
        h = pokerhands.deal_twopair_B()
        expected = 31308140000
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_twopair_B_returnsTWOPAIR(self):
        h = pokerhands.deal_twopair_B()
        val = evaluator.get_value(h)
        expected = 'TWO PAIR'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_pairB_returns21405030200(self):
        h = pokerhands.deal_pair_A()
        expected = 21405030200
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_pair_A_returnsPAIR(self):
        h = pokerhands.deal_pair_A()
        val = evaluator.get_value(h)
        expected = 'PAIR'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_pairA_returns20214050300(self):
        h = pokerhands.deal_pair_B()
        expected = 20214050300
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_pair_B_returnsPAIR(self):
        h = pokerhands.deal_pair_B()
        val = evaluator.get_value(h)
        expected = 'PAIR'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    # Draws
    def test_getvalue_OESFD_returns1110090802(self):
        h = pokerhands.deal_OESFD()
        expected = 1110090802
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype__returnsHIGHCARD(self):
        h = pokerhands.deal_OESFD()
        val = evaluator.get_value(h)
        expected = 'HIGH CARD'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_GSSFD_returns1110090702(self):
        h = pokerhands.deal_GSSFD()
        expected = 1110090702
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_GSSFD_returnsHIGHCARD(self):
        h = pokerhands.deal_GSSFD()
        val = evaluator.get_value(h)
        expected = 'HIGH CARD'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_flushdraw_hi_returns1410090702(self):
        h = pokerhands.deal_flushdraw_hi()
        expected = 1410090702
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushdrawhi_returnsHIGHCARD(self):
        h = pokerhands.deal_flushdraw_hi()
        val = evaluator.get_value(h)
        expected = 'HIGH CARD'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_flushdraw_returns1009070302(self):
        h = pokerhands.deal_flushdraw()
        expected = 1009070302
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushdraw_returnsHIGHCARD(self):
        h = pokerhands.deal_flushdraw()
        val = evaluator.get_value(h)
        expected = 'HIGH CARD'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_OESD_returns1110090802(self):
        h = pokerhands.deal_OESD()
        expected = 1110090802
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_OESD_returns(self):
        h = pokerhands.deal_OESD()
        val = evaluator.get_value(h)
        expected = 'HIGH CARD'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_GSSD_returns1413111002(self):
        h = pokerhands.deal_GSSD()
        expected = 1413111002
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_GSSD_returnsHIGHCARD(self):
        h = pokerhands.deal_GSSD()
        val = evaluator.get_value(h)
        expected = 'HIGH CARD'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_wheeldraw_returns1413040302(self):
        h = pokerhands.deal_wheeldraw()
        expected = 1413040302
        result = evaluator.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_wheeldraw_returnsHIGHCARD(self):
        h = pokerhands.deal_wheeldraw()
        val = evaluator.get_value(h)
        expected = 'HIGH CARD'
        result = evaluator.get_type(val)
        self.assertEqual(expected, result)
