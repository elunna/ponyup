from ponyup import colors
import datetime
import logging

DEBUG_FILE = 'logs/debug.log'
INFO_FILE = 'logs/info.log'
LOGDIR = 'logs/'
old_factory = logging.getLogRecordFactory()


def color_stuff(msg):
    if 'fold' in msg:
        return colors.color_tuple('PURPLE')
    elif 'check' in msg:
        return colors.color_tuple('WHITE')
    elif 'allin' in msg:
        return colors.color_tuple('WHITE')
    elif 'call' in msg:
        return colors.color_tuple('WHITE')
    elif 'bet' in msg:
        return colors.color_tuple('RED')
    elif 'raise' in msg:
        return colors.color_tuple('RED')
    elif '$' in msg:
        return colors.color_tuple('YELLOW')
    else:
        return '', ''


class ContextFilter(logging.Filter):
    """ This is a filter which injects contextual information into the log.  """
    def filter(self, record):
        act_str = record.getMessage()

        record.begin, record.end = color_stuff(act_str)

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
    """ Returns a list of strings for the header"""
    dt = datetime.datetime
    time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    header = []
    header.append('PonyUp Game ID {}: {} - '.format(_round.gameid, _round.gametype))
    header.append('{}'.format(_round.blinds.stakes()))
    header.append('\n')
    header.append('{} - {}\n'.format(_round.table.name, time))
    return header
