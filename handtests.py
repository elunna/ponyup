#!/usr/bin/env python3

from __future__ import print_function
import deck
import card
import hand
import evaluator as ev


def dealhand(quantity):
    # Deal a regular 5 card hand from a new deck
    d = deck.Deck()
    d.shuffle()
    #  dealtcards = [d.deal() for i in range(quantity)]
    #  newhand = hand.Hand(dealtcards)
    #  return newhand
    return [d.deal() for i in range(quantity)]


def deal_duplicates():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('3', 'h'))
    h.append(card.Card('A', 's'))
    h.append(card.Card('4', 'd'))
    h.append(card.Card('5', 'c'))
    return h


def deal_royalflush():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('K', 's'))
    h.append(card.Card('J', 's'))
    h.append(card.Card('T', 's'))
    h.append(card.Card('Q', 's'))
    return h


def deal_straightflush_A():
    h = []
    h.append(card.Card('9', 's'))
    h.append(card.Card('K', 's'))
    h.append(card.Card('Q', 's'))
    h.append(card.Card('J', 's'))
    h.append(card.Card('T', 's'))
    return h


def deal_straightflush_B():
    h = []
    h.append(card.Card('2', 's'))
    h.append(card.Card('A', 's'))
    h.append(card.Card('3', 's'))
    h.append(card.Card('4', 's'))
    h.append(card.Card('5', 's'))
    return h


def deal_4ofakind_A():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('A', 'd'))
    h.append(card.Card('A', 'h'))
    h.append(card.Card('A', 'c'))
    h.append(card.Card('8', 'c'))
    return h


def deal_4ofakind_B():
    h = []
    h.append(card.Card('8', 's'))
    h.append(card.Card('8', 'd'))
    h.append(card.Card('8', 'h'))
    h.append(card.Card('8', 'c'))
    h.append(card.Card('A', 'c'))
    return h


def deal_fullhouse_A():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('A', 'd'))
    h.append(card.Card('A', 'h'))
    h.append(card.Card('K', 'd'))
    h.append(card.Card('K', 'c'))
    return h


def deal_fullhouse_B():
    h = []
    h.append(card.Card('K', 's'))
    h.append(card.Card('K', 'd'))
    h.append(card.Card('K', 'h'))
    h.append(card.Card('A', 'd'))
    h.append(card.Card('A', 'c'))
    return h


def deal_flush():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('3', 's'))
    h.append(card.Card('5', 's'))
    h.append(card.Card('9', 's'))
    h.append(card.Card('7', 's'))
    return h


def deal_high_straight():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('T', 'c'))
    h.append(card.Card('K', 's'))
    h.append(card.Card('J', 'd'))
    h.append(card.Card('Q', 'h'))
    return h


def deal_mid_straight():
    h = []
    h.append(card.Card('7', 's'))
    h.append(card.Card('8', 'c'))
    h.append(card.Card('9', 's'))
    h.append(card.Card('T', 'd'))
    h.append(card.Card('J', 'h'))
    return h


def deal_low_straight():
    h = []
    h.append(card.Card('2', 's'))
    h.append(card.Card('3', 'h'))
    h.append(card.Card('A', 's'))
    h.append(card.Card('4', 'd'))
    h.append(card.Card('5', 'c'))
    return h


def deal_3ofakind_A():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('K', 'h'))
    h.append(card.Card('A', 'h'))
    h.append(card.Card('A', 'd'))
    h.append(card.Card('Q', 'c'))
    return h


def deal_3ofakind_B():
    h = []
    h.append(card.Card('K', 's'))
    h.append(card.Card('Q', 'h'))
    h.append(card.Card('K', 'h'))
    h.append(card.Card('K', 'd'))
    h.append(card.Card('A', 'c'))
    return h


def deal_twopair_A():
    h = []
    h.append(card.Card('K', 's'))
    h.append(card.Card('8', 'h'))
    h.append(card.Card('A', 's'))
    h.append(card.Card('A', 'd'))
    h.append(card.Card('K', 'c'))
    return h


