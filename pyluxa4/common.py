"""Common functions and constants."""

LED_ALL = 0xff
LED_FRONT = 0x41
LED_BACK = 0x42
LED_1 = 1
LED_2 = 2
LED_3 = 3
LED_4 = 4
LED_5 = 5
LED_6 = 6
LED_VALID = frozenset([LED_1, LED_2, LED_3, LED_4, LED_5, LED_6, LED_FRONT, LED_BACK, LED_ALL])

WAVE_1 = WAVE_SHORT = 1
WAVE_2 = WAVE_LONG = 2
WAVE_3 = WAVE_OVERLAPPING_SHORT = 3
WAVE_4 = WAVE_OVERLAPPING_LONG = 4
WAVE_5 = 5
WAVE_VALID = frozenset([WAVE_1, WAVE_2, WAVE_3, WAVE_4, WAVE_5])

PATTERN_1 = PATTERN_TRAFFIC_LIGHT = 1
PATTERN_2 = PATTERN_RANDOM1 = 2
PATTERN_3 = PATTERN_RANDOM2 = 3
PATTERN_4 = PATTERN_RANDOM3 = 4
PATTERN_5 = PATTERN_POLICE = 5
PATTERN_6 = PATTERN_RANDOM4 = 6
PATTERN_7 = PATTERN_RANDOM5 = 7
PATTERN_8 = PATTERN_RAINBOW = 8
PATTERN_VALID = frozenset([PATTERN_1, PATTERN_2, PATTERN_3, PATTERN_4, PATTERN_5, PATTERN_6, PATTERN_7, PATTERN_8])

COLOR_RED = ord('R')
COLOR_GREEN = ord('G')
COLOR_BLUE = ord('B')
COLOR_CYAN = ord('C')
COLOR_YELLOW = ord('Y')
COLOR_MAGENTA = ord('M')
COLOR_WHITE = ord('W')
COLOR_OFF = ord('O')
COLOR_VALID = frozenset(
    [COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_CYAN, COLOR_YELLOW, COLOR_MAGENTA, COLOR_WHITE, COLOR_OFF]
)

BYTE_MIN = 0
BYTE_MAX = 255


LED_MAP = {
    "all": LED_ALL,
    "back": LED_BACK,
    "front": LED_FRONT
}

PATTERN_MAP = {
    'traffic-light': PATTERN_TRAFFIC_LIGHT,
    'police': PATTERN_POLICE,
    'rainbow': PATTERN_RAINBOW,
    'random1': PATTERN_RANDOM1,
    'random2': PATTERN_RANDOM2,
    'random3': PATTERN_RANDOM3,
    'random4': PATTERN_RANDOM4,
    'random5': PATTERN_RANDOM5
}

WAVE_MAP = {
    "short": WAVE_SHORT,
    "long": WAVE_LONG,
    "overlapping-short": WAVE_OVERLAPPING_SHORT,
    "overlapping-long": WAVE_OVERLAPPING_LONG
}


def validate_wave(wave):
    """Validate wave."""

    if wave not in WAVE_VALID:
        raise ValueError('Wave must be a positive integer between 1-5, {} was given'.format(wave))


def validate_speed(speed):
    """Validate speed."""

    if not (BYTE_MIN <= speed <= BYTE_MAX):
        raise ValueError('Speed channel must be a positive integer between 0-255, {} was given'.format(speed))


def validate_repeat(repeat):
    """Validate repeat."""

    if not (BYTE_MIN <= repeat <= BYTE_MAX):
        raise ValueError('Repeat channel must be a positive integer between 0-255, {} was given'.format(repeat))


def validate_pattern(pattern):
    """Validate pattern."""

    if pattern not in PATTERN_VALID:
        raise ValueError('Pattern must be a positive integer between 1-8, {} was given'.format(pattern))


def validate_led(led):
    """Validate led."""

    if led not in LED_VALID:
        raise ValueError("LED must either be an integer 1-6, 0x41, 0x42, or 0xFF, {} was given".format(led))


def validate_simple_color(color):
    """Validate simple color code."""

    if color not in COLOR_VALID:
        raise ValueError("Accepted color codes are R, G, B, C, M, Y, W, and O, {} was given".format(color))


def validate_timer_cycle(cycle):
    """Validate the timer cycle."""

    if cycle < 0:
        raise ValueError("Timer cycle can not be less than zero")


def is_bool(name, value):
    """Check if bool."""

    if not isinstance(value, bool):
        raise TypeError("'{}' must be a boolean".format(name))


def is_str(name, value):
    """Check if bool."""

    if not isinstance(value, str):
        raise TypeError("'{}' must be a string".format(name))


def is_int(name, value):
    """Check if bool."""

    if not isinstance(value, int):
        raise TypeError("'{}' must be a integer".format(name))


def resolve_led(value):
    """Resolve LED."""

    led = value.lower()
    if led in LED_MAP:
        led = LED_MAP[led]
    else:
        try:
            led = int(led)
            validate_led(led)
        except Exception:
            raise ValueError('Invalid LED value of {}'.format(led))
    return led


def resolve_pattern(value):
    """Resolve pattern."""

    p = value.lower()
    if p in PATTERN_MAP:
        p = PATTERN_MAP[p]
    else:
        try:
            p = int(p)
            validate_pattern(p)
        except Exception:
            raise ValueError('Invalid pattern value of {}'.format(p))
    return p


def resolve_wave(value):
    """Resolve wave."""

    w = value.lower()
    if w in WAVE_MAP:
        w = WAVE_MAP[w]
    else:
        try:
            w = int(w)
            validate_wave(w)
        except Exception:
            raise ValueError('Invalid wave value of {}'.format(w))
    return w
