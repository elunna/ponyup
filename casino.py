#!/usr/bin/env python3

from __future__ import print_function
import colors
import combos
import console
import lobby
import os
import session_factory

NAME = 'AORIST'
GAME = lobby.default()

# Define menu opions
options = {}
options['c'] = ('(C)ombination counts', 'view_combos()')
options['p'] = ('(P)lay Poker!', 'play_poker()')
options['n'] = ('(N)ame change', 'pick_name()')
options['g'] = ('(G)ame change', 'pick_game()')
options['q'] = ('(Q)uit', 'exitgracefully()')


def pick_name():
    global NAME
    NAME = console.pick_name()


def pick_game():
    global GAME
    GAME = console.pick_game()


def print_logo():
    txt = ''
    with open('logo2.txt') as f:
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
    print('{:>15}: {}'.format('Table Name', GAME.tablename))
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


def play_poker():
    print('Alright, let\'s play some poker!')

    print('Initializing new game...\n')

    #  g = session_factory.make(GAME, NAME)
    g = session_factory.factory(
        seats=GAME.seats,
        game=GAME.game,
        tablename=GAME.tablename,
        level=GAME.level,
        heroname=NAME,
        names='random',
    )

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
    exit()


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
