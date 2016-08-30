import deck
import names
import player
import player_5card
import pokerhands
import table

STARTINGCHIPS = 1000

HANDS = (pokerhands.royalflush(),
         pokerhands.straightflush_high(),
         pokerhands.boat_high(),
         pokerhands.flush_high(),
         pokerhands.straight_high(),
         pokerhands.set_high()
         )


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
        t.seats[i].chips = STARTINGCHIPS
    return t


def test_table(seats):
    # Populate a Table of the specified # of seats with players.
    # This table doesn't have button or blinds set.
    t = table.Table(seats)

    for i in range(seats):
        t.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
        t.seats[i].add_chips(STARTINGCHIPS)
    return t


def allin_table(seats, REVERSEHANDS=False):
    # Populates a table with different levels of stack sizes by 100's
    # ex: 100, 200, 300, 400, etc.
    DEFAULT_CHIPS = 100
    t = table.Table(seats)
    for i in range(seats):
        t.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
        t.seats[i].add_chips(DEFAULT_CHIPS * (i + 1))

    if REVERSEHANDS is True:
        deal_hands_weakfirst(t)
    else:
        deal_hands_strongfirst(t)
    return t


def deal_cards(table):
    d = deck.Deck()

    for p in table:
        p.add_card(d.deal())


def deal_hands_strongfirst(table):
    # Deal out the hands: strongest first
    for i, s in enumerate(table.seats):
        s._hand.cards = HANDS[i]
        s._hand.update()


def deal_hands_weakfirst(table):
    # Deal out the hands: strongest first
    reversed_hands = list(reversed(HANDS))
    for i, s in enumerate(table.seats):
        s._hand.cards = list(reversed_hands[i])
        s._hand.update()
