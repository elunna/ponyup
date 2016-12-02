"""
  " Manages the player database so we can save and load human players.
  """
import sqlite3
from ponyup import player

DB = 'data/game.db'


def load_player(name):
    """ Gets the username, checks for any previous player info and loads the
        player. Returns a Player object.
    """
    p = player_exists(name)
    if p:
        p = player.Player(name=p[0], bank=p[1], playertype="HUMAN")
    return p


def new_player(name):
    """ Create new player in sqlite3 database """
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    p = player_exists(name)
    result = False
    if not p:
        c.execute('INSERT INTO players VALUES("{}",{})'.format(name, player.HUMAN_BANK_BITS))
        result = True

    conn.commit()
    c.close()
    conn.close()
    return result


def update_player(plyr):
    """ Saves the Player current stats to the database. """
    if plyr:
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute('UPDATE players SET bank = {} WHERE name = "{}"'.format(plyr.bank, plyr.name))
        conn.commit()
        c.close()
        conn.close()
        return True
    else:
        return False


def player_exists(name):
    """ Checks if a player exists in the sqlite3 database. """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute('SELECT * FROM players WHERE name=("{}")'.format(name))
    names = [(r[0], r[1]) for r in rows]
    result = False

    if len(names) > 1:
        raise Exception('Player has more than one entry in the database!')
    else:
        result = names[0]

    c.close()
    conn.close()
    return result


def get_players():
    """ Get a list of all players from the database. """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    names = [n for n in c.execute('SELECT * FROM players')]

    c.close()
    conn.close()
    return names


def del_player(name):
    """ Removes a player from the database. """
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    result = False
    if player_exists(name):
        c.execute('DELETE FROM players WHERE name = "{}"'.format(name))
        result = True

    conn.commit()
    c.close()
    conn.close()
    return result
