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
