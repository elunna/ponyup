#!/usr/bin/env python3

from __future__ import print_function
import os
from ponyup import colors
from ponyup import combos
from ponyup import console
from ponyup import lobby
from ponyup import player
from ponyup import factory
from ponyup import logger


HERO = None
LOBBY = lobby.Lobby()
GAME = LOBBY.default()
LOGO = 'data/logo2.txt'
_logger = logger.get_logger(__name__)

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
    _logger.debug('load_player')
    name = console.pick_name()
    _logger.debug('Player entered {}'.format(name))
    global HERO
    HERO = player.load_player(name)
    _logger.debug('Loaded player')
    pause()


def create_player():
    _logger.debug('create_player')
    name = console.pick_name()
    _logger.debug('Player entered {}'.format(name))
    global HERO
    HERO = player.create_player(name)
    _logger.debug('Created player')
    pause()


def delete_player():
    _logger.debug('delete_player')
    name = console.pick_name()
    _logger.debug('Player entered {}'.format(name))
    player.del_player(name)
    if HERO is not None and name == HERO.name:
        _logger.debug('Renaming the HERO variable to None because the player deleted the current player')
        global HERO
        HERO = None
    else:
        _logger.debug('Player deleted a player other than the current HERO.')

    pause()


def pick_game():
    _logger.debug('pick_game')
    global GAME
    GAME = console.pick_game(LOBBY)
    _logger.debug('The game picked was: {}'.format(GAME))


def logo():
    _logger.debug('Printing out the logo')
    txt = ''
    with open(LOGO) as f:
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
    _logger.debug('Printing out the menu')
    _str = ''
    for o in sorted(options.keys()):
        _str += '{:12}{}\n'.format('', options[o][0])
    return _str


def view_combos():
    _logger.debug('Printing out the card combinations in the deck.')
    _str = ''
    _str += "Calculating different possibilities for combinations in a standard 52-card deck:"
    for i in range(1, 52):
        _str += '{} card: {} combos.\n'.format(i, combos.n_choose_k(52, i))
    return _str


def play_poker():
    _logger.debug('Preparing to play the selected game.')
    if HERO is None:
        print('You need to load or create a player first!')
        pause()
        return

    _logger.debug('Getting the buyin from the player')
    rebuy = console.get_buyin(GAME, HERO)
    _logger.debug('The buyin selected was: {}'.format(rebuy))

    _logger.debug('Constructing the session from a factory.')
    g = factory.session_factory(
        seats=GAME.seats,
        game=GAME.game,
        tablename=GAME.tablename,
        level=GAME.level,
        hero=HERO,
        names='random',
        herobuyin=rebuy,
        varystacks=True
    )
    playing = True

    while playing:
        _logger.debug('Clearing the screen.')
        os.system('clear')
        _logger.debug('Play a round of the selected session game.')
        g.play()
        # Check if hero went broke
        _logger.debug('Check if the hero went broke.')
        if g.find_hero().stack == 0:
            _logger.debug('Hero went broke, offer them the option to rebuy back in.')
            rebuy = console.get_buyin(GAME, HERO)

            _logger.debug('Hero entered {} for rebuy.'.format(rebuy))

        _logger.debug('Perform in-between game activities')
        g.table_maintainance()

        _logger.debug('Offer the player the option to keep playing the session or quit.')
        choice = input('keep playing? > ')
        _logger.debug('Player entered {}'.format(choice))
        if choice.lower() == 'n':
            _logger.debug('Setting playing to False.')
            playing = False
            _logger.debug('Removing the hero from the table.')
            g.find_hero().standup()
            _logger.debug('Saving the player info to file.')
            player.save_player(HERO)
        else:
            _logger.debug('Player elected to continue playing.')


def exitgracefully():
    _logger.debug('Exiting the program.')
    print('Bye!')
    exit()


def pause():
    _logger.debug('Pausing the game. Waiting for a keypress.')
    input('Press any key to continue...')


def main_menu():
    os.system('clear')
    print(logo())
    print(console.title('-=- Settings -=-'))
    print(console.color_name(HERO))
    print(console.color_game(GAME))
    print(console.title('-=- Main Menu Options -=-'))
    print(menu_str())


def process_user_choice():
    _logger.debug('Getting user input.')
    choice = input(':> ')

    _logger.debug('Hero entered {}.'.format(choice))
    choice = choice.lower()

    if choice in options:
        _logger.debug('User input was valid, processing option.')
        exec(options[choice][1])
    else:
        _logger.debug('User input was not valid.')
        print('Not a valid option!')

    if choice == 'm':
        _logger.debug('User looked at math combinations, pausing.')
        pause()

if __name__ == "__main__":

    _logger.debug('New run of {}'.format(__name__))

    _logger.debug('Starting game loop.')
    while True:
        main_menu()
        process_user_choice()
