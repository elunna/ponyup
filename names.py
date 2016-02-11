import random

names = ['Seidel', 'Doyle', 'Mercier', 'Negreanu', 'Grospellier', 'Hellmuth', 'Mortensen',
         'Antonius', 'Harman', 'Ungar', 'Dwan', 'Greenstein', 'Chan', 'Moss', 'Ivey', 'Brunson',
         'Reese', 'Esfandiari', 'Juanda', 'Duhamel', 'Gold', 'Cada', 'Mizrachi', 'Schulman',
         'Selbst', 'Duke', 'Rousso', 'Liebert', 'Galfond', 'Elezra', 'Benyamine', 'Booth',
         'DAgostino', 'Eastgate', 'Farha', 'Ferguson', 'Forrest', 'Hansen', 'Hachem', 'Kaplan',
         'Laak', 'Lederer', 'Lindren', 'Matusow', 'Minieri']


def generate_random_namelist(num, full=True):
    nameset = []
    if full is True:
        sparseness = 10
    else:
        sparseness = 7

    for i in range(num):
        # We'll use a 66% chance that a seat will be filled
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
