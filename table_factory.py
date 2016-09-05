import player
import table
import names

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
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STARTINGCHIPS


class SteppedStackTable(table.Table):
    """
    Creates a table of bobs with stack sizes starting from 100 and increasing in 100's for
    each seat.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STEP * (i + 1)


class Draw5Table(table.Table):
    """
    Creates a table of bobs that are 5 Card Players, and with the default stack size.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player5Card('bob{}'.format(i), None))
            self.seats[i].chips = STARTINGCHIPS


class HeroTable(table.Table):
    """
    Creates a table with the human hero player, and populates the table full of random named
    players. Each player has the default starting stack size.
    """
    def __init__(self, seats, hero, game):
        super().__init__(seats)

        nameset = names.random_names(seats)
        # Add the hero to seat 0
        self.add_player(0, player.Player(hero, 'HUMAN'))

        for i, s in enumerate(self.seats):
            if s is None:
                #  self.add_player(i, player.Player(nameset.pop(), "CPU"))
                newplayer = get_player(nameset.pop(), game)
                self.add_player(i, newplayer)
            else:
                nameset.pop()
            self.seats[i].chips = STARTINGCHIPS


def get_player(name, game):
    if game == "FIVE CARD DRAW":
        return player.Player5Card(name)
    elif game == "FIVE CARD STUD":
        return player.Player5Stud(name)
    elif game is None:
        return player.Player(name, "CPU")


def change_playertypes(table, playertype):
    for p in table:
        if p.playertype == "HUMAN":
            pass
        else:
            p.playertype = playertype
