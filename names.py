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
    nameset = []

    # Make sure all the names are unique
    for i in range(num):
        while True:
            nextname = random.choice(names)
            if nextname not in nameset:
                nameset.append(nextname)
                break
    return nameset


def names_with_gaps(num):
    nameset = []
    sparseness = 7

    for i in range(num):
        # 66% chance that a seat will be filled
        # So we can test the gaps/skipping/etc.
        chance = random.randint(0, 10)
        if chance < sparseness:
            # Make sure all the names are unique
            while True:
                nextname = random.choice(names)
                if nextname not in nameset:
                    nameset.append(nextname)
                    break
        else:
            nameset.append(None)
    return nameset


def isValidName(name):
    if len(name) < 3 or len(name) > 12:
        return False
    else:
        return True


def contains_surrounding_chars(username):
    re1 = re.compile(r"[<>/{}[\]~`^'\\]")
    if re1.search(username):
        #  print ("RE1: Invalid char detected.")
        return False
    else:
        #  print ("RE1: No invalid char detected.")
        return True
