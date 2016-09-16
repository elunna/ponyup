import pickle

PONYPICKLE = 'data/ponynames.dat'
PONYNAMES = 'ponynames.txt'


def read_ponynames():
    names = []
    with open(PONYNAMES) as f:
        for l in f.readlines():
            names.append(l.strip())
    return names


def pickle_names(namelist):
    try:
        with open(PONYPICKLE, 'wb') as f:
            pickle.dump(namelist, f)
    except IOError:
        print('An error occurred while writing, aborting program!')


def unpickle_names():
    """
    Gets the username, checks for any previous player info and loads the player. If no player
    file it creates a new one. Returns a Player object.
    """
    try:
        with open(PONYPICKLE, 'rb') as f:
            namelist = pickle.load(f)
            return namelist

    except IOError:
        print('No info found for {}'.format(PONYPICKLE))


if __name__ == "__main__":
    print('testing the reading....\n\n')
    n = read_ponynames()

    print('testing writing....\n\n')
    pickle_names(n)

    print('testing unpickling ....\n\n')
    mynames = unpickle_names()
    print('testing the reading - post pickling....\n\n')
    print('len of mynames = {}'.format(len(mynames)))
    print(mynames)
