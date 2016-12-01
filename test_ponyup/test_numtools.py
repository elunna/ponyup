"""
  " Tests for numtools.py
  """
import unittest
from ponyup import numtools


class TestNumtools(unittest.TestCase):
    """ Function tests """
    def test_isinteger_10_returnsTrue(self):
        expected = True
        result = numtools.is_integer(10)
        self.assertEqual(expected, result)

    def test_isinteger_str10_returnsTrue(self):
        expected = True
        result = numtools.is_integer('10')
        self.assertEqual(expected, result)

    def test_isinteger_string_returnsFalse(self):
        expected = False
        result = numtools.is_integer('string')
        self.assertEqual(expected, result)

    def test_isinteger_float_returnsFalse(self):
        expected = False
        result = numtools.is_integer(10.5)
        self.assertEqual(expected, result)

    def test_isinteger_str10pt3_returnsTrue(self):
        expected = False
        result = numtools.is_integer('10.3')
        self.assertEqual(expected, result)

    def test_roundnumber_10pt5_returns11(self):
        num = 10.5
        expected = 11
        result = numtools.round_number(num)
        self.assertEqual(expected, result)

    def test_roundnumber_10pt4_returns10(self):
        num = 10.4
        expected = 10
        result = numtools.round_number(num)
        self.assertEqual(expected, result)

    def test_roundnumber_1_returns1(self):
        num = 1
        expected = 1
        result = numtools.round_number(num)
        self.assertEqual(expected, result)
