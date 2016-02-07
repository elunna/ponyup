import deck
import table
import player
import random


def dealhand(quantity):
    # Deal a regular 5 card hand from a new deck
    d = deck.Deck()
    d.shuffle()
    return [d.deal() for i in range(quantity)]


def deal_players(players, deck, qty):
    """
    Take a list of Players and their Deck. Deals qty hands to each.
    """

    # Check that the requirements of the players and handsizes don't over deplete the deck
    if len(players) * qty > len(deck):
        print('The required players and hand sizes would deplete the deck below negative!')
        return ValueError()

    for i in range(qty):
        for p in players:
            p._hand.add(deck.deal())

    # Verify hand sizes
    for p in players:
        if not len(p._hand) == qty:
            print('Corrupt player decks, uneven starting numbers.')
            return False
    return True


def setup_test_table(num, hero=None):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    names = ['Seidel', 'Doyle', 'Mercier', 'Negreanu', 'Grospellier', 'Hellmuth', 'Mortensen',
             'Antonius', 'Harman', 'Ungar', 'Dwan', 'Greenstein', 'Chan', 'Moss', 'Ivey',
             'Brunson', 'Reese', 'Esfandiari', 'Juanda', 'Duhamel', 'Gold', 'Cada', 'Mizrachi',
             'Schulman', 'Selbst', 'Duke', 'Rousso', 'Liebert', 'Galfond', 'Elezra',
             'Benyamine', 'Booth', 'D Agostino', 'Eastgate', 'Farha', 'Ferguson', 'Forrest',
             'Hansen', 'Hachem', 'Kaplan', 'Laak', 'Lederer', 'Lindren', 'Matusow', 'Minieri']

    t = table.Table(num)

    nameset = []
    for i in range(num):
        #  t.add_player(i, player.Player(names.pop()))

        # Make sure all the names are unique
        while True:
            nextname = random.choice(names)
            if nextname not in nameset:
                nameset.append(nextname)
                break

    for i, n in enumerate(nameset):
        if i == 0 and hero is not None:
            t.add_player(0, player.Player(hero, 'HUMAN'))
        t.add_player(i, player.Player(n, 'CPU'))

    return t


if __name__ == "__main__":
    # Tests
    print('Testing table setup')
    t = setup_test_table(2)
    print(t)

    t = setup_test_table(6)
    print(t)

    t = setup_test_table(9)
    print(t)

    t = setup_test_table(10)
    print(t)

    print('#'*80)
    print('Testing table get_players')
    print('Setting a random button')
    t.randomize_button()
    #  p = t.get_players()
    #  print_playerlist(p)
    print(t)

    t.remove_player(0)
    t.remove_player(1)
    print(t)

    print('Next player from 0: {}'.format(t.next(0)))
    print('Next player from 2: {}'.format(t.next(2)))

    t.remove_player(3)
    t.remove_player(5)
    print(t)

    print('Next player from 2: {}'.format(t.next(2)))
    print('Next player from 9: {}'.format(t.next(9)))

    print('#'*80)
    print('testing the button movement')
    for i in range(10):
        t.move_button()
        print(t)

    print('Testing deal_players')
    playertable = setup_test_table(6)
    d = deck.Deck()
    print(playertable)
    print('The tables players: {}'.format(playertable.get_players()))
    print('dealing cards')
    deal_players(playertable.get_players(), d, 5)
    print('Deck size: {}'.format(len(d)))
    print(playertable)
