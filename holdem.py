def card2text(cards):
    if len(cards) != 2:
        raise ValueError('Only accepts a list of exactly 2 cards!')

    rankhi = cards[0].rank
    ranklo = cards[1].rank
    suited = cards[0].suit == cards[1].suit

    # Check for pair
    # Check for suited
    # Offsuit
