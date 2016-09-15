import blinds
import stud
import draw5
import table_factory


def factory(**new_config):
    config = {
        'seats': None,
        'game': None,
        'tablename': 'default',
        'table': None,
        'heroname': None,  # If there is a hero, they will be placed at the hero seat.
        'heroseat': None,
        'level': 0,
        'names': 'bob',
    }
    config.update(new_config)

    # Construct the table
    t = table_factory.factory(
        seats=config['seats'],
        heroname=config['heroname'],
        game=config['game'],
        tablename=config['tablename'],
        names=config['names'],
    )

    if config['game'] == 'FIVE CARD STUD':
        b = blinds.BlindsAnte(config['level'])
        sesh = stud.Stud5Session(config['game'], table=t, blinds=b)

    elif config['game'] == 'FIVE CARD DRAW':
        b = blinds.BlindsNoAnte(config['level'])
        sesh = draw5.Draw5Session(config['game'], table=t, blinds=b)
    else:
        raise ValueError('Game unknown to session!')

    return sesh
