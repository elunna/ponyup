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
    return sort_by_stakes(drawgames) + sort_by_stakes(studgames)


def available_games():
    gamelist = set([g.game for g in lobbylist])
    return list(gamelist)


def get_game(L, game):
    return [x for x in L if x.game == game]


def sort_by_name(L):
    return sorted(L, key=lambda x: x.name)


def sort_by_stakes(L):
    return sorted(L, key=lambda x: x.blinds.level)


def sort_by_seats(L):
    return sorted(L, key=lambda x: x.seats)


def numbered_list(L):
    _str = ''
    fmt_str = '{:<8}{:20}{:<8}{:12}{:25}\n'
    print(fmt_str.format('Pick#', 'Game', 'Seats', 'Stakes', 'Table Name'))

    for i, gt in enumerate(L):
        _str += (fmt_str.format(i, gt.game.title(), gt.seats, gt.blinds.stakes(), gt.tablename))
    return _str
