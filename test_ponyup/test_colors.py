import unittest
from ponyup import colors


class TestColors(unittest.TestCase):

    """
    Tests for
    """
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
