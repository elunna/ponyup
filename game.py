import table
import deck
import fivecarddraw

# blindstructures = [ante, sb, bb]
structures = {}
structures['2/4'] = [0, 2, 4]
structures['3/6'] = [0, 3, 6]
structures['4/8'] = [0, 4, 8]


class Game():
    def __init__(self, struct, table):
        self.blinds = structures[struct]
        self._table = table
        self.betcap = 4
        self.rounds = 1

    def __str__(self):
        #  display = 'Game details\n'
        display = ''
        #  display += 'Blinds: {}/{}\n'.format(self.blinds[1], self.blinds[2])
        display += '${}/${}\n'.format(self.blinds[1], self.blinds[2])
        #  display += 'Bet cap limit: {}\n'.format(self.betcap)
        #  display += 'Table size: {}\n'.format(len(self.table))
        display += 'Round: {}\n'.format(self.rounds)
        return display

    def get_stacks(self):
        # Create a list(or tuple) beginning with the button that contains:
        # seat, username, chips
        """
        startingstacks = []
        num_players = len(table)
        c = table.btn
        for i in range(num_players):
            #  currentindex = (num_players + i) % num_players
            startingstacks.append(tuple(
                currentseatable.seats[currentindex])

        #  return self.table.seats
        """
        startingstacks = {}
        for i in len(table):
            startingstacks[i] = self._table.seats[i].chips
        return startingstacks

    def playround(self):

        newround = Round(self)

        newround.check_for_stale_cards()

        # todo: Postblinds

        newround.deal_hands()

        # Pre-draw betting round

        # Show table post draw
        print(self._table)

        newround.discard_phase()

        # Show table post draw
        print(self._table)

        # Post-draw betting round

        # Check for winners/showdown
        newround.get_winner()

        # Award pot

        # ================== CLEANUP
        newround.verify_muck()

        # Move the table button
        self._table.move_button()

        # Advance round counter
        self.rounds += 1


class Round():
    def __init__(self, game):
        self._game = game
        self.street = 0
        self.pot = 0
        self.muck = []

        self.d = deck.Deck()
        for i in range(3):
            self.d.shuffle()

        # Create a list of the players from the table, and place the button at index 0
        self.players = game._table.get_players()

        #  Remember starting stacks of all playerso
        self.startingstacks = []

    def post_blinds(self):
        pass

    def check_for_stale_cards(self):
        pass
        # Check that no players have lingering cards
        #  print('displaying hand lengths')
        #  for p in self.players:
            #  print(len(p._hand))
            #  if p is not None:
                #  if len(p._hand) > 0:
                    #  raise ValueError('Player has cards when they should not!')

    def deal_hands(self):
        for i in range(5):
            for p in self.players:
                p.add(self.d.deal())

    def discard_phase(self):
        # Make sure the button goes last!
        for i in range(1, len(self.players) + 1):
            plyr = i % len(self.players)

            if self.players[plyr].playertype == 'HUMAN':
                discards = fivecarddraw.human_discard(self.players[plyr]._hand)
            else:
                discards = fivecarddraw.auto_discard(self.players[plyr]._hand)

            print('{} discards {}'.format(self.players[plyr], discards))

            for c in discards:
                self.muck.append(self.players[plyr].discard(c))
                self.players[plyr].add(self.d.deal())

    def verify_muck(self):
        # Clear hands
        for p in self.players:
            self.muck.extend(p.fold())
        print('muck size = {}'.format(len(self.muck)))
        print('adding the remainder of the deck')
        # Add the remainder of the deck
        self.muck.extend(self.d.cards)
        print('muck size = {}'.format(len(self.muck)))

    def get_winner(self):
        """
        Takes in a list of Players and determines who has the best hand
        * Should we return just the Player?
        """

        # besthand tuple is (player index, hand value)
        besthand = {'player': -1, 'value': -1}

        for i, p in enumerate(self.players):
            if p._hand.value > besthand['value']:
                besthand['value'] = self.players[i]._hand.value
                besthand['player'] = i

        print('')

        print('{} wins with a {}!'.format(
            str(self.players[besthand['player']]),
            self.players[besthand['player']]._hand.handrank))
