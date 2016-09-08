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
