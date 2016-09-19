from collections import namedtuple
import blinds
import sqlite3

"""
This lobby listing is a list of all the available cash tables a pony can play
at. Each has: Table name, seats, stakes level, game type.
"""
Game = namedtuple('Game', ['tablename', 'seats', 'level', 'stakes', 'game', 'format'])
DEFAULT_TABLE = 'Wonderbolt Academy'
DB = 'lobby.db'


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


def default():
    return DEFAULT_TABLE


def available_games(L):
    gamelist = set([g.game for g in L])
    return list(gamelist)


def get_game(L, game):
    return [x for x in L if x.game == game]


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
        _str += (fmt_str.format(i, gt.game.title(), gt.seats, blinds.get_stakes(gt.level),
                                gt.tablename))
    return _str
