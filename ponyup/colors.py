"""
  " Tools for adding color to ASCII text.
  """
from functools import wraps
from ponyup import card

CSI = "\x1b["
CSI_end = "\x1b[0m"
#  reset = CSI + "m"


STYLES = {
    'NORMAL': 0,
    'BOLD': 1,
    'FADE': 2,
    'ITALIC': 3,
    'UNDERLINE': 4,
}

COLORS = {
    'RED': 31,
    'GRAY': 40,
    'GREEN': 32,
    'YELLOW': 33,
    'BLUE': 34,
    'PURPLE': 35,
    'LIGHTBLUE': 36,
    'WHITE': 37,
}


def color(string, fg, bg='GRAY', STYLE='NORMAL'):
    """
    Returns a colored version of the given string. Can specify the foreground color, background
    color, and style of returned text.
    """
    if fg.upper() in COLORS:
        return '{}{};{};{}m{}{}'.format(
            CSI,
            STYLES[STYLE],
            COLORS[fg.upper()],
            COLORS[bg.upper()],
            string,
            CSI_end)
    else:
        raise ValueError('Passed arg color is not in the available colors!')


def colorit(c):
    """ Coloring decorator. """
    def decorate(func):
        """ A decorator that when attached to a function, lets you provide a color. """
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return '{}{};{};{}m{}{}'.format(
                CSI, STYLES['NORMAL'], COLORS[c.upper()], 40, result, CSI_end)

            # return func(*args, **kwargs)
        return wrapper
    return decorate


@colorit('yellow')
def pot(p):
    return 'pot={}'.format(p)


def color_options(actions):
    colored_options = ['[' + color(v.name[0], 'white', STYLE='BOLD') + ']' + v.name[1:].lower()
                       for v in sorted(actions.values())]

    return '/'.join(colored_options)


@colorit("WHITE")
def color_setting(s):
    return s


@colorit("PURPLE")
def color_param(p):
    return p


@colorit("WHITE")
def title(title):
    return title


@colorit("YELLOW")
def color_chips(amt):
    return '$' + amt


def color_action(space, act_str):
    """ Colors a player's action in a poker game based on the actions meaning. """
    mstart = act_str.find('$')
    chips = color_chips(act_str[mstart+1:])

    if 'fold' in act_str:
        print('{}{}'.format(space, color(act_str, 'PURPLE')))
    elif 'check' in act_str:
        print('{}{}'.format(space, color(act_str, 'WHITE')))
    elif 'allin' in act_str:
        print('{}{}'.format(space, color(act_str, 'WHITE')))
    elif 'call' in act_str:
        print('{}{}{}'.format(space, color(act_str[:mstart], 'WHITE'), chips))
    elif 'bet' in act_str:
        print('{}{}{}'.format(space, color(act_str[:mstart], 'RED'), chips))
    elif 'raise' in act_str:
        print('{}{}{}'.format(space, color(act_str[:mstart], 'RED'), chips))


def color_cards(cards):
    """ Process card text to color representation """
    _str = ''
    for c in cards.split():
        if c == 'Xx':
            _str += color(c, 'PURPLE') + ' '
        else:
            _str += color(c, card.COLORS[c[1]]) + ' '
    return _str.strip()


def display_table(table, hero=None):
    """ Return the string representation of the table, with colors. """
    _str = '\n'
    _str = color('{:5}{:7}{:7}{:20}{:<17}{:16}\n'.format(
        'Seat', 'Blinds', 'Dealer', 'Player', 'Chips', 'Hand'), 'gray', STYLE='BOLD')

    for i, s in enumerate(table.seats):
        if s is None:
            # No player is occupying the seat
            _str += '{}\n'.format(i)
            continue
        else:
            _str += '{:<5}'.format(i)

        if table.TOKENS['SB'] == i:
            _str += color('{:7}'.format('[SB]'), 'lightblue')
        elif table.TOKENS['BB'] == i:
            _str += color('{:7}'.format('[BB]'), 'blue')
        elif table.TOKENS['BI'] == i:
            _str += color('{:7}'.format('[BI]'), 'lightblue')
        else:
            _str += ' '*7

        if table.TOKENS['D'] == i:
            _str += color('{:7}'.format('[D]'), 'purple')
        else:
            _str += ' '*7

        if s.occupied():
            _str += '{:20}'.format(str(s.player))
            _str += color_chips('{:<16}'.format(s.stack))
        else:
            # Don't show anything for vacant seats.
            _str += '{:20}{:16}'.format('', '')

        # Display hand if available
        if s == hero:
            _str += '{:16}'.format(color_cards(s.hand.peek()))
        elif s.hand is not None:
            _str += '{:16}'.format(color_cards(str(s.hand)))
        _str += '\n'

    return _str


def color_logo(LOGO):
    """ Adds color to the game logo. """
    txt = ''
    with open(LOGO) as f:
        for c in f.read():
            if c == '$':
                txt += color(c, 'yellow')
            else:
                txt += color(c, 'green')
    txt += '\n'
    txt += ('~'*70)
    txt += '\n'
    return txt
