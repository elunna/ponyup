"""
  " Tests for numtools.py
  """
from ..src import numtools


def test_isinteger_10_returnsTrue():
    assert numtools.is_integer(10)


def test_isinteger_str10_returnsTrue():
    assert numtools.is_integer('10')


def test_isinteger_string_returnsFalse():
    assert numtools.is_integer('string') is False


def test_isinteger_float_returnsFalse():
    assert numtools.is_integer(10.5) is False


def test_isinteger_str10pt3_returnsTrue():
    assert numtools.is_integer('10.3') is False


def test_roundnumber_10pt5_returns11():
    assert numtools.round_number(10.5) == 11


def test_roundnumber_10pt4_returns10():
    assert numtools.round_number(10.4) == 10


def test_roundnumber_1_returns1():
    assert numtools.round_number(1) == 1
