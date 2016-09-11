import colors
import lobby
import names

"""
Provides tools for interacting with the user at the text-based console.
"""


def is_integer(num):
    """
    Returns True if the num argument is an integer, and False if it is not.
    """
    try:
        num = float(num)
    except:
        return False

    return num.is_integer()


def pick_game():
    LOBBY = lobby.lobbylist
    drawgames = lobby.get_game(LOBBY, "FIVE CARD DRAW")
    drawgames = lobby.sort_by_level(drawgames)
    studgames = lobby.get_game(LOBBY, "FIVE CARD STUD")
    studgames = lobby.sort_by_level(studgames)

    tables = drawgames + studgames

    print('What game do you want to play?')
    print(lobby.display_numbered_list(tables))

    valid_choices = list(range(len(tables)))

    while True:
        choice = input(':> ')
        if is_integer(choice) is False:
            print('Please enter a number for your selection!')
        elif int(choice) in valid_choices:
            return tables[int(choice)]
        else:
            print('Selection not available, try again.')


def pick_name():
    print('Please enter your username.')
    while True:
        name = input(':> ')
        if not names.is_validname(name):
            print('Name must be between {} and {} characters long.'.format(
                names.MIN_LEN, names.MAX_LEN))
        elif names.has_surr_char(name):
            print('Name cannot have any of these characters: {}'.format(
                names.INVALID_CHARACTERS))
        else:
            return name


def menu(options):
    """
    Display a list of betting options, and get input from the player to pick a valid option.
    """
    nice_opts = ['[' + colors.color(v.name[0], 'white', STYLE='BOLD') + ']' +
                 v.name[1:].lower()
                 for k, v in sorted(options.items())]
    choices = '/'.join(nice_opts)

    print('')
    while True:
        choice = input('{}? :> '.format(choices))

        if choice == 'q':
            exit()
        elif choice.lower() in options:
            return options[choice]
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
            _str += '{:16}'.format(str(s.hand.peek()))
        elif s.hand is not None:
            _str += '{:16}'.format(str(s.hand))
        _str += '\n'

    return _str


def player_listing(table):
    """
    Returns the list of seats with players and stacks, for the hand history.
    """
    _str = ''
    for i, s in enumerate(table.seats):
        _str += 'Seat #{}: {}(${})\n'.format(i, str(s.player), s.stack)
    return _str


"""
How to make this display color?
def action_string(action):
    s = self.get_bettor()
    act_str = ''
    act_str += '{} {}s'.format(s.player, action.name.lower())

    amt = colors.color(' $' + str(action.cost), 'yellow')

    if action.name in ['BET', 'RAISE']:
        return colors.color(act_str, 'red') + amt
    elif action.name == 'CALL':
        return colors.color(act_str, 'white') + amt
    elif action.name == 'FOLD':
        return colors.color(act_str, 'purple')
    elif action.name == 'CHECK':
        return colors.color(act_str, 'white')
    elif action.name == 'ALLIN':
        return colors.color(
            '{}{} is all in.'.format(spacing(self.level()), s.player), 'gray')
    else:
        raise Exception('Error processing the action!')
"""
