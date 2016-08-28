CSI = "\x1b["
CSI_end = "\x1b[0m"
#  reset = CSI + "m"

NORMAL = 0
BOLD = 1
FADE = 2
ITALIC = 3
UNDERLINE = 4

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


def color(string, fg, bg='GRAY'):
    if fg.upper() in COLORS:
        return '{}{};{};{}m{}{}'.format(
            CSI,
            BOLD,
            COLORS[fg.upper()],
            COLORS[bg.upper()],
            string,
            CSI_end)
    else:
        raise ValueError('Passed arg color is not in the available colors!')

if __name__ == "__main__":
    text = 'Octavia is best pony!'
    print(color(text, 'green'))
    print(color(text, 'red'))
    print(color(text, 'yellow'))
