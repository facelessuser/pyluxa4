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
LED_VALID = (LED_1, LED_2, LED_3, LED_4, LED_5, LED_6, LED_FRONT, LED_BACK, LED_ALL)

WAVE_SHORT = 1
WAVE_LONG = 2
WAVE_OVERLAPPING_SHORT = 3
WAVE_OVERLAPPING_LONG = 4

PATTERN_TRAFFIC_LIGHT = 1
PATTERN_RANDOM1 = 2,
PATTERN_RANDOM2 = 3,
PATTERN_RANDOM3 = 4,
PATTERN_POLICE = 5
PATTERN_RANDOM4 = 6,
PATTERN_RANDOM5 = 7,
PATTERN_RAINBOW = 8


def resolve_led(option):
    """Resolve the LED option to the actual required value."""

    led = option.lower()
    if led == 'all':
        led = LED_ALL
    elif led == 'back':
        led = LED_BACK
    elif led == 'front':
        led = LED_FRONT
    else:
        try:
            led = int(led)
        except Exception:
            raise ValueError('Invalid LED value of {}'.format(led))
    return led
