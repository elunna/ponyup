""" Manages a regular hand of cards. """

from . import evaluator


class Hand(object):
    """ Poker Hand object """
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    def __len__(self):
        """ Returns how many cards are in the hand.  """
        return len(self.cards)

    def __str__(self):
        handstr = ''
        for i, c in enumerate(self.cards):
            handstr += str(c)
            if i != len(self.cards) - 1:
                handstr += ' '
        return handstr

    def __contains__(self, card):
        return card in self.cards

    def add(self, card):
        """ Adds a card to the hand. """
        self.cards.append(card)

    def discard(self, card):
        """ Removes card from the hand and returns it. """
        i = self.cards.index(card)
        copy = self.cards.pop(i)
        return copy

    def unhide(self):
        """ Switches all cards in the hand to be faceup. """
        for c in self.cards:
            c.hidden = False

    def sort(self):
        """ Sorts the cards in the hand. """
        self.cards = sorted(self.cards)

    def value(self):
        return evaluator.get_value(self.cards)

    def rank(self):
        return evaluator.get_type(self.value())

    def desc(self):
        return evaluator.get_description(self.value(), self.cards)

    def get_upcards(self):
        """ Returns a list of all the face-up cards the player has. """
        return [c for c in self.cards if c.hidden is False]

    def peek(self):
        return [c.peek() + ' ' for c in self.cards]
