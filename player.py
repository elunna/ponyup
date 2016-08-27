import hand
import names

TYPES = ['FISH', 'JACKAL', 'MOUSE', 'LION']


class Player():
    def __init__(self, name, playertype="CPU"):
        self.set_name(name)
        self.playertype = playertype
        self.chips = 0
        self._hand = hand.Hand()

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return str(self)

    def set_name(self, name):
        if names.isValidName(name):
            self.name = name
        else:
            raise ValueError('Invalid username "{}" for object!'.format(name))

    #  def __eq__(self, other):
        #  return self.name == other.name

    def bet(self, amt):
        if amt > self.chips:
            # Put the player all-in
            amt = self.chips
            self.chips = 0
            return amt
        else:
            self.chips -= amt
            return amt

    def add_chips(self, amt):
        self.chips += amt

    def showhand(self):
        self._hand.unhide()

    def fold(self):
        copy = self._hand.cards[:]
        self._hand.cards = []
        return copy

    # hand management
    def add_card(self, card):
        # Make sure we can see the card! (if we're human...)
        if self.playertype == 'HUMAN':
            card.hidden = False
        self._hand.add(card)

    def discard(self, card):
        # Test if the card is actually in the hand
        if card not in self._hand.cards:
            raise ValueError('Card not in players hand!')
        else:
            return self._hand.discard(card)

    def get_upcards(self):
        # return a list of all the non-hidden cards the player has.
        upcards = []
        for c in self._hand.cards:
            if c.hidden is False:
                upcards.append(c)
        return upcards
