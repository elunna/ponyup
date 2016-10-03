from ponyup import deck
from ponyup import card


class PiquetDeck(deck.Deck):
    """
    Creates a 48 card Pinochle deck with 2 of each rank: 9, T, J, Q, K, A.
    """
    def __init__(self):
        pinochle_cards = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.cards = [card.Card(r, s[0])
                      for s in card.SUITS for r in card.RANKS if r in pinochle_cards]
