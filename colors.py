from functools import wraps
CSI = "\x1b["
CSI_end = "\x1b[0m"
#  reset = CSI + "m"


STYLES = {
    'NORMAL': 0,
    'BOLD': 1,
    'FADE': 2,
    'ITALIC': 3,
    'UNDERLINE': 4,
}

COLORS = {
    'RED': 31,
    'GRAY': 40,
    'GREEN': 32,
    'YELLOW': 33,
    'BLUE': 34,
    'PURPLE': 35,
    'LIGHTBLUE': 36,
    'WHITE': 37,
}


def color(string, fg, bg='GRAY', STYLE='NORMAL'):
    """
    Returns a colored version of the given string. Can specify the foreground color, background
    color, and style of returned text.
    """
    if fg.upper() in COLORS:
        return '{}{};{};{}m{}{}'.format(
            CSI,
            STYLES[STYLE],
            COLORS[fg.upper()],
            COLORS[bg.upper()],
            string,
            CSI_end)
    else:
        raise ValueError('Passed arg color is not in the available colors!')


def colorit(c):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return '{}{};{};{}m{}{}'.format(
                CSI, STYLES['NORMAL'], COLORS[c.upper()], 40, result, CSI_end)

            return func(*args, **kwargs)
        return wrapper
    return decorate


@colorit('yellow')
def pot(p):
    return 'pot={}'.format(p)


if __name__ == "__main__":
    print(pot(10))
