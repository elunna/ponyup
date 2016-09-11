import blinds
import session_stud5
import session_draw5
import table_factory


def make(gametuple, name):
    t = table_factory.HeroTable(gametuple.seats, name, gametuple.game)

    if gametuple.game == "FIVE CARD DRAW":
        NOANTE = blinds.BlindsNoAnte(gametuple.level)
        t.randomize_button()
        g = session_draw5.Draw5Session(gametuple.game, t, NOANTE)
        return g

    elif gametuple.game == "FIVE CARD STUD":
        ANTE = blinds.BlindsAnte(gametuple.level)
        return session_stud5.Stud5Session(gametuple.game, t, ANTE)


def draw5_session(level, players=6):
    """
    Create a table of 6 draw5 players with default starting stacks.
    """
    STAKES = blinds.BlindsNoAnte(level)
    table = table_factory.Draw5Table(players)
    return session_draw5.Draw5Session('FIVE CARD DRAW', table, STAKES)


def stud5_session(level, players=6):
    """
    Create a table of 6 draw5 players with default starting stacks.
    """
    STAKES = blinds.BlindsAnte(level)
    table = table_factory.Stud5Table(players)
    return session_stud5.Stud5Session('FIVE CARD STUD', table, STAKES)
