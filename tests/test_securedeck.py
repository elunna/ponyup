"""
  " Tests for secure_deck.py
  """

import pytest
from ..src import card
from ..src import secure_deck


@pytest.fixture
def sc():
    return secure_deck.SecureDeck()


def test_init_size52(sc):
    assert len(sc) == 52


def test_deal_size51(sc):
    sc.deal()
    assert len(sc) == 51


def test_deal_returnsCard(sc):
    c = sc.deal()
    assert isinstance(c, card.Card)


def test_deal_allcards_raiseException(sc):
    with pytest.raises(Exception):
        while True:
            sc.deal()


def test_copy_card_list_raiseException(sc):
    # We should not be able to get the list
    with pytest.raises(Exception):
        sc.cards[:]


def test_access_card_list_raiseException(sc):
    # We should not be able to get the list
    with pytest.raises(Exception):
        sc.cards
