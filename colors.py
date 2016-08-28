CSI = "\x1b["
CSI_end = "\x1b[0m"
#  reset = CSI + "m"
STYLE = 0

COLORS = {
    'RED': 31,
    'GRAY': 40,
    'GREEN': 32,
    'YELLOW': 33,
}


def color(string, color):
    if color.upper() in COLORS:
        return '{}{};{};{}m{}{}'.format(
            CSI,
            STYLE,
            COLORS[color.upper()],
            COLORS[color.upper()],
            string,
            CSI_end)
    else:
        raise ValueError('Passed arg color is not in the available colors!')

if __name__ == "__main__":
    text = 'Octavia is best pony!'
    print(color(text, 'green'))
    print(color(text, 'red'))
    print(color(text, 'yellow'))
