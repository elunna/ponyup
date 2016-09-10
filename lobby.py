import blinds
import table_selection
"""
This lobby listing is a list of all the available cash tables a pony can play
at. Each has: Table name, seats, stakes level, game type.
"""
L = table_selection.tables
DEFAULT_TABLE = 0


def default():
    return L[DEFAULT_TABLE]


def sort_by_name():
    return sorted(L, key=lambda x: x.name)


def sort_by_level():
    return sorted(L, key=lambda x: x.level)


def get_games(game):
    return [x for x in L if x.game == game]


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


def display_numbered_list():
    _str = ''
    fmt_str = '{:4}: {:25} {:9} {:6} {}\n'
    print(fmt_str.format('', 'Table Name', 'Stakes', 'Seats', 'Game'))
    for i, k in enumerate(L):

        _stakes = stakes(k)
        _str += (fmt_str.format(i, k.name, _stakes, k.seats, k.game))
    return _str
