import blinds
import session_stud5
import session_draw5
import table_factory


def make(gametuple, name):
    t = table_factory.factory(seats=gametuple.seats, heroname=name, game=gametuple.game)

    if gametuple.game == "FIVE CARD DRAW":
        NOANTE = blinds.BlindsNoAnte(gametuple.level)
        t.randomize_button()
        g = session_draw5.Draw5Session(gametuple.game, t, NOANTE, label=gametuple.name)
        return g

    elif gametuple.game == "FIVE CARD STUD":
        ANTE = blinds.BlindsAnte(gametuple.level)
        return session_stud5.Stud5Session(gametuple.game, t, ANTE, label=gametuple.name)


def draw5_session(level, players=6):
    """
    Create a table of 6 draw5 players with default starting stacks.
    """
    STAKES = blinds.BlindsNoAnte(level)

    t = table_factory.factory(seats=players, game="FIVE CARD DRAW")
    return session_draw5.Draw5Session('FIVE CARD DRAW', t, STAKES)


def stud5_session(level, players=6):
    """
    Create a table of 6 draw5 players with default starting stacks.
    """
    STAKES = blinds.BlindsAnte(level)
    t = table_factory.factory(seats=players, game="FIVE CARD STUD")

    return session_stud5.Stud5Session('FIVE CARD STUD', t, STAKES)
