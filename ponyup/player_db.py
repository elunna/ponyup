import sqlite3
from ponyup import player

DB = 'data/game.db'


def load_player(name):
    """
    Gets the username, checks for any previous player info and loads the player. Returns a
    Player object.
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute('SELECT * FROM players WHERE name=("{}")'.format(name))
    players = [(r[0], r[1]) for r in rows]

    if players:
        p = player.Player(*players[0])
        print('Loaded player {}'.format(p))
    else:
        print('player not found')
        p = None

    c.close()
    conn.close()
    return p


def new_player(name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if player_exists(name):
        print('Player already exists in database!')
    else:
        try:
            c.execute('INSERT INTO players VALUES("{}",{})'.format(name, player.HUMAN_BANK_BITS))
            #  c.execute("INSERT INTO players VALUES(?,?)", (name, player.HUMAN_BANK_BITS, ))
        except ValueError:
            pass

    conn.commit()
    c.close()
    conn.close()


def save_player(plyr):
    """
    Saves the Player current stats to the database.
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    conn.commit()
    c.close()
    conn.close()


def player_exists(name):
    pass


def get_players():
    """
    Get a list of all players from the database.
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    names = [n for n in c.execute('SELECT * FROM players')]

    c.close()
    conn.close()
    return names


def del_player(name):
    pass
