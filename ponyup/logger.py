#!/usr/bin/env python3
import logging

DEBUG_FILE = 'logs/debug.log'
INFO_FILE = 'logs/info.log'


def get_logger(name, filename=DEBUG_FILE):
    # Logger setup
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Setup file handlers
    debug_fh = logging.FileHandler(filename)
    debug_fh.setLevel(logging.DEBUG)

    info_fh = logging.FileHandler(INFO_FILE)
    info_fh.setLevel(logging.INFO)

    # Setup console stream handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Setup formatting
    debug_fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    info_fmt = logging.Formatter('%(message)s')
    debug_fh.setFormatter(debug_fmt)
    info_fh.setFormatter(info_fmt)
    ch.setFormatter(debug_fmt)

    # Add handlers to logger
    logger.addHandler(debug_fh)
    logger.addHandler(info_fh)
    #  logger.addHandler(ch)
    return logger
