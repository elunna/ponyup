"""
  " Tests for card.py
  """
import pytest
from ..src import card
BACK_TEXT = card.BACK_TEXT


@pytest.fixture
def testcard():
    return card.Card('As')


def test_init_cardtype(testcard):
    assert isinstance(testcard, card.Card)


def test_init_str(testcard):
    assert str(testcard) == BACK_TEXT  # Should be hidden by default


def test_init_default_hiddenIsTrue(testcard):
    assert testcard.hidden is True


def test_str_hiddenCard_returnsXx(testcard):
    assert str(testcard) == BACK_TEXT


def test_repr_hiddenCard_returnsXx(testcard):
    assert repr(testcard) == BACK_TEXT


def test_repr_FaceupAs_returnsAs(testcard):
    testcard.hidden = False
    assert repr(testcard) == 'As'


def test_hide(testcard):
    testcard.hide()
    assert testcard.hidden is True


def test_unhide(testcard):
    testcard.unhide()
    assert testcard.hidden is False


def test_peek_hidden(testcard):
    testcard.hide()
    assert str(testcard) == BACK_TEXT


def test_peek_faceup(testcard):
    testcard.unhide()
    assert str(testcard) == 'As'
