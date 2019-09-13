"""Common functions and constants."""

LED_ALL = 0xff
LED_BACK = 0x42
LED_FRONT = 0x41
LED_VALID = (1, 2, 3, 4, 5, 6, LED_FRONT, LED_BACK, LED_ALL)


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
