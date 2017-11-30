#!/usr/bin/env python3
"""
  " The command line interface for playing the ponyup game.
  """
import cmd
import os
from ponyup import casino
from ponyup import lobby
from ponyup import logger

_logger = logger.get_logger(__name__)


DISPLAYWIDTH = 80
LOGO = 'data/logo2.txt'

credits = """
Author: Erik Lunna
Web Portfolio: http://eslunna.byethost24.com
Location: Minnesota

Erik is a passionate Python developer originally from Vermont but now settled in
Minnesota. He loves music, drumming, poker, beer, and solving puzzles.

This project started as an exploration of what Java could do - I wanted to see
if I could make a typical 5-card draw program in Java. I eventually was able to
get it into a simple format where you play a Video Poker machine and I created a
GUI for that in Netbeans. I also made a small multiplayer CPU capability, you
could play 6 players at 5 card draw, but my limited design skills made the code
quickly grow out of control and I let it rest for a while.  Then a couple of
years later I discovered Python and how friendly it was, and I figured a good
way to learn Python would be to remake my poker program with it.  This time I
separated out things a lot better (although I still need lots of discipline with
that!) and incorporated MUCH MORE testing.  So far it can do a lot but I know
I'm just scratching the surface and want to take this as far as I can and
incorporated MUCH MORE testing.

I would like to thank:
    My family, my mom for being so creative and helping me be an out of the box
    thinker and my dad for infusing me with an iron-clad work ethic. And my
    sister for always pushing me to reach further.
    And of course, Anna! :)
"""


class Game(cmd.Cmd):
    """ Command-line console interface for the PonyUp card casino. """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "(ponyup) :> "
        self.casino = casino.Casino()
        self.lobby = lobby.Lobby()
        os.system('clear')
        self.intro = self.menu()

    def do_new(self, args):
        """ Create a new player.
        Usage: new <player>
        ex: To create a new player "erik"
        :> new erik
        """
        if not args.strip():
            _logger.info('No name specified for the new player!\n')
        elif self.casino.new_player(args):
            _logger.info("Successfully created new player '{}'\n".format(args))
        else:
            _logger.info("Failed to create new player '{}'\n".format(args))

    def do_load(self, args):
        """ Load a player.
        Usage: load <player>
        ex: To load player "erik"
        :> load erik
        """
        if not args.strip():
            _logger.info('No name specified!\n')
        elif self.casino.load_player(args):
            _logger.info('Loaded {} successfully!\n'.format(self.casino.hero))
        else:
            _logger.info("Load failed for '{}'!\n".format(self.casino.hero))
            _logger.info('Here are all the available players:\n')
            _logger.info(self.casino.list_players())

    def do_save(self, args):
        """ Save the current player's info.
        Usage: save
        :> save
        """
        if self.casino.save_player():
            _logger.info("Saved '{}' successfully!\n".format(self.casino.hero))
        else:
            _logger.info("Save failed for '{}'!\n".format(self.casino.hero))

    def do_del(self, args):
        """ Delete a player.
        Usage: del <player>
        ex: To delete player "erik"
        :> del erik
        """
        if not args.strip():
            _logger.info('No name specified!\n')
        elif self.casino.delete_player(args):
            _logger.info("Successfully deleted '{}'!\n".format(args))
        else:
            _logger.info("Delete failed for '{}'!\n".format(args))
            _logger.info('Here are all the available players:\n')
            _logger.info(self.casino.list_players())

    def do_table(self, args):
        """ Select a table to play at.
        Usage: table
        You will be presented with a list of all the tables, then just select one.
        """
        games = lobby.sort_by_stakes(self.lobby.all_tables())
        _logger.info(lobby.numbered_list(games))

        valid_choices = list(range(len(games)))

        try:
            choice = int(input('Pick a game to play :> '))
        except ValueError:
            _logger.info('Not a valid table... staying with default\n')
            return

        if choice in valid_choices:
            g = games[choice]
            self.casino.set_game(g)
            _logger.info('Game set to {}\n'.format(g.tablename))
        else:
            _logger.info('Not a valid game...\n')

    def do_credits(self, args):
        """ View game producer credits. """
        _logger.info(credits)

    def do_options(self, args):
        """ View and edit game options. """
        pass

    def do_play(self, args):
        """ Play the selected game.
        Supply a buyin amount or use the default buyin.

        Usage: play or play <buyin amount>
        ex: To play for the default
        :> play

        ex: To play for 100 chips
        :> play 100

        """
        if not args:
            _logger.info('Getting default buyin.\n')
            buyin = self.casino.default_buyin()
        else:
            try:
                buyin = int(buyin)
            except:
                _logger.info('Amount needs to be an integer!.')
                _logger.info('You need to enter a number for the buyin!.')
                return False

        if not self.casino.valid_buyin(buyin):
            return False

        sesh = self.casino.make_session(buyin)

        # Launch a new shell for playing the Session and Rounds
        sub_cmd = SessionInterpreter(sesh)
        sub_cmd.cmdloop()
        self.do_save(None)

    def do_quit(self, args):
        """ Leaves the game . """
        # self.postcmd(True, args)
        _logger.info('Goodbye!\n')
        exit()
        # return True

    def menu(self):
        """ Display the logo """

        with open(LOGO) as f:
            for l in f.read():
                _logger.info(l)
        _logger.info('~'*70 + '\n')

        self.casino.get_info()

    def postcmd(self, stop, args):
        if args != 'help':
            input('Press any key')
            os.system('clear')
            _logger.info(self.menu())


class SessionInterpreter(cmd.Cmd):
    """ Runs through an ongoing session of poker. """
    def __init__(self, session):
        cmd.Cmd.__init__(self)
        self.session = session
        self.playing = True
        self.play_round()
        self.prompt = 'Press enter to play again, or "[q]uit" to go back to the lobby.'

    def emptyline(self):
        self.play_round()

    def play_round(self):
        os.system('clear')
        self.session.play()
        self.post_round()

    def post_round(self):
        """ Perform post round checks """
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
        self.session.find_hero().standup()
        return True
