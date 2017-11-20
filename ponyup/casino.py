"""
  " Manages elements in the casino - the players file, tables, and cashier.
  """
import json
from ponyup import blinds
from ponyup import factory
from ponyup import lobby
from ponyup import player_db

DISPLAYWIDTH = 80
SETTINGS = 'data/settings.json'
DEFAULT_PLAYER = 'luna'
DEFAULT_STACK = 20  # Big blinds
MINIMUM_STACK = 5  # Big blinds


class Casino(object):
    """ Manages the lobby and game environment for the player. """

    def __init__(self):
        self.lobby = lobby.Lobby()
        self.settings = load_settings()
        self.hero = player_db.load_player(self.settings['hero'])
        self.game = self.lobby.get_game(self.settings['game'])

    def save_settings(self):
        """ Write the game as the new default in the settings """
        with open(SETTINGS, 'w') as f:
            json.dump(self.settings, f)

    def get_info(self):
        """ Return a string containing the game info. """
        _str = ''
        title = '-=- Game info -=-'.center(DISPLAYWIDTH)
        _str += title + '\n'

        playertxt = ''
        if self.hero:
            playertxt = '{}(${})'.format(self.hero, self.hero.bank)
            _str += '{:15} {}\n'.format('Player:', playertxt)
        else:
            _str += '{:15} {}\n'.format('Player:', 'n/a')

        if self.game:
            _str += '{:15} {}\n'.format('Table Name:', self.game.tablename)
            _str += '{:15} {}\n'.format('Game:', self.game.game)
            _str += '{:15} {}\n'.format('Stakes:', blinds.get_stakes(self.game.level))
            _str += '{:15} {}\n'.format('Seats:', self.game.seats)
        else:
            _str += '{:15} {}\n'.format('Game:', 'n/a (use the "games" command to set the game.')

        return _str

    def list_players(self):
        return player_db.get_players()

    def new_player(self, args):
        """ Create a new player. """
        if player_db.new_player(args):
            self.hero = player_db.load_player(args)

    def load_player(self, name):
        """ Load a player. """
        hero = player_db.load_player(name)
        if hero:
            self.hero = hero
            self.settings['hero'] = self.hero.name
            self.save_settings()

    def save_player(self):
        """ Save the current player's info to the database. """
        if player_db.update_player(self.hero):
            print('Saved {} successfully!'.format(self.hero))
        else:
            print('Save failed!')

    def delete_player(self, name):
        """ Delete a player from the database. """
        if player_db.del_player(name):
            # Check if we deleted the current player
            if self.hero is not None:
                if name == self.hero.name:
                    # Reset current player
                    self.hero = None
                    self.settings['hero'] = 'None'
                    self.save_settings()

    def valid_buyin(self, buyin):
        """ Returns True if the player has a valid buyin amount, False otherwise. """
        minbuyin = blinds.stakes[self.game.level] * MINIMUM_STACK

        # Check hero bank
        if self.hero.bank < minbuyin:
            print('You don\'t have enough chips to buyin to this game!')
            return False

        # Check the buyin
        if buyin >= minbuyin:
            return True
        else:
            print('The minimum buy-in is ${} bits.'.format(minbuyin))
            return False

    def default_buyin(self):
        return blinds.stakes[self.game.level] * DEFAULT_STACK

    def make_session(self, buyin):
        """ Creates a Session from the current settings. """

        sesh = factory.session_factory(
            seats=self.game.seats,
            game=self.game.game,
            tablename=self.game.tablename,
            level=self.game.level,
            hero=self.hero,
            names='random',
            herobuyin=buyin,
            varystacks=True,
        )
        return sesh

    def set_game(self, game):
        """ View the available games."""
        self.game = game


def load_settings():
    with open(SETTINGS, 'r') as f:
        settings = f.read()
        return json.loads(settings)
