#!/usr/bin/env python3
"""
This is a collection of functions that return lists of cards that compose all the regular poker
hands and also some variations on them. These are meant to be used for testing.
"""
from __future__ import print_function
import evaluator as ev

# These are constants to help with computer AI
HI_AQ = 1412000000
PAIR_22 = 20000000000
PAIR_66 = 20600000000
PAIR_JJ = 21100000000
PAIR_AA = 21400000000
TWOPAIR_22 = 30000000000
TWOPAIR_JJ = 31100000000
TRIPS = 40000000000


def dupes():
    return ev.convert_to_cards(['As', '3h', 'As', '4d', '5c'])


def royalflush():
    return ev.convert_to_cards(['As', 'Ks', 'Js', 'Ts', 'Qs'])


def straightflush_high():
    return ev.convert_to_cards(['9s', 'Ks', 'Qs', 'Js', 'Ts'])


def straightflush_low():
    return ev.convert_to_cards(['2s', 'As', '3s', '4s', '5s'])


def quads_high():
    return ev.convert_to_cards(['As', 'Ad', 'Ah', 'Ac', 'Kc'])


def quads_low():
    return ev.convert_to_cards(['2s', '2d', '2h', '2c', '3c'])


def fullhouse_high():
    return ev.convert_to_cards(['As', 'Ad', 'Ah', 'Kd', 'Kc'])


def fullhouse_low():
    return ev.convert_to_cards(['2s', '2d', '2h', '3d', '3c'])


def flush_high():
    return ev.convert_to_cards(['As', 'Ks', 'Qs', 'Js', '9s'])


def flush_low():
    return ev.convert_to_cards(['2s', '3s', '4s', '5s', '7s'])


def straight_high():
    return ev.convert_to_cards(['As', 'Tc', 'Ks', 'Jd', 'Qh'])


def straight_mid():
    return ev.convert_to_cards(['8s', '7h', '9s', 'Td', 'Jh'])


def straight_low():
    return ev.convert_to_cards(['2s', '3h', 'As', '4d', '5c'])


def trips_high():
    return ev.convert_to_cards(['As', 'Kh', 'Ah', 'Ad', 'Qc'])


def trips_low():
    return ev.convert_to_cards(['2s', '2h', '2h', '3d', '4c'])


def twopair_high():
    return ev.convert_to_cards(['As', 'Ah', 'Ks', 'Kd', 'Qc'])


def twopair_low():
    return ev.convert_to_cards(['2s', '2h', '3s', '3d', '4c'])


def pair_high():
    return ev.convert_to_cards(['Ks', 'Qh', 'As', 'Ad', 'Jc'])


def pair_low():
    return ev.convert_to_cards(['2s', '3h', '2c', '4d', '5c'])


# Open Ended Straight Flush Draw
def OESFD():
    return ev.convert_to_cards(['Js', 'Ts', '8s', '2d', '9s'])


# Gut-Shot Straight Flush Draw
def GSSFD():
    return ev.convert_to_cards(['Js', 'Ts', '7s', '2d', '9s'])


def flushdrawA():
    return ev.convert_to_cards(['As', 'Ts', '7s', '2d', '9s'])


def flushdrawB():
    return ev.convert_to_cards(['3s', 'Ts', '7s', '2d', '9s'])


# Open Ended Straight Draw
def OESD():
    return ev.convert_to_cards(['Jh', 'Ts', '8c', '2d', '9s'])


# Gut-shot Straight Draw
def GSSD():
    return ev.convert_to_cards(['Jh', 'Ts', 'As', '2d', 'Kh'])


def wheeldraw():
    return ev.convert_to_cards(['3h', '4s', 'As', '2d', 'Kh'])


# Backdoor Flush Draw
def BDFD1():
    return ev.convert_to_cards(['2d', '4s', '5s', '7s', 'Kh'])


# Backdoor Flush Draw
def BDFD2():
    return ev.convert_to_cards(['Ad', '4s', '5s', '7s', 'Kh'])


def highcards1():
    return ev.convert_to_cards(['Ad', '4s', 'Qs', '7s', 'Kh'])


def acehigh():
    return ev.convert_to_cards(['Ad', '4s', '5s', '7s', '9h'])


# Backdoor Straight Draw
def BDSD1():
    return ev.convert_to_cards(['2d', '7s', '8s', '9d', 'Kh'])


# Backdoor Straight Draw
def BDSD2():
    return ev.convert_to_cards(['2d', '7s', '8s', 'Td', 'Kh'])


def junk():
    return ev.convert_to_cards(['2d', '3s', '6s', '8d', 'Th'])
