#!/usr/bin/env python3

from __future__ import print_function
import colors
import combos
import console
import lobby
import os
import session_factory

NAME = 'Aorist Twilist'
GAME = lobby.default()
DISPLAYWIDTH = 70

# Define menu opions
options = {}
options['c'] = ('(C)ombination counts', 'print(view_combos())')
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


def logo():
    txt = ''
    with open('logo2.txt') as f:
        for c in f.read():
            if c == '$':
                txt += colors.color(c, 'yellow')
            else:
                txt += colors.color(c, 'green')
    txt += '\n'
    txt += ('~'*70)
    txt += '\n'
    return txt


@colors.colorit("WHITE")
def settings_title():
    return '-=- Settings -=-'.center(70)


@colors.colorit("LIGHTBLUE")
def menu_str():
    _str = ''
    for o in sorted(options.keys()):
        _str += '{}\n'.format(options[o][0])
    return _str


def view_combos():
    _str = ''
    _str += "Calculating different possibilities for combinations in a standard 52-card deck:"
    for i in range(1, 52):
        _str += '{} card: {} combos.\n'.format(i, combos.n_choose_k(52, i))
    return _str


def play_poker():
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


def main_menu():
    os.system('clear')
    print(logo())
    print(settings_title())
    print(console.color_name(NAME))
    print(console.color_game(GAME))
    print(menu_str())


if __name__ == "__main__":
    while True:
        main_menu()
        choice = input('> ')
        choice = choice.lower()

        if choice in options:
            exec(options[choice][1])
        else:
            print('Not a valid option!')

        input('Press any key to continue...')
