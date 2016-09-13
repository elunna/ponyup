import player
import table
import names
import random

DEPOSIT = 10000
DEF_STACK = 1000
STEP = 100


def factory(**new_config):
    config = {
        'seats': 6,
        'game': None,
        'tablename': 'default',
        'types': None,  # Player types
        'names': 'bob',  # Player names, can be 'random'
        'heroname': None,  # If there is a hero, they will be placed at the hero seat.
        'heroseat': 0,
        'deposit': DEPOSIT,
        'stack': DEF_STACK,
        'stepstacks': False,
        'variance': None  # A percentage that the stack size can randomly vary.
    }

    config.update(new_config)
    SEATS = config['seats']
    t = table.Table(SEATS)

    # Create a list of players
    if config['names'] == 'random':
        # Generate random names
        nameset = names.random_names(SEATS)
    else:
        nameset = [config['names'] + str(i) for i in range(SEATS)]

    # Create and place the hero player.
    if config['heroname']:
        hero = player.Player(config['heroname'])
        hero.deposit(config['deposit'])
        heroseat = t.seats[config['heroseat']]
        heroseat.sitdown(hero)

    # Fund and Seat the players
    for i, s in enumerate(t):
        if not s.is_empty():
            continue  # Save this seat for the hero.
        p = player.factory(nameset[i], config['game'], config['types'])

        p.deposit(config['deposit'])
        s.sitdown(p)

    # Players buyin to the table.
    # There are a few different ways to set stack sizes.
    # - There is a DEF_STACK value for a default.
    # - stack parameter sets the stack amount.
    # - There is a stepstacks bool to trigger stacksizes as a stepped 100, 200, 300, pattern.
    # - There is a BBs parameter passed as a (BB size, BB quantity) pair to set stacks to the
    #    commonly measured units of big blinds.
    # - There is a stackvariation parameter to randomly vary the sizes of the stacks. The
    #   parameter is a float value that is used to randomly calculate the variations.
    #
    if config['stepstacks']:
        for i, s in enumerate(t):
            s.buy_chips(STEP * (i + 1))
    elif config['stack']:
        for i, s in enumerate(t):
            s.buy_chips(config['stack'])
    else:
        for s in t:
            s.buy_chips(DEF_STACK)

    # Random variations
    if config['variance']:

        for s in t:
            hilimit = int(s.stack * config['variance'])
            offset = random.randint(0, hilimit)
            s.stack -= offset
    return t
