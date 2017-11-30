#!/usr/bin/env python3

import time
from ponyup import war

if __name__ == '__main__':
    # The main game loop that controls the game flow.
    GAME = war.War()

    while True:
        GAME.show_stacks()
        time.sleep(GAME.delay)
        GAME.playround()

        if GAME.shuffle_between_rounds:
            GAME.shuffle()
