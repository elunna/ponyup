"""
  " Tests for tools.py
  """
import pytest
from ..src import playingcard as pc
from ..src import evaluator as ev
from ..src import tools


def test_tocard_As_returnsAs():
    string = 'As'
    result = tools.to_card(string)
    assert result.rank == 'A'
    assert result.suit == 's'


def test_tocard_AA_returnsAs():
    with pytest.raises(Exception):
        tools.to_card('AA')


def test_converttocards_AsKs_returnsCardAsKs():
    As, Ks = pc.PlayingCard('A', 's'), pc.PlayingCard('K', 's')
    tools.convert_to_cards(['As', 'Ks']) == [As, Ks]


def test_make_royalflush_returnsRoyalFlush():
    h = tools.make('royalflush')
    assert ev.get_type(ev.get_value(h)) == 'ROYAL FLUSH'


def test_getcards_0_returns0cards():
    h = tools.get_cards(0)
    assert len(h) == 0


def test_getcards_1_returns1card():
    h = tools.get_cards(1)
    assert len(h) == 1


def test_getcards_2_returns2cards():
    h = tools.get_cards(2)
    assert len(h) == 2


""" Tests for all the poker hands to make sure get_value, get_type, and
    get_description work.
"""


def test_getvalue_royalflush_returns100000000000():
    h = tools.make('royalflush')
    assert ev.get_value(h) == 100000000000


def test_gettype_royalflush_returnsROYALFLUSH():
    h = tools.make('royalflush')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'ROYAL FLUSH'


def test_get_description_royalflush_returnsAHigh():
    h = tools.make('royalflush')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A High'


def test_getvalue_straightflushhigh_returns90900000000():
    h = tools.make('straightflush_high')
    assert ev.get_value(h) == 91300000000


