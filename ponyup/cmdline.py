#!/usr/bin/env python3
"""
  " The command line interface for playing the ponyup game.
  """
import cmd
import os
from ponyup import casino
from ponyup import lobby


DISPLAYWIDTH = 80
LOGO = 'data/logo.txt'


class Game(cmd.Cmd):
    """ Command-line console interface for the PonyUp card casino. """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "/): "
        self.casino = casino.Casino()
        self.lobby = lobby.Lobby()
        os.system('clear')
        self.intro = self.logo()

    def do_quit(self, args):
        # pylint: disable=unused-argument, no-self-use
        """ Leaves the game . """
        return True

    def do_new(self, args):
        """ Create a new player.  """
        self.casino.new_player(args)

    def do_players(self, args):
        # pylint: disable=unused-argument, no-self-use
        print(self.casino.list_players())

    def do_load(self, args):
        """ Load a player.  """
        self.casino.load_player(args)

    def do_save(self, args):
        """ Save the current player's info.  """
        # pylint: disable=unused-argument
        self.casino.save_player()

    def do_del(self, args):
        """ Delete a player.  """
        self.casino.delete_player(args)

    def do_info(self, args):
        """ View current game info and settings.  """
        # pylint: disable=unused-argument
        print(self.casino.get_info())

    def do_games(self, args):
        """ View the available games.  """
        # pylint: disable=unused-argument, bad-builtin
        games = lobby.sort_by_stakes(self.lobby.all_tables())
        print(lobby.numbered_list(games))

        valid_choices = list(range(len(games)))

        try:
            choice = int(input('Pick a game to play :> '))
        except ValueError:
            print('Not a valid number...')
            return

        if choice in valid_choices:
            g = games[choice]
            self.casino.set_game(g)
            print('Game set to {}'.format(g.tablename))
        else:
            print('Not a valid game...')

    def do_credits(self, args):
        """ View game producer credits.  """

    def do_options(self, args):
        """ Go to game options """
        pass

    def do_play(self, args):
        """ Play the selected game. Supply a buyin amount or use the default buyin. """
        if not args:
            print('Getting default buyin')
            buyin = self.casino.default_buyin()
        else:
            try:
                buyin = int(buyin)
            except:
                print('Amount needs to be an integer!')
                print('You need to enter a number for the buyin!')
                return False

        if not self.casino.valid_buyin(buyin):
            return False

        sesh = self.casino.make_session(buyin)

        # Launch a new shell for playing the Session and Rounds
        sub_cmd = SessionInterpreter(sesh)
        sub_cmd.cmdloop()
        self.do_save(None)

    def logo(self):
        """ Display the logo """
        txt = ''
        with open(LOGO) as f:
            for l in f.readlines():
                txt += l
        txt += '\n' + '~'*70 + '\n'

        txt += self.casino.get_info()
        return txt


class SessionInterpreter(cmd.Cmd):
    """ Runs through an ongoing session of poker. """
    def __init__(self, session):
        cmd.Cmd.__init__(self)
        self.session = session
        self.playing = True
        self.play_round()
        self.prompt = 'Press enter to play again, or "quit" to go back to the lobby.'

    def emptyline(self):
        self.play_round()

    def play_round(self):
        os.system('clear')
        self.session.play()
        self.post_round()

    def post_round(self):
        """ Perform post round checks """
        # pylint: disable=bad-builtin
        # Check if hero went broke
        if self.session.find_hero().stack == 0:
            rebuy = input('Rebuy?')
            if not self.valid_buyin(rebuy):
                self.do_quit(None)
            else:
                self.session.find_hero().buy_chips(rebuy)

        self.session.table_maintainance()

    def do_quit(self, args):
        """ Quits the poker session. """
        # pylint: disable=unused-argument
        self.session.find_hero().standup()
        return True
