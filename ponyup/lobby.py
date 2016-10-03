from collections import namedtuple
import sqlite3

"""
This lobby listing is a list of all the available cash tables a pony can play
at. Each has: Table name, seats, stakes level, game type.
"""
Game = namedtuple('Game', ['tablename', 'game', 'seats', 'level', 'stakes',  'format'])
DEFAULT_TABLE = 'Twilight\'s Lab'
DB = 'data/lobby.db'


class Lobby():
    def __init__(self):
        # Import the database to Game namedtuples
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        self.tables = []
        games = c.execute('SELECT * from games')
        for g in games:
            self.tables.append(Game(*g))
        c.close()
        conn.close()

    def default(self):
        for t in self.tables:
            if t.tablename == DEFAULT_TABLE:
                return t
        else:
            return None

    def available_games(self):
        return list(set([g.game for g in self.tables]))

    def get_game(self, game):
        return [x for x in self.tables if x.game == game]


def sort_by_name(L):
    return sorted(L, key=lambda x: x.tablename)


def sort_by_stakes(L):
    return sorted(L, key=lambda x: x.level)


def sort_by_seats(L):
    return sorted(L, key=lambda x: x.seats)


def numbered_list(L):
    _str = ''
    fmt_str = '{:<8}{:20}{:<8}{:12}{:25}\n'
    print(fmt_str.format('Pick#', 'Game', 'Seats', 'Stakes', 'Table Name'))

    for i, gt in enumerate(L):
        _str += (fmt_str.format(i, gt.game.title(), gt.seats, gt.stakes, gt.tablename))
    return _str
