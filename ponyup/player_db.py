"""
  " Manages the player database so we can save and load human players.
  """
import sqlite3
from ponyup import names
from ponyup import player

DB = 'data/game.db'


def new_player(name):
    """ Create new player in sqlite3 database """
    if not names.is_validname(name):
        return False

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    p = load_player(name)
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


def load_player(name):
    """ Gets the username, checks for any previous player info and loads the
        player. Returns a Player object.
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute('SELECT * FROM players WHERE name=("{}")'.format(name))
    players = [(r[0], r[1]) for r in rows]

    if len(players) == 0:
        result = False
    elif len(players) > 1:
        raise Exception('Player has more than one entry in the database!')
    else:
        p = players[0]
        result = player.Player(
            name=p[0],
            bank=p[1],
            playertype="HUMAN"
        )

    c.close()
    conn.close()
    return result


def get_players():
    """ Get a list of all players from the database. """
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    players = [n for n in c.execute('SELECT * FROM players')]

    c.close()
    conn.close()
    return players


def del_player(name):
    """ Removes a player from the database. """
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    result = False
    if load_player(name):
        c.execute('DELETE FROM players WHERE name = "{}"'.format(name))
        result = True

    conn.commit()
    c.close()
    conn.close()
    return result
