"""
  " Tests for colors.py
  """

from ..src import card
from ..src import colors


# Pass an integer 10. Returns True.
def test_color_redforeground():
    txt = 'test'
    expected = '\x1b[0;31;40m' + txt + '\x1b[0m'
    assert colors.color(txt, 'RED') == expected


def test_color_greenforeground():
    txt = 'test'
    expected = '\x1b[0;32;40m' + txt + '\x1b[0m'
    assert colors.color(txt, 'GREEN') == expected


def test_color_yellowforeground():
    txt = 'test'
    expected = '\x1b[0;33;40m' + txt + '\x1b[0m'
    assert colors.color(txt, 'YELLOW') == expected


def test_color_hiddenCard_returnsPurpleXx():
    c = card.Card('A', 's')
    expected = '\x1b[0;35;40mXx\x1b[0m'
    assert colors.color_cards(str(c)) == expected


def test_color_Ac_returnsGreenText():
    c = card.Card('A', 'c')
    c.hidden = False
    expected = '\x1b[0;32;40mAc\x1b[0m'
    assert colors.color_cards(str(c)) == expected


def test_color_Ad_returnsBlueText():
    c = card.Card('A', 'd')
    c.hidden = False
    expected = '\x1b[0;34;40mAd\x1b[0m'
    assert colors.color_cards(str(c)) == expected


def test_color_Ah_returnsRedText():
    c = card.Card('A', 'h')
    c.hidden = False
    expected = '\x1b[0;31;40mAh\x1b[0m'
    assert colors.color_cards(str(c)) == expected


def test_color_As_returnsWhiteText():
    c = card.Card('A', 's')
    c.hidden = False
    expected = '\x1b[0;37;40mAs\x1b[0m'
    assert colors.color_cards(str(c)) == expected
