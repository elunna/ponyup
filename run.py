#!/usr/bin/env python3
"""
Runs the console version.
"""
#  from ponyup import console
from ponyup import cmdline


if __name__ == "__main__":
    game = cmdline.Game()
    game.cmdloop()
