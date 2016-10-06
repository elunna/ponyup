from collections import namedtuple
import sqlite3

"""
This lobby listing is a list of all the available cash tables a pony can play
at. Each has: Table name, seats, stakes level, game type.
"""
Game = namedtuple('Game', ['tablename', 'game', 'seats', 'level', 'stakes',  'format'])
DB = 'data/game.db'


class Lobby():
    def __init__(self):
        # Import the database to Game namedtuples
        self.conn = sqlite3.connect(DB)
        self.c = self.conn.cursor()

    def shutdown(self):
        self.c.close()
        self.conn.close()

    def get_game(self, name):
        for t in self.all_tables():
            if t.tablename == name:
                return t
        else:
            return None

    def all_tables(self):
        return [Game(*g) for g in self.c.execute('SELECT * FROM games')]

    def get_gametypes(self):
        return list(set([t.game for t in self.all_tables()]))

    def filter_by_game(self, game):
        games = self.c.execute('SELECT * FROM games WHERE game="{}"'.format(game))
        return [Game(*g) for g in games]

    def filter_by_seats(self, seats):
        games = self.c.execute('SELECT * FROM games WHERE seats={}'.format(seats))
        return [Game(*g) for g in games]

    def filter_by_level(self, level):
        games = self.c.execute('SELECT * FROM games WHERE level={}'.format(level))
        return [Game(*g) for g in games]

    def filter_by_stakes(self, stakes):
        games = self.c.execute('SELECT * FROM games WHERE stakes="{}"'.format(stakes))
        return [Game(*g) for g in games]

    def filter_by_format(self, format):
        games = self.c.execute('SELECT * FROM games WHERE format="{}"'.format(format))
        return [Game(*g) for g in games]


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
