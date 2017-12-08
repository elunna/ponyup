"""
  " Tests for blinds.py
  """
from ..src import blinds
import pytest


@pytest.fixture
def _blinds():
    return blinds.Blinds(antes=0, sb=2, bb=4)


@pytest.fixture
def _antes():
    return blinds.Blinds(antes=1, sb=2, bb=4)


def test_str(_blinds):
    assert str(_blinds) == 'SB: $2, BB: $4\n'


def test_str_with_antes(_antes):
    assert str(_antes) == 'Ante: $1, SB: $2, BB: $4\n'


def test_stakes(_blinds):
    assert _blinds.stakes() == "$4-$8"


def test_stakes_with_antes(_antes):
    assert _antes.stakes() == "$4-$8"


def test_bigblinds(_blinds):
    stack = 100
    assert _blinds.big_blinds(stack) == 25


def test_bigblinds_with_antes(_antes):
    stack = 100
    assert _antes.big_blinds(stack) == 25


def test_trueBB(_blinds):
    # ($4 + $0)
    assert _blinds.trueBB(players=10) == 4


def test_trueBB_with_antes(_antes):
    # ($4 + $2 + (10 * $1)) * .66 == 10.5, round up to 11
    assert _antes.trueBB(players=10) == 11


def test_effectiveBB(_blinds):
    # 100 / 4 = 25
    assert _blinds.effectiveBB(stack=100, players=10) == 25


def test_effectiveBB_with_antes(_antes):
    # 100 / 10.5  = 9.5, round down to 9
    assert _antes.effectiveBB(stack=100, players=10) == 9.0
