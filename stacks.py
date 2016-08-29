# Stack sizes module


def largest(table):
    """ Return the largest stack size at the table."""
    pass


def smallest(table):
    """ Return the smallest stack size at the table."""
    pass


def average(table):
    """ Return the average stack size at the table."""
    pass


def effective(table):
    """ Return the effetive stack size at the table. (Note: It's also the smallest."""
    pass


def stacklist(table):
    """ Returns a list of all the stack sizes. """
    return [p.chips for p in table]


def stackdict(table):
    """ Returns a name/stacksize dictionary for each player at the table. """
    stacks = {}
    for p in table:
        stacks[p.name] = p.chips
    return stacks
