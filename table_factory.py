import table
import random
import session_factory

DEF_STACK = 1000
DEFAULT_BB = 100
STEP = 100


def factory(**new_config):
    config = {
        'seats': None,
        'tablename': 'default',
        'playerpool': None,
        'heroseat': None,
        'stack': DEF_STACK,
        'stepstacks': False,
        'variance': None,   # A percentage that the stack size can randomly vary.
        'remove': None,
        'bb': None
    }
    config.update(new_config)

    tbl = table.Table(config['seats'])
    tbl.name = config['tablename']

    # If playerpool is none, use a default playerpool.
    if config['playerpool'] is None:
        pool = session_factory.make_playerpool(quantity=10)

    elif len(config['playerpool']) < config['seats']:
        raise Exception('The playerpool doesn\'t have another players to cover the table!')
    else:
        pool = config['playerpool']

    # Fund and Seat the players
    for i, s in enumerate(tbl):
        if i == config['heroseat']:
            continue  # Save this seat for the hero.
        s.sitdown(pool.pop(0))

    # Players buyin to the table.
    # There are a few different ways to set stack sizes.
    # - There is a DEF_STACK value for a default.
    # - stack parameter sets the stack amount.
    # - There is a stepstacks bool to trigger stacksizes as a stepped 100, 200, 300, pattern.
    # - There is a BBs parameter passed as a (BB size, BB quantity) pair to set stacks to the
    #    commonly measured units of big blinds.
    # - There is a stackvariation parameter to randomly vary the sizes of the stacks. The
    #   parameter is a float value that is used to randomly calculate the variations.

    # *** Player buyins ***
    # Go through all the seats
    for i, s in enumerate(tbl):
        # Check if the seat is occupied or vacant.
        if s.vacant():
            continue

        # Buy chips based on the parameter preference
        if config['stepstacks']:
            s.buy_chips(STEP * (i + 1))
        elif config['stack']:
            s.buy_chips(config['stack'])
        else:
            s.buy_chips(DEF_STACK)

        # Random variations
        if config['variance']:
            hilimit = int(s.stack * config['variance'])
            offset = random.randint(-hilimit, hilimit)
            s.stack -= offset

    # Removes a player from the table, if specified.
    if config['remove'] is not None:
        tbl.pop(config['remove'])

    return tbl
