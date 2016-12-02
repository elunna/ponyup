"""
  " Tests for colors.py
  """

import unittest
from ponyup import card
from ponyup import colors


class TestColors(unittest.TestCase):
    """ Function tests for colors.py """

    # Pass an integer 10. Returns True.
    def test_color_redforeground(self):
        txt = 'test'
        expected = '\x1b[0;31;40m' + txt + '\x1b[0m'
        result = colors.color(txt, 'RED')
        self.assertEqual(expected, result)

    def test_color_greenforeground(self):
        txt = 'test'
        expected = '\x1b[0;32;40m' + txt + '\x1b[0m'
        result = colors.color(txt, 'GREEN')
        self.assertEqual(expected, result)

    def test_color_yellowforeground(self):
        txt = 'test'
        expected = '\x1b[0;33;40m' + txt + '\x1b[0m'
        result = colors.color(txt, 'YELLOW')
        self.assertEqual(expected, result)

    def test_color_hiddenCard_returnsPurpleXx(self):
        c = card.Card('A', 's')
        expected = '\x1b[0;35;40mXx\x1b[0m'
        result = colors.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_Ac_returnsGreenText(self):
        c = card.Card('A', 'c')
        c.hidden = False
        expected = '\x1b[0;32;40mAc\x1b[0m'
        result = colors.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_Ad_returnsBlueText(self):
        c = card.Card('A', 'd')
        c.hidden = False
        expected = '\x1b[0;34;40mAd\x1b[0m'
        result = colors.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_Ah_returnsRedText(self):
        c = card.Card('A', 'h')
        c.hidden = False
        expected = '\x1b[0;31;40mAh\x1b[0m'
        result = colors.color_cards(str(c))
        self.assertEqual(expected, result)

    def test_color_As_returnsWhiteText(self):
        c = card.Card('A', 's')
        c.hidden = False
        expected = '\x1b[0;37;40mAs\x1b[0m'
        result = colors.color_cards(str(c))
        self.assertEqual(expected, result)
