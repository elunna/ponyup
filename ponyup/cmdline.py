#!/usr/bin/env python3
import cmd
import textwrap
from ponyup import blinds
from ponyup import lobby
from ponyup import logger
from ponyup import names
from ponyup import player_db

DISPLAYWIDTH = 70
DEFAULT_PLAYER = 'luna'
LOGO = 'data/logo2.txt'
_logger = logger.get_logger(__name__)


class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "/): "
        self.intro = logo()
        self.hero = player_db.load_player(DEFAULT_PLAYER)
        self.lobby = lobby.Lobby()
        self.game = self.lobby.default()

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

    def do_info(self, args):
        """
        View current game info and settings.
        """
        print('-=- Game info -=-'.center(DISPLAYWIDTH))
        playertxt = ''
        if self.hero:
            playertxt = '{}(${})'.format(self.hero, self.hero.bank)

        print('{:15} {}'.format('Player:', playertxt))
        print('{:15} {}'.format('Table Name:', self.game.tablename))
        print('{:15} {}'.format('Game:', self.game.game))
        print('{:15} {}'.format('Stakes:', blinds.get_stakes(self.game.level)))
        print('{:15} {}'.format('Seats:', self.game.seats))

    def do_games(self, args):
        """
        View the available games.
        """
        sub_cmd = GameSelection()
        sub_cmd.cmdloop()
        if sub_cmd.game:
            self.game = sub_cmd.game

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


def logo():
    txt = ''
    with open(LOGO) as f:
        for l in f.readlines():
            txt += l
    txt += '\n' + '~'*70 + '\n'
    return txt


def is_integer(num):
    """
    Returns True if the num argument is an integer, and False if it is not.
    """
    try:
        num = float(num)
    except:
        return False

    return num.is_integer()
