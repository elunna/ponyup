def calc_odds(bet, pot):
    """ Calculate the odds offered to a player given a bet amount and a pot amount."""
    if bet < 0 or pot < 0:
        raise ValueError('bet or pot must be positive!')
    odds = pot / bet
    return odds
