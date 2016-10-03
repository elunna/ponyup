import random
from ponyup import draw5
from ponyup import names
from ponyup import player
from ponyup import stacks
from ponyup import stud
from ponyup import table

CPU_BANK_BITS = 10000
DEF_STACK = 1000
DEFAULT_BB = 100
DEFAULT_POOL = 100
STEP = 100


def table_factory(**new_config):
    config = {
        'seats': None,
        'tablename': 'default',
        'playerpool': None,
        'heroseat': None,
        'stack': DEF_STACK,
        'stepstacks': False,
        'remove': None,
        'bb': None,
        'varystacks': False
    }
    config.update(new_config)

    tbl = table.Table(config['seats'])
    tbl.name = config['tablename']

    # If playerpool is none, use a default playerpool.
    if config['playerpool'] is None:
        pool = make_playerpool(quantity=10)

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
        elif config['varystacks']:
            # Get a different stacksize(in BB's) for each player
            s.buy_chips(stacks.random_stack(config['bb']))

        elif config['stack']:
            s.buy_chips(config['stack'])
        else:
            s.buy_chips(DEF_STACK)

        # Random variations
            hilimit = int(s.stack * config['variance'])
            offset = random.randint(-hilimit, hilimit)
            s.stack -= offset

    # Removes a player from the table, if specified.
    if config['remove'] is not None:
        tbl.pop(config['remove'])

    return tbl


def session_factory(**new_config):
    config = {
        'seats': None,
        'poolsize': DEFAULT_POOL,
        'game': None,
        'tablename': 'default',
        'table': None,
        'hero': None,  # If there is a hero, they will be placed at the hero seat.
        'heroseat': 0,
        'herobuyin': None,
        'level': 1,
        'names': 'bob',
        'deposit': CPU_BANK_BITS,
        'varystacks': False
    }

    config.update(new_config)

    if config['game'] == 'FIVE CARD STUD':
        sesh = stud.Stud5Session()
    elif config['game'] == 'FIVE CARD DRAW':
        sesh = draw5.Draw5Session()
    else:
        raise ValueError('Game unknown to session!')

    # Set the blind level
    sesh.blinds.set_level(config['level'])

    # Make the playerpool
    pool = make_playerpool(
        quantity=config['poolsize'],
        game=config['game'],
        names=config['names'],
        varystacks=config['varystacks']
    )

    # Construct the table
    t = table_factory(
        seats=config['seats'],
        playerpool=pool,
        heroseat=(config['heroseat'] if config['hero'] is not None else None),
        tablename=config['tablename'],
        varystacks=config['varystacks'],
        bb=sesh.blinds.SMBET * 2
    )

    # Create and place the hero player.
    if config['hero']:
        hero = config['hero']
        heroseat = t.seats[config['heroseat']]
        heroseat.sitdown(hero)
        heroseat.buy_chips(config['herobuyin'])
        sesh.hero = heroseat

    # Set the session playerpool - the players in the table should have been popped out.
    sesh._table = t
    sesh.playerpool = pool
    return sesh


def make_playerpool(**new_config):
    config = {
        'quantity': None,
        'game': None,
        'types': 'random',  # Player types
        'names': 'bob',  # Player names, can be 'random'
        'deposit': CPU_BANK_BITS,
    }
    config.update(new_config)
    qty = config['quantity']

    if qty is None or qty <= 0:
        raise ValueError('Cannot make an empty playerpool!')

    # Create a list of players
    if config['names'] == 'random':
        # Generate random names
        nameset = names.random_names(qty)
    else:
        nameset = [config['names'] + str(i) for i in range(qty)]

    playerpool = []

    # Create the players
    for i, n in enumerate(nameset):
        p = player.factory(n, config['game'], config['types'])
        playerpool.append(p)

    # Fund the players
    for p in playerpool:
        p.deposit(config['deposit'])

    return playerpool