def deal_twopair_B():
    h = []
    h.append(card.Card('K', 's'))
    h.append(card.Card('A', 'h'))
    h.append(card.Card('8', 's'))
    h.append(card.Card('8', 'd'))
    h.append(card.Card('K', 'c'))
    return h


def deal_pair_A():
    h = []
    h.append(card.Card('2', 's'))
    h.append(card.Card('3', 'h'))
    h.append(card.Card('A', 's'))
    h.append(card.Card('A', 'd'))
    h.append(card.Card('5', 'c'))
    return h


def deal_pair_B():
    h = []
    h.append(card.Card('A', 's'))
    h.append(card.Card('3', 'h'))
    h.append(card.Card('2', 's'))
    h.append(card.Card('2', 'd'))
    h.append(card.Card('5', 'c'))
    return h


def test_hand(cards):
    h = deck.Deck(cards)
    #  hand.cards = hand.sort()
    #  hand.sort()
    print(h)
    if not ev.is_validhand(h):
        return
    value = ev.get_value(h.cards)
    print('Hand Value: {}'.format(value))
    print('Hand Type: {}'.format(ev.get_type(value)))
    print('')

if __name__ == "__main__":
    # Test the deck and cards

    # Random cards
    test_hand(dealhand(4))
    test_hand(dealhand(5))
    test_hand(dealhand(6))

    print('Test hand with 2 As\'s')
    test_hand(deal_duplicates())
    print('')
    print('')

    print('Royal Flush: ', end='')
    test_hand(deal_royalflush())

    print('Straight Flush A:', end='')
    test_hand(deal_straightflush_A())

    print('Straight Flush B:', end='')
    test_hand(deal_straightflush_B())

    print('Quads A: ', end='')
    test_hand(deal_4ofakind_A())

    print('Quads B: ', end='')
    test_hand(deal_4ofakind_B())

    print('Full House A: ', end='')
    test_hand(deal_fullhouse_A())

    print('Full House B: ', end='')
    test_hand(deal_fullhouse_B())

    print('Flush: ', end='')
    test_hand(deal_flush())

    print('High straight: ', end='')
    test_hand(deal_high_straight())

    print('Middle straight: ', end='')
    test_hand(deal_mid_straight())

    print('Low straight: ', end='')
    test_hand(deal_low_straight())

    print('Set A: ', end='')
    test_hand(deal_3ofakind_A())

    print('Set B: ', end='')
    test_hand(deal_3ofakind_B())

    print('Two Pair A: ', end='')
    test_hand(deal_twopair_A())

    print('Two Pair B: ', end='')
    test_hand(deal_twopair_B())

    print('Pair A: ', end='')
    test_hand(deal_pair_A())

    print('Pair B: ', end='')
    test_hand(deal_pair_B())

    print('#'*80)
    print('')
    print('Hand generation tests')

    hands = []
    hands.append(hand.Hand(deal_royalflush()))
    hands.append(hand.Hand(deal_straightflush_A()))
    hands.append(hand.Hand(deal_4ofakind_A()))
    hands.append(hand.Hand(deal_fullhouse_A()))
    hands.append(hand.Hand(deal_flush()))
    hands.append(hand.Hand(deal_high_straight()))
    hands.append(hand.Hand(deal_mid_straight()))
    hands.append(hand.Hand(deal_low_straight()))
    hands.append(hand.Hand(deal_3ofakind_A()))
    hands.append(hand.Hand(deal_twopair_A()))
    hands.append(hand.Hand(deal_pair_A()))
    hands.append(hand.Hand(deal_pair_B()))

    #  for h in hands:
        #  print('')
        #  print(h)
        #  print('value: {}'.format(h.value))
        #  print('type: {}'.format(h.handrank))

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

    print('#'*80)
    print('')
    print('Test the best hand finder')

    for i in range(10):
        group = dealhand(7)
        ev.print_cardlist(group)
        besthand = ev.find_best_hand(group)
        print('Best hand in the group: ', end='')
        print(besthand)
        print('')
