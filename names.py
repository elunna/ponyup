import random
import re
"""
Rules for player names:
    Must be 3 to 12 characters long.
    Can contain special characters.
    Cannot contain any non-ASCII characters or characters that do unusual things.
"""

names = ['Seidel', 'Doyle', 'Mercier', 'Negreanu', 'Grospellier', 'Hellmuth', 'Mortensen',
         'Antonius', 'Harman', 'Ungar', 'Dwan', 'Greenstein', 'Chan', 'Moss', 'Ivey', 'Brunson',
         'Reese', 'Esfandiari', 'Juanda', 'Duhamel', 'Gold', 'Cada', 'Mizrachi', 'Schulman',
         'Selbst', 'Duke', 'Rousso', 'Liebert', 'Galfond', 'Elezra', 'Benyamine', 'Booth',
         'DAgostino', 'Eastgate', 'Farha', 'Ferguson', 'Forrest', 'Hansen', 'Hachem', 'Kaplan',
         'Laak', 'Lederer', 'Lindren', 'Matusow', 'Minieri']


def random_names(num):
    """
    Generate a unique list of names from the names module. num specifies how many names.
    """
    nameset = []

    # Make sure all the names are unique
    for i in range(num):
        while True:
            nextname = random.choice(names)
            if nextname not in nameset:
                nameset.append(nextname)
                break
    return nameset


def is_validname(name):
    """
    Returns True if the given name is between 3 and 12 characters long, False otherwise.
    """
    if len(name) < 3 or len(name) > 12:
        return False
    else:
        return True


def has_surr_char(string):
    """
    Returns True if the given string contains any 'surround' characters, False otherwise.
    These characters many cause bugs in programs if used.
    """

    re1 = re.compile(r"[<>()/{}[\]~`^'\\]")
    if re1.search(string):
        #  print ("RE1: Invalid char detected.")
        return True
    else:
        #  print ("RE1: No invalid char detected.")
        return False
