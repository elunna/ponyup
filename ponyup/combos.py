"""
  " Tools for getting combinations and permutations of poker cards
  """
import itertools


def n_choose_k(n, k):
    """ Returns how many combos of k are in a group of n.  """
    if n <= 0 or k <= 0:
        raise ValueError('N or K passed is less than or equal to 0!')
    elif k > n:
        raise ValueError('Pick is larger than quantity of objects!')

    numerator = [x for x in range(1, n + 1)]

    diff = n - k
    denominator = [x for x in range(1, diff + 1)]
    denominator.extend([x for x in range(1, k + 1)])

    dups = list(set(numerator) & set(denominator))
    for d in dups:
        numerator.remove(d)
        denominator.remove(d)

    numproduct, denproduct = 1, 1
    for n in numerator:
        numproduct *= n

    for n in denominator:
        denproduct *= n

    return int(numproduct / denproduct)


def get_combolist(cards, n):
    """ Takes a list and returns a list of all the combinations of size n """
    return list(itertools.combinations(cards, n))


def get_allcombos(items):
    """ Returns all combos of all possible sizes in the given list.  """
    combos = []
    maxsize = len(items) + 1
    for i in range(1, maxsize):
        for c in list(get_combolist(items, i)):
            combos.append(c)
    return combos
