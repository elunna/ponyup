"""
  " Module for producing new names for computer players.
  " Rules for player names:
  "     Must be 3 to 20 characters long.
  "     Can contain special characters.
  "     Cannot contain any non-ASCII characters or characters that do unusual things.
  """
from random import shuffle
import re


MIN_LEN, MAX_LEN = 3, 20
INVALID_CHARACTERS = r"[<>()/{}[\]`'\\]"

pokerplayers = [
    'Seidel',
    'Doyle',
    'Mercier',
    'Negreanu',
    'Grospellier',
    'Hellmuth',
    'Mortensen',
    'Antonius',
    'Harman',
    'Ungar',
    'Dwan',
    'Greenstein',
    'Chan',
    'Moss',
    'Ivey',
    'Brunson',
    'Reese',
    'Esfandiari',
    'Juanda',
    'Duhamel',
    'Gold',
    'Cada',
    'Mizrachi',
    'Schulman',
    'Selbst',
    'Duke',
    'Rousso',
    'Liebert',
    'Galfond',
    'Elezra',
    'Benyamine',
    'Booth',
    'DAgostino',
    'Eastgate',
    'Farha',
    'Ferguson',
    'Forrest',
    'Hansen',
    'Hachem',
    'Kaplan',
    'Laak',
    'Lederer',
    'Lindren',
    'Matusow',
    'Minieri'
]


def random_names(num, namelist=pokerplayers):
    """ Generate a unique list of names from the namelist.
        num specifies how many names
    """
    shuffle(namelist)
    try:
        return namelist[:num]
    except:
        return namelist


def is_validname(name):
    """ Returns True if the given name is between MIN_LEN and MAX_LENcharacters
        long, False otherwise.
    """
    if len(name) < MIN_LEN or len(name) > MAX_LEN:
        return False
    elif has_surr_char(name):
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
