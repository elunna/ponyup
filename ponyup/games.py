from collections import namedtuple

Street = namedtuple('Street', ['name', 'betsize'])

GAMES = {
    # Just deals 5 cards
    'POKER': [
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
    ]

    #  'SEVEN CARD STUD': [1, 1, 2, 2, 2],
    #  'OMAHA': [1, 1, 2, 2],
    #  'HOLDEM': [1, 1, 2, 2],
}
