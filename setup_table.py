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
