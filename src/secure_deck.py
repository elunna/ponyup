from . import deck


class SecureDeck(object):
    """ Manages a deck of Cards using a stack structure.
        This is intended to be a secure deck for professional gambling applications.
        Access to the cards is only allowed as a Stack structure. Only the top
        card can be dealt out.

        None of the inner cards can be examined, removed, copied, or manipulated.
        Cards cannot be added.

        Eventually, a signature may be need to be able to access the deal function.
    """

    def __init__(self):
        """ Initializes a new standard 52 card deck. """
        self.cards = deck.std_deck()

    def __len__(self):
        """ Returns how many cards are in the deck. """
        return len(self.cards)

    def deal(self):
        """ Removes the top card off the deck and returns it. Raises an exception
            if the deck is empty.
        """
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            raise Exception('Deck is empty, cannot deal cards!')
