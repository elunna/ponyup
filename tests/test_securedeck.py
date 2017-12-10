"""
  " Tests for secure_deck.py
  """

import pytest
from ..src import secure_deck


@pytest.fixture
def sc():
    return secure_deck.SecureDeck()


def test_init_size52(sc):
    assert len(sc) == 52
