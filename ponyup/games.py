"""
  " Manages the broad basics of each poker game.
  """
from collections import namedtuple

Street = namedtuple('Street', ['name', 'betsize'])

GAMES = {
    'POKER': [
        # Just deals 5 cards
        Street(name="Deal", betsize=1),
    ],

    'FIVE CARD DRAW': [
        Street(name="Predraw", betsize=1),
        Street(name="Postdraw", betsize=2),
    ],

    'FIVE CARD STUD': [
        Street(name="Second Street", betsize=1),
        Street(name="Third Street", betsize=1),
        Street(name="Fourth Street", betsize=2),
        Street(name="Fifth Street", betsize=2),
    ],

    'SEVEN CARD STUD': [
        Street(name="Third Street", betsize=1),
        Street(name="Fourth Street", betsize=1),
        Street(name="Fifth Street", betsize=2),
        Street(name="Sixth Street", betsize=2),
        Street(name="SeventhStreet", betsize=2),
    ],
    'HOLDEM': [
        Street(name="Preflop", betsize=1),
        Street(name="Flop", betsize=1),
        Street(name="Turn", betsize=2),
        Street(name="Turn", betsize=2),
    ],
    'OMAHA': [
        Street(name="Preflop", betsize=1),
        Street(name="Flop", betsize=1),
        Street(name="Turn", betsize=2),
        Street(name="Turn", betsize=2),
    ],
}
