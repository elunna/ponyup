#!/usr/bin/env python3

from __future__ import print_function
import colors
import combos
import blinds
import player
import os
import sessions
import sys
import table
import testtools

GAME = 'FIVE CARD DRAW'
TABLE = 2
BLINDS = blinds.Blinds()
NAME = 'Aorist'
OPPONENT = 'FISH'

# Define menu opions
options = {}
options['c'] = ('(C)ombination counts', 'view_combos()')
options['p'] = ('(P)lay Poker!', 'play_poker()')
options['n'] = ('(N)ame change', 'pick_name()')
options['g'] = ('(G)ame change', 'pick_game()')
options['s'] = ('(S)takes', 'pick_limit(BLINDS)')
options['t'] = ('(T)able size', 'pick_table()')
options['m'] = ('(M)enu', 'menu()')
options['o'] = ('(O)pponent type', 'pick_opp()')
options['q'] = ('(Q)uit', 'exitgracefully()')


def print_logo():
    txt = ''
    with open('logo.txt') as f:
        #  print(f.read())
        for c in f.read():
            if c == '$':
                txt += colors.color(c, 'yellow')
            else:
                txt += colors.color(c, 'green')
    txt += '\n'
    print(txt)
    print('~'*70)
    print('~'*70)


def menu():
    os.system('clear')
    print_logo()
    print('')
    print('-=- Settings -=-'.center(70))
    print('{:>15}: {}'.format('Playername', NAME))
    print('{:>15}: {}'.format('Game', GAME))
    print('{:>15}: {}'.format('Stakes',  BLINDS))
    print('{:>15}: {}'.format('Seats', TABLE))
    print('{:>15}: {}'.format('Opponent Type', OPPONENT))
    print('')

    #  options = sorted(options.keys())
    for o in sorted(options.keys()):
        print(options[o][0])


def view_combos():
    for i in range(1, 8):
        print("There are {} combos of {} cards in a standard 52 card deck.".format(
            combos.n_choose_k(52, i), i))


def pick_limit(_blinds):
    print('Please enter what limit you want to play:')
    _blinds.levels()

    while True:
        choice = int(input(':> '))
        if choice in _blinds.blind_dict.keys():
            _blinds.set_level(choice)
            print('You selected {}'.format(_blinds))
            break
        else:
            print('Selection not available, try again.')


def pick_opp():
    print('What type of opponent do you want to play:')

    for t in player.TYPES:
        print(t)

    while True:
        choice = input(':> ')
        if choice.upper() in player.TYPES:
            global OPPONENT
            OPPONENT = choice.upper()
            print('You selected {}'.format(OPPONENT))
            break
        else:
            print('Selection not available, try again.')


def pick_table():
    print('What size table do you want to play?')
    for l in table.VALID_SIZES:
        print('{}, '.format(l), end='')

    while True:
        choice = int(input(':> '))
        if choice in table.VALID_SIZES:
            print('You selected {}'.format(choice))
            global TABLE
            TABLE = int(choice)
            break
        else:
            print('Selection not available, try again.')


def pick_name():
    print('Please enter your username.')
    while True:
        name = input(':> ')
        if len(name) > 15:
            print('Name is too long! Must be less than 15 characters.')
        else:
            break
    global NAME
    NAME = name


def pick_game():
    print('What game do you want to play?')
    gamelist = sorted(sessions.GAMES.keys())

    for i, k in enumerate(gamelist):
        print('{}: {}'.format(i + 1, k))

    while True:
        choice = int(input(':> '))
        if choice in list(range(1, len(gamelist) + 1)):
            global GAME
            GAME = gamelist[choice - 1]
            print('You selected {}'.format(GAME))
            break
        else:
            print('Selection not available, try again.')


def play_poker():
    print('Alright, let\'s play some poker!')

    print('Initializing new game...\n')

    t = testtools.HeroTable(TABLE, NAME, GAME, OPPONENT)

    if GAME == "FIVE CARD DRAW":
        g = sessions.Draw5Session(GAME, t, BLINDS)
        t.randomize_button()
    elif GAME == "FIVE CARD STUD":
        g = sessions.Stud5Session(GAME, t, BLINDS)

    playing = True

    while playing:
        os.system('clear')
        print(g)
        g.play()
        choice = input('keep playing? > ')
        if choice.lower() == 'n' or choice == 0:
            playing = False

    exit()


def exitgracefully():
    print('Bye!')
    sys.exit()


if __name__ == "__main__":
    BLINDS.set_level(10)

    while True:
        os.system('clear')
        print_logo()
        menu()
        choice = input('> ')
        choice = choice.lower()

        if choice in options:
            exec(options[choice][1])
            input('Press any key to continue...')
        else:
            print('Not a valid option!')
