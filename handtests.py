#!/usr/bin/env python3

from __future__ import print_function
import deck
import card
import hand
import evaluator as ev
import fivecarddraw


def dealhand(quantity):
    # Deal a regular 5 card hand from a new deck
    d = deck.Deck()
    d.shuffle()
    #  dealtcards = [d.deal() for i in range(quantity)]
    #  newhand = hand.Hand(dealtcards)
    #  return newhand
    return [d.deal() for i in range(quantity)]


def deal_duplicates():
    dupes = [('A', 's'), ('3', 'h'), ('A', 's'), ('4', 'd'), ('5', 'c')]
    return [card.Card(x[0], x[1]) for x in dupes]


##########################################################################
# Made Hands

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

##########################################################################
# Draws


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


def test_hand(cards):
    if not ev.is_validhand(cards):
        return

    h = hand.Hand(cards)
    #  value = ev.get_value(cards)
    #  _type = ev.get_type(value)

    print('{:15}{:15}{:15}'.format(h.handrank, str(h), h.value))
    k, d = fivecarddraw.auto_discard(h)
    print('keep:{} discard:{}'.format(k, d))
    print('')


if __name__ == "__main__":
    # Test the deck and cards

    print('Testing boundary cases:\n')
    # Random cards
    print('')
    random_4cards = dealhand(4)
    print('Attempting to deal 4 cards')
    print(random_4cards)
    test_hand(random_4cards)

    print('')
    random_5cards = dealhand(5)
    print('Attempting to deal 5 cards')
    print(random_5cards)
    test_hand(random_4cards)

    print('')
    random_6cards = dealhand(6)
    print('Attempting to deal 6 cards')
    print(random_6cards)
    test_hand(random_6cards)

    print('')
    print('Test hand with 2 As\'s')
    test_hand(deal_duplicates())
    print('')

    print('#'*80)
    print('')
    print('Hand generation tests')

    hands = []
    hands.append(deal_royalflush())
    hands.append(deal_straightflush_A())
    hands.append(deal_lowstraightflush())
    hands.append(deal_4ofakind_A())
    hands.append(deal_4ofakind_B())
    hands.append(deal_fullhouse_A())
    hands.append(deal_fullhouse_B())
    hands.append(deal_flush())
    hands.append(deal_high_straight())
    hands.append(deal_mid_straight())
    hands.append(deal_low_straight())
    hands.append(deal_3ofakind_A())
    hands.append(deal_3ofakind_B())
    hands.append(deal_twopair_A())
    hands.append(deal_twopair_B())
    hands.append(deal_pair_A())
    hands.append(deal_pair_B())
    # Draws
    hands.append(deal_OESFD())
    hands.append(deal_GSSFD())
    hands.append(deal_flushdraw_hi())
    hands.append(deal_flushdraw())
    hands.append(deal_OESD())
    hands.append(deal_GSSD())
    hands.append(deal_wheeldraw())

    for h in hands:
        test_hand(h)

    """
    print('#'*80)
    print('')
    print('Hand comparison tests')

    handA = hand.Hand(dealhand(5))

    for h in hands:
        print('{}(A) vs {}(B)'.format(handA, h))
        if handA.value > h.value:
            print('Hand A wins!')
        elif handA.value < h.value:
            print('Hand B wins!')
        else:
            print('Tie!')
    """

    print('#'*80)
    print('')
    print('Test the best hand finder:')

    for i in range(10):
        group = dealhand(7)
        #  ev.print_cardlist(group)
        print(group)
        besthand = ev.find_best_hand(group)
        print('\t\t\t\tBest hand: ', end='')
        print(besthand)
        print('')
