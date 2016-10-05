#!/usr/bin/env python3
import cmd
from ponyup import blinds
from ponyup import lobby
from ponyup import player

DISPLAYWIDTH = 70
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

    def do_new(self, args):
        """
        Create a new player.
        """
        hero = player.create_player(args)
        if hero:
            print('Created player {}'.format(hero))
            self.hero = player.load_player(args)
        else:
            print('Create player failed.')

    def do_load(self, args):
        """
        Load a player.
        """
        hero = player.load_player(args)
        if hero:
            print('{} loaded.'.format(hero))
            self.hero = hero
        else:
            print('Player load error.')

    def do_del(self, args):
        """
        Delete a player.
        """
        result = player.del_player(args)
        if result:
            print('Player {} deleted.'.format(args))
            if self.hero is not None and args == self.hero.name:
                self.hero = None
        else:
            print('Delete player error.')

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
