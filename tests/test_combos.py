"""
  " Tests for combos.py
  """
import pytest
from ponyup import combos
from ponyup import deck
from ponyup import tools


def test_nchoosek_0pick1_raiseException():
    with pytest.raises(ValueError):
        combos.n_choose_k(0, 1)


def test_nchoosek_1pick0_raiseException():
    with pytest.raises(ValueError):
        combos.n_choose_k(1, 0)


def test_nchoosek_neg1pick1_raiseException():
    with pytest.raises(ValueError):
        combos.n_choose_k(-1, 1)


def test_nchoosek_1pickneg1_raiseException():
    with pytest.raises(ValueError):
        combos.n_choose_k(1, -1)


# K larger than N
def test_nchoosek_1pick2_raiseException():
    with pytest.raises(ValueError):
        combos.n_choose_k(1, 2)


def test_nchoosek_1pick1_returns1():
    assert combos.n_choose_k(1, 1) == 1


def test_nchoosek_2pick1_returns1():
    assert combos.n_choose_k(2, 1) == 2


def test_nchoosek_3pick2_returns3():
    assert combos.n_choose_k(3, 2) == 3


def test_getcombos_of1withfullDeck_52combos():
    d = deck.Deck()
    combosof1 = combos.get_combolist(d.cards, 1)
    assert len(combosof1) == 52


def test_getcombos_of2withfullDeck_1326combos():
    d = deck.Deck()
    combosof2 = combos.get_combolist(d.cards, 2)
    assert len(combosof2) == 1326


def test_getcombos_of3withfullDeck_22100combos():
    d = deck.Deck()
    combosof3 = combos.get_combolist(d.cards, 3)
    assert len(combosof3) == 22100

"""
def test_getcombos_of4withfullDeck_combos270725():
    d = deck.Deck()
    combosof4 = combos.get_combolist(d.cards, 4)
    assert len(combosof4) == 270725


def test_getcombos_of5withfullDeck_2598960combos():
    d = deck.Deck()
    combosof5 = combos.get_combolist(d.cards, 5)
    assert len(combosof5) == 2598960
"""


def test_getallcombos_emptylist_returns0():
    allcombos = combos.get_allcombos([])
    assert len(allcombos) == 0


def test_getallcombos_1card_returns1():
    cards = tools.convert_to_cards(['As'])
    allcombos = combos.get_allcombos(cards)
    assert len(allcombos) == 1


def test_getallcombos_2cards_returns3():
    cards = tools.convert_to_cards(['As', 'Ks'])
    allcombos = combos.get_allcombos(cards)
    assert len(allcombos) == 3


def test_getallcombos_3cards_returns7():
    cards = tools.convert_to_cards(['As', 'Ks', 'Qs'])
    allcombos = combos.get_allcombos(cards)
    assert len(allcombos) == 7
