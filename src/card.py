"""
  " Manages the suit, rank, comparison, and display of playing cards.
  " There are many types of cards in games:
  " Playing cards, tarot cards, Magic cards, flash cards
  """

BACK_TEXT = 'Xx'


class Card(object):
    """Represents a card """
    def __init__(self, top_text, back_text=BACK_TEXT):
        self.top_text = top_text
        self.back_text = back_text
        self.hidden = True

    def __str__(self):
        """Returns the string representation. """
        if self.hidden:
            return self.back_text
        else:
            return self.top_text

    def __repr__(self):
        """Returns the string representation of the Card. """
        return str(self)

    def hide(self):
        self.hidden = True

    def unhide(self):
        self.hidden = False

    def peek(self):
        """ This is how human/hero's are able to view hidden cards. """
        return self.top_text
