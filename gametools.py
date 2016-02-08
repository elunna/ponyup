import deck
import table
#  import player
#  import random


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


if __name__ == "__main__":
    # Tests
    print('Testing table setup')
    t = table.setup_test_table(2)
    print(t)

    t = table.setup_test_table(6)
    print(t)

    t = table.setup_test_table(9)
    print(t)

    t = table.setup_test_table(10)
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
    playertable = table.setup_test_table(6)
    d = deck.Deck()
    print(playertable)
    print('The tables players: {}'.format(playertable.get_players()))
    print('dealing cards')
    deal_players(playertable.get_players(), d, 5)
    print('Deck size: {}'.format(len(d)))
    print(playertable)
