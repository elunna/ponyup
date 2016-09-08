import lobby
import names
import numbers

"""
Provides tools for interacting with the user at the text-based console.
"""


def is_integer(num):
    """
    Determines if the variable is an integer.
    """
    try:
        num = int(num)
    except:
        return False
    return isinstance(num, numbers.Integral)


def pick_game():
    print('What game do you want to play?')
    tables = lobby.sort_by_level(lobby.tables)
    print(lobby.display_numbered_list(tables))

    while True:
        choice = input(':> ')
        if is_integer(choice) is False:
            print('Please enter a number for your selection!')
        elif int(choice) in list(range(len(tables))):
            return tables[int(choice)]
        else:
            print('Selection not available, try again.')


def pick_name():
    print('Please enter your username.')
    while True:
        name = input(':> ')
        if not names.is_validname(name):
            print('Name is too long! Must be between {} and {} characters long.'.format(
                names.MIN_LEN, names.MAX_LEN))
        elif names.has_surr_char(name):
            print('Name cannot have any of these characters: {}'.format(
                names.INVALID_CHARACTERS))
        else:
            return name
