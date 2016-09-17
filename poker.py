from __future__ import print_function
import betting
import colors
import console
import deck
import evaluator
import handhistory
import pots


class Round():
    def __init__(self, session):
        """
        Initialize the next round of Poker.
        """
        self.gametype = session.gametype
        self.blinds = session.blinds
        self.streets = session.streets
        self._table = session._table
        self.hero = session.hero
        self.street = 0
        self.pot = pots.Pot(self._table)

        self.muck = []
        self.d = deck.Deck()
        self.d.shuffle(17)  # Shuffle 17 times for good measure.
        self.DECKSIZE = len(self.d)
        self.exposed = []

        self.check_integrity_pre()

        self.hh = handhistory.HandHistory(self)

    def __str__(self):
        """
        Return info about the current round.
        """
        _str = '{} -- {}, {} '.format(self.label, self.gametype, self.blinds)
        _str += 'Potsize: {}'.format(self.pot)
        _str += 'Street: {}'.format(self.street)
        return _str

    def log(self, txt, echo=True, decorate=False):
        if decorate:
            txt = handhistory.decorate(txt)
        if echo:
            print(txt)
        self.hh.log(txt)

    def log_holecards(self):
        self.log('Hole Cards', decorate=True, echo=False)
        hero = self.hero
        cards = hero.hand.peek()
        self.log('{}: [{}]'.format(hero, cards.strip()), echo=False)

    def deal_cards(self, qty, faceup=False, handreq=False):
        """
        Deal the specified quantity of cards to each player. If faceup is True, the cards are
        dealt face-up, otherwise they are face-down.
        """
        for i in range(qty):
            for s in self._table.get_players():
                if handreq and not s.has_hand():
                    continue
                c = self.d.deal()
                s.hand.add(c)
                if faceup is True:
                    c.hidden = False

                    if s is not self.hero:
                        self.log('{} was dealt [{}]'.format(s.player, c), echo=False)
                    self.exposed.append(c)

    def show_cards(self):
        """
        Unhides all player hands.
        """
        for s in self._table.get_players(hascards=True):
            s.hand.unhide()

    def sortcards(self):
        """
        Sort all cards in all players hands.
        """
        for s in self._table:
            s.hand.sort()

    def discard(self, seat, c):
        """
        Takes the card from the seat's hand and transfers it to the muck. Returns True if the
        operation was successful, False if it didn't.
        """
        self.muck.append(seat.hand.discard(c))

    def burn(self):
        self.muck.append(self.d.deal())

    def muck_all_cards(self):
        """
        Muck all player hands, and muck the contents of the deck.
        """
        # Clear hands
        for s in self._table:
            self.muck.extend(s.fold())
        # Add the remainder of the deck
        while len(self.d) > 0:
            self.muck.append(self.d.deal())

    def post_antes(self):
        """
        All players bet the ante amount and it's added to the pot.
        """
        actions = ''
        for s in self._table:
            actions += '{} posts ${} ante.\n'.format(s, self.blinds.ANTE)
            self.pot += s.bet(self.blinds.ANTE)

        self.log(actions, echo=False)
        return actions

    def post_blinds(self):
        """
        Gets the small and big blind positions from the table and makes each player bet the
        appropriate mount to the pot. Returns a string describing what the blinds posted.
        """
        if self._table.TOKENS['D'] == -1:
            raise Exception('Button has not been set yet!')

        if len(self._table.get_players()) < 2:
            raise ValueError('Not enough players to play!')
            exit()
        sb = self._table.seats[self._table.TOKENS['SB']]
        bb = self._table.seats[self._table.TOKENS['BB']]

        # Bet the SB and BB amounts and add to the pot
        self.pot += sb.bet(self.blinds.SB)
        self.pot += bb.bet(self.blinds.BB)
        actions = ''
        actions += '{} posts ${}\n'.format(sb, self.blinds.SB)
        actions += '{} posts ${}'.format(bb, self.blinds.BB)

        self.log(actions, echo=False)
        return actions

    def post_bringin(self):
        """
        Gets the player who must post the bringin amount, adds their bet to the pot, and
        returns a string describing what the blinds posted.
        """
        table = self._table
        bi = table.TOKENS['BI']
        if bi == -1:
            raise Exception('Bringin has not been set on the table!')

        seat = table.seats[bi]

        # Bet the Bringin amount and add to the pot
        self.pot += seat.bet(self.blinds.BRINGIN)
        action = ''
        action += '{} brings it in for ${}'.format(seat.player, self.blinds.BRINGIN)

        self.log(action, echo=False)
        return action

    def highhand(table):
        """
        Finds which player has the highest showing hand and return their seat index.  For stud
        games, after the first street, the high hand on board initiates the action (a tie is
        broken by position, with the player who received cards first acting first).
        """
        highvalue = 0
        seat = None
        ties = []

        for s in table.get_players(hascards=True):
            h = s.hand.get_upcards()
            value = evaluator.get_value(h)

            if value > highvalue:
                highvalue, seat = value, s
                ties = [seat]  # Reset any lower ties.
            elif value == highvalue:
                ties.append(s)
                if seat not in ties:
                    ties.append(seat)

        # Return the seat index of the first-to-act.
        if len(ties) > 1:
            # Process ties, get the player who was dealt first.
            for s in table.get_players(hascards=True):
                if s in ties:
                    return s.NUM
        else:
            return seat.NUM

    def next_street(self):
        """
        Advanced the street counter by one.
        """
        if self.street >= len(self.streets):
            raise Exception('The last street has been reached on this game!')
        else:
            self.street += 1

    def get_street(self):
        return self.streets[self.street]

    def one_left(self):
        cardholders = self._table.get_players(hascards=True)
        if len(cardholders) == 1:
            return cardholders.pop()
        else:
            return None

    def betting_round(self):
        """
        Run through a round of betting. Returns a victor if it exists.
        """
        print(console.display_table(self._table, self.hero))
        br = betting.BettingRound(self)

        for p in br:
            o = br.player_decision(p)
            br.process_option(o)
            act_str = br.action_string(o)
            space = betting.spacing(br.level())
            console.print_action(space, act_str)

            # Log every action
            self.hh.log(act_str)

        console.print_pot(self.pot)

    def betting_over(self):
        """
        Checks the players and sees if any valid bettors are left to duke it out. If no more
        than 1 is left, the betting is over. Returns True if there is no more betting, False
        otherwise.
        """
        hands = len(self._table.get_players(hascards=True))
        broke = len(self._table.get_broke_players())
        if hands - broke <= 1:
            return True
        else:
            return False

    def found_winner(self):
        victor = self.one_left()
        if victor is None:
            self.next_street()
            return False
        else:
            # One player left, award them the pot!
            oneleft = 'Only one player left!'.rjust(70)
            print(colors.color(oneleft, 'LIGHTBLUE'))

            awardtext = pots.award_pot(victor, self.pot.pot)
            self.log(awardtext)
            return True

    def showdown(self):
        """
        Compare all the hands of players holding cards and determine the winner(s). Awards each
        winner the appropriate amount.
        """
        title = 'Showdown!'
        self.log(title, decorate=True, echo=False)
        console.right_align(title)
        self.show_cards()

        self.log(console.show_hands(self._table, color=False), echo=False)
        console.right_align((console.show_hands(self._table, color=True)))

        award_txt = self.pot.allocate_money_to_winners()
        self.log(award_txt, echo=False)
        console.right_align(award_txt)

    def cleanup(self):
        self.muck_all_cards()

        if not self.check_integrity_post():
            raise Exception('Integrity of game could not be verified after round was complete!')

    def check_integrity_pre(self):
        """
        Verify that the game elements are set up correctly.
        """
        # Check that the deck is full.
        if len(self.d) != self.DECKSIZE:
            return False
        # Check that the muck is empty.
        if len(self.muck) != 0:
            return False
        # Check that no players have cards.
        if len(self._table.get_players(hascards=True)) > 0:
            return False
        # Check that the pot is 0.
        if self.pot != 0:
            return False
        return True

    def check_integrity_post(self):
        """
        Verify that the game elements have been cleaned up correctly and that all cards are
        accounted for.
        """
        # Check that all cards have been used up.
        if len(self.d) != 0:
            return False
        # Check that the muck is the same size as the original starting deck.
        if len(self.muck) != self.DECKSIZE:
            return False
        # Check that all players have folded.
        if len(self._table.get_players(hascards=True)) > 0:
            return False
        # The sum of all sidepots should equal the potsize.

        return True

    def exposed_cards(self):
        exposed = []
        for s in self._table:
            exposed.extend(s.hand.get_upcards())
        return exposed
