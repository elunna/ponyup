"""
  " Tests for blinds.py
  """
import pytest
from ..src import blinds


def test_init_shouldbelevel1():
    b = blinds.Blinds()
    assert b.level == 1

# Can use blinds and antes
# Can use bringin and antes
# Can't use both blinds and bringin.


def test_str_level1_returns_SB1_BB2(self):
    b = blinds.Blinds(1)
    assert str(b) == 'SB: $1, BB: $2\n'


def test_str_level5_returns_SB15_BB30(self):
    b = blinds.Blinds(5)
    assert str(b) == 'SB: $15, BB: $30\n'


def test_str_level5_withantes__returns_SB30_BB60_ante15(self):
    b = blinds.Blinds(5, antes=True)
    assert str(b) == 'Ante: $7.50, SB: $15, BB: $30\n'

# Test antes, bringin


# trying to use a limit outside out the bounds of the blind_dictionary, raise exception
def test_setlevel_level0_raiseException(self):
    b = blinds.Blinds()
    with pytest.raises(ValueError):
        b.set_level(0)


def test_setlevel_level1000_raiseException(self):
    b = blinds.Blinds()

    with pytest.raises(ValueError):
        b.set_level(1000)


def test_setlevel_level1_SB1_BB2(self):
    b = blinds.Blinds()
    assert b.SB == 1
    assert b.BB == 2


def test_str_level1_returns2_4_stakes(self):
    b = blinds.Blinds()
    assert b.stakes() == '$2-$4'


def test_str_level5_returns30_60_stakes(self):
    b = blinds.Blinds(5)
    assert b.stakes() == '$30-$60'


# 50/100 blinds
def test_bigblinds_BB2_stack100_returns50(self):
    b = blinds.Blinds(1)
    stack = 100
    assert b.big_blinds(stack) == 50


# 50/100 blinds
def test_bigblinds_BB100_stack1000_returns10(self):
    b = blinds.Blinds(7)
    stack = 1000
    assert b.big_blinds(stack) == 10


# 50/100 blinds
def test_bigblinds_BB100_stack1050_returns11(self):
    b = blinds.Blinds(7)
    stack = 1050
    assert b.big_blinds(stack) == 11


def test_bigblinds_BB100_stack1070_returns11(self):
    b = blinds.Blinds(7)
    stack = 1070
    assert b.big_blinds(stack) == 11


def test_bigblinds_BB100_antes_stack1000_returns10(self):
    b = blinds.Blinds(7, antes=True)
    stack = 1000
    assert b.big_blinds(stack) == 10


# 50/100 blinds with no ante. No change from regular BB
def test_trueBB_BB100_returns100(self):
    b = blinds.Blinds(7)
    assert b.trueBB(players=8) == b.BB


# 50/100 blinds w ante
def test_trueBB_BB100_8players_returns429(self):
    b = blinds.Blinds(7, antes=True)
    assert b.trueBB(players=8) == 231


# 100/200 blinds with 25 ante.
def test_trueBB_BB200_8players_returns660(self):
    b = blinds.Blinds(8, antes=True)
    assert b.trueBB(players=8) == 462


# 100/200 blinds with 50 ante.
def test_effectiveBB_BB200_10000stack_8players_returns30(self):
    b = blinds.Blinds(8, antes=True)
    stack = 10000
    assert b.effectiveBB(stack, players=8) == 22


# 100/200 blinds with 50 ante.
def test_effectiveBB_BB200_10500stack_8players_returns32(self):
    b = blinds.Blinds(8, antes=True)
    stack = 10500
    assert b.effectiveBB(stack, players=8) == 23


# 100/200 blinds with 25 ante.
def test_effectiveBB_BB200_10350stack_8players_returns31(self):
    b = blinds.Blinds(8, antes=True)
    stack = 10350
    assert b.effectiveBB(stack, players=8) == 22


# lev1: SB=1, Ante=.50
def test_sbtoanteratio_lev1_returns2(self):
    b = blinds.Blinds(level=1, antes=True)
    assert b.sb_to_ante_ratio() == 2


# lev5: SB=15, ante=7.50
def test_sbtoanteratio_lev5_returns2(self):
    b = blinds.Blinds(level=5, antes=True)
    assert b.sb_to_ante_ratio() == 2
