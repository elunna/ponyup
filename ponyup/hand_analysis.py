"""
  " Analysis of all possible hands in a regular card deck.
  """
import pickle
from ponyup import combos
from ponyup import deck
from ponyup import evaluator


def typecount_dict(handlist):
    """
    Takes in a list of hands and counts all the occurences of each type of hand and tallies
    it up in a dictionary. Returns the dictionary.
    """
    type_count = {}

    for c in handlist:
        v = evaluator.get_value(c)
        t = evaluator.get_type(v)
        #  h = hand.Hand(c)
        #  rank = h.rank()
        if t not in type_count:
            type_count[t] = 1
        else:
            type_count[t] += 1

    return type_count


def get_unique_5cardhands(combolist):
    """
    Filters out all the hands that have the same value so we can see how many unique values
    there are.
    """
    hands = {}

    # Run through all combinations of 5 card hands
    for c in combolist:
        #  h = hand.Hand(c)
        v = evaluator.get_value(c)
        #  hands[h.value()] = h
        hands[v] = c

    return len(hands)


def sort_handslist(handdict):
    """
    Takes a list of Hands and returns a list sorted by value.
    """
    sortedhands = []
    for h in handdict:
        sortedhands.append((handdict[h].value(), handdict[h].rank(), handdict[h].cards))

    return sorted(sortedhands)


def print_unique_5cardhands(handlist):
    for h in handlist:
        print('{:<15}{:<15}{:<15}'.format(
            h[0], h[1], evaluator.print_cardlist(h[2])))


def count_all_handtypes(combolist):
    print('')
    print('Counting all the hand types in the list of {} hands.'.format(len(combosof5)))
    type_count = typecount_dict(combolist)

    print('Results:')
    for t in type_count:
        print('{}: {}'.format(t, type_count[t]))


def enumerate_unique_5cardhands(combolist):
    print('Enumerating unique 5-card hands by value')
    unique_hands = get_unique_5cardhands(combolist)
    sortedhands = sort_handslist(unique_hands)
    print_unique_5cardhands(sortedhands)


def write_handcombos(combolist):
    print('Enumerating unique 5-card hands by value')
    unique_hands = get_unique_5cardhands(combolist)

    with open('handcombos.dat', 'wb') as db:
        pickle.dump(unique_hands, db)


if __name__ == "__main__":
    d = deck.Deck()

    print('Counting all 5 card hands in a deck')
    combosof5 = combos.get_combolist(d.cards, 5)
    print('Combos counted.')
    print('There are {} combos of 5 in a standard deck.'.format(len(combosof5)))

    # Reuse the combolist

    count_all_handtypes(combosof5)

    enumerate_unique_5cardhands(combosof5)
