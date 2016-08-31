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


def convert_to_cards(cardlist):
    return [card.Card(x[0], x[1]) for x in cardlist]


def deal_duplicates():
    return convert_to_cards([('A', 's'), ('3', 'h'), ('A', 's'), ('4', 'd'), ('5', 'c')])


def royalflush():
    return convert_to_cards([('A', 's'), ('K', 's'), ('J', 's'), ('T', 's'), ('Q', 's')])


def straightflush_high():
    return convert_to_cards([('9', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('T', 's')])


def straightflush_low():
    return convert_to_cards([('2', 's'), ('A', 's'), ('3', 's'), ('4', 's'), ('5', 's')])


def quads_high():
    return convert_to_cards([('A', 's'), ('A', 'd'), ('A', 'h'), ('A', 'c'), ('K', 'c')])


def quads_low():
    return convert_to_cards([('2', 's'), ('2', 'd'), ('2', 'h'), ('2', 'c'), ('3', 'c')])


def boat_high():
    return convert_to_cards([('A', 's'), ('A', 'd'), ('A', 'h'), ('K', 'd'), ('K', 'c')])


def boat_low():
    return convert_to_cards([('2', 's'), ('2', 'd'), ('2', 'h'), ('3', 'd'), ('3', 'c')])


def flush_high():
    return convert_to_cards([('A', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('9', 's')])


def flush_low():
    return convert_to_cards([('2', 's'), ('3', 's'), ('4', 's'), ('5', 's'), ('7', 's')])


def straight_high():
    return convert_to_cards([('A', 's'), ('T', 'c'), ('K', 's'), ('J', 'd'), ('Q', 'h')])


def straight_mid():
    return convert_to_cards([('8', 's'), ('7', 'h'), ('9', 's'), ('T', 'd'), ('J', 'h')])


def straight_low():
    return convert_to_cards([('2', 's'), ('3', 'h'), ('A', 's'), ('4', 'd'), ('5', 'c')])


def set_high():
    return convert_to_cards([('A', 's'), ('K', 'h'), ('A', 'h'), ('A', 'd'), ('Q', 'c')])


def set_low():
    return convert_to_cards([('2', 's'), ('2', 'h'), ('2', 'h'), ('3', 'd'), ('4', 'c')])


def twopair_high():
    return convert_to_cards([('A', 's'), ('A', 'h'), ('K', 's'), ('K', 'd'), ('Q', 'c')])


def twopair_low():
    return convert_to_cards([('2', 's'), ('2', 'h'), ('3', 's'), ('3', 'd'), ('4', 'c')])


def pair_high():
    return convert_to_cards([('K', 's'), ('Q', 'h'), ('A', 's'), ('A', 'd'), ('J', 'c')])


def pair_low():
    return convert_to_cards([('2', 's'), ('3', 'h'), ('2', 'c'), ('4', 'd'), ('5', 'c')])


def OESFD():
    return convert_to_cards([('J', 's'), ('T', 's'), ('8', 's'), ('2', 'd'), ('9', 's')])


def GSSFD():
    return convert_to_cards([('J', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')])


def flushdrawA():
    return convert_to_cards([('A', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')])


def flushdrawB():
    return convert_to_cards([('3', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')])


def OESD():
    return convert_to_cards([('J', 'h'), ('T', 's'), ('8', 'c'), ('2', 'd'), ('9', 's')])


def GSSD():
    return convert_to_cards([('J', 'h'), ('T', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')])


def wheeldraw():
    return convert_to_cards([('3', 'h'), ('4', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')])


def BDFD1():
    return convert_to_cards([('2', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('K', 'h')])


def BDFD2():
    return convert_to_cards([('A', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('K', 'h')])


def highcards1():
    return convert_to_cards([('A', 'd'), ('4', 's'), ('Q', 's'), ('7', 's'), ('K', 'h')])


def acehigh():
    return convert_to_cards([('A', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('9', 'h')])


def BDSD1():
    return convert_to_cards([('2', 'd'), ('7', 's'), ('8', 's'), ('9', 'd'), ('K', 'h')])


def BDSD2():
    return convert_to_cards([('2', 'd'), ('7', 's'), ('8', 's'), ('T', 'd'), ('K', 'h')])


def junk():
    return convert_to_cards([('2', 'd'), ('3', 's'), ('6', 's'), ('8', 'd'), ('T', 'h')])
