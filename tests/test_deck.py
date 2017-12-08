"""
  " Tests for deck.py
  """
import pytest
from ..src import deck
from ..src import card
from ..src import tools


def test_str_2cards_returnsAsKsinParentheses():
    cards = tools.convert_to_cards(['As', 'Ks'])
    d = deck.Deck(cards)
    d.unhide()  # They are hidden by default
    assert str(d) == 'As Ks'


def test_len_size52():
    d = deck.Deck()
    assert len(d) == 52


def test_len_2cards_haslen2():
    cards = tools.convert_to_cards(['As', 'Ks'])
    d = deck.Deck(cards)
    assert len(d) == 2


def test_contains_AceSpadesinStandardDeck_returnsTrue():
    d = deck.Deck()
    c = card.Card('A', 's')
    assert c in d


def test_contains_JokerinStandardDeck_returnsFalse():
    d = deck.Deck()
    c = card.JOKER1
    assert c not in d


def test_sort_2cards_deuceisfirst():
    cards = tools.convert_to_cards(['As', '2s'])
    d = deck.Deck(cards)
    d.sort()
    assert d.cards[0].rank == '2'


def test_sort_3cards_deuceisfirst():
    cards = tools.convert_to_cards(['As', '7s', '2s'])
    d = deck.Deck(cards)
    d.sort()
    assert d.cards[0].rank == '2'


def test_deal_stddeck_sizeIs51():
    d = deck.Deck()
    d.deal()
    assert len(d) == 51


def test_deal_As_returnsCard():
    c = card.Card('A', 's')
    d = deck.Deck([c])
    assert d.deal() == c


def test_deal_emptydeck_raiseException():
    d = deck.Deck([])
    assert len(d) == 0
    with pytest.raises(Exception):
        d.deal


def test_isempty_fulldeck_returnFalse():
    d = deck.Deck()
    assert not d.is_empty()


def test_isempty_emptydeck_returnTrue():
    d = deck.Deck([])
    assert d.is_empty()


def test_remove_removeAs_sizeIs51():
    d = deck.Deck()
    c = card.Card('A', 's')
    d.remove(c)
    assert len(d) == 51


def test_remove_cardnotindeck_returnsNone():
    d = deck.Deck()
    c = card.Card('Z', 's')
    assert d.remove(c) == None


def test_removecards_removeAs_sizeIs51():
    d = deck.Deck()
    c = card.Card('A', 's')
    d.remove_cards([c])
    assert len(d) == 51


def test_removecards_removeAs_containsIsFalse():
    d = deck.Deck()
    c = card.Card('A', 's')
    d.remove_cards([c])
    assert c not in d


def test_removecards_removeAsKs_containsNeither():
    d = deck.Deck()
    cards = tools.convert_to_cards(['As', 'Ks'])
    d.remove_cards(cards)
    assert cards[0] not in d
    assert cards[1] not in d


# All cards in deck are faceup
def test_unhide_2cards_bothfaceup():
    cards = tools.convert_to_cards(['As', 'Ks'])
    d = deck.Deck(cards)
    d.unhide()
    assert d.cards[0].hidden is False
    assert d.cards[1].hidden is False


""" Tests for Deck1Joker """


def test_init_Deck1Joker_size53():
    d = deck.Deck1Joker()
    assert len(d) == 53


def test_init_Deck1Joker_containsZs():
    d = deck.Deck1Joker()
    joker = card.Card('Z', 's')
    assert joker in d


""" Tests for Deck2Joker """


def test_init_Deck2Joker_size54():
    d = deck.Deck2Joker()
    assert len(d) == 54


def test_init_Deck2Joker_containsZsZc():
    d = deck.Deck2Joker()
    joker1 = card.Card('Z', 's')
    joker2 = card.Card('Z', 'c')
    assert joker1 in d
    assert joker2 in d


""" Tests for PiquetDeck"""


def test_init_PiquetDeck_size32():
    d = deck.PiquetDeck()
    assert len(d) == 32


def test_init_PiquetDeck_4Aces():
    d = deck.PiquetDeck()
    result = sum(1 for c in d.cards if c.rank == 'A')
    assert result == 4


def test_init_PiquetDeck_1AceSpades():
    d = deck.PiquetDeck()
    c = card.Card('A', 's')
    assert d.cards.count(c) == 1


""" Tests for PinochleDeck """


def test_init_PinochleDeck_size48():
    d = deck.PinochleDeck()
    assert len(d) == 48


def test_init_PinochleDeck_8Aces():
    d = deck.PinochleDeck()
    result = sum(1 for c in d.cards if c.rank == 'A')
    assert result == 8


def test_init_PinochleDeck_2AceSpades():
    c = card.Card('A', 's')
    d = deck.PinochleDeck()
    assert d.cards.count(c) == 2


""" Tests for BlackjackDeck """


def test_init_0shoes_raiseException():
    with pytest.raises(ValueError):
        deck.BlackjackDeck(0)


def test_init_negshoes_raiseException():
    with pytest.raises(ValueError):
        deck.BlackjackDeck(-1)


def test_init_4shoes_208cards():
    d = deck.BlackjackDeck(4)
    assert len(d) == 208


def test_init_4shoes_4AceSpaces():
    d = deck.BlackjackDeck(4)
    c = card.Card('A', 's')
    assert d.cards.count(c) == 4


def test_init_6shoes_312cards():
    d = deck.BlackjackDeck(6)
    assert len(d) == 312
