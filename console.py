import card
import colors
import lobby
import names

"""
Provides tools for interacting with the user at the text-based console.
"""

DISPLAYWIDTH = 70
menu = {}
menu['h'] = ('(H)elp', 'show_help()')
menu['o'] = ('(O)ptions', 'show_options()')
menu['q'] = ('(Q)uit', 'exit()')


def is_integer(num):
    """
    Returns True if the num argument is an integer, and False if it is not.
    """
    try:
        num = float(num)
    except:
        return False

    return num.is_integer()


def show_help():
    print('This is the help menu')


def show_options():
    print('This is the options menu')


def prompt(p=''):
    print(p)
    i = input(':> ')
    # Process the universal options
    if i in menu:
        exec(menu[i][1])  # Execute the menu item.
        return None
    else:  # We got something else...
        return i


def pick_game():
    tables = lobby.sorted_by_game_and_lev()
    print(lobby.numbered_list(tables))
    valid_choices = list(range(len(tables)))

    while True:
        choice = prompt('What game do you want to play?')
        if choice is None:
            pass
        elif is_integer(choice) is False:
            print('Please enter a number for your selection!')
        elif int(choice) in valid_choices:
            return tables[int(choice)]
        else:
            print('Selection not available, try again.')


def pick_name():
    while True:
        name = prompt('Please enter your username.')
        if name is None:
            pass
        elif not names.is_validname(name):
            print('Name must be between {} and {} characters long.'.format(
                names.MIN_LEN, names.MAX_LEN))
        elif names.has_surr_char(name):
            print('Name cannot have any of these characters: {}'.format(
                names.INVALID_CHARACTERS))
        else:
            return name


def betmenu(actions):
    """
    Display a list of betting options, and get input from the player to pick a valid option.
    """
    nice_opts = ['[' + colors.color(v.name[0], 'white', STYLE='BOLD') + ']' +
                 v.name[1:].lower()
                 for k, v in sorted(actions.items())]
    choices = '/'.join(nice_opts)

    while True:
        choice = prompt('{}?'.format(choices))
        if choice is None:
            pass  # They chose a main menu option
        elif choice.lower() in actions:
            return actions[choice]
        else:
            print('Invalid choice, try again.')


def display_table(table, hero=None):
    """
    Return the string representation of the table, with colors.
    """
    _str = ''
    _str = colors.color('{:5}{:7}{:7}{:20}{:<17}{:16}\n'.format(
        'Seat', 'Blinds', 'Dealer', 'Player', 'Chips', 'Hand'), 'gray', STYLE='BOLD')

    for i, s in enumerate(table.seats):
        if s is None:
            # No player is occupying the seat
            _str += '{}\n'.format(i)
            continue
        else:
            _str += '{:<5}'.format(i)

        if table.TOKENS['SB'] == i:
            _str += colors.color('{:7}'.format('[SB]'), 'lightblue')
        elif table.TOKENS['BB'] == i:
            _str += colors.color('{:7}'.format('[BB]'), 'blue')
        elif table.TOKENS['BI'] == i:
            _str += colors.color('{:7}'.format('[BI]'), 'lightblue')
        else:
            _str += ' '*7

        if table.TOKENS['D'] == i:
            _str += colors.color('{:7}'.format('[D]'), 'purple')
        else:
            _str += ' '*7

        _str += '{:20}'.format(str(s.player))

        _str += colors.color('${:<16}'.format(s.stack), 'yellow')

        # Display hand if available
        if s == hero:
            _str += '{:16}'.format(color_cards(s.hand.peek()))
        elif s.hand is not None:
            _str += '{:16}'.format(color_cards(str(s.hand)))
        _str += '\n'

    return _str


@colors.colorit("WHITE")
def color_setting(p):
    return p


@colors.colorit("PURPLE")
def color_param(p):
    return p


def color_name(name):
    return '{:>15}: {}'.format(color_setting('Name'), color_param(name))


def color_game(GAME):
    FMT = '{:>15}: {}\n'
    _str = ''
    _str += FMT.format(color_setting('Table Name'), color_param(GAME.tablename))
    _str += FMT.format(color_setting('Game'), color_param(GAME.game))
    _str += FMT.format(color_setting('Stakes'), color_param(lobby.stakes(GAME)))
    _str += FMT.format(color_setting('Seats'), color_param(GAME.seats))

    return _str


def color_cards(cards):
    """
    Process card text to color representation
    """
    _str = ''
    for c in cards.split():
        if c == 'Xx':
            _str += colors.color(c, 'PURPLE') + ' '
        else:
            _str += colors.color(c, card.COLORS[c[1]]) + ' '
    return _str.strip()


@colors.colorit("YELLOW")
def colorpot(amt):
    return '$' + amt


def print_pot(pot):
    txt = colorpot(pot).strip()
    print('Pot: ' + txt)


def print_action(space, act_str):
    if 'fold' in act_str:
        print(space, colors.color(act_str, 'PURPLE'))
    elif 'check' in act_str:
        print(space, colors.color(act_str, 'WHITE'))
    elif 'allin' in act_str:
        print(space, colors.color(act_str, 'WHITE'))
    elif 'bet' in act_str:
        print(space, colors.color(act_str, 'RED'))
    elif 'raise' in act_str:
        print(space, colors.color(act_str, 'RED'))
