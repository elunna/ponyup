import player
import table
import names

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
        'BB': None,  # Size of the big blind.
        'deposit': DEPOSIT,
        'stack': DEF_STACK,
        'stepstacks': False,
        'stackvariation': None,
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
        #  nameset = ['bob' for i in range(SEATS)]

    # Fund and Seat the players
    for i, s in enumerate(t):
        p = player.factory(nameset[i], config['game'], config['types'])

        #  p.deposit(config['deposit'])
        s.sitdown(p)

    """
    # Create and place the hero player.
    if config['heroname']:
        hero = player.Player(config['heroname'])
        heroseat = t.seats[config['heroseat']]
        heroseat.sitdown(hero)

    # Players buyin to the table.
    if config['stepstacks']:
        for i, s in enumerate(t):
            s.buy_chips(STEP * (i + 1))
    else:
        for s in t:
            s.buy_chips(DEF_STACK)
    """
    return t
