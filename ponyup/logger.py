from ponyup import colors
import datetime
import logging

DEBUG_FILE = 'logs/debug.log'
INFO_FILE = 'logs/info.log'
LOGDIR = 'logs/'
old_factory = logging.getLogRecordFactory()


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def filter(self, record):
        record.begin, record.end = '', ''

        act_str = record.getMessage()

        if 'fold' in act_str:
            record.begin, record.end = colors.color_tuple('PURPLE')
        elif 'check' in act_str:
            record.begin, record.end = colors.color_tuple('WHITE')
        elif 'allin' in act_str:
            record.begin, record.end = colors.color_tuple('WHITE')
        elif 'call' in act_str:
            record.begin, record.end = colors.color_tuple('WHITE')
        elif 'bet' in act_str:
            record.begin, record.end = colors.color_tuple('RED')
        elif 'raise' in act_str:
            record.begin, record.end = colors.color_tuple('RED')

        return True


def get_logger(name):
    # Logger setup
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # logging.setLogRecordFactory(record_factory)

    # Setup file handlers
    debug_fh = logging.FileHandler(DEBUG_FILE)
    debug_fh.setLevel(logging.DEBUG)

    info_fh = logging.FileHandler(INFO_FILE)
    info_fh.setLevel(logging.INFO)

    # Setup console stream handler
    ch = logging.StreamHandler()
    ch.terminator = ''
    ch.setLevel(logging.INFO)

    # Setup formatting
    debug_fmt = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s',
                                  "%d-%m-%y %H:%M:%S")
    info_fmt = logging.Formatter('%(message)s')

    con_fmt = logging.Formatter('%(begin)s%(message)s%(end)s')
    # con_fmt = logging.Formatter('%(message)s')

    debug_fh.setFormatter(debug_fmt)
    info_fh.setFormatter(info_fmt)
    ch.setFormatter(con_fmt)

    # Custom filter
    cfilter = ContextFilter()
    ch.addFilter(cfilter)

    # Add handlers to logger
    logger.addHandler(debug_fh)
    logger.addHandler(info_fh)
    logger.addHandler(ch)
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
