"""
  " Tools for rounding numbers and managing miscellaneous aspects of floats and integers.
  """
import math


def round_number(num):
    """ Rounds a number up or down  """
    if num % 1 >= 0.5:
        return math.ceil(num)
    else:
        return math.floor(num)


def fmtnum(num):
    """ Formats the given number so that if it has decimal points it will display
        them, and if it is a plain integer, it will not display the decimal point
        or decimals.
    """
    if num % 1 > 0:
        return '{:.2f}'.format(num)
    else:
        return '{}'.format(int(num))


def cleannum(num):
    if num % 1 > 0:
        return num
    else:
        return int(num)


def is_integer(num):
    """ Returns True if the num argument is an integer, and False if it is not. """
    try:
        num = float(num)
    except ValueError:
        return False

    return num.is_integer()
