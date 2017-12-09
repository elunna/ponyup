from . import deck


class BlackjackDeck(deck.Deck):
    """ Creates a blackjack deck with the specified number of 'shoes' included.
        4 shoes is the most common size for a Las Vegas blackjack deck.
    """
    def __init__(self, shoes=4):
        if shoes < 1:
            raise ValueError('BlackjackDeck must be passed a value of 1 or more for shoes!')

        super(BlackjackDeck, self).__init__()
        cardset = self.cards[:]
        for _ in range(shoes - 1):
            self.cards.extend(cardset)
