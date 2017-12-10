"""
  " Tests for secure_deck.py
  """

from ..src import secure_deck as sc


def test_init_size52():
    d = sc.SecureDeck()
    assert len(d) == 52
