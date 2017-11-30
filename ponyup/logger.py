from ponyup import card
from ponyup import colors
import datetime
import logging
import types

DEBUG_FILE = 'logs/debug.log'
INFO_FILE = 'logs/info.log'
LOGDIR = 'logs/'
old_factory = logging.getLogRecordFactory()

cards = (
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac',
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
)


def color_card(text):
    if text in cards:
        return colors.color_tuple(card.COLORS[text[1]])
    elif text == 'Xx':
        return colors.color_tuple('PURPLE')
    else:
        return None


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

    card_tup = color_card(msg.strip())
    if card_tup:
        return card_tup
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

    # This allows us to attach the display method to the logger so we can print
    # lists of strings. We have to use types.MethodType because just attaching
    # it doesn't work
    logger.display = types.MethodType(display, logger)

    return logger


def display(self, list_o_strings):
    for s in list_o_strings:
        self.info(s)


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
