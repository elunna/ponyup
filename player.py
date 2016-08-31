import hand
import names

TYPES = ['FISH', 'JACKAL', 'MOUSE', 'LION']


class Player():
    def __init__(self, name, playertype="CPU"):
        self.set_name(name)
        self._type = playertype
        self.chips = 0
        self._hand = hand.Hand()

    def __str__(self):
        """
        Returns the player's name.
        """
        return '{}'.format(self.name)

    def __repr__(self):
        """
        Same as str, returns name.
        """
        return str(self)

    def set_name(self, name):
        """
        Checks the player name, and sets it if valid. Raises an exception if not valid.
        """
        if names.is_validname(name):
            self.name = name
        else:
            raise ValueError('Invalid username "{}" for object!'.format(name))

    def bet(self, amt):
        """
        Removes the amount given from the player's stack and returns it. If the amount is more
        than the player has, then the remaining amount in the player's stack is remoevd and
        returned.
        """
        if amt < 0:
            raise ValueError('Player cannot bet a negative amount!')
        if amt > self.chips:
            # Put the player all-in
            amt = self.chips
            self.chips = 0
            return amt
        else:
            self.chips -= amt
            return amt

    def add_chips(self, amt):
        """
        Adds the specified amount of chips to the player's stack.
        """
        self.chips += amt

    def showhand(self):
        """
        Unhides all cards in the player hand.
        """
        self._hand.unhide()

    def fold(self):
        """
        Removes all the cards in the player's hand and returns them as a list.
        """
        copy = self._hand.cards[:]
        self._hand.cards = []
        return copy

    def add_card(self, card):
        """
        Takes a card and adds it to the player hand. If the player is human, we unhide it so
        we can see it.
        """
        if self.is_human():
            card.hidden = False
        self._hand.add(card)

    def discard(self, card):
        """
        Removes and returns a specific card from the player's hand. If the card is not in the
        hand, raises an Exception.
        """
        if card not in self._hand.cards:
            raise ValueError('Card not in players hand!')
        else:
            return self._hand.discard(card)

    def get_upcards(self):
        """
        Returns a list of all the face-up cards the player has.
        """
        upcards = []
        for c in self._hand.cards:
            if c.hidden is False:
                upcards.append(c)
        return upcards

    def is_human(self):
        """
        Returns True if the player is a HUMAN type, False otherwise.
        """
        return self._type == 'HUMAN'

    def is_allin(self):
        """
        Returns True if the player has 0 chips in their stack, False otherwise.
        """
        return self.chips == 0

    def has_cards(self):
        """
        Returns True if the player has one or more cards in their hand, False otherwise.
        """
        return len(self._hand) > 0
