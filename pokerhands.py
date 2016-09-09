#!/usr/bin/env python3
"""
This is a collection of functions that return lists of cards that compose all the regular poker
hands and also some variations on them. These are meant to be used for testing.
"""
from __future__ import print_function
import card


def to_card(string):
    if len(string) != 2:
        raise Exception('String must be exactly 2 characters to convert to a card!')
    return card.Card(string[0], string[1])


def convert_to_cards(strings):
    # Unhide for testing purposes
    cards = [to_card(x) for x in strings]
    for c in cards:
        c.hidden = False
    return cards


def make(hand_name, hidden=False):
    h = convert_to_cards(HANDS[hand_name])
    if not hidden:
        for c in h:
            c.hidden = False
    return h


# These are constants to help with computer AI
HI_KT = 1310000000
HI_AQ = 1412000000
PAIR_22 = 20000000000
PAIR_66 = 20600000000
PAIR_88 = 20800000000
PAIR_JJ = 21100000000
PAIR_KK = 21300000000
PAIR_AA = 21400000000
TWOPAIR_22 = 30000000000
TWOPAIR_88 = 30800000000
TWOPAIR_TT = 31000000000
TWOPAIR_JJ = 31100000000
TWOPAIR_KK = 31300000000
TRIPS = 40000000000
STRAIGHT = 40000000000
FLUSH = 50000000000

HANDS = {
    'dupes': ['As', '3h', 'As', '4d', '5c'],
    'royalflush': ['As', 'Ks', 'Js', 'Ts', 'Qs'],
    'straightflush_high': ['9s', 'Ks', 'Qs', 'Js', 'Ts'],
    'straightflush_low': ['2s', 'As', '3s', '4s', '5s'],
    'quads_high': ['As', 'Ad', 'Ah', 'Ac', 'Kc'],
    'quads_low': ['2s', '2d', '2h', '2c', '3c'],
    'fullhouse_high': ['As', 'Ad', 'Ah', 'Kd', 'Kc'],
    'fullhouse_low': ['2s', '2d', '2h', '3d', '3c'],
    'flush_high': ['As', 'Ks', 'Qs', 'Js', '9s'],
    'flush_low': ['2s', '3s', '4s', '5s', '7s'],
    'straight_high': ['As', 'Tc', 'Ks', 'Jd', 'Qh'],
    'straight_mid': ['8s', '7h', '9s', 'Td', 'Jh'],
    'straight_low': ['2s', '3h', 'As', '4d', '5c'],
    'trips_high': ['As', 'Kh', 'Ah', 'Ad', 'Qc'],
    'trips_low': ['2s', '2h', '2h', '3d', '4c'],
    'twopair_high': ['As', 'Ah', 'Ks', 'Kd', 'Qc'],
    'twopair_low': ['2s', '2h', '3s', '3d', '4c'],
    'pair_high': ['Ks', 'Qh', 'As', 'Ad', 'Jc'],
    'pair_low': ['2s', '3h', '2c', '4d', '5c'],
    'OESFD': ['Js', 'Ts', '8s', '2d', '9s'],
    'GSSFD': ['Js', 'Ts', '7s', '2d', '9s'],
    'flushdrawA': ['As', 'Ts', '7s', '2d', '9s'],
    'flushdrawB': ['3s', 'Ts', '7s', '2d', '9s'],
    'OESD': ['Jh', 'Ts', '8c', '2d', '9s'],
    'GSSD': ['Jh', 'Ts', 'As', '2d', 'Kh'],
    'wheeldraw': ['3h', '4s', 'As', '2d', 'Kh'],
    'BDFD1': ['2d', '4s', '5s', '7s', 'Kh'],
    'BDFD2': ['Ad', '4s', '5s', '7s', 'Kh'],
    'highcards': ['Ad', '4s', 'Qs', '7s', 'Kh'],
    'acehigh': ['Ad', '4s', '5s', '7s', '9h'],
    'BDSD1': ['2d', '7s', '8s', '9d', 'Kh'],
    'BDSD2': ['2d', '7s', '8s', 'Td', 'Kh'],
    'junk': ['2d', '3s', '6s', '8d', 'Th'],
    '2AA_v1': ['2s', 'As', 'Ah'],
    '2AA_v2': ['2c', 'Ad', 'Ac'],
    '2KK': ['2h', 'Ks', 'Kh'],
    '2QQ': ['2d', 'Qs', 'Qh'],
    '3AK_v1': ['3s', 'As', 'Ks'],
    '3AK_v2': ['3h', 'Ah', 'Kh'],
    '3AK_v3': ['3c', 'Ac', 'Kc'],
    'QKA_v1': ['Qs', 'Kh', 'As'],
    'QKA_v2': ['Qc', 'Ks', 'Ac'],
    'JTQ': ['Jh', 'Ts', 'Qh'],
    '234': ['3s', '4s', '5s'],
    '345': ['3d', '4d', '5d'],
    '245': ['2c', '4c', '5c'],
    '89J': ['8c', '9s', 'Js'],
    '567': ['5c', '6s', '7s'],
    'A': ['As'],
    'AKs': ['Ac', 'Kc'],
    'AKo': ['As', 'Kd'],
    'AA': ['Ac', 'Ah'],
    'KK_dupes': ['Ks', 'Ks'],
}

RANKEDHANDS = {
    0: make('royalflush'),
    1: make('straightflush_high'),
    2: make('fullhouse_high'),
    3: make('flush_high'),
    4: make('straight_high'),
    5: make('trips_high'),
    6: make('twopair_high'),
    7: make('pair_high'),
    8: make('pair_low'),
    9: make('acehigh'),
}
