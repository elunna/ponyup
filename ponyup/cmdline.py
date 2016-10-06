#!/usr/bin/env python3
import cmd
import json
import os
import textwrap
from ponyup import blinds
from ponyup import factory
from ponyup import lobby
from ponyup import logger
from ponyup import names
from ponyup import player_db

DISPLAYWIDTH = 70
DEFAULT_PLAYER = 'luna'
DEFAULT_STACK = 25  # Big blinds
MINIMUM_STACK = 10  # Big blinds
LOGO = 'data/logo2.txt'
SETTINGS = 'data/settings.json'
_logger = logger.get_logger(__name__)


class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "/): "
        self.lobby = lobby.Lobby()
        self.hero, self.game = None, None
        self.load_settings()

        os.system('clear')
        self.intro = self.logo()

    def load_settings(self):
        with open(SETTINGS, 'r') as f:
            settings = f.read()
            self.settings = json.loads(settings)

        self.hero = player_db.load_player(self.settings['hero'])
        self.game = self.lobby.get_game(self.settings['game'])

    def save_settings(self):
        # Write the game as the new default in the settings
        with open(SETTINGS, 'w') as f:
            json.dump(self.settings, f)

    def get_info(self):
        """
        Return a string containing the game info.
        """
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

    ###################
    # THROWAWAY TEST FUNC
    def do_win(self, args):
        print('Hero won $100!!!!!')
        self.hero.bank += 100

    def do_quit(self, args):
        """
        Leaves the game.
        """
        return True

    def do_new(self, args):
        """
        Create a new player.
        """
        if player_db.new_player(args):
            self.hero = player_db.load_player(args)

    def do_players(self, args):
        print(player_db.get_players())

    def do_load(self, args):
        """
        Load a player.
        """
        hero = player_db.load_player(args)
        if hero:
            self.hero = hero
            self.settings['hero'] = self.hero.name
            self.save_settings()

    def do_save(self, args):
        """
        Save the current player's info.
        """
        if player_db.update_player(self.hero):
            print('Saved {} successfully!'.format(self.hero))
        else:
            print('Save failed!')

    def do_del(self, args):
        """
        Delete a player.
        """
        if player_db.del_player(args):
            # Check if we deleted the current player
            if self.hero is not None:
                if args == self.hero.name:
                    # Reset current player
                    self.hero = None
                    self.settings['hero'] = 'None'
                    self.save_settings()

    def do_info(self, args):
        """
        View current game info and settings.
        """
        print(self.get_info())

    def do_games(self, args):
        """
        View the available games.
        """
        sub_cmd = GameSelection()
        sub_cmd.cmdloop()
        if sub_cmd.game:
            self.game = sub_cmd.game
            self.settings['game'] = self.game.tablename
            self.save_settings()

    def do_names(self, args):
        """
        View the stored CPU names.
        """
        namelist = ', '.join(names.get_names_from_db())
        for line in textwrap.wrap(namelist, 80):
            print(line)

    def do_combos(self, args):
        """
        View all combinations in a deck of cards.
        """

    def do_credits(self, args):
        """
        View game producer credits.
        """

    def do_options(self, args):
        """
        Go to game options
        """

    def valid_buyin(self, amt):
        minbuyin = blinds.stakes[self.game.level] * MINIMUM_STACK

        # Check hero bank
        if self.hero.bank < minbuyin:
            print('You don\'t have enough chips to buyin to this game!')
            return False

        # Check the buyin
        if not is_integer(amt):
            print('Invalid buyin!')
            return False
        elif int(amt) < minbuyin:
            print('The minimum buy-in is ${} bits.'.format(minbuyin))
            return False
        else:
            return True

    def valid_settings(self):
        if self.hero is None or self.game is None:
            print('Game or player has not been set!')
            return False
        else:
            return True

    def do_play(self, args):
        """
        Play the selected game. Supply a buyin amount or use the default buyin.
        """
        if not self.valid_settings():
            return False

        if args:
            if self.valid_buyin(args):
                buyin = int(args)
            else:
                return False
        else:
            buyin = blinds.stakes[self.game.level] * DEFAULT_STACK

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

        # Launch a new shell for playing the Session and Rounds
        sub_cmd = SessionInterpreter(sesh)
        sub_cmd.cmdloop()

    def logo(self):
        txt = ''
        with open(LOGO) as f:
            for l in f.readlines():
                txt += l
        txt += '\n' + '~'*70 + '\n'

        txt += self.get_info()
        return txt


class GameSelection(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "games:> "
        self.game = None
        self.tables = lobby.sort_by_stakes(lobby.Lobby().all_tables())
        self.valid_choices = list(range(len(self.tables)))

        print(lobby.numbered_list(self.tables))

    def precmd(self, args):
        if is_integer(args):
            i = int(args)
            if i in self.valid_choices:
                self.game = self.tables[i]
        return args

    def onecmd(self, args):
        if self.game or args.lower().startswith('q'):
            return True


class SessionInterpreter(cmd.Cmd):
    def __init__(self, session):
        cmd.Cmd.__init__(self)
        self.session = session
        self.playing = True

    def emptyline(self):
        os.system('clear')
        self.session.play()

    def postcmd(self, emptyline, stop=False):
        # Check if hero went broke
        if self.session.find_hero().stack == 0:
            rebuy = input('Rebuy?')
            if not self.valid_buyin(rebuy):
                self.do_quit()
            else:
                self.session.find_hero().buy_chips(rebuy)

        self.session.table_maintainance()

    def do_quit(self, args):
        self.session.find_hero().standup()
        self.do_save(None)
        return True


def is_integer(num):
    """
    Returns True if the num argument is an integer, and False if it is not.
    """
    try:
        num = float(num)
    except:
        return False

    return num.is_integer()
