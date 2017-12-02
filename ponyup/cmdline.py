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
        """Create a new player.
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
        """Load a player.
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
        """Save the current player's info.
        Usage: save
        :> save
        """
        if self.casino.save_player():
            _logger.info("Saved '{}' successfully!\n".format(self.casino.hero))
        else:
            _logger.info("Save failed for '{}'!\n".format(self.casino.hero))

    def do_del(self, args):
        """Delete a player.
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

    def do_game(self, args):
        """Select a table game to play at.
        Usage: game
        You will be presented with a list of all the games, then just select one.
        """
        games = lobby.sort_by_stakes(self.lobby.all_tables())
        _logger.display(lobby.numbered_list(games))

        valid_choices = list(range(len(games)))

        try:
            choice = int(input('Pick a game to play :> '))
        except ValueError:
            _logger.info('Not a valid game... staying with default\n')
            return

        if choice in valid_choices:
            g = games[choice]
            self.casino.set_game(g)
            _logger.info('Game set to {}\n'.format(g.tablename))
        else:
            _logger.info('Not a valid game...\n')

    def do_credits(self, args):
        """View game producer credits. """
        _logger.info(credits)

    def do_options(self, args):
        """View and edit game options. """
        pass

    def do_play(self, args):
        """Play the selected game.
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

        # Launch a new shell for playing the Session and Rounds
        play_session(self.casino.make_session(buyin))

        self.do_save(None)

    def do_quit(self, args):
        """Leaves the game . """
        # self.postcmd(True, args)
        _logger.info('Goodbye!\n')
        exit()
        # return True

    def menu(self):
        """Display the logo """

        with open(LOGO) as f:
            for l in f.read():
                _logger.info(l)
        _logger.info('~'*70 + '\n')

        self.casino.get_info()

    def postcmd(self, stop, args):
        if args not in ['help', 'h', '?']:
            input('Press any key')
            os.system('clear')
            self.menu()

    def do_c(self, args):
        """Alias for credits command"""
        return self.do_credits(args)

    def do_d(self, args):
        """Alias for del command"""
        return self.do_del(args)

    def do_g(self, args):
        """Alias for game command"""
        return self.do_game(args)

    def do_h(self, args):
        """Alias for help command"""
        return self.do_help(args)

    def do_l(self, args):
        """Alias for load command"""
        return self.do_load(args)

    def do_n(self, args):
        """Alias for new command"""
        return self.do_new(args)

    def do_o(self, args):
        """Alias for options command"""
        return self.do_options(args)

    def do_p(self, args):
        """Alias for play command"""
        return self.do_play(args)

    def do_q(self, args):
        """Alias for quit command"""
        return self.do_quit(args)

    def do_s(self, args):
        """Alias for save command"""
        return self.do_save(args)


def play_session(session):
    # Play as long as the hero has money

    hero_seat = session.find_hero()
    while True:
        os.system('clear')
        session.play()

        if hero_seat.stack == 0:
            _logger.info('You busted!\n')
            break

        session.table_maintainance()

        _logger.info('Keep playing[enter], [q]uit.\n')
        c = input(':> ')
        if c.lower().startswith('q'):
            break

    session.find_hero().standup()
