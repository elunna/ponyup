#!/usr/bin/env python3
import logging


def get_logger(name):
    # Logger setup
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Setup file handler
    fh = logging.FileHandler('data/poker.log')
    fh.setLevel(logging.DEBUG)

    # Setup console stream handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Setup formatting
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    #  logger.addHandler(ch)
    return logger
