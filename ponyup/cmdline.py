#!/usr/bin/env python3
import cmd
from ponyup import player
from ponyup import lobby
DEFAULT_PLAYER = 'luna'
LOGO = 'data/logo2.txt'


def logo():
    txt = ''
    with open(LOGO) as f:
        for l in f.readlines():
            txt += l
    txt += '\n' + '~'*70 + '\n'
    return txt


class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "/): "
        self.intro = logo()
        self.hero = player.load_player(DEFAULT_PLAYER)
        self.lobby = lobby.Lobby()
        self.game = self.lobby.default()

    def do_quit(self, args):
        """
        Leaves the game.
        """
        return True

    def do_load(self, args):
        """
        Load a player.
        """

    def do_new(self, args):
        """
        Create a new player.
        """

    def do_games(self, args):
        """
        View the available games.
        """

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
