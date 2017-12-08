"""
  " Tests for blinds.py
  """
import pytest
from ..src import antes


@pytest.fixture
def _antes():
    return antes.Antes(antes=1, bringin=2)


def test_str(_antes):
    assert str(_antes) == 'Ante: $1, Bringin: $2\n'


def test_stakes(_antes):
    assert _antes.stakes() == "$2-$4"


def test_bigblinds(_antes):
    stack = 100
    assert _antes.big_blinds(stack) == 50


def test_trueBB(_antes):
    # ($2 + (10 * $1)) * .66
    assert _antes.trueBB(players=10) == 8


def test_effectiveBB(_antes):
    # 100 / 8 = 12.5, round up to 13
    assert _antes.effectiveBB(stack=100, players=10) == 13
