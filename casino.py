from __future__ import print_function

import blinds
import table


def print_logo():
    print('*'*80)
    with open('logo.txt') as f:
        print(f.read())


def pick_limit():
    print('Please enter what limit you want to play:(default 2/4)')

    struct_list = sorted(blinds.limit.keys())
    for l in struct_list:
        print('{}, '.format(l), end='')

    choice = input(':> ')
    if choice in blinds.limit:
        print('You selected {}'.format(choice))
        return blinds.limit[choice]
    else:
        print('Selection not available, going with default blinds: 2/4')
        return blinds.limit['2/4']


def pick_table():
    print('What size table do you want to play? (default is 2 seats)')

    for l in table.VALID_SIZES:
        print('{}, '.format(l), end='')

    choice = input(':> ')
    if int(choice) in table.VALID_SIZES:
        print('You selected {}'.format(choice))
        return choice
    else:
        print('Selection not available, going with default: 2 seats')
        return 2


def pick_name():
    print('Please enter your username.')
    while True:
        name = input(':> ')
        if len(name) > 15:
            print('Name is too long! Must be less than 15 characters.')
        else:
            break
    return name
