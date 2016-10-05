import sqlite3
from ponyup import player

DB = 'data/game.db'


def load_player(name):
    """
    Gets the username, checks for any previous player info and loads the player. Returns a
    Player object.
    """
    p = player_exists(name)
    if p:
        p = player.Player(*p)
        print('Loaded player {}'.format(p))
    else:
        print('player not found')
        p = None
    return p


def new_player(name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    p = player_exists(name)
    if p:
        print('Player already exists in database!')
        return False
    else:
        c.execute('INSERT INTO players VALUES("{}",{})'.format(name, player.HUMAN_BANK_BITS))
        print('Created new player {}'.format(name))
        return True

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
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute('SELECT * FROM players WHERE name=("{}")'.format(name))
    names = [(r[0], r[1]) for r in rows]

    result = False
    if len(names) == 0:
        print('Player not in database.')
    elif len(names) > 1:
        raise Exception('Player has more than one entry in the database!')
    else:
        result = names[0]

    c.close()
    conn.close()
    return result


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
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if player_exists(name):
        c.execute('DELETE FROM players WHERE name = "{}"'.format(name))
        print('Player {} deleted.'.format(name))
        return True
    else:
        print('Player not found in database.')
        return False

    conn.commit()
    c.close()
    conn.close()
