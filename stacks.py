# Stack sizes module


def largest(table):
    """
    Return the largest stack size at the table.
    """
    return max(stacklist(table))


def smallest(table):
    """
    Return the smallest stack size at the table.
    """
    return min(stacklist(table))


def average(table):
    """
    Return the average stack size at the table.
    """
    _stacks = stacklist(table)
    return sum(_stacks) / len(_stacks)


def effective(table):
    """
    Return the effetive stack size at the table. (Note: It's also the smallest.
    """
    return smallest(table)


def stacklist(table):
    """
    Returns a list of all the stack sizes.
    """
    return [p.chips for p in table]
