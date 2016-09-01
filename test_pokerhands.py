import unittest
import evaluator as ev
import pokerhands

class TestPokerHands(unittest.TestCase):
    ##################################################
    # ROYAL FLUSHES
    ##################################################
    def test_getvalue_royalflush_returns100000000000(self):
        #  h = pokerhands.royalflush()
        h = pokerhands.make('royalflush')
        expected = 100000000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_royalflush_returnsROYALFLUSH(self):
        h = pokerhands.make('royalflush')
        h = pokerhands.make('royalflush')
        val = ev.get_value(h)
        expected = 'ROYAL FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_royalflush_returnsAHigh(self):
        h = pokerhands.make('royalflush')
        val = ev.get_value(h)
        expected = 'A High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # STRAIGHT FLUSHES
    ##################################################
    def test_getvalue_straightflushhigh_returns90900000000(self):
        h = pokerhands.make('straightflush_high')
        expected = 90900000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightflushhigh_returnsSTRAIGHTFLUSH(self):
        h = pokerhands.make('straightflush_high')
        val = ev.get_value(h)
        expected = 'STRAIGHT FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightflushhigh_returnKHigh(self):
        h = pokerhands.make('straightflush_high')
        val = ev.get_value(h)
        expected = 'K High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_straightflushlow_returns90000000000(self):
        h = pokerhands.make('straightflush_low')
        expected = 90000000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightflushlow_returnsSTRAIGHTFLUSH(self):
        h = pokerhands.make('straightflush_low')
        val = ev.get_value(h)
        expected = 'STRAIGHT FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightflushlow_return5High(self):
        h = pokerhands.make('straightflush_low')
        val = ev.get_value(h)
        expected = '5 High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # FOUR OF A KINDS, ('QUADS')
    ##################################################
    def test_getvalue_quadshigh_returns81413000000(self):
        h = pokerhands.make('quads_high')
        expected = 81413000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_quadshigh_returnsQUADS(self):
        h = pokerhands.make('quads_high')
        val = ev.get_value(h)
        expected = 'QUADS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_quadshigh_returnsAs(self):
        h = pokerhands.make('quads_high')
        val = ev.get_value(h)
        expected = 'A\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_quadslow_returns80203000000(self):
        h = pokerhands.make('quads_low')
        expected = 80203000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_quadslow_returnsQUADS(self):
        h = pokerhands.make('quads_low')
        val = ev.get_value(h)
        expected = 'QUADS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_quadslow_returns2s(self):
        h = pokerhands.make('quads_low')
        val = ev.get_value(h)
        expected = '2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # FULL HOUSES ('BOATS')
    ##################################################
    def test_getvalue_fullhousehigh_returns71413000000(self):
        h = pokerhands.make('fullhouse_high')
        expected = 71413000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_fullhousehigh_returnsFULLHOUSE(self):
        h = pokerhands.make('fullhouse_high')
        val = ev.get_value(h)
        expected = 'FULL HOUSE'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_fullhousehigh_returnsAsfullofKs(self):
        h = pokerhands.make('fullhouse_high')
        val = ev.get_value(h)
        expected = 'A\'s full of K\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_fullhouselow_returns70203000000(self):
        h = pokerhands.make('fullhouse_low')
        expected = 70203000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_fullhouselow_returnsFULLHOUSE(self):
        h = pokerhands.make('fullhouse_low')
        val = ev.get_value(h)
        expected = 'FULL HOUSE'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_fullhouselow_returns2sfullof3s(self):
        h = pokerhands.make('fullhouse_low')
        val = ev.get_value(h)
        expected = '2\'s full of 3\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # FLUSHES
    ##################################################
    def test_getvalue_flushhigh_returns61413121109(self):
        h = pokerhands.make('flush_high')
        expected = 61413121109
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushhigh_returns(self):
        h = pokerhands.make('flush_high')
        val = ev.get_value(h)
        expected = 'FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_flushhigh_returnsAhigh(self):
        h = pokerhands.make('flush_high')
        val = ev.get_value(h)
        expected = 'A High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_flushlow_returns60705040302(self):
        h = pokerhands.make('flush_low')
        expected = 60705040302
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushlow_returns(self):
        h = pokerhands.make('flush_low')
        val = ev.get_value(h)
        expected = 'FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_flushlow_returns7high(self):
        h = pokerhands.make('flush_low')
        val = ev.get_value(h)
        expected = '7 High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # STRAIGHTS
    ##################################################
    def test_getvalue_straighthigh_returns51413121110(self):
        h = pokerhands.make('straight_high')
        expected = 51413121110
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straighthigh_returnsSTRAIGHT(self):
        h = pokerhands.make('straight_high')
        val = ev.get_value(h)
        expected = 'STRAIGHT'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straighthigh_returnAHigh(self):
        h = pokerhands.make('straight_high')
        val = ev.get_value(h)
        expected = 'A High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_straightmid_returns51110090807(self):
        h = pokerhands.make('straight_mid')
        expected = 51110090807
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightmid_returnsSTRAIGHT(self):
        h = pokerhands.make('straight_mid')
        val = ev.get_value(h)
        expected = 'STRAIGHT'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightmid_returnJHigh(self):
        h = pokerhands.make('straight_mid')
        val = ev.get_value(h)
        expected = 'J High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_straightlow_returns50000000000(self):
        h = pokerhands.make('straight_low')
        expected = 50000000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightlow_returnsSTRAIGHT(self):
        h = pokerhands.make('straight_low')
        val = ev.get_value(h)
        expected = 'STRAIGHT'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightlow_return5High(self):
        h = pokerhands.make('straight_low')
        val = ev.get_value(h)
        expected = '5 High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # THREE OF A KIND ('SET', 'TRIPS'
    ##################################################
    def test_getvalue_tripshigh_returns41413120000(self):
        h = pokerhands.make('trips_high')
        expected = 41413120000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_tripshigh_returnsTRIPS(self):
        h = pokerhands.make('trips_high')
        val = ev.get_value(h)
        expected = 'TRIPS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_tripshigh_returnsAs(self):
        h = pokerhands.make('trips_high')
        val = ev.get_value(h)
        expected = 'A\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_tripslow_returns40204030000(self):
        h = pokerhands.make('trips_low')
        expected = 40204030000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_tripslow_returnsTRIPS(self):
        h = pokerhands.make('trips_low')
        val = ev.get_value(h)
        expected = 'TRIPS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_tripslow_returns2s(self):
        h = pokerhands.make('trips_low')
        val = ev.get_value(h)
        expected = '2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # TWO PAIRS
    ##################################################
    def test_getvalue_twopairhigh_returns31413120000(self):
        h = pokerhands.make('twopair_high')
        expected = 31413120000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_twopairhigh_returnsTWOPAIR(self):
        h = pokerhands.make('twopair_high')
        val = ev.get_value(h)
        expected = 'TWO PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_twopairhigh_returnsAsAndKs(self):
        h = pokerhands.make('twopair_high')
        val = ev.get_value(h)
        expected = 'A\'s and K\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_twopairlow_returns30302040000(self):
        h = pokerhands.make('twopair_low')
        expected = 30302040000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_twopairlow_returnsTWOPAIR(self):
        h = pokerhands.make('twopair_low')
        val = ev.get_value(h)
        expected = 'TWO PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_twopairlow_returns3sAnd2s(self):
        h = pokerhands.make('twopair_low')
        val = ev.get_value(h)
        expected = '3\'s and 2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    ##################################################
    # PAIRS
    ##################################################
    def test_getvalue_pairhigh_returns21413121100(self):
        h = pokerhands.make('pair_high')
        expected = 21413121100
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_pairhigh_returnsPAIR(self):
        h = pokerhands.make('pair_high')
        val = ev.get_value(h)
        expected = 'PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_pairhigh_returnsAs(self):
        h = pokerhands.make('pair_high')
        val = ev.get_value(h)
        expected = 'A\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_pairlow_returns20205040300(self):
        h = pokerhands.make('pair_low')
        expected = 20205040300
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_pairlow_returnsPAIR(self):
        h = pokerhands.make('pair_low')
        val = ev.get_value(h)
        expected = 'PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_pairlow_returns2s(self):
        h = pokerhands.make('pair_low')
        val = ev.get_value(h)
        expected = '2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # Draws
    def test_getvalue_OESFD_returns1110090802(self):
        h = pokerhands.make('OESFD')
        expected = 1110090802
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype__returnsHIGHCARD(self):
        h = pokerhands.make('OESFD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_GSSFD_returns1110090702(self):
        h = pokerhands.make('GSSFD')
        expected = 1110090702
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_GSSFD_returnsHIGHCARD(self):
        h = pokerhands.make('GSSFD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_flushdraw_hi_returns1410090702(self):
        h = pokerhands.make('flushdrawA')
        expected = 1410090702
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushdrawhi_returnsHIGHCARD(self):
        h = pokerhands.make('flushdrawA')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_flushdraw_returns1009070302(self):
        h = pokerhands.make('flushdrawB')
        expected = 1009070302
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushdraw_returnsHIGHCARD(self):
        h = pokerhands.make('flushdrawB')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_OESD_returns1110090802(self):
        h = pokerhands.make('OESD')
        expected = 1110090802
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_OESD_returns(self):
        h = pokerhands.make('OESD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_GSSD_returns1413111002(self):
        h = pokerhands.make('GSSD')
        expected = 1413111002
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_GSSD_returnsHIGHCARD(self):
        h = pokerhands.make('GSSD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_wheeldraw_returns1413040302(self):
        h = pokerhands.make('wheeldraw')
        expected = 1413040302
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_wheeldraw_returnsHIGHCARD(self):
        h = pokerhands.make('wheeldraw')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)
