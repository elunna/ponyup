import random
import re
"""
Rules for player names:
    Must be 3 to 20 characters long.
    Can contain special characters.
    Cannot contain any non-ASCII characters or characters that do unusual things.
"""

# Maximum name length
MAX_LEN = 20
MIN_LEN = 3
INVALID_CHARACTERS = r"[<>()/{}[\]`'\\]"

names = ['Seidel', 'Doyle', 'Mercier', 'Negreanu', 'Grospellier', 'Hellmuth', 'Mortensen',
         'Antonius', 'Harman', 'Ungar', 'Dwan', 'Greenstein', 'Chan', 'Moss', 'Ivey', 'Brunson',
         'Reese', 'Esfandiari', 'Juanda', 'Duhamel', 'Gold', 'Cada', 'Mizrachi', 'Schulman',
         'Selbst', 'Duke', 'Rousso', 'Liebert', 'Galfond', 'Elezra', 'Benyamine', 'Booth',
         'DAgostino', 'Eastgate', 'Farha', 'Ferguson', 'Forrest', 'Hansen', 'Hachem', 'Kaplan',
         'Laak', 'Lederer', 'Lindren', 'Matusow', 'Minieri']


def read_ponynames():
    names = []
    with open('ponynames.txt') as f:
        for l in f.readlines():
            names.append(l.strip())
    return names


def random_names(num):
    """
    Generate a unique list of names from the names module. num specifies how many names.
    """
    nameset = []

    # Make sure all the names are unique
    for i in range(num):
        while True:
            nextname = random.choice(read_ponynames())
            if nextname not in nameset and is_validname(nextname):
                nameset.append(nextname)
                break
    return nameset


def is_validname(name):
    """
    Returns True if the given name is between MIN_LEN and MAX_LENcharacters long, False
    otherwise.
    """
    if len(name) < MIN_LEN or len(name) > MAX_LEN:
        return False
    else:
        return True


def has_surr_char(string):
    """
    Returns True if the given string contains any 'surround' characters, False otherwise.
    These characters many cause bugs in programs if used.
    """
    re1 = re.compile(INVALID_CHARACTERS)
    if re1.search(string):
        #  print ("RE1: Invalid char detected.")
        return True
    else:
        #  print ("RE1: No invalid char detected.")
        return False
