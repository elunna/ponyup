"""
  " Console interface for the poker game.
  " I'm Using the cmd module now, see cmdline.py.
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

DISPLAYWIDTH = 80
LOGO = 'data/logo.txt'
HERO = 'luna'
DEFAULT_TABLE = "Twilight's Lab"


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
            return name


def load_player():
    name = pick_name()
    global HERO
    HERO = player.load_player(name)
    pause()


def create_player():
    name = pick_name()
    global HERO
    HERO = player.create_player(name)
    pause()


def delete_player():
    name = pick_name()
    result = player.del_player(name)
    if result:
        if HERO is not None and name == HERO.name:
            global HERO
            HERO = None
    pause()


def pick_game():
    tables = lobby.sort_by_stakes(LOBBY.all_tables())

    print(lobby.numbered_list(tables))
    valid_choices = list(range(len(tables)))
    print('What game do you want to play?')
    return tables[get_menu_number(valid_choices)]


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
    """ Display the game logo """
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
    for o in sorted(menu_options.keys()):
        _str += '{}\n'.format(menu_options[o][0])
    return _str


def view_combos():
    print('Printing out the card combinations in the deck.')
    _str = ''
    _str += "Calculating different possibilities for combinations in a standard 52-card deck:"
    for i in range(1, 52):
        _str += '{} card: {} combos.\n'.format(i, combos.n_choose_k(52, i))
    print(_str)
    pause()


def play_poker():
    """ Start a session of poker """
    if HERO is None:
        print('You need to load or create a player first!')
        pause()
        return

    rebuy = get_buyin(GAME, HERO)

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
        os.system('clear')
        g.play()
        # Check if hero went broke
        if g.find_hero().stack == 0:
            rebuy = get_buyin(GAME, HERO)

        g.table_maintainance()

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


def player_info(p):
    if HERO:
        return '{}(${} in bank)'.format(str(HERO), HERO.bank)
    else:
        return ''


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

menu = {
    'h': ('(H)elp', 'show_help()'),
    'o': ('(O)ptions', 'show_options()'),
    'q': ('(Q)uit', 'exit()'),
}

# Define menu opions
menu_options = {
    'm': ('(M)athematical Analysis', 'view_combos()'),
    'p': ('(P)lay Poker!', 'play_poker()'),
    'l': ('(L)oad Player', 'load_player()'),
    'n': ('(N)ew Player', 'create_player()'),
    'd': ('(D)elete Player', 'delete_player()'),
    'g': ('(G)ame change', 'pick_game()'),
    'q': ('(Q)uit', 'exitgracefully()'),
}


def main_menu(session):
    """ Display the main menu """
    os.system('clear')
    print(logo())
    print('-=- Settings -=-'.center(DISPLAYWIDTH))
    print('{:15} {}'.format('Player:', player_info(session['hero'])))
    print('{:15} {}'.format('Table Name:', session['tablename']))
    print('{:15} {}'.format('Game:', session['game']))
    print('{:15} {}'.format('Stakes:', blinds.get_stakes(session['level'])))
    print('{:15} {}'.format('Seats:', session['seats']))
    print('-=- Main Menu Options -=-'.center(DISPLAYWIDTH))
    print(menu_str())


def process_user_choice():
    choice = input(':> ')
    choice = choice.lower()

    if choice in menu_options:
        exec(menu_options[choice][1])
    else:
        print('Not a valid option!')


def main():
    """ Main entry point """

    SESSION = {
        'game': 'FIVE CARD DRAW',
        'level': 1,
        'seats': 6,
        'rounds': 0,
        'table': lobby.get_game(DEFAULT_TABLE),
        'hero': player.load_player(HERO),
    }

    while True:
        main_menu(SESSION)
        process_user_choice()


if __name__ == "__main__":
    main()
