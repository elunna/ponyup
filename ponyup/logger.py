import datetime
import logging

DEBUG_FILE = 'logs/debug.log'
INFO_FILE = 'logs/info.log'
LOGDIR = 'logs/'


def get_logger(name):
    # Logger setup
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Setup file handlers
    debug_fh = logging.FileHandler(DEBUG_FILE)
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
    ch.setFormatter(info_fmt)

    # Add handlers to logger
    logger.addHandler(debug_fh)
    logger.addHandler(info_fh)
    #  logger.addHandler(ch)
    return logger


def hh_logname(session):
    dt = datetime.datetime
    stakes = '${}-${}'.format(session.blinds.SMBET, session.blinds.SMBET * 2)
    filename = 'HH_{}_-_{}_{}_{}(Pony Bits)'.format(
        dt.now().strftime('%Y%m%d'),
        session.table.name,
        session.gametype,
        stakes
    )
    return LOGDIR + filename


def round_header(_round):
    dt = datetime.datetime
    date = dt.today()
    time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    header = 'PonyUp Poker Game ID# {}: Table {} - {} - {} - {}\n'.format(
        _round.gameid,
        _round.table.name,
        _round.blinds.stakes(),
        _round.gametype,
        time,
        date)
    return header