def test_gettype_straightflushhigh_returnsSTRAIGHTFLUSH():
    h = tools.make('straightflush_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'STRAIGHT FLUSH'


def test_get_description_straightflushhigh_returnKHigh():
    h = tools.make('straightflush_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'K High'


def test_getvalue_straightflushlow_returns90000000000():
    h = tools.make('straightflush_low')
    assert ev.get_value(h) == 90000000000


def test_gettype_straightflushlow_returnsSTRAIGHTFLUSH():
    h = tools.make('straightflush_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'STRAIGHT FLUSH'


def test_get_description_straightflushlow_return5High():
    h = tools.make('straightflush_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '5 High'


def test_getvalue_quadshigh_returns81413000000():
    h = tools.make('quads_high')
    assert ev.get_value(h) == 81413000000


def test_gettype_quadshigh_returnsQUADS():
    h = tools.make('quads_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'QUADS'


def test_get_description_quadshigh_returnsAs():
    h = tools.make('quads_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A\'s'


def test_getvalue_quadslow_returns80203000000():
    h = tools.make('quads_low')
    assert ev.get_value(h) == 80203000000


def test_gettype_quadslow_returnsQUADS():
    h = tools.make('quads_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'QUADS'


def test_get_description_quadslow_returns2s():
    h = tools.make('quads_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '2\'s'


def test_getvalue_fullhousehigh_returns71413000000():
    h = tools.make('fullhouse_high')
    assert ev.get_value(h) == 71413000000


def test_gettype_fullhousehigh_returnsFULLHOUSE():
    h = tools.make('fullhouse_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'FULL HOUSE'


def test_get_description_fullhousehigh_returnsAsfullofKs():
    h = tools.make('fullhouse_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A\'s full of K\'s'


def test_getvalue_fullhouselow_returns70203000000():
    h = tools.make('fullhouse_low')
    assert ev.get_value(h) == 70203000000


def test_gettype_fullhouselow_returnsFULLHOUSE():
    h = tools.make('fullhouse_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'FULL HOUSE'


def test_get_description_fullhouselow_returns2sfullof3s():
    h = tools.make('fullhouse_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '2\'s full of 3\'s'


def test_getvalue_flushhigh_returns61413121109():
    h = tools.make('flush_high')
    assert ev.get_value(h) == 61413121109


def test_gettype_flushhigh_returns():
    h = tools.make('flush_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'FLUSH'


def test_get_description_flushhigh_returnsAhigh():
    h = tools.make('flush_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A High'


def test_getvalue_flushlow_returns60705040302():
    h = tools.make('flush_low')
    assert ev.get_value(h) == 60705040302


def test_gettype_flushlow_returns():
    h = tools.make('flush_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'FLUSH'


def test_get_description_flushlow_returns7high():
    h = tools.make('flush_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '7 High'


def test_getvalue_straighthigh_returns51413121110():
    h = tools.make('straight_high')
    assert ev.get_value(h) == 51413121110


def test_gettype_straighthigh_returnsSTRAIGHT():
    h = tools.make('straight_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'STRAIGHT'


def test_get_description_straighthigh_returnAHigh():
    h = tools.make('straight_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A High'


def test_getvalue_straightmid_returns51110090807():
    h = tools.make('straight_mid')
    assert ev.get_value(h) == 51110090807


def test_gettype_straightmid_returnsSTRAIGHT():
    h = tools.make('straight_mid')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'STRAIGHT'


def test_get_description_straightmid_returnJHigh():
    h = tools.make('straight_mid')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'J High'


def test_getvalue_straightlow_returns50000000000():
    h = tools.make('straight_low')
    assert ev.get_value(h) == 50000000000


def test_gettype_straightlow_returnsSTRAIGHT():
    h = tools.make('straight_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'STRAIGHT'


def test_get_description_straightlow_return5High():
    h = tools.make('straight_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '5 High'


def test_getvalue_tripshigh_returns41413120000():
    h = tools.make('trips_high')
    assert ev.get_value(h) == 41413120000


def test_gettype_tripshigh_returnsTRIPS():
    h = tools.make('trips_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'TRIPS'


def test_get_description_tripshigh_returnsAs():
    h = tools.make('trips_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A\'s'


def test_getvalue_tripslow_returns40204030000():
    h = tools.make('trips_low')
    assert ev.get_value(h) == 40204030000


def test_gettype_tripslow_returnsTRIPS():
    h = tools.make('trips_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'TRIPS'


def test_get_description_tripslow_returns2s():
    h = tools.make('trips_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '2\'s'


# TWO PAIRS
def test_getvalue_twopairhigh_returns31413120000():
    h = tools.make('twopair_high')
    assert ev.get_value(h) == 31413120000


def test_gettype_twopairhigh_returnsTWOPAIR():
    h = tools.make('twopair_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'TWO PAIR'


def test_get_description_twopairhigh_returnsAsAndKs():
    h = tools.make('twopair_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A\'s and K\'s'


def test_getvalue_twopairlow_returns30302040000():
    h = tools.make('twopair_low')
    assert ev.get_value(h) == 30302040000


def test_gettype_twopairlow_returnsTWOPAIR():
    h = tools.make('twopair_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'TWO PAIR'


def test_get_description_twopairlow_returns3sAnd2s():
    h = tools.make('twopair_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '3\'s and 2\'s'


def test_getvalue_pairhigh_returns21413121100():
    h = tools.make('pair_high')
    assert ev.get_value(h) == 21413121100


def test_gettype_pairhigh_returnsPAIR():
    h = tools.make('pair_high')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'PAIR'


def test_get_description_pairhigh_returnsAs():
    h = tools.make('pair_high')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == 'A\'s'


def test_getvalue_pairlow_returns20205040300():
    h = tools.make('pair_low')
    assert ev.get_value(h) == 20205040300


def test_gettype_pairlow_returnsPAIR():
    h = tools.make('pair_low')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'PAIR'


def test_get_description_pairlow_returns2s():
    h = tools.make('pair_low')
    val = ev.get_value(h)
    assert ev.get_description(val, h) == '2\'s'


def test_getvalue_OESFD_returns1110090802():
    h = tools.make('OESFD')
    assert ev.get_value(h) == 1110090802


def test_gettype__returnsHIGHCARD():
    h = tools.make('OESFD')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'HIGH CARD'


def test_getvalue_GSSFD_returns1110090702():
    h = tools.make('GSSFD')
    assert ev.get_value(h) == 1110090702


def test_gettype_GSSFD_returnsHIGHCARD():
    h = tools.make('GSSFD')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'HIGH CARD'


def test_getvalue_flushdraw_hi_returns1410090702():
    h = tools.make('flushdrawA')
    assert ev.get_value(h) == 1410090702


def test_gettype_flushdrawhi_returnsHIGHCARD():
    h = tools.make('flushdrawA')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'HIGH CARD'


def test_getvalue_flushdraw_returns1009070302():
    h = tools.make('flushdrawB')
    assert ev.get_value(h) == 1009070302


def test_gettype_flushdraw_returnsHIGHCARD():
    h = tools.make('flushdrawB')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'HIGH CARD'


def test_getvalue_OESD_returns1110090802():
    h = tools.make('OESD')
    assert ev.get_value(h) == 1110090802


def test_gettype_OESD_returns():
    h = tools.make('OESD')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'HIGH CARD'


def test_getvalue_GSSD_returns1413111002():
    h = tools.make('GSSD')
    assert ev.get_value(h) == 1413111002


def test_gettype_GSSD_returnsHIGHCARD():
    h = tools.make('GSSD')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'HIGH CARD'


def test_getvalue_wheeldraw_returns1413040302():
    h = tools.make('wheeldraw')
    assert ev.get_value(h) == 1413040302


def test_gettype_wheeldraw_returnsHIGHCARD():
    h = tools.make('wheeldraw')
    val = ev.get_value(h)
    assert ev.get_type(val) == 'HIGH CARD'
