"""
  " Manages all the aspects of a round of poker
  """
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


class Round(object):
    """ A single round of poker in a longer running Session """

    def __init__(self, session):
        """ Initialize the next round of Poker.  """
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

        self.get_utg = self.position_by_button

        self.check_integrity_pre()

    def __str__(self):
        """ Return info about the current round.  """
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

    def setup(self):
        """ Perform the pre-round payment actions, check the blinds object for
            what is turned on.
        """
        if self.blinds.antes:
            self.post_antes()

        if self.blinds.blinds:
            self.table.set_blinds()
            self.post_blinds()

        # ! We can't set bringin until cards are dealt
        #  if self.blinds.bringin:
            #  self.post_bringin()

    @classmethod
    def decorate(self, text):
        return '\n~~~ {} ~~~\n'.format(text)

    def log_holecards(self):
        _logger.info(self.decorate('Hole Cards'))

        hero = self.find_hero()
        _logger.debug('Hero is: {}'.format(hero.player))

        _logger.info('{}: [ '.format(hero))
        for c in hero.hand.peek():
            _logger.info('{}'.format(c))

        _logger.info(']\n')

    def log_hh(self):
        """ Creates a new handhistory entry in the handhistory file. """
        dt = datetime.datetime
        filename = 'HH_{}_-_{}_{}_{}.log'.format(
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

        for txt in logger.round_header(self):
            _logger.info(txt)
        # _logger.info(self.table.player_listing())  # Too much info?
        # _logger.info('\n')
        _logger.info('\n')
        _logger.info('Seat {} has the button.\n'.format(self.table.TOKENS['D']))

    def deal_cards(self, qty, faceup=False, handreq=False):
        """ Deal the specified quantity of cards to each player. If faceup is
            True, the cards are dealt face-up, otherwise they are face-down.
        """
        _logger.debug('Dealing cards out to table.')
        _logger.debug('qtt={}, faceup={}, handreq={}'.format(qty, faceup, handreq))

        for _ in range(qty):
            for s in self.table.get_players():
                if handreq and not s.has_hand():
                    continue
                c = self.d.deal()
                s.hand.add(c)
                if faceup is True:
                    c.hidden = False

                    if s is not self.find_hero():
                        _logger.info('{} was dealt [{}]\n'.format(s.player, c))
                    self.exposed.append(c)

    def show_cards(self):
        """ Unhides all player hands. """
        _logger.debug('All player hands are being revealed.')
        for s in self.table.get_players(hascards=True):
            _logger.debug('Unhiding {}\'s hand.'.format(s.player))
            s.hand.unhide()

        _str = ''
        for s in self.table.get_players(hascards=True):
            _str += '{:20} shows {}\n'.format(str(s), str(s.hand))
        _str += '\n'
        return _str

    def sortcards(self):
        """ Sort all cards in all players hands. """
        _logger.debug('Sorting all player hands.')
        for s in self.table:
            s.hand.sort()

    def burn(self):
        _logger.debug('Burning a card to the muck.')
        self.muck.append(self.d.deal())

    def muck_all_cards(self):
        """ Muck all player hands, and muck the contents of the deck. """
        _logger.debug('Mucking all player hands.')
        for s in self.table:
            self.muck.extend(s.fold())

        _logger.debug('Mucking the deck.')
        while len(self.d) > 0:
            self.muck.append(self.d.deal())

    def post_antes(self):
        """ All players bet the ante amount and it's added to the pot. """
        _logger.debug('Making players post antes.')
        for s in self.table:
            _logger.info('{} posts ${} ante.\n'.format(s, self.blinds.ANTE))
            self.pot += s.bet(self.blinds.ANTE)

    def post_blinds(self):
        """ Gets the small and big blind positions from the table and makes each
            player bet the appropriate mount to the pot. Returns a string
            describing what the blinds posted.
        """
        _logger.debug('Making players post blinds.')

        if self.table.TOKENS['D'] == -1:
            _logger.error('Button has not been set yet!')
            raise Exception('Button has not been set yet!')

        if len(self.table.get_players()) < 2:
            _logger.error('Not enough players to play!')
            raise ValueError('Not enough players to play!')
        sb = self.table.seats[self.table.TOKENS['SB']]
        bb = self.table.seats[self.table.TOKENS['BB']]

        # Bet the SB and BB amounts and add to the pot
        self.pot += sb.bet(self.blinds.SB)
        self.pot += bb.bet(self.blinds.BB)

        _logger.info('{} posts ${}\n'.format(sb, self.blinds.SB))
        _logger.info('{} posts ${}\n'.format(bb, self.blinds.BB))

    def post_bringin(self):
        """ Gets the player who must post the bringin amount, adds their bet to
            the pot, and returns a string describing what the blinds posted.
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

        _logger.info('{} brings it in for ${}'.format(seat.player, self.blinds.BRINGIN))

    def next_street(self):
        """ Advanced the street counter by one. """
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
        """ Determines if only one valid bettor with cards is left. """
        cardholders = self.table.get_players(hascards=True)
        if len(cardholders) == 1:
            _logger.debug('There is only one seat left with cards.')
            _logger.debug('Returning the last remaining seat')
            return cardholders.pop()
        else:
            _logger.debug('More than one player has cards.')
            return None

    def betting_round(self):
        """ Run through a round of betting. Returns a victor if it exists.  """
        for txt in self.table.display():
            _logger.info(txt)

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
                        _logger.info('Invalid choice, try again.\n')
            else:
                # Get cpu decision
                action = br.cpu_decision(seat)

            br.process_option(action)
            act_str = br.action_string(action)
            space = betting.spacing(br.level())

            _logger.info('{}{}\n'.format(space, act_str))

        _logger.info('Pot: ${}\n'.format(self.pot))

    def betting_over(self):
        """ Checks the players and sees if any valid bettors are left to duke it
            out. If no more than 1 is left, the betting is over. Returns True if
            there is no more betting, False otherwise.
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
        """ Check if one player is remaining to claim the pot. """
        victor = self.one_left()

        if victor is None:
            _logger.debug('No winner, proceeding to next street..')
            self.next_street()
            return False
        else:
            _logger.info('Only one player left!\n'.rjust(70))

            pots.award_pot(victor, self.pot.pot)
            awardtext = '{} wins ${} without a showdown!\n'.format(victor, self.pot.pot)
            _logger.info(awardtext)
            return True

    def showdown(self):
        """ Compare all the hands of players holding cards and determine the
            winner(s). Awards each winner the appropriate amount.
        """
        sd_text = ''

        title = self.decorate('Showdown!')
        sd_text += title

        revealed = self.show_cards()
        sd_text += '\n' + revealed

        _logger.debug('Calculating pots and sidepots.')
        award_txt = self.pot.allocate_money_to_winners()

        sd_text += award_txt

        return sd_text

    def cleanup(self):
        _logger.debug('Cleanup phase.')
        self.muck_all_cards()

        if not self.check_integrity_post():
            _logger.error('Integrity of game could not be verified after round was complete!')
            raise Exception('Integrity of game could not be verified after round was complete!')

    def check_integrity_pre(self):
        """ Verify that the game elements are set up correctly. """
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
        """ Verify that the game elements have been cleaned up correctly and that
            all cards are accounted for.
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
        """ Looks at all cards that are faceup in the game environment and adds
            them to the list of exposed cards.
        """
        exposed = []
        for s in self.table:
            exposed.extend(s.hand.get_upcards())
        return exposed

    def highhand(self):
        """ Finds which player has the highest showing hand and return their seat
            index.  For stud games, after the first street, the high hand on
            board initiates the action (a tie is broken by position, with the
            player who received cards first acting first).
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
            s = None
            # Process ties, get the player who was dealt first.
            for s in self.table.get_players(hascards=True):
                if s in ties:
                    _logger.debug('Seat {} was dealt first, returning its index.'.format(s.NUM))
                    return s.NUM
        else:
            _logger.debug('Seat {} has high hand, returning its index.'.format(s.NUM))
            return seat.NUM

    def position_by_button(self):
        """ Get position based on button. """
        if self.table.TOKENS['D'] == -1:
            raise Exception('Cannot set bettor or closer in the if button isn\'t set!')

        if self.street == 0:
            return self.table.next_player(self.table.TOKENS['BB'])
        else:
            return self.table.next_player(self.table.TOKENS['D'], hascards=True)

    def position_by_upcards(self):
        """ Override the base Round get_utg, and get position based on upcards. """
        if self.street == 0:
            return self.table.TOKENS['BI']
        else:
            return self.highhand()


class StudRound(Round):
    """A poker Round customized for playing Stud games.
        Notable differences in Stud games:
        * Uses Antes
        * Uses a Bringin 'blind' to determine the first player to act.
        * Uses the highhand on board to determine position
    """
    def __init__(self, session):
        super().__init__(session)
        # super(StudRound, self).__init__(self)
        self.get_utg = self.position_by_upcards


class ButtonRound(Round):
    """ A poker Round customized for playing poker games with a dealer button
        (holdem, omaha, draw5)
        Notable differences in Button games:
        * Uses a small blind and big blind.
        * Uses the the dealer button to determine position
        * The button is moved 1 seat clockwise at the beginning of every round.
    """

    def __init__(self, session):
        super().__init__(session)
        # super(ButtonRound, self).__init__(self)
        self.get_utg = self.position_by_button
