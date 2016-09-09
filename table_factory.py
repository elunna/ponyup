import player
import table
import names

DEPOSIT = 10000
STARTINGCHIPS = 1000
STEP = 100


class BobTable(table.Table):
    """
    Creates a table of generic Player objects named bob0, bob1, bob2, etc... with the default
    chip stack.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            s.sitdown(player.Player('bob{}'.format(i), 'CPU'))
            s.player.deposit(DEPOSIT)
            s.buy_chips(STARTINGCHIPS)


class SteppedStackTable(table.Table):
    """
    Creates a table of bobs with stack sizes starting from 100 and increasing in 100's for
    each seat.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            s.sitdown(player.Player('bob{}'.format(i), 'CPU'))
            s.player.deposit(DEPOSIT)
            s.buy_chips(STEP * (i + 1))


class Draw5Table(table.Table):
    """
    Creates a table of bobs that are 5 Card Players, and with the default stack size.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            s.sitdown(player.Player5Card('bob{}'.format(i), None))
            s.player.deposit(DEPOSIT)
            s.buy_chips(STARTINGCHIPS)


class Stud5Table(table.Table):
    """
    Creates a table of bobs that are 5 Card Players, and with the default stack size.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            s.sitdown(player.Player5Stud('bob{}'.format(i), None))
            s.player.deposit(DEPOSIT)
            s.buy_chips(STARTINGCHIPS)


class HeroTable(table.Table):
    """
    Creates a table with the human hero player, and populates the table full of random named
    players. Each player has the default starting stack size.
    """
    def __init__(self, seats, hero, game):
        super().__init__(seats)

        nameset = names.random_names(seats)
        # Add the hero to seat 0
        self.seats[0].sitdown(player.Player(hero, 'HUMAN'))
        self.seats[0].player.deposit(DEPOSIT)

        for i, s in enumerate(self.seats):
            if s.is_empty():
                newplayer = player_factory(game, nameset.pop())
                s.sitdown(newplayer)
            else:
                nameset.pop()

            s.player.deposit(DEPOSIT)
            s.buy_chips(STARTINGCHIPS)


def change_playertypes(table, playertype):
    for p in table:
        if p.playertype == "HUMAN":
            pass
        else:
            p.playertype = playertype


def player_factory(game, name, playertype=None):
    if game == "FIVE CARD DRAW":
        p = player.Player5Card(name, playertype)
    elif game == "FIVE CARD STUD":
        p = player.Player5Stud(name, playertype)
    elif game is None:
        p = player.Player(name, playertype="CPU")

    return p
