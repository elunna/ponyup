"""
  " Tests for hand.py
  """
import pytest
from ..src import playingcard as pc
from ..src import hand
from ..src import tools


""" Function tests for hand.py """


def test_init_invalidboth_raiseEx():
    with pytest.raises(ValueError):
        pc.PlayingCard('s', 'A')


# No cards pass, length = 0
def test_init_0cardspassed_length0():
    h = hand.Hand()
    assert len(h) == 0


# 1 card passed, length = 1
def test_init_1cardpassed_length1():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    assert len(h) == 1


# 1 card passed, contains the card
def test_init_1cardpassed_containsCard():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    assert c in h.cards


# No cards pass, displays nothing
def test_str_0cardspassed_returnsNothing():
    h = hand.Hand()
    assert str(h) == ''


# 1 card passed, displays the hidden card as "Xx"
def test_str_1card_hidden_returnsAs():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    assert str(h) == 'Xx'


# 1 card passed, displays the hidden card as "Xx"
def test_str_1card_unhidden_returnsAs():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    h.unhide()
    assert str(h) == 'As'


# 1 card passed, displays the hidden card as "Xx"
def test_str_2cards_unhidden_returnsAs_Ks():
    cards = tools.convert_to_cards(['As', 'Ks'])
    h = hand.Hand(cards)
    h.unhide()
    assert str(h) == 'As Ks'


# Empty hand, adding 1 card, size = 1
def test_add_1card_length1():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand()
    h.add(c)
    assert len(h) == 1


# Empty hand, adding 1 card, contains the card
def test_add_1card_containsCard():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand()
    h.add(c)
    assert c in h.cards


# Discarding the only card in the hand, size = 0
def test_discard_1card_length0():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    h.discard(c)
    assert len(h) == 0


# Discarding the only card in the hand, returns the card
def test_discard_1card_returnsCard():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    assert h.discard(c) == c


# Discarding a card not in the hand, raise exception
def test_discard_cardNotInHand_raiseException():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand()
    with pytest.raises(ValueError):
        h.discard(c)


# Unhide a 1 card hand, the card is up
def test_unhide_1card_cardIsUp():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    h.unhide()
    assert h.cards[0].hidden is False


def test_unhide_2cards_bothcardsUp():
    """ Unhide a 2 card hand, both cards are up """
    c1 = pc.PlayingCard('A', 's')
    c2 = pc.PlayingCard('K', 's')
    h = hand.Hand()
    h.add(c1)
    h.add(c2)
    h.unhide()

    assert h.cards[0].hidden is False
    assert h.cards[1].hidden is False


# Takes in a 564 hand and after it is 456
def test_sort_unsortedhand_sortedafter():
    cards = tools.convert_to_cards(['5s', '6s', '4s'], hidden=False)
    h = hand.Hand(cards)
    h.sort()
    assert h.cards == [cards[2], cards[0], cards[1]]


def test_value_royalflush_returns100000000000():
    h = hand.Hand(tools.make('royalflush'))
    assert h.value() == 100000000000


def test_rank_royalflush_returnsROYALFLUSH():
    h = hand.Hand(tools.make('royalflush'))
    assert h.rank() == 'ROYAL FLUSH'


def test_desc_royalflush_AceHigh():
    h = hand.Hand(tools.make('royalflush'))
    assert h.desc() == 'A High'


# 1 card hand that is hidden - return empty list
def test_getupcards_1downcard_returnsEmptyList():
    c = pc.PlayingCard('A', 's')
    h = hand.Hand([c])
    assert h.get_upcards() == []


# 1 card hand that is up - return card
def test_getupcards_1upcard_returnsUpCard():
    c = pc.PlayingCard('A', 's')
    c.hidden = False
    h = hand.Hand([c])
    assert h.get_upcards() == [c]


# 2 card hand - 1 up, 1 down - returns the up card
def test_getupcards_1up1down_returns1up():
    cards = tools.convert_to_cards(['As', 'Ks'])
    cards[0].hidden = False
    h = hand.Hand(cards)
    assert len(h.get_upcards()) == 1


def test_peek_AsKs_returnslist():
    cards = tools.convert_to_cards(['As', 'Ks'])
    h = hand.Hand(cards)
    assert h.peek() == ['As ', 'Ks ']


def test_peek_AsKs_stillhidden():
    cards = tools.convert_to_cards(['As', 'Ks'])
    h = hand.Hand(cards)
    h.peek()
    assert h.cards[0].hidden is True
    assert h.cards[1].hidden is True
