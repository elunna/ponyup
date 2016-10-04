#!/usr/bin/env python3
import logging

FILENAME = 'data/poker.log'


def get_logger(name, filename=FILENAME):
    # Logger setup
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Setup file handler
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)

    # Setup console stream handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Setup formatting
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    #  logger.addHandler(ch)
    return logger
