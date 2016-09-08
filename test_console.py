import console
import unittest


class TestConsole(unittest.TestCase):

    """
    Tests for is_integer(num)
    """
    # Pass an integer 10. Returns True.
    def test_isinteger_10_returnsTrue(self):
        expected = True
        result = console.is_integer(10)
        self.assertEqual(expected, result)

    # Pass an integer 10. Returns True.
    def test_isinteger_str10_returnsTrue(self):
        expected = True
        result = console.is_integer('10')
        self.assertEqual(expected, result)

    # Pass a string. Returns False.
    def test_isinteger_string_returnsFalse(self):
        expected = False
        result = console.is_integer('string')
        self.assertEqual(expected, result)

    # Pass a float 10.5. Returns False.
    def test_isinteger_float_returnsFalse(self):
        expected = False
        result = console.is_integer(10.5)
        self.assertEqual(expected, result)

    # Pass an integer 10. Returns True.
    def test_isinteger_str10pt3_returnsTrue(self):
        expected = False
        result = console.is_integer('10.3')
        self.assertEqual(expected, result)
