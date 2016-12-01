"""
  " Original console interface for the poker game.
  " Deprecated: I'm Using the cmd module now, see cmdline.py.
  """
#!/usr/bin/env python3

from __future__ import print_function
import os
from ponyup import blinds
from ponyup import combos
from ponyup import lobby
from ponyup import names
from ponyup import numtools
from ponyup import player
from ponyup import factory
from ponyup import logger

DEFAULT_PLAYER = 'luna'
DISPLAYWIDTH = 70
HERO = player.load_player(DEFAULT_PLAYER)
LOBBY = lobby.Lobby()
GAME = LOBBY.default()
LOGO = 'data/logo.txt'
_logger = logger.get_logger(__name__)

menu = {}
menu['h'] = ('(H)elp', 'show_help()')
menu['o'] = ('(O)ptions', 'show_options()')
menu['q'] = ('(Q)uit', 'exit()')

# Define menu opions
options = {}
options['m'] = ('(M)athematical Analysis', 'view_combos()')
options['p'] = ('(P)lay Poker!', 'play_poker()')
options['l'] = ('(L)oad Player', 'load_player()')
options['n'] = ('(N)ew Player', 'create_player()')
options['d'] = ('(D)elete Player', 'delete_player()')
options['g'] = ('(G)ame change', 'pick_game()')
options['q'] = ('(Q)uit', 'exitgracefully()')


def prompt(p=''):
    print(p)
    i = input(':> ')
    # Process the universal options
    if i in menu:
        exec(menu[i][1])  # Execute the menu item.
        return None
    else:  # We got something else...
        return i


def pick_name():
    _logger.debug('pick_name')
    while True:
        name = prompt('Username?')
        if name is None:
            pass
        elif name == '':
            return None
        elif not names.is_validname(name):
            print('Name must be between {} and {} characters long.'.format(
                names.MIN_LEN, names.MAX_LEN))
        elif names.has_surr_char(name):
            print('Name cannot have any of these characters: {}'.format(
                names.INVALID_CHARACTERS))
        else:
            _logger.debug('pick_name input: "{}"'.format(name))
            return name


def load_player():
    _logger.debug('load_player')
    name = pick_name()
    global HERO
    HERO = player.load_player(name)
    if HERO:
        _logger.debug('Loaded player')
    else:
        _logger.debug('Player load error.')
    pause()


def create_player():
    _logger.debug('create_player')
    name = pick_name()
    global HERO
    HERO = player.create_player(name)
    if HERO:
        _logger.debug('Created player {}'.format(name))
    else:
        _logger.debug('Create player failed.')
    pause()


def delete_player():
    _logger.debug('delete_player')
    name = pick_name()
    result = player.del_player(name)
    if result:
        if HERO is not None and name == HERO.name:
            _logger.debug('Renaming the HERO variable to None because the player deleted the current player')
            global HERO
            HERO = None
        else:
            _logger.debug('Player deleted a player other than the current HERO.')
    else:
        _logger.debug('Delete player failed.')
    pause()


def pick_game():
    _logger.debug('pick_game')
    tables = lobby.sort_by_stakes(LOBBY.all_tables())

    print(lobby.numbered_list(tables))
    valid_choices = list(range(len(tables)))
    print('What game do you want to play?')
    return tables[get_menu_number(valid_choices)]

    _logger.debug('The game picked was: {}'.format(GAME))


def get_menu_number(validchoices):
    while True:
        choice = prompt()
        if choice is None:
            pass
        elif numtools.is_integer(choice) is False:
            print('Please enter a number for your selection!')
        elif int(choice) in validchoices:
            return int(choice)
        else:
            print('Selection not available, try again.')


def logo():
    txt = ''
    with open(LOGO) as f:
        for l in f.readlines():
            txt += l
    txt += '\n'
    txt += ('~'*70)
    txt += '\n'
    return txt


def menu_str():
    _str = ''
    for o in sorted(options.keys()):
        _str += '{}\n'.format(options[o][0])
    return _str


def view_combos():
    _logger.debug('Printing out the card combinations in the deck.')
    _str = ''
    _str += "Calculating different possibilities for combinations in a standard 52-card deck:"
    for i in range(1, 52):
        _str += '{} card: {} combos.\n'.format(i, combos.n_choose_k(52, i))
    print(_str)
    pause()


def play_poker():
    _logger.debug('Preparing poker game.')
    if HERO is None:
        print('You need to load or create a player first!')
        pause()
        return

    _logger.debug('Getting the buyin from the player')
    rebuy = get_buyin(GAME, HERO)
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
            rebuy = get_buyin(GAME, HERO)

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
    _logger.debug('Waiting for a keypress.')
    input('Press any key to continue...')


def player_info(p):
    if HERO:
        return '{}(${} in bank)'.format(str(HERO), HERO.bank)
    else:
        return ''


def main_menu():
    os.system('clear')
    print(logo())
    print('-=- Settings -=-'.center(DISPLAYWIDTH))
    print('{:15} {}'.format('Player:', player_info(HERO)))
    print('{:15} {}'.format('Table Name:', GAME.tablename))
    print('{:15} {}'.format('Game:', GAME.game))
    print('{:15} {}'.format('Stakes:', blinds.get_stakes(GAME.level)))
    print('{:15} {}'.format('Seats:', GAME.seats))
    print('-=- Main Menu Options -=-'.center(DISPLAYWIDTH))
    print(menu_str())


def process_user_choice():
    choice = input(':> ')

    _logger.debug('Hero entered {}.'.format(choice))
    choice = choice.lower()

    if choice in options:
        _logger.debug('Valid input, processing option.')
        exec(options[choice][1])
    else:
        _logger.debug('Input not valid.')
        print('Not a valid option!')


def get_buyin(game, hero):
    minbuyin = blinds.stakes[game.level] * 10
    if hero.bank < minbuyin:
        print('Sorry, you don\'t have enough chips to buyin to this game!')
        return None
    print('The minimum buy-in for {} is {} bits.'.format(
        blinds.get_stakes(game.level), minbuyin))

    while True:
        print('How much do you want to buyin for? (Minimum={})'.format(minbuyin))

        choice = prompt()
        if numtools.is_integer(choice):
            if int(choice) < minbuyin:
                print('Not enough!\n')
            elif int(choice) > hero.bank:
                print('This is more chips than you can afford!\n')
            else:
                return int(choice)
        else:
            print('Invalid input!\n')


def right_align(txt):
    for l in txt.split('\n'):
        print(l.rjust(DISPLAYWIDTH))


def gameloop():
    _logger.debug('New run of {}'.format(__name__))

    _logger.debug('Starting game loop.')
    while True:
        main_menu()
        process_user_choice()
