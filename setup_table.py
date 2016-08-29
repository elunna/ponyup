import deck
import names
import player
import player_5card
import table


def make(num, hero=None, gametype="DRAW5"):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    t = table.Table(num)
    nameset = names.random_names(num)

    for i, s in enumerate(t.seats):
        # Always put hero in 0 seat.
        if i == 0 and hero is not None:
            t.add_player(0, player.Player(hero, 'HUMAN'))

        elif nameset[-1] is not None:
            t.add_player(i, player_5card.Player5Card(nameset.pop()))
        else:
            nameset.pop()
    return t


def test_table(seats):
    # Populate a Table of the specified # of seats with players.
    DEFAULT_CHIPS = 1000
    t = table.Table(seats)
    for i in range(seats):
        t.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
        t.seats[i].add_chips(DEFAULT_CHIPS)
    return t


def allin_table(seats):
    # Populates a table with different levels of stack sizes by 100's
    # ex: 100, 200, 300, 400, etc.
    DEFAULT_CHIPS = 100
    t = table.Table(seats)
    for i in range(seats):
        t.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
        t.seats[i].add_chips(DEFAULT_CHIPS * (i + 1))
    return t


def deal_cards(table):
    d = deck.Deck()

    for p in table:
        p.add_card(d.deal())
