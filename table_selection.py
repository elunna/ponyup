import blinds
import sqlite3
from games import Game

# TABLENAME | TABLE SIZE | STAKES | GAME
tables = (
    # Headsup
    Game('Twilight\'s Balloon', seats=2, level=1, game="FIVE CARD DRAW"),
    Game('Apple Acres', seats=2, level=2, game="FIVE CARD DRAW"),
    Game('Rainbow Dash\'s House', seats=2, level=3, game="FIVE CARD DRAW"),
    Game('Ponyville Tower', seats=2, level=4, game="FIVE CARD DRAW"),
    Game('Zecora\'s Hut', seats=2, level=5, game="FIVE CARD DRAW"),
    Game('Rainbow Factory', seats=2, level=6, game="FIVE CARD DRAW"),
    Game('Trixie\'s Wagon', seats=2, level=7, game="FIVE CARD DRAW"),

    # 3max
    Game('Fluttershy\'s cottage', seats=3, level=1, game="FIVE CARD DRAW"),
    Game('Twilight\'s Lab', seats=3, level=2, game="FIVE CARD DRAW"),
    Game('Quills and Sofas', seats=3, level=3, game="FIVE CARD DRAW"),
    Game('CMC Clubhouse', seats=3, level=4, game="FIVE CARD DRAW"),
    Game('Mr. Breezy\'s Fan shop', seats=3, level=5, game="FIVE CARD DRAW"),
    Game('Wonderbolt Academy', seats=3, level=6, game="FIVE CARD DRAW"),
    Game('Mirror Pool', seats=3, level=7, game="FIVE CARD DRAW"),

    # 6max
    Game('Golden Oak Library', seats=6, level=1, game="FIVE CARD DRAW"),
    Game('Carousel Boutique', seats=6, level=2, game="FIVE CARD DRAW"),
    Game('Ponyville Schoolhouse', seats=6, level=3, game="FIVE CARD DRAW"),
    Game('Sugarcube Corner', seats=6, level=4, game="FIVE CARD DRAW"),
    Game('Pinkie\'s Party Cave', seats=6, level=5, game="FIVE CARD DRAW"),
    Game('Cutie Map', seats=6, level=6, game="FIVE CARD DRAW"),


    # ### 5-card stud
    # HU
    Game('Everfree Forest', seats=2, level=1, game="FIVE CARD STUD"),
    Game('White Tail Woods', seats=2, level=2, game="FIVE CARD STUD"),
    Game('Galloping Gorge', seats=2, level=3, game="FIVE CARD STUD"),
    Game('Mount Everhoof', seats=2, level=4, game="FIVE CARD STUD"),
    Game('Ghastly Gorge', seats=2, level=5, game="FIVE CARD STUD"),
    Game('Froggy Bottom Bogg', seats=2, level=6, game="FIVE CARD STUD"),
    Game('Dragon Lands', seats=2, level=7, game="FIVE CARD STUD"),

    # 3max
    Game('Saddle Lake', seats=3, level=1, game="FIVE CARD STUD"),
    Game('Raket Range', seats=3, level=2, game="FIVE CARD STUD"),
    Game('Friffish Islaes', seats=3, level=3, game="FIVE CARD STUD"),
    Game('Unicorn Range', seats=3, level=4, game="FIVE CARD STUD"),
    Game('Crystal Mountains', seats=3, level=5, game="FIVE CARD STUD"),
    Game('Hollow Shades', seats=3, level=6, game="FIVE CARD STUD"),

    # 6max
    Game('Horseshoe Bay', seats=6, level=1, game="FIVE CARD STUD"),
    Game('San Palomino Desert', seats=6, level=2, game="FIVE CARD STUD"),
    Game('Dragon Lands', seats=6, level=3, game="FIVE CARD STUD"),
    Game('Winsome Falls', seats=6, level=4, game="FIVE CARD STUD"),
    Game('Dodge Junction', seats=6, level=5, game="FIVE CARD STUD"),
    Game('Tenochtitlan Basin', seats=6, level=6, game="FIVE CARD STUD"),
    Game('Tartarus', seats=6, level=7, game="FIVE CARD STUD"),
)

# 'CMC Clubhouse' in [n.name for n in l]


def make_db():
    conn = sqlite3.connect('lobby.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS games(name TEXT, game TEXT, seats INTEGER, level INTEGER, stakes TEXT, format TEXT)')

    # Build a database from the existing dictionary.
    for g in tables:
        stakes = blinds.get_stakes(g.level)
        c.execute("INSERT INTO games VALUES(?, ?, ?, ?, ?, ?)", (g.tablename, g.game, g.seats, g.level, stakes, 'CASH'))

    # Anytime we change something, we need to commit to save.
    conn.commit()
    c.close()
    conn.close()

if __name__ == "__main__":
    make_db()
