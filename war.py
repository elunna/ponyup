#!/usr/bin/env python3

from __future__ import print_function
#  import gametools
import sys
import time
import random
import deck

# Rules:
# If a player runs out of cards they lose.
# If a player draws a last card for war that is an exception.

#  players = gametools.deal_players(2, 26)
players = [[], []]
d = deck.Deck()
while len(d) > 0:
    players[0].append(d.deal())
    players[1].append(d.deal())


def checkstatus():
    if len(players[0]) == 0 and len(players[1]) == 0:
        print('Tie!')
        sys.exit()
        #  return 0  # Tie
    elif len(players[0]) == 0:
        print('Player 2 wins!')
        sys.exit()
        #  return 2  # Player 2 wins
    elif len(players[1]) == 0:
        print('Player 1 wins!')
        sys.exit()
        #  return 1  # Player 1 wins
    else:
        return 0


def playround(warlevel):
    checkstatus()
    print('{}    vs    {}'.format(players[0][0], players[1][0]))

    if players[0][0].val() > players[1][0].val():
        print('Player 1 takes the round!')
        # Add the compared cards to player 1's stack
        players[0].append(players[0].pop(0))
        players[0].append(players[1].pop(0))
        return 1
    elif players[0][0].val() < players[1][0].val():
        # Add the compared cards to player 2's stack
        print('Player 2 takes the round!')
        players[1].append(players[0].pop(0))
        players[1].append(players[1].pop(0))
        return 2
    else:
        # Go into the 'war' mode.
        # Use a counter to count what level of war we're at
        warlevel += 1
        result = war(warlevel)
        return result


def war(warlevel):
    # Check player stacks first
    print('WAR!!! LEVEL {}'.format(warlevel))

    # Pause button
    #  input()

    spoils = []
    for i in range(4):
        checkstatus()
        spoils.append(players[0].pop(0))
        spoils.append(players[1].pop(0))

    list_cards(spoils)
    result = playround(warlevel)

    if result == 1:
        print('Player 1 wins the war #{}!'.format(warlevel))
        players[0].extend(spoils)
        return 1
    elif result == 2:
        print('Player 2 wins the war #{}!'.format(warlevel))
        players[1].extend(spoils)
        return 2


def gameloop():
    rounds = 0
    while True:

        # Optional sleep
        time.sleep(.05)

        random.shuffle(players[0])
        random.shuffle(players[1])

        rounds += 1
        print('\nRound {}....Player1 = {}    Player2 = {}'.format(
            rounds, len(players[0]), len(players[1])))

        #  Pause button
        #  input()

        playround(warlevel=0)


def list_cards(hand):
    for c in hand:
        print('{} '.format(str(c)), end='')
    print('')


if __name__ == '__main__':
    gameloop()
