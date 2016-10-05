import sqlite3
from ponyup import logger
from ponyup import player

_logger = logger.get_logger(__name__)
DB = 'data/game.db'


def load_player(name):
    """
    Gets the username, checks for any previous player info and loads the player. Returns a
    Player object.
    """
    _logger.debug('Attempting to load player from sqlite3 database.')
    p = player_exists(name)
    if p:
        p = player.Player(*p)
        _logger.debug('Loaded player {}'.format(p))
        _logger.debug('Bank: {}'.format(p.bank))
    else:
        _logger.info('Player {} not found'.format(name))
    return p


def new_player(name):
    _logger.debug('Attempting to create new player in sqlite3 database.')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    p = player_exists(name)
    result = False
    if p:
        _logger.info('Player already exists in database!')
    else:
        c.execute('INSERT INTO players VALUES("{}",{})'.format(name, player.HUMAN_BANK_BITS))
        _logger.info('Created new player {}'.format(name))
        result = True

    conn.commit()
    c.close()
    conn.close()
    return result


def save_player(plyr):
    """
    Saves the Player current stats to the database.
    """
    _logger.debug('Attempting to update player info in sqlite3 database.')
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    conn.commit()
    c.close()
    conn.close()


def player_exists(name):
    _logger.debug('Checking if a player exists in the sqlite3 database.')
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute('SELECT * FROM players WHERE name=("{}")'.format(name))
    names = [(r[0], r[1]) for r in rows]
    result = False

    if len(names) == 0:
        _logger.debug('Player {} not in database.'.format(name))
    elif len(names) > 1:
        _logger.error('Player has more than one entry in the database!')
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
    _logger.debug('Querying sqlite3 database for all players.')
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    names = [n for n in c.execute('SELECT * FROM players')]

    c.close()
    conn.close()
    return names


def del_player(name):
    _logger.debug('Attempting to delete a player from the sqlite3 database.')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    result = False
    if player_exists(name):
        c.execute('DELETE FROM players WHERE name = "{}"'.format(name))
        _logger.info('Player {} deleted.'.format(name))
        result = True
    else:
        _logger.debug('Player {} not found in database.'.format(name))

    conn.commit()
    c.close()
    conn.close()
    return result
