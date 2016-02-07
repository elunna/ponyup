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

        self.value = evaluator.get_value(self.cards)
        self.handrank = evaluator.get_type(self.value)

    def __str__(self):
        handstr = ''
        for c in self.cards:
            handstr += str(c) + ' '
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

    def update(self):
        # Sorting should make it easier to read!
        self.cards = sorted(self.cards)
        self.value = evaluator.get_value(self.cards)
        self.handrank = evaluator.get_type(self.value)

    def unhide(self):
        for c in self.cards:
            c.hidden = False
