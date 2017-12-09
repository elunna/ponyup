"""
  " Tests for card.py
  """
import pytest
from ..src import card
Card = card.Card
BACK_TEXT = card.BACK_TEXT


@pytest.fixture
def testcard():
    return Card('As')


def test_init_cardtype(testcard):
    assert isinstance(testcard, Card)


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


def test_eq_SameCard_returnsTrue():
    """ __equals__ tests that the two cards have exactly the same suit and rank."""
    c1 = Card('As')
    c2 = Card('As')
    assert c1 == c2


def test_eq_DiffSuits_returnsFalse():
    c1 = Card('As')
    c2 = Card('Ac')
    assert c1 != c2


def test_hash1():
    c1 = Card('As')
    # Not sure if this will work long term, but this is the hash for this card
    assert hash(c1) == 8320049985075186


def test_hash2():
    c2 = Card('Ac')
    # Not sure if this will work long term, but this is the hash for this card
    assert hash(c2) == 8320049985075170
