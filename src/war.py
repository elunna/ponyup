#!/usr/bin/env python3
"""
Simulates a standard game of War. Players each start with a 27 card stack, 2 jokers included.
Each player plays a card and tries to beat the rank of the other. The winner keeps the 2 cards.
If two cards of the same rank are played, a "War" round is played where 3 additional cards are
set down by each player, and a final determining card is played for all 10 cards. If these
cards tie for rank, we proceed to an additional level of War and so on. Play ends when one
player has won all the cards.

Other clarification:
* If a player runs out of cards they lose.
* If a player draws a last card for war that is an exception.
"""


from __future__ import print_function
from ponyup import deck
import random
import sys
import time

TIE = 0
PLAYER1WIN = 1
PLAYER2WIN = 2
PLAYING = -1
SHUFFLES = 10
WIDTH = 70
SOUND = True

WAR = {
    1: 'WAR',
    2: 'DOUBLE WAR',
    3: 'TRIPLE WAR',
    4: 'QUADRUPLE WAR',
    5: 'QUINTUPLE WAR',
    6: 'SEXTUPLE WAR'
}


class War(object):
    """ Manages a game of War. """
    def __init__(self):
        self.rounds = 0
        self.warlevel = 0
        self.spoils = []
        self.players = {1: [], 2: []}
        self.shuffle_between_rounds = True
        self.warcount = {}
        self.delay = .02
        self.deal_cards()

    def __str__(self):
        return 'Round {}: Player 1 = {} Player2 = {}'.format(
            self.rounds, len(self.players[1]), len(self.players[2]))

    def deal_cards(self):
        """ Divies up the deck evenly """
        _deck = deck.Deck2Joker()
        _deck.unhide()

        for _ in range(SHUFFLES):
            _deck.shuffle()

        while len(_deck) > 0:
            self.players[1].append(_deck.deal())
            self.players[2].append(_deck.deal())

    def show_stacks(self):
        """ Display how many cards are in each players deck. """
        left = 'P1: '
        right = ' :P2'
        stack1 = '#' * len(self.players[1])
        stack2 = '#' * len(self.players[2])
        spacing = (WIDTH - 54 - (len(left) + len(right))) * ' '
        print('{}{}{}{}{}'.format(left, stack1, spacing, stack2, right))

    def shuffle(self):
        """ Shuffle each players stack of cards. """
        random.shuffle(self.players[1])
        random.shuffle(self.players[2])

    def gamestate(self):
        """ Returns a number that indicates the state of the game:
            -1 = Still playing
            0 = Tie
            1 = Player 1 won
            2 = Player 2 won
        """
        if len(self.players[1]) == 0 and len(self.players[2]) == 0:
            return TIE
        elif len(self.players[1]) == 0:
            return PLAYER2WIN
        elif len(self.players[2]) == 0:
            return PLAYER1WIN
        else:
            return PLAYING

    def get_winner(self):
        """
        Determines the winner by looking at the top card of each players pile.
            Returns 1 if player 1 has a higher card.
            Returns 2 if player 2 has a higher card.
            Returns 0 if they tie.
        """
        if self.players[1][0] > self.players[2][0]:
            return PLAYER1WIN
        elif self.players[2][0] > self.players[1][0]:
            return PLAYER2WIN
        else:
            return TIE

    def show_topcards(self):
        """ Returns a string showing the top card of each players pile vs the other. """

        card1 = str(self.players[1][0])
        card2 = str(self.players[2][0])
        _str = card1 + card2.rjust(WIDTH - 10)
        print(_str.center(WIDTH))

    def award_cards(self, player):
        """ Add the compared cards to specified player's stack """

        self.players[player].extend(self.spoils)
        self.spoils = []

    def playround(self):
        """ Play through one round."""
        # Delay
        time.sleep(self.delay)

        if self.gamestate() >= 0:
            self.gameover()

        # A War doesn't count as a new round.
        if self.warlevel == 0:
            self.rounds += 1

        if self.warlevel == 0:
            print('Round {}'.format(self.rounds).center(WIDTH))

        self.show_topcards()
        winner = self.get_winner()
        self.get_spoils(1)

        if winner > 0:
            self.award_cards(winner)
            return winner

        else:
            # War: Use a counter to count what level of war we're at
            self.warlevel += 1

            if self.warlevel not in self.warcount:
                self.warcount[self.warlevel] = 1
            else:
                self.warcount[self.warlevel] += 1

            warwinner = self.war()
            return warwinner

    def war(self):
        """ Executes a round of War when each player ties for rank. If a player
            doesn't have 4 cards for a standard war, we'll take just enough so
            they can play war and the determining 2 cards.
        """

        text = '{}'.format(get_wartext(self.warlevel))
        print(text.center(WIDTH))

        self.get_spoils(3)
        print(card_text(self.spoils).center(WIDTH))

        # Play a sound
        time.sleep(2)  # Sleep x seconds

        winner = self.playround()

        self.award_cards(winner)
        print('Player {} wins!'.format(winner).center(WIDTH))

        # Play a sound
        time.sleep(1)  # Sleep x seconds

        self.warlevel = 0
        return winner

    def get_spoils(self, qty):
        """ Collects the cards that go into the War pile. Cannot add the last
            card in a players stack.
        """
        # Adjust for a very shallow stack.
        smallerstack = min([len(i) for i in self.players.values()])
        if smallerstack < qty:
            qty = smallerstack - 1

        for _ in range(qty):
            if self.gamestate() >= 0:
                self.gameover()
            self.add_spoils()

    def add_spoils(self):
        """ Takes a card off the top of each players stack and adds it to the
            community spoils stack.
        """
        self.spoils.append(self.players[1].pop(0))
        self.spoils.append(self.players[2].pop(0))

    def gameover(self):
        """ The game has ended, prints out the appropriate ending text, and exits. """
        state = self.gamestate()
        print('Game over! ', end='')
        if state == 0:
            print('TIE GAME!')
        elif state == 1:
            print('Player 1 wins!')
        if state == 2:
            print('Player 2 wins!')

        self.summary()
        sys.exit()

    def summary(self):
        """ Show game stats from a finished game. """
        print('\n\n')
        print('~~/) Game summary ~~(\\')
        print('Rounds: {}'.format(self.rounds))
        print('War counts:')
        for k, v in self.warcount.items():
            print('\t{}: {}x'.format(get_wartext(k), v))


def card_text(cardlist):
    """ Returns a string representing the cards in the list. """
    return '[' + ' '.join(str(c) for c in cardlist) + ']'


def get_wartext(level):
    """ Display the correct text for when a round hits any level of War.  """
    exclaimations = 2 * (level + 1)
    return '{}{}'.format(WAR[level], '!' * exclaimations)
