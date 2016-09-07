#!/usr/bin/env python3

from __future__ import print_function
import colors
import combos
import lobby
import os
import sys

NAME = 'Loose Canon'
GAME = lobby.tables[0]

# Define menu opions
options = {}
options['c'] = ('(C)ombination counts', 'view_combos()')
options['p'] = ('(P)lay Poker!', 'play_poker()')
options['n'] = ('(N)ame change', 'pick_name()')
options['g'] = ('(G)ame change', 'pick_game()')
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
    print('{:>15}: {}'.format('Table Name', GAME.name))
    print('{:>15}: {}'.format('Game', GAME.game))
    print('{:>15}: {}'.format('Stakes',  lobby.stakes(GAME)))
    print('{:>15}: {}'.format('Seats', GAME.seats))
    print('')

    for o in sorted(options.keys()):
        print(options[o][0])


def view_combos():
    print("Calculating different possibilities for combinations in a standard 52-card deck:")
    for i in range(1, 52):
        print('{} card: {} combos '.format(i, combos.n_choose_k(52, i)))

    input('Press any key to continue...')


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
    tables = lobby.sort_by_level(lobby.tables)
    print(lobby.display_numbered_list(tables))

    while True:
        choice = int(input(':> '))
        if choice in list(range(len(tables))):
            global GAME
            GAME = tables[choice]
            print('You selected {}'.format(GAME))
            break
        else:
            print('Selection not available, try again.')


def play_poker():
    print('Alright, let\'s play some poker!')

    print('Initializing new game...\n')

    g = lobby.session_factory(GAME, NAME)
    playing = True

    while playing:
        os.system('clear')
        print(g)
        g.play()
        choice = input('keep playing? > ')
        if choice.lower() == 'n' or choice == 0:
            playing = False

    return


def exitgracefully():
    print('Bye!')
    sys.exit()


if __name__ == "__main__":

    while True:
        os.system('clear')
        print_logo()
        menu()
        choice = input('> ')
        choice = choice.lower()

        if choice in options:
            exec(options[choice][1])
        else:
            print('Not a valid option!')
            input('Press any key to continue...')
