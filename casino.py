#!/usr/bin/env python3

from __future__ import print_function
import blinds
import table
import os
import sys
import game
import combos

GAME = 'FIVE CARD DRAW'
TABLE = 6
STAKES = blinds.limit['50/100']
NAME = 'LUNNA'

# Define menu opions
options = {}
options['c'] = ('View card (C)ombination counts', 'view_combos()')
options['f'] = ('Play (F)ive card Draw', 'play_poker()')
options['u'] = ('Run (U)nit Tests', '')
options['n'] = ('Change (N)ame', 'pick_name()')
options['s'] = ('Change (S)takes', 'pick_limit()')
options['t'] = ('Change (T)able size', 'pick_name()')
options['m'] = ('(M)enu', 'menu()')
options['e'] = ('(E)xit', 'exitgracefully()')


def print_logo():
    with open('logo.txt') as f:
        print(f.read())
    print('='*80)


def exitgracefully():
    print('Bye!')
    sys.exit()


def menu():
    os.system('clear')
    print_logo()
    print('')
    print('Settings:')
    print('Playername: {}'.format(NAME))
    print('Game:       {}'.format(GAME))
    print('Table Size: {}'.format(TABLE))
    print('Stakes:     ${}/{}'.format(STAKES[0], STAKES[0]))
    print('')
    for o in options:
        print(options[o][0])


def view_combos():
    combos.view_combo_counts()


def pick_limit():
    print('Please enter what limit you want to play:(default 2/4)')

    struct_list = sorted(blinds.limit.keys())
    for l in struct_list:
        print('{}, '.format(l), end='')

    choice = input(':> ')
    if choice in blinds.limit:
        print('You selected {}'.format(choice))
        STAKES = blinds.limit[choice]
    else:
        print('Selection not available, going with default blinds: 2/4')
        global STAKES
        STAKES = blinds.limit['2/4']


def pick_table():
    print('What size table do you want to play? (default is 2 seats)')

    for l in table.VALID_SIZES:
        print('{}, '.format(l), end='')

    choice = input(':> ')
    if int(choice) in table.VALID_SIZES:
        print('You selected {}'.format(choice))
        TABLE = choice
    else:
        print('Selection not available, going with default: 6 seats')
        global TABLE
        TABLE = 6


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


def play_poker():
    print('Alright, let\'s play some poker!')

    print('Initializing new game...\n')
    g = game.Game('FIVE CARD DRAW', STAKES, TABLE, NAME)

    playing = True

    while playing:
        print(g)
        g.play()
        choice = input('keep playing? > ')
        if choice.lower() == 'n' or choice == 0:
            playing = False

        os.system('clear')
    exit()


if __name__ == "__main__":
    print_logo()
    menu()

    while True:
        choice = input('> ')
        choice = choice.lower()

        if choice in options:
            exec(options[choice][1])
        else:
            print('Not a valid option!')
