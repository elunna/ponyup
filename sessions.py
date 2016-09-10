import betting
import colors
import poker
import options

DISPLAYWIDTH = 70
GAMES = {
    #  'OMAHA': [1, 1, 2, 2],
    #  'HOLDEM': [1, 1, 2, 2],
    'FIVE CARD DRAW': [1, 2],
    'FIVE CARD STUD': [1, 1, 2, 2],
    #  'SEVEN CARD STUD': [1, 1, 2, 2, 2],
}


class Session():
    """
    The Session object manages the general structure of a poker game. It sets up the essentials:
        game type, the table, and stakes.
    """
    def __init__(self, gametype, table, blinds):
        """
        Initialize the poker Session settings.
        """
        self.gametype = gametype
        self.rounds = 1
        self._table = table
        self.streets = GAMES[gametype]
        self.blinds = blinds
        self.options = options.OPTIONS

    def __str__(self):
        """
        Returns the Session info.
        """
        _str = '{} {}'.format(self.blinds.stakes(), self.gametype)
        rnd_str = 'Round: {:<5}\n'.format(self.rounds)
        _str += rnd_str.rjust(DISPLAYWIDTH - len(_str))

        return _str

    def new_round(self):
        return poker.Round(self)

    def play(self):
        """
        Defines the structure of how a single hand in the poker game is played.
        """
        print('Stub play function')

    def betting_round(self, _round):
        """
        Run through a round of betting. Returns a victor if it exists.
        """
        print(self._table)
        br = betting.BettingRound(_round)

        for p in br:
            o = br.player_decision(p)
            br.process_option(o)
            print(br.action_string(o))
            if self.options['debug']:
                print('Bet: {} Betlevel: {}'.format(br.bet, br.level()))

        print(_round)           # Display pot

    def found_winner(self, _round):
        victor = _round.one_left()
        if victor is None:
            _round.next_street()
            return False
        else:
            # One player left, award them the pot!
            oneleft = 'Only one player left!'.rjust(70)
            print(colors.color(oneleft, 'LIGHTBLUE'))
            _round.award_pot(victor, _round.pot)
            return True
