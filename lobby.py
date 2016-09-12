import blinds
import table_selection
"""
This lobby listing is a list of all the available cash tables a pony can play
at. Each has: Table name, seats, stakes level, game type.
"""
lobbylist = table_selection.tables
DEFAULT_TABLE = 0


def default():
    return lobbylist[DEFAULT_TABLE]


def sorted_by_game_and_lev():
    drawgames = get_game(lobbylist, "FIVE CARD DRAW")
    studgames = get_game(lobbylist, "FIVE CARD STUD")
    return sort_by_level(drawgames) + sort_by_level(studgames)


def get_game(L, game):
    return [x for x in L if x.game == game]


def sort_by_name(L):
    return sorted(L, key=lambda x: x.name)


def sort_by_level(L):
    return sorted(L, key=lambda x: x.level)


def sort_by_seats(L):
    return sorted(L, key=lambda x: x.seats)


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


def numbered_list(L):
    _str = ''
    fmt_str = '{:<8}{:20}{:<8}{:12}{:25}\n'
    print(fmt_str.format('Pick#', 'Game', 'Seats', 'Stakes', 'Table Name'))

    for i, gt in enumerate(L):
        _stakes = stakes(gt)
        _str += (fmt_str.format(i, gt.game.title(), gt.seats, _stakes, gt.name))
    return _str
