"""
  " Module for producing new names for computer players.
  " Rules for player names:
  "     Must be 3 to 20 characters long.
  "     Can contain special characters.
  "     Cannot contain any non-ASCII characters or characters that do unusual things.
  """
import random
import re
import sqlite3

MIN_LEN, MAX_LEN = 3, 20
INVALID_CHARACTERS = r"[<>()/{}[\]`'\\]"
DB = 'data/game.db'

pokerplayers = [
    'Seidel', 'Doyle', 'Mercier', 'Negreanu', 'Grospellier', 'Hellmuth', 'Mortensen',
    'Antonius', 'Harman', 'Ungar', 'Dwan', 'Greenstein', 'Chan', 'Moss', 'Ivey', 'Brunson',
    'Reese', 'Esfandiari', 'Juanda', 'Duhamel', 'Gold', 'Cada', 'Mizrachi', 'Schulman',
    'Selbst', 'Duke', 'Rousso', 'Liebert', 'Galfond', 'Elezra', 'Benyamine', 'Booth',
    'DAgostino', 'Eastgate', 'Farha', 'Ferguson', 'Forrest', 'Hansen', 'Hachem', 'Kaplan',
    'Laak', 'Lederer', 'Lindren', 'Matusow', 'Minieri'
]


def get_names_from_db():
    """ Retrieve the names from the SQL database """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    names = [n[0] for n in c.execute('SELECT * FROM ponies')]

    c.close()
    conn.close()
    return names


def random_names(num, namelist=get_names_from_db()):
    """ Generate a unique list of names from the names module.
        num specifies how many names
    """
    nameset = []

    # Make sure all the names are unique
    for _ in range(num):
        nameset.append(new_name(nameset, namelist))
    return nameset


def new_name(taken, namelist):
    while True:
        nextname = random.choice(namelist)
        if nextname not in taken and is_validname(nextname):
            return nextname


def is_validname(name):
    """ Returns True if the given name is between MIN_LEN and MAX_LENcharacters
        long, False otherwise.
    """
    if len(name) < MIN_LEN:
        print('Name is too short!')
    elif len(name) > MAX_LEN:
        print('Name is too long!')
        return False
    elif has_surr_char(name):
        print('Name has illegal characters!')
        return False
    else:
        return True


def has_surr_char(string):
    """ Returns True if the given string contains any 'surround' characters,
        False otherwise.
        These characters many cause bugs in programs if used.
    """
    re1 = re.compile(INVALID_CHARACTERS)
    if re1.search(string):
        return True
    else:
        return False
