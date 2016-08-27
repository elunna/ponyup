import deck
import names
import player
import player_5card
import table


def make(num, hero=None, gametype="DRAW5"):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    t = table.Table(num)
    nameset = names.generate_random_namelist(num)

    for i, s in enumerate(t.seats):
        if i == 0 and hero is not None:
            t.add_player(0, player.Player(hero, 'HUMAN'))

        elif nameset[-1] is not None:
            #  t.add_player(i, player.Player(nameset.pop()))
            t.add_player(i, player_5card.Player5Card(nameset.pop()))
        else:
            nameset.pop()
    return t


def test_table(seats):
    # Populate a Table of the specified # of seats with players.
    t = table.Table(seats)
    for i in range(seats):
        t.add_player(i, player.Player('bob{}'.format(i), 'CPU'))

    for p in t:
        p.add_chips(1000)

    return t

def deal_cards(table):
    d = deck.Deck()

    for p in table:
        p.add_card(d.deal())

