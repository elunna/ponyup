def display(tbl):
    """ Return the string representation of the table, with colors. """
    _str = []
    _str.append('\n')
    _str.append('{:10}'.format('Seat'))
    _str.append('{:10}'.format('Blinds'))
    _str.append('{:10}'.format('Dealer'))
    _str.append('{:20}'.format('Player'))
    _str.append('{:<16}'.format('Chips'))
    _str.append('{:15}'.format('Hand'))
    _str.append('\n')

    for i, s in enumerate(tbl.seats):
        if s is None:
            # No player is occupying the seat
            _str.append('{}\n'.format(i))
            continue
        else:
            _str.append('{:<10}'.format(i))

        if tbl.TOKENS['SB'] == i:
            _str.append('{:10}'.format('[SB]'))
        elif tbl.TOKENS['BB'] == i:
            _str.append('{:10}'.format('[BB]'))
        elif tbl.TOKENS['BI'] == i:
            _str.append('{:10}'.format('[BI]'))
        else:
            _str.append(' '*10)

        if tbl.TOKENS['D'] == i:
            _str.append('{:10}'.format('[D]'))
        else:
            _str.append(' '*10)

        if s.occupied():
            _str.append('{:20}'.format(str(s.player)))
            _str.append('${:<15.2f}'.format(s.stack))
            # Display hand if available
            if s.player.is_human():
                _str.extend(s.hand.peek())

            elif s.hand is not None:
                _str.extend(str(c) + ' ' for c in s.hand.cards)
                # _str.append('{:15}'.format(str(s.hand.cards)))

        else:
            # Don't show anything for vacant seats.
            _str.append('{:20}{:15}'.format('', ''))

        _str.append('\n')

    return _str
