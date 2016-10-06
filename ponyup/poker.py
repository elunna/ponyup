from __future__ import print_function
import datetime
import logging
import random
from ponyup import betting
from ponyup import deck
from ponyup import evaluator
from ponyup import logger
from ponyup import pots

_logger = logger.get_logger(__name__)
LOGDIR = 'logs/'
MAX_HANDLERS = 3


class Round():
    def __init__(self, session):
        """
        Initialize the next round of Poker.
        """
        _logger.debug('Initialized a new Round.')

        self.sesh = session
        self.gameid = random.randint(100000000, 999999999)
        self.street = 0
        self.pot = pots.Pot(self.table)

        self.muck = []
        self.d = deck.Deck()
        self.d.shuffle(17)  # Shuffle 17 times for good measure.
        self.DECKSIZE = len(self.d)
        self.exposed = []

        self.check_integrity_pre()

    def __str__(self):
        """
        Return info about the current round.
        """
        _str = '{} -- {}, {} '.format(self.label, self.gametype, self.blinds)
        _str += 'Potsize: {}'.format(self.pot)
        _str += 'Street: {}'.format(self.street)
        return _str

    def __getattr__(self, name):
        try:
            return getattr(self.sesh, name)
        except AttributeError:
            _logger.error('Error - {} attribute not in self.session'.format(name))
            raise AttributeError("Child' object has no attribute {}".format(name))

    @classmethod
    def decorate(self, text):
        #  L, R = '/)(\ ', ' /)(\'
        #  L, R = '(\/) ', ' (\/)'
        #  L, R = '~~(\ ', ' /)~~'
        L, R = '~~/) ', ' (\~~'
        return '\n' + L + text + R

    def log_holecards(self):
        _logger.info(self.decorate('Hole Cards'))

        hero = self.find_hero()
        _logger.debug('Hero is: {}'.format(hero.player))

        cards = hero.hand.peek()
        _logger.info('{}: [{}]'.format(hero, cards.strip()))

    def log_hh(self):
        dt = datetime.datetime
        filename = 'HH_{}_-_{}_{}_{}(Pony Bits).log'.format(
            dt.now().strftime('%Y%m%d'),
            self.table.name,
            self.gametype,
            self.blinds.stakes()
        )
        # Check if the handhistory log handler has been made
        if len(_logger.handlers) < MAX_HANDLERS:
            hh_file = LOGDIR + filename

            hh_fh = logging.FileHandler(hh_file)
            hh_fh.setLevel(logging.INFO)
            fmt = logging.Formatter('%(message)s')
            hh_fh.setFormatter(fmt)
            _logger.addHandler(hh_fh)

        _logger.debug('Round - gameid: {}'.format(self.gameid))
        _logger.debug('Round - street: {}'.format(self.street))
        _logger.debug('Round - pot: {}'.format(self.pot))
        _logger.debug('Round - muck: {}'.format(self.muck))
        _logger.debug('Round - deck: {}'.format(self.d))
        _logger.debug('Round - exposed: {}'.format(self.exposed))

        _logger.info(logger.round_header(self))
        _logger.info(self.table.player_listing())
        _logger.info('Seat {} has the button.'.format(self.table.TOKENS['D']))

    def deal_cards(self, qty, faceup=False, handreq=False):
        """
        Deal the specified quantity of cards to each player. If faceup is True, the cards are
        dealt face-up, otherwise they are face-down.
        """
        _logger.debug('Dealing cards out to table.')
        _logger.debug('qtt={}, faceup={}, handreq={}'.format(qty, faceup, handreq))

        for i in range(qty):
            for s in self.table.get_players():
                if handreq and not s.has_hand():
                    continue
                c = self.d.deal()
                s.hand.add(c)
                if faceup is True:
                    c.hidden = False

                    if s is not self.find_hero():
                        _logger.info('{} was dealt [{}]'.format(s.player, c))
                    self.exposed.append(c)

    def show_cards(self):
        """
        Unhides all player hands.
        """
        _logger.debug('All player hands are being revealed.')
        for s in self.table.get_players(hascards=True):
            _logger.debug('Unhiding {}\'s hand.'.format(s.player))
            s.hand.unhide()

        _str = ''
        for s in self.table.get_players(hascards=True):
            _str += '{:20} shows {}\n'.format(str(s), str(s.hand))
        _logger.info(_str)
        _str += '\n'
        return _str

    def sortcards(self):
        """
        Sort all cards in all players hands.
        """
        _logger.debug('Sorting all player hands.')
        for s in self.table:
            s.hand.sort()

    def discard(self, seat, c):
        """
        Takes the card from the seat's hand and transfers it to the muck. Returns True if the
        operation was successful, False if it didn't.
        """
        _logger.debug('Seat {} is discarding {}.'.format(seat.NUM, c))
        self.muck.append(seat.hand.discard(c))

    def burn(self):
        _logger.debug('Burning a card to the muck.')
        self.muck.append(self.d.deal())

    def muck_all_cards(self):
        """
        Muck all player hands, and muck the contents of the deck.
        """
        _logger.debug('Mucking all player hands.')
        for s in self.table:
            self.muck.extend(s.fold())

        _logger.debug('Mucking the deck.')
        while len(self.d) > 0:
            self.muck.append(self.d.deal())

    def post_antes(self):
        """
        All players bet the ante amount and it's added to the pot.
        """
        _logger.debug('Making players post antes.')
        actions = ''
        for s in self.table:
            actions += '{} posts ${} ante.\n'.format(s, self.blinds.ANTE)
            self.pot += s.bet(self.blinds.ANTE)

        _logger.info(actions)
        return actions

    def post_blinds(self):
        """
        Gets the small and big blind positions from the table and makes each player bet the
        appropriate mount to the pot. Returns a string describing what the blinds posted.
        """
        _logger.debug('Making players post blinds.')

        if self.table.TOKENS['D'] == -1:
            _logger.error('Button has not been set yet!')
            raise Exception('Button has not been set yet!')

        if len(self.table.get_players()) < 2:
            _logger.error('Not enough players to play!')
            raise ValueError('Not enough players to play!')
            exit()
        sb = self.table.seats[self.table.TOKENS['SB']]
        bb = self.table.seats[self.table.TOKENS['BB']]

        # Bet the SB and BB amounts and add to the pot
        self.pot += sb.bet(self.blinds.SB)
        self.pot += bb.bet(self.blinds.BB)
        actions = ''
        actions += '{} posts ${}\n'.format(sb, self.blinds.SB)
        actions += '{} posts ${}'.format(bb, self.blinds.BB)

        _logger.info(actions)
        return actions

    def post_bringin(self):
        """
        Gets the player who must post the bringin amount, adds their bet to the pot, and
        returns a string describing what the blinds posted.
        """
        _logger.debug('Finding the player who is the bringin.')
        table = self.table
        bi = table.TOKENS['BI']
        if bi == -1:
            _logger.error('Bringin has not been set on the table!')
            raise Exception('Bringin has not been set on the table!')

        seat = table.seats[bi]

        _logger.debug('Making a player post the bringin.')
        # Bet the Bringin amount and add to the pot
        self.pot += seat.bet(self.blinds.BRINGIN)
        action = ''
        action += '{} brings it in for ${}'.format(seat.player, self.blinds.BRINGIN)

        _logger.info(action)
        return action

    def next_street(self):
        """
        Advanced the street counter by one.
        """
        if self.street >= len(self.streets):
            _logger.error('The last street has been reached on this game!')
            raise Exception('The last street has been reached on this game!')
        else:
            _logger.debug('Advancing the Round to the next street.')
            self.street += 1

    def get_street(self):
        _logger.debug('Returning the current Street.')
        return self.streets[self.street]

    def one_left(self):
        cardholders = self.table.get_players(hascards=True)
        if len(cardholders) == 1:
            _logger.debug('There is only one seat left with cards.')
            _logger.debug('Returning the last remaining seat')
            return cardholders.pop()
        else:
            _logger.debug('More than one player has cards.')
            return None

    def betting_round(self):
        """
        Run through a round of betting. Returns a victor if it exists.
        """
        print(self.table)
        br = betting.BettingRound(self)

        _logger.debug('Starting iteration new Betting object.')
        for seat in br:
            if seat == self.find_hero():
                # Get player action
                while True:
                    actions = br.get_options(seat)
                    choice = input('{}?'.format(br.betmenu(actions)))
                    if choice.lower() in actions:
                        action = actions[choice]
                        break
                    else:
                        print('Invalid choice, try again.')
            else:
                # Get cpu decision
                action = br.cpu_decision(seat)

            br.process_option(action)
            act_str = br.action_string(action)
            space = betting.spacing(br.level())

            print(space, act_str)
            _logger.info(act_str)

        print('Pot: ${}'.format(self.pot))

    def betting_over(self):
        """
        Checks the players and sees if any valid bettors are left to duke it out. If no more
        than 1 is left, the betting is over. Returns True if there is no more betting, False
        otherwise.
        """
        hands = len(self.table.get_players(hascards=True))
        _logger.debug('There are {} seats with hands left.'.format(hands))

        broke = len(self.table.get_broke_players())
        _logger.debug('There are {} broke players.'.format(broke))

        if hands - broke <= 1:
            _logger.debug('The betting round is over')
            return True
        else:
            _logger.debug('The betting round will continue.')
            return False

    def found_winner(self):
        _logger.debug('Checking if a one player is left to claim the pot.')
        victor = self.one_left()

        if victor is None:
            _logger.debug('No winner, proceeding to next street..')
            self.next_street()
            return False
        else:
            _logger.debug('One player left.')
            print('Only one player left!'.rjust(70))

            awardtext = pots.award_pot(victor, self.pot.pot)
            _logger.info(awardtext)
            return True

    def showdown(self):
        """
        Compare all the hands of players holding cards and determine the winner(s). Awards each
        winner the appropriate amount.
        """
        sd_text = ''

        title = self.decorate('Showdown!')
        _logger.info(title)
        sd_text += title

        revealed = self.show_cards()
        sd_text += revealed

        _logger.debug('Calculating pots and sidepots.')
        award_txt = self.pot.allocate_money_to_winners()

        _logger.info(award_txt)
        sd_text += award_txt

        return sd_text

    def cleanup(self):
        _logger.debug('Cleanup phase.')
        self.muck_all_cards()

        if not self.check_integrity_post():
            _logger.error('Integrity of game could not be verified after round was complete!')
            raise Exception('Integrity of game could not be verified after round was complete!')

    def check_integrity_pre(self):
        """
        Verify that the game elements are set up correctly.
        """
        _logger.debug('Checking the integrity of the game, pre-deal.')

        # Check that the deck is full.
        if len(self.d) != self.DECKSIZE:
            _logger.error('Deck is corrupted, not full size.')
            return False

        _logger.debug('Deck is full.')

        # Check that the muck is empty.
        if len(self.muck) != 0:
            _logger.error('Muck is corrupted, has cards in it.')
            return False

        _logger.debug('Muck is empty.')

        # Check that no players have cards.
        if len(self.table.get_players(hascards=True)) > 0:
            _logger.error('Play is corrupted, a seat has cards pre-deal.')
            return False

        _logger.debug('No players have cards.')

        # Check that the pot is 0.
        if self.pot != 0:
            _logger.error('Pot is corrupted, has chips in it.')
            return False

        _logger.debug('Pot is empty.')

        _logger.debug('All checks pass. Pre-deal integrity intact.')
        return True

    def check_integrity_post(self):
        """
        Verify that the game elements have been cleaned up correctly and that all cards are
        accounted for.
        """
        _logger.debug('Checking the integrity of the game, post-showdown.')

        # Check that all cards have been used up.
        if len(self.d) != 0:
            _logger.error('Deck is corrupted, has cards in it.')
            return False

        _logger.debug('Deck is empty.')

        # Check that the muck is the same size as the original starting deck.
        if len(self.muck) != self.DECKSIZE:
            _logger.error('Muck is corrupted, doesn\'t equal starting deck size.')
            return False

        _logger.debug('Muck is full.')

        # Check that all players have folded.
        if len(self.table.get_players(hascards=True)) > 0:
            _logger.error('Seat is corrupted, has cards.')
            return False

        _logger.debug('No players have cards.')

        # The sum of all sidepots should equal the potsize.

        _logger.debug('All checks pass. Post-showdown integrity intact.')
        return True

    def exposed_cards(self):
        _logger.debug('Finding new exposed cards to add to the Rounds list.')
        exposed = []
        for s in self.table:
            exposed.extend(s.hand.get_upcards())
        return exposed

    def highhand(self):
        """
        Finds which player has the highest showing hand and return their seat index.  For stud
        games, after the first street, the high hand on board initiates the action (a tie is
        broken by position, with the player who received cards first acting first).
        """
        _logger.debug('Determining which player has the highest exposed hand.')
        seat, highvalue = None, 0
        ties = []

        for s in self.table.get_players(hascards=True):
            h = s.hand.get_upcards()
            value = evaluator.get_value(h)

            if value > highvalue:
                highvalue, seat = value, s
                ties = [seat]  # Reset any lower ties.
                _logger.debug('Current high hand value: {}.'.format(highvalue))
                _logger.debug('Seat with current highest hand: {}.'.format(seat.NUM))
            elif value == highvalue:
                _logger.debug('Seat {} tied for current high value.'.format(s.NUM))
                ties.append(s)

                # Is this needed?
                if seat not in ties:
                    ties.append(seat)

        # Return the seat index of the first-to-act.
        if len(ties) > 1:
            _logger.debug('There was a tie for high hand, breaking tie with seat position')
            # Process ties, get the player who was dealt first.
            for s in self.table.get_players(hascards=True):
                if s in ties:
                    _logger.debug('Seat {} was dealt first, returning its index.'.format(s.NUM))
                    return s.NUM
        else:
            _logger.debug('Seat {} has high hand, returning its index.'.format(s.NUM))
            return seat.NUM
