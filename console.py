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
    tables = lobby.sort_by_level()
    print(lobby.display_numbered_list())

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


def discard_menu(hand):
    cards = ' '.join([str(c) for c in hand.cards])
    txt = 'Your discard....1  2  3  4  5\n'.rjust(70)
    txt += '\t'*7 + cards
    txt += '\n'
    return txt


def human_discard(hand, max_discards=5):
    """
    Offers the human player a menu of discard options and returns the list of chosen discards.
    """
    print(discard_menu(hand))
    while True:
        helpme = ['?', 'h', 'help']
        user_str = input(':> ')
        if user_str in helpme:
            print('')
            print('Enter the cards you want to discard:')
            print('Example: "1" discards card 1, "12" discards cards 1 and 2, etc.')
            continue

        # Split up the #s, and reverse them so we can remove them without the list
        # collapsing and disrupting the numbering.
        valid_picks = ['1', '2', '3', '4', '5']
        picks = sorted(
            [int(x) for x in set(user_str) if x in valid_picks], reverse=True)

        if len(picks) > max_discards:
            print('Sorry, the deck is low -- you can only pick up to {} cards.'.format(
                max_discards))
            continue

        discards = []

        for n in picks:
            discards.append(hand.cards[int(n) - 1])
        break
    return discards
