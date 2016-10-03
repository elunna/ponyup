#!/usr/bin/env python3
import cmd


class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "/): "

    def do_quit(self, args):
        """
        Leaves the game.
        """
        return True

    def do_load(self, args):
        """
        Load a player.
        """

    def do_save(self, args):
        """
        Save a player.
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


if __name__ == "__main__":
    game = Game()
    game.cmdloop()
