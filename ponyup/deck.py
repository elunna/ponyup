#!/usr/bin/env python
"""
Creates a Deck of cards.
"""
from __future__ import print_function
import random
from ponyup import card


class Deck():
    """
    Creates a standard 52 card deck, with no Jokers.
    """
    def __init__(self, cards=None):
        if cards is None:
            self.cards = \
                [card.Card(r, s[0]) for s in card.SUITS for r in card.RANKS if r != 'Z']
        else:
            self.cards = cards

    def __str__(self):
        """
        Returns a string showing all the cards in the deck.
        """
        _str = ''
        for i, c in enumerate(self.cards):
            if i % 13 == 0 and i != 0:
                _str += '\n'
            _str += '{} '.format(str(c))
        return _str.strip()

    def __len__(self):
        """
        Returns how many cards are in the Deck.
        """
        return len(self.cards)

    def __contains__(self, card):
        """
        Returns True if the given Card is in the deck, False otherwise.
        """
        return card in self.cards

    def shuffle(self, x):
        """
        Shuffles the deck of cards once.
        """
        for i in range(x):
            random.shuffle(self.cards)

    def sort(self):
        """
        Sorts the deck by card rank.
        """
        self.cards.sort(key=lambda x: x.val())

    def deal(self):
        """
        Removes the top card off the deck and returns it. Raises an exception if the deck is
        empty.
        """
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            raise Exception('Deck is empty, cannot deal cards!')

    def is_empty(self):
        """
        Returns True if the Deck is empty, False otherwise.
        """
        return len(self.cards) == 0

    def remove(self, card):
        """
        Removes the specified Card from the deck.
        """
        if card in self.cards:
            self.cards.remove(card)
        else:
            return None

    def remove_cards(self, cards):
        """
        Removes a sequence of cards from the deck. If a card in the sequence is not in the deck
        it is simply ignored.
        """
        for c in cards:
            self.remove(c)

    def unhide(self):
        """
        Goes through all cards in the deck and unhides them.
        """
        for c in self.cards:
            c.hidden = False


class Deck1Joker(Deck):
    """
    Creates a deck with one Joker.
    """
    def __init__(self):
        super().__init__()
        self.cards.append(card.JOKER1)


class Deck2Joker(Deck):
    """
    Creates a deck with two Jokers.
    """
    def __init__(self):
        super().__init__()
        self.cards.append(card.JOKER1)
        self.cards.append(card.JOKER2)


class PiquetDeck(Deck):
    """
    Creates a 48 card Pinochle deck with 2 of each rank: 9, T, J, Q, K, A.
    """
    def __init__(self):
        pinochle_cards = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.cards = [card.Card(r, s[0])
                      for s in card.SUITS for r in card.RANKS if r in pinochle_cards]


class PinochleDeck(Deck):
    """
    Creates a 48 card Pinochle deck with 2 of each rank: 9, T, J, Q, K, A.
    """
    def __init__(self):
        pinochle_cards = ['9', 'T', 'J', 'Q', 'K', 'A']
        c = [card.Card(r, s[0]) for s in card.SUITS for r in card.RANKS if r in pinochle_cards]

        self.cards = c + c


class BlackjackDeck(Deck):
    """
    Creates a blackjack deck with the specified number of 'shoes' included. 4 shoes is the most
    common size for a Las Vegas blackjack deck.
    """
    def __init__(self, shoes=4):
        if shoes < 1:
            raise ValueError('BlackjackDeck must be passed a value of 1 or more for shoes!')

        super().__init__()
        cardset = self.cards[:]
        for i in range(shoes - 1):
            self.cards.extend(cardset)
