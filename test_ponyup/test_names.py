import unittest
from ponyup import names


class TestNames(unittest.TestCase):

    """
    Tests for random_names(num)
    """
    def test_randomnames_10_returns10names(self):
        namelist = names.random_names(10, names.pokerplayers)
        expected = 10
        result = len(namelist)
        self.assertEqual(expected, result)

    def test_randomnames_10_isset(self):
        qty = 10
        namelist = names.random_names(qty, names.pokerplayers)
        expected = qty
        result = len(set(namelist))
        self.assertEqual(expected, result)

    """
    Tests for is_validname(name)
    """
    def test_isvalidname_2char_returnsFalse(self):
        name = 'qz'
        expected = False
        result = names.is_validname(name)
        self.assertEqual(expected, result)

    def test_isvalidname_20char_returnsTrue(self):
        name = 'qzqzqzqzqzqzqzqzqzqz'
        expected = True
        result = names.is_validname(name)
        self.assertEqual(expected, result)

    def test_isvalidname_21char_returnsFalse(self):
        name = 'qzqzqzqzqzqzqzqzqzqzz'
        self.assertTrue(len(name) == 21)
        expected = False
        result = names.is_validname(name)
        self.assertEqual(expected, result)

    def test_isvalidname_10char_returnsFalse(self):
        name = 'eriktheguy'
        expected = True
        result = names.is_validname(name)
        self.assertEqual(expected, result)

    """
    Tests for has_surr_char(string):
    """
    def test_hassurrchar_angle_returnsTrue(self):
        name = 'eriktheguy>'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_brace_returnsTrue(self):
        name = 'eriktheguy}'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_parentheses_returnsTrue(self):
        name = '(eriktheguy)'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_bracket_returnsTrue(self):
        name = '[eriktheguy]'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_fslash_returnsTrue(self):
        name = '/eriktheguy/'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_bslash_returnsTrue(self):
        name = 'eriktheguy\\'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_tilde_returnsFalse(self):
        name = '~eriktheguy'
        expected = False
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_backtick_returnsTrue(self):
        name = '`eriktheguy'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_caret_returnsFalse(self):
        name = '^eriktheguy'
        expected = False
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_singlequote_returnsTrue(self):
        name = '\'eriktheguy'
        expected = True
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)

    def test_hassurrchar_normal_returnsFalsej(self):
        name = 'eriktheguy'
        expected = False
        result = names.has_surr_char(name)
        self.assertEqual(expected, result)
