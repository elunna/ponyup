"""
  " Tests for hand.py
  """
import pytest
from ..src import hand
from ..src import playingcard as pc


@pytest.fixture
def _hand():
    # Create a test Hand with one card, Ace of Spades.
    c = pc.PlayingCard('A', 's')
    h = hand.Hand()
    h.add(c)
    return h


@pytest.fixture
def queen_spades():
    return pc.PlayingCard('Q', 's')


def test_len_newcardlist_size0():
    h = hand.Hand()
    assert len(h) == 0


def test_len_1card_len1(_hand):
    assert len(_hand) == 1


def test_str_1card(_hand):
    _hand.reveal()
    assert str(_hand) == 'As'


def test_add_1card_length1(queen_spades):
    h = hand.Hand()
    h.add(queen_spades)
    assert len(h) == 1


def test_add_1card_containsCard(queen_spades):
    h = hand.Hand()
    h.add(queen_spades)
    assert queen_spades in h.cards


def test_discard_1card_length0(_hand):
    ace = pc.PlayingCard('A', 's')
    _hand.discard(ace)
    assert len(_hand) == 0


def test_discard_1card_returnsCard(_hand):
    ace = pc.PlayingCard('A', 's')
    assert _hand.discard(ace) == ace


def test_discard_cardNotInHand_raiseException(queen_spades):
    h = hand.Hand()
    with pytest.raises(ValueError):
        h.discard(queen_spades)


def test_getupcards_1downcard_returnsEmptyList(_hand):
    assert _hand.get_upcards() == []


def test_getupcards_1upcard_returnsUpCard(queen_spades):
    queen_spades.hidden = False
    h = hand.Hand()
    h.add(queen_spades)
    assert h.get_upcards() == [queen_spades]


def test_getupcards_1up1down_returns1up(_hand):
    c = pc.PlayingCard('K', 's')
    _hand.add(c)
    _hand.cards[0].hidden = False
    assert len(_hand.get_upcards()) == 1


def test_isempty_hasacard_returnFalse(_hand):
    assert _hand.is_empty() is False


def test_isempty_emptylist_returnTrue():
    _hand = hand.Hand()
    assert _hand.is_empty()


def test_reveal_1card_cardIsUp(_hand):
    _hand.reveal()
    assert _hand.cards[0].hidden is False


def test_reveal_2cards_bothcardsUp(_hand):
    """ Unhide a 2 card hand, both cards are up """
    c = pc.PlayingCard('K', 's')
    _hand.add(c)
    _hand.reveal()
    assert _hand.cards[0].hidden is False
    assert _hand.cards[1].hidden is False


def test_reveal_1card_faceup(_hand):
    _hand.reveal()
    assert _hand.cards[0].hidden is False
