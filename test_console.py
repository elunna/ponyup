import card
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

    """
    Tests for color(self):
    """
    def test_color_hiddenCard_returnsPurpleXx(self):
        c = card.Card('A', 's')
        expected = '\x1b[0;35;40mXx\x1b[0m'
        result = console.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_Ac_returnsGreenText(self):
        c = card.Card('A', 'c')
        c.hidden = False
        expected = '\x1b[0;32;40mAc\x1b[0m'
        result = console.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_Ad_returnsBlueText(self):
        c = card.Card('A', 'd')
        c.hidden = False
        expected = '\x1b[0;34;40mAd\x1b[0m'
        result = console.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_Ah_returnsRedText(self):
        c = card.Card('A', 'h')
        c.hidden = False
        expected = '\x1b[0;31;40mAh\x1b[0m'
        result = console.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_As_returnsWhiteText(self):
        c = card.Card('A', 's')
        c.hidden = False
        expected = '\x1b[0;37;40mAs\x1b[0m'
        result = console.color_cards(str(c))
        self.assertEqual(expected, result)
