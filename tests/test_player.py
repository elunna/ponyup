"""
  " Tests for player.py
  """
import pytest
from ..src import player


# valid name, player name is ok
def test_init_validname_namematches():
    p = player.Player('Erik')
    assert p.name == 'Erik'


# new player - bank == 0
def test_init_validname_has0chips():
    p = player.Player('Erik')
    assert p.bank == 0


def test_init__():
    with pytest.raises(ValueError):
        player.Player('ab')


# Return players name
def test_str_validname_returnsName():
    p = player.Player('Erik')
    assert str(p) == 'Erik'


# Return players name
def test_repr_validname_returnsName():
    p = player.Player('Erik')
    assert p.__repr__() == 'Erik'


# If a player has 0 and bets 0, it returns 0
def test_withdraw_has0chipsbets0_returns0():
    p = player.Player('Erik')
    assert p.withdraw(0) == 0


# If a player has 0 and bets 1, it returns 0
def test_withdraw_has0chipsbets1_returns0():
    p = player.Player('Erik')
    assert p.withdraw(1) == 0


# If a player has 1 and bets 1, it returns 1
def test_withdraw_has1chipbets1_returns1():
    p = player.Player('Erik')
    p.deposit(1)
    assert p.withdraw(1) == 1


# If a player has 1 and bets 1, they have 0 chips.
def test_withdraw_has1chipbets1_has0chips():
    p = player.Player('Erik')
    p.deposit(1)
    p.withdraw(1)
    assert p.bank == 0


# If a player has 1 and bets 1, they have 0 chips.
def test_withdraw_negativebet_raisesException():
    p = player.Player('Erik')
    p.deposit(1)
    with pytest.raises(ValueError):
        p.withdraw(-1)


# Adding 1 chip results in their stack being 1. Starting with 1.
def test_deposit_newplayer_add1chip_has1chip():
    p = player.Player('Erik')
    p.deposit(1)
    assert p.bank == 1


# Adding 0 chips results in no chips added.
def test_deposit_newplayer_add0chips_has0chip():
    p = player.Player('Erik')
    p.deposit(0)
    assert p.bank == 0


# Cannot add negative chips!
def test_deposit_negativechips_raisesException():
    p = player.Player('Erik')
    with pytest.raises(Exception):
        p.deposit(-100)
