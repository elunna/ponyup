import blinds
import stud
import draw5
import table_factory


def make(gametuple, name):
    t = table_factory.factory(
        seats=gametuple.seats,
        heroname=name,
        game=gametuple.game
    )

    if gametuple.game == "FIVE CARD DRAW":
        NOANTE = blinds.BlindsNoAnte(gametuple.level)
        t.randomize_button()
        g = draw5.Draw5Session(
            gametuple.game, t, NOANTE, label=gametuple.name
        )
        return g

    elif gametuple.game == "FIVE CARD STUD":
        ANTE = blinds.BlindsAnte(gametuple.level)

        return stud.Stud5Session(
            gametuple.game, t, ANTE, label=gametuple.name
        )


def factory(**new_config):
    config = {
        'seats': None,
        'game': None,
        'tablename': 'default',
        'table': None,
        'heroname': None,  # If there is a hero, they will be placed at the hero seat.
        'heroseat': None,
        'blindlvl': 0,
    }
    config.update(new_config)

    # Construct the table
    t = table_factory.factory(
        seats=config['seats'],
        heroname=config['heroname'],
        game=config['game'],
        tablename=config['tablename']
    )

    if config['game'] == 'FIVE CARD STUD':
        b = blinds.BlindsAnte(config['blindlvl'])
        sesh = stud.Stud5Session(config['game'], t, b)

    elif config['game'] == 'FIVE CARD DRAW':
        b = blinds.BlindsNoAnte(config['blindlvl'])
        sesh = draw5.Draw5Session(config['game'], t, b)
    else:
        raise ValueError('Game unknown to session!')

    return sesh
