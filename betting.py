def calc_odds(bet, pot):
    """ Calculate the odds offered to a player given a bet amount and a pot amount."""
    print('first draft')
    print('Bet = {}, pot = {}'.format(bet, pot))
    print('bet is {}% of the pot'.format(bet/pot * 100))

    odds = pot / bet
    print('The odds are {}-to-1'.format(odds))
    return odds
