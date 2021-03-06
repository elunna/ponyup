import sqlite3
from ponyup import blinds
from ponyup.table_selection import tables

NAME_FILE = 'data/ponynames.txt'
DB = 'data/game.db'


def mk_tables_table(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS games(name TEXT, game TEXT, seats INTEGER, level INTEGER, stakes TEXT, format TEXT)')

    # Build a database from the existing dictionary.
    for gt in tables:
        stakes = blinds.get_stakes(gt.level)
        cursor.execute("INSERT INTO games VALUES(?, ?, ?, ?, ?, ?)", (gt.tablename, gt.game, gt.seats, gt.level, stakes, 'CASH'))

    conn.commit()


def mk_names_table(cursor, namelist):
    cursor.execute('CREATE TABLE IF NOT EXISTS ponies(name TEXT NOT NULL)')

    for n in namelist:
        cursor.execute("INSERT INTO ponies VALUES(?)", (n, ))

    conn.commit()


def mk_players_table(cursor):
    """
    Make the initial players table for the database.
    """
    c.execute('CREATE TABLE IF NOT EXISTS players(name TEXT NOT NULL, bank INTEGER NOT NULL)')
    conn.commit()


def read_names_from_file():
    names = []
    with open(NAME_FILE) as f:
        for l in f.readlines():
            names.append(l.strip())
    return names


def print_db(cursor, table):
    rows = cursor.execute('SELECT * from {}'.format(table))
    for r in rows:
        print(r)

if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Import the pony-names into the database.
    names = read_names_from_file()
    mk_names_table(c, names)

    # Import the lobby tables into the database.
    mk_tables_table(c)

    # Create an empty players table.
    mk_players_table(c)

    c.close()
    conn.close()
