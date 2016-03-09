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


def deal_royalflush():
    rf = [('A', 's'), ('K', 's'), ('J', 's'), ('T', 's'), ('Q', 's')]
    return [card.Card(x[0], x[1]) for x in rf]


def deal_straightflush_A():
    sf = [('9', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('T', 's')]
    return [card.Card(x[0], x[1]) for x in sf]


def deal_lowstraightflush():
    sf = [('2', 's'), ('A', 's'), ('3', 's'), ('4', 's'), ('5', 's')]
    return [card.Card(x[0], x[1]) for x in sf]


def deal_4ofakind_A():
    quads = [('A', 's'), ('A', 'd'), ('A', 'h'), ('A', 'c'), ('8', 'c')]
    return [card.Card(x[0], x[1]) for x in quads]


def deal_4ofakind_B():
    quads = [('8', 's'), ('8', 'd'), ('8', 'h'), ('8', 'c'), ('A', 'c')]
    return [card.Card(x[0], x[1]) for x in quads]


def deal_fullhouse_A():
    fullhouse = [('A', 's'), ('A', 'd'), ('A', 'h'), ('K', 'd'), ('K', 'c')]
    return [card.Card(x[0], x[1]) for x in fullhouse]


def deal_fullhouse_B():
    fullhouse = [('K', 's'), ('K', 'd'), ('K', 'h'), ('A', 'd'), ('A', 'c')]
    return [card.Card(x[0], x[1]) for x in fullhouse]


def deal_flush():
    flush = [('A', 's'), ('3', 's'), ('5', 's'), ('9', 's'), ('7', 's')]
    return [card.Card(x[0], x[1]) for x in flush]


def deal_high_straight():
    straight = [('A', 's'), ('T', 'c'), ('K', 's'), ('J', 'd'), ('Q', 'h')]
    return [card.Card(x[0], x[1]) for x in straight]


def deal_mid_straight():
    straight = [('8', 's'), ('7', 'h'), ('9', 's'), ('T', 'd'), ('J', 'h')]
    return [card.Card(x[0], x[1]) for x in straight]


def deal_low_straight():
    straight = [('2', 's'), ('3', 'h'), ('A', 's'), ('4', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in straight]


def deal_3ofakind_A():
    trips = [('A', 's'), ('K', 'h'), ('A', 'h'), ('A', 'd'), ('Q', 'c')]
    return [card.Card(x[0], x[1]) for x in trips]


def deal_3ofakind_B():
    trips = [('K', 's'), ('Q', 'h'), ('K', 'h'), ('K', 'd'), ('A', 'c')]
    return [card.Card(x[0], x[1]) for x in trips]


def deal_twopair_A():
    twopair = [('K', 's'), ('8', 'h'), ('A', 's'), ('A', 'd'), ('K', 'c')]
    return [card.Card(x[0], x[1]) for x in twopair]


def deal_twopair_B():
    twopair = [('K', 's'), ('A', 'h'), ('8', 's'), ('8', 'd'), ('K', 'c')]
    return [card.Card(x[0], x[1]) for x in twopair]


def deal_pair_A():
    pair = [('2', 's'), ('3', 'h'), ('A', 's'), ('A', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_pair_B():
    pair = [('A', 's'), ('3', 'h'), ('2', 's'), ('2', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_OESFD():
    pair = [('J', 's'), ('T', 's'), ('8', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_GSSFD():
    pair = [('J', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_flushdraw_hi():
    pair = [('A', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_flushdraw():
    pair = [('3', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_OESD():
    pair = [('J', 'h'), ('T', 's'), ('8', 'c'), ('2', 'd'), ('9', 's')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_GSSD():
    pair = [('J', 'h'), ('T', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
    return [card.Card(x[0], x[1]) for x in pair]


def deal_wheeldraw():
    pair = [('3', 'h'), ('4', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
    return [card.Card(x[0], x[1]) for x in pair]
