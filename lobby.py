import blinds
import table_selection
"""
This lobby listing is a list of all the available cash tables a pony can play
at. Each has: Table name, seats, stakes level, game type.
"""
lobbylist = table_selection.tables
DEFAULT_TABLE = 0


def get_games(game):
    return [x for x in lobbylist if x.game == game]


def default():
    return lobbylist[DEFAULT_TABLE]


def sort_by_name(L):
    return sorted(L, key=lambda x: x.name)


def sort_by_level(L):
    return sorted(L, key=lambda x: x.level)


def stakes(gametuple):
    """
    Return the small bet and big bet sizes.
    """
    if gametuple.game == "FIVE CARD STUD":
        sb = blinds.ante[gametuple.level][0]
        return '${}/${}'.format(sb, sb*2)
    elif gametuple.game == "FIVE CARD DRAW":
        sb = blinds.no_ante[gametuple.level][0]
        return '${}/${}'.format(sb, sb*2)


def display_numbered_list(L):
    _str = ''
    fmt_str = '{:4}: {:25} {:9} {:6} {}\n'
    print(fmt_str.format('', 'Table Name', 'Stakes', 'Seats', 'Game'))
    for i, k in enumerate(L):

        _stakes = stakes(k)
        _str += (fmt_str.format(i, k.name, _stakes, k.seats, k.game))
    return _str
