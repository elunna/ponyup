#!/usr/bin/env python3
"""
This is a collection of functions that return lists of cards that compose all the regular poker
hands and also some variations on them. These are meant to be used for testing.
"""
from __future__ import print_function
import deck
import card

# These are constants to help with computer AI
HI_AQ = 1412000000
PAIR_22 = 20000000000
PAIR_66 = 20600000000
PAIR_JJ = 21100000000
PAIR_AA = 21400000000
TWOPAIR_22 = 30000000000
TWOPAIR_JJ = 31100000000
TRIPS = 40000000000


def dealhand(quantity):
    # Deal a regular 5 card hand from a new deck
    d = deck.Deck()
    for c in d.cards:
        c.hidden = False
    d.shuffle()
    return [d.deal() for i in range(quantity)]


def deal_duplicates():
    dupes = [('A', 's'), ('3', 'h'), ('A', 's'), ('4', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in dupes]


def royalflush():
    h = [('A', 's'), ('K', 's'), ('J', 's'), ('T', 's'), ('Q', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def straightflush_high():
    h = [('9', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('T', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def straightflush_low():
    h = [('2', 's'), ('A', 's'), ('3', 's'), ('4', 's'), ('5', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def quads_high():
    h = [('A', 's'), ('A', 'd'), ('A', 'h'), ('A', 'c'), ('K', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def quads_low():
    h = [('2', 's'), ('2', 'd'), ('2', 'h'), ('2', 'c'), ('3', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def boat_high():
    h = [('A', 's'), ('A', 'd'), ('A', 'h'), ('K', 'd'), ('K', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def boat_low():
    h = [('2', 's'), ('2', 'd'), ('2', 'h'), ('3', 'd'), ('3', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def flush_high():
    h = [('A', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def flush_low():
    h = [('2', 's'), ('3', 's'), ('4', 's'), ('5', 's'), ('7', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def straight_high():
    h = [('A', 's'), ('T', 'c'), ('K', 's'), ('J', 'd'), ('Q', 'h')]
    return [card.Card(x[0], x[1]) for x in h]


def straight_mid():
    h = [('8', 's'), ('7', 'h'), ('9', 's'), ('T', 'd'), ('J', 'h')]
    return [card.Card(x[0], x[1]) for x in h]


def straight_low():
    h = [('2', 's'), ('3', 'h'), ('A', 's'), ('4', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def set_high():
    h = [('A', 's'), ('K', 'h'), ('A', 'h'), ('A', 'd'), ('Q', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def set_low():
    h = [('2', 's'), ('2', 'h'), ('2', 'h'), ('3', 'd'), ('4', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def twopair_high():
    h = [('A', 's'), ('A', 'h'), ('K', 's'), ('K', 'd'), ('Q', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def twopair_low():
    h = [('2', 's'), ('2', 'h'), ('3', 's'), ('3', 'd'), ('4', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def pair_high():
    h = [('K', 's'), ('Q', 'h'), ('A', 's'), ('A', 'd'), ('J', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def pair_low():
    h = [('2', 's'), ('3', 'h'), ('2', 'c'), ('4', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in h]


def OESFD():
    h = [('J', 's'), ('T', 's'), ('8', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def GSSFD():
    h = [('J', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def flushdrawA():
    h = [('A', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def flushdrawB():
    h = [('3', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def OESD():
    h = [('J', 'h'), ('T', 's'), ('8', 'c'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in h]


def GSSD():
    h = [('J', 'h'), ('T', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
    return [card.Card(x[0], x[1]) for x in h]


def wheeldraw():
    h = [('3', 'h'), ('4', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
    return [card.Card(x[0], x[1]) for x in h]
