#!/usr/bin/env python3
"""
This is a collection of functions that return lists of cards that compose all the regular poker
hands and also some variations on them. These are meant to be used for testing.
"""
from __future__ import print_function
import deck
import card


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
    rf = [('A', 's'), ('K', 's'), ('J', 's'), ('T', 's'), ('Q', 's')]
    return [card.Card(x[0], x[1]) for x in rf]


def straightflush_high():
    sf = [('9', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('T', 's')]
    return [card.Card(x[0], x[1]) for x in sf]


def straightflush_low():
    sf = [('2', 's'), ('A', 's'), ('3', 's'), ('4', 's'), ('5', 's')]
    return [card.Card(x[0], x[1]) for x in sf]


def quads_high():
    quads = [('A', 's'), ('A', 'd'), ('A', 'h'), ('A', 'c'), ('K', 'c')]
    return [card.Card(x[0], x[1]) for x in quads]


def quads_low():
    quads = [('2', 's'), ('2', 'd'), ('2', 'h'), ('2', 'c'), ('3', 'c')]
    return [card.Card(x[0], x[1]) for x in quads]


def boat_high():
    fullhouse = [('A', 's'), ('A', 'd'), ('A', 'h'), ('K', 'd'), ('K', 'c')]
    return [card.Card(x[0], x[1]) for x in fullhouse]


def boat_low():
    fullhouse = [('2', 's'), ('2', 'd'), ('2', 'h'), ('3', 'd'), ('3', 'c')]
    return [card.Card(x[0], x[1]) for x in fullhouse]


def flush_high():
    flush = [('A', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in flush]


def flush_low():
    flush = [('2', 's'), ('3', 's'), ('4', 's'), ('5', 's'), ('7', 's')]
    return [card.Card(x[0], x[1]) for x in flush]


def straight_high():
    straight = [('A', 's'), ('T', 'c'), ('K', 's'), ('J', 'd'), ('Q', 'h')]
    return [card.Card(x[0], x[1]) for x in straight]


def straight_mid():
    straight = [('8', 's'), ('7', 'h'), ('9', 's'), ('T', 'd'), ('J', 'h')]
    return [card.Card(x[0], x[1]) for x in straight]


def straight_low():
    straight = [('2', 's'), ('3', 'h'), ('A', 's'), ('4', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in straight]


def set_high():
    trips = [('A', 's'), ('K', 'h'), ('A', 'h'), ('A', 'd'), ('Q', 'c')]
    return [card.Card(x[0], x[1]) for x in trips]


def set_low():
    trips = [('2', 's'), ('2', 'h'), ('2', 'h'), ('3', 'd'), ('4', 'c')]
    return [card.Card(x[0], x[1]) for x in trips]


def twopair_high():
    twopair = [('A', 's'), ('A', 'h'), ('K', 's'), ('K', 'd'), ('Q', 'c')]
    return [card.Card(x[0], x[1]) for x in twopair]


def twopair_low():
    twopair = [('2', 's'), ('2', 'h'), ('3', 's'), ('3', 'd'), ('4', 'c')]
    return [card.Card(x[0], x[1]) for x in twopair]


def pair_high():
    pair = [('K', 's'), ('Q', 'h'), ('A', 's'), ('A', 'd'), ('J', 'c')]
    return [card.Card(x[0], x[1]) for x in pair]


def pair_low():
    pair = [('2', 's'), ('3', 'h'), ('2', 'c'), ('4', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in pair]


def OESFD():
    pair = [('J', 's'), ('T', 's'), ('8', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def GSSFD():
    pair = [('J', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def flushdrawA():
    pair = [('A', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def flushdrawB():
    pair = [('3', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def OESD():
    pair = [('J', 'h'), ('T', 's'), ('8', 'c'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def GSSD():
    pair = [('J', 'h'), ('T', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
    return [card.Card(x[0], x[1]) for x in pair]


def wheeldraw():
    pair = [('3', 'h'), ('4', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
    return [card.Card(x[0], x[1]) for x in pair]
