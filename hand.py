#!/usr/bin/env python

from __future__ import print_function
import evaluator


class Hand():
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
        self.update()

    def __str__(self):
        handstr = ''
        #  for i, c in enumerate(sorted(self.cards)):
        # Sort here?
        for i, c in enumerate(self.cards):
            handstr += str(c)
            if i != len(self.cards) - 1:
                handstr += ' '
        return handstr

    def add(self, card):
        self.cards.append(card)
        self.update()

    def discard(self, card):
        i = self.cards.index(card)
        copy = self.cards.pop(i)
        self.update()
        return copy

    def __len__(self):
        return len(self.cards)

    def unhide(self):
        for c in self.cards:
            c.hidden = False

    def update(self):
        self.cards = sorted(self.cards)
        self.value = evaluator.get_value(self.cards)
        self.handrank = evaluator.get_type(self.value)
        self.description = evaluator.get_description(self.value, self.cards)
