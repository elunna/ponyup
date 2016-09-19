#!/usr/bin/env python3

from __future__ import print_function
import colors
import combos
import console
import lobby
import os
import player
import factory

HERO = None
LOBBY = lobby.Lobby()
GAME = LOBBY.default()

# Define menu opions
options = {}
options['m'] = ('(M)athematical Analysis', 'print(view_combos())')
options['p'] = ('(P)lay Poker!', 'play_poker()')
options['l'] = ('(L)oad Player', 'load_player()')
options['c'] = ('(C)reate Player', 'create_player()')
options['d'] = ('(D)elete Player', 'delete_player()')
options['g'] = ('(G)ame change', 'pick_game()')
options['q'] = ('(Q)uit', 'exitgracefully()')


def load_player():
    name = console.pick_name()
    global HERO
    HERO = player.load_player(name)
    pause()


def create_player():
    name = console.pick_name()
    global HERO
    HERO = player.create_player(name)
    pause()


def delete_player():
    name = console.pick_name()
    player.del_player(name)
    if HERO is not None and name == HERO.name:
        global HERO
        HERO = None
    pause()


def pick_game():
    global GAME
    GAME = console.pick_game(LOBBY)


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


@colors.colorit("LIGHTBLUE")
def menu_str():
    _str = ''
    for o in sorted(options.keys()):
        _str += '{:12}{}\n'.format('', options[o][0])
    return _str


def view_combos():
    _str = ''
    _str += "Calculating different possibilities for combinations in a standard 52-card deck:"
    for i in range(1, 52):
        _str += '{} card: {} combos.\n'.format(i, combos.n_choose_k(52, i))
    return _str


def play_poker():
    if HERO is None:
        print('You need to load or create a player first!')
        pause()
        return

    buyin = console.get_buyin(GAME, HERO)

    g = factory.session_factory(
        seats=GAME.seats,
        game=GAME.game,
        tablename=GAME.tablename,
        level=GAME.level,
        hero=HERO,
        names='random',
        herobuyin=buyin,
        varystacks=True
    )
    playing = True

    while playing:
        os.system('clear')
        g.play()
        # Check if hero went broke
        if g.find_hero().stack == 0:
            buyin = console.get_buyin(GAME, HERO)

        g.table_maintainance()  # Perform in-between game activities

        choice = input('keep playing? > ')
        if choice.lower() == 'n':
            playing = False
            g.find_hero().standup()
            player.save_player(HERO)


def exitgracefully():
    print('Bye!')
    exit()


def pause():
    input('Press any key to continue...')


def main_menu():
    os.system('clear')
    print(logo())
    print(console.title('-=- Settings -=-'))
    print(console.color_name(HERO))
    print(console.color_game(GAME))
    print(console.title('-=- Main Menu Options -=-'))
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

        if choice == 'm':
            pause()
