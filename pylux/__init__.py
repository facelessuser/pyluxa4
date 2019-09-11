"""
Luxafor control via the Python hid wrapper around libusb/hidapi.

apmorton/pyhidapi: https://github.com/apmorton/pyhidapi
libusb/hidapi: https://github.com/libusb/hidapi

"""
import hid
import sys

__version__ = '0.1'

__all__ = ('LuxFlag',)

COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 102, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_PINK = (255, 0, 255)
COLOR_PURPLE = (75, 0, 130)
COLOR_CYAN = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_OFF = (0, 0, 0)

LUXAFOR_VENDOR = 0x04d8
LUXAFOR_PRODUCT = 0xf372

MODE_SIMPLE = 0x00
MODE_STATIC = 0x01
MODE_FADE = 0x02
MODE_STROBE = 0x03
MODE_WAVE = 0x04
MODE_PATTERN = 0x6
MODE_INVALID = -1
MODE_VALID = (MODE_STATIC, MODE_FADE, MODE_STROBE, MODE_WAVE, MODE_PATTERN)
MODE_MAP = {
    'static': MODE_STATIC,
    'fade': MODE_FADE,
    'strobe': MODE_STROBE,
    'wave': MODE_WAVE,
    'pattern': MODE_PATTERN
}

PINS_ALL = 0xff
PINS_BACK_SIDE = 0x42
PINS_TAB_SIDE = 0x41
PINS_VALID = (1, 2, 3, 4, 5, 6, 0x41, 0x42, 0xff)

# Message that is sent when a command, that cannont be completed immediatey,
# complets (such as fade).
MSG_NON_IMMEDIATE_COMPLETE = b'\x00\x01\x00\x00\x00\x00\x00\x00'
MSG_NONE = b''
MSG_SIZE = 8

CMD_REPORT_NUM = 0

# Extra custom patterns
PAT_RAINBOW = 9


def clamp(value, mn=0, mx=255):
    """Clamp the value to the the given minimum and maximum."""

    return max(min(value, mx), mn)


def resolve_pins(option):
    """Resolve the pins option to the actual required value."""

    pins = option.lower()
    if pins == 'all':
        pins = PINS_ALL
    elif pins == 'back':
        pins = PINS_BACK_SIDE
    elif pins == 'tab':
        pins = PINS_TAB_SIDE
    else:
        try:
            pins = int(pins)
        except Exception:
            raise ValueError('Invalid pin value of {}'.format(pins))
    return pins


class _LuxCmd:
    """
    Luxafor command class.

    These are not implemented.

    - Simple

      Byte 0: Report number (Luxafor flag only has 0)
      Byte 1: Color: R, G, B, C, M, Y, W, O
      Byte 2: NA
      Byte 3: NA
      Byte 4: NA
      Byte 5: NA
      Byte 6: NA
      Byte 7: NA
      Byte 8: NA

    - Productivity

      Byte 0: Report number: 0 (Luxafor flag only has 0)
      Byte 1: Command Mode: 10
      Byte 2: Command: E (enable), D (Disable), R, G, B, C, Y, M, W, O (colors)

    """

    def __init__(self, red, green, blue, mode=MODE_STATIC, pins=PINS_ALL, speed=1, repeat=1, wave=1, pattern=1):
        """Initialize."""

        self.mode = mode
        self.red = red
        self.green = green
        self.blue = blue
        self.wave = wave
        self.pattern = pattern
        self.speed = speed
        self.repeat = repeat
        self.pins = pins

        if mode == MODE_FADE:
            cmd = self.cmd_fade()
        elif mode == MODE_STROBE:
            cmd = self.cmd_strobe()
        elif mode == MODE_WAVE:
            cmd = self.cmd_wave()
        elif mode == MODE_PATTERN:
            cmd = self.cmd_pattern()
        else:
            cmd = self.cmd_static()

        self.cmd = bytes(cmd)

    def cmd_pattern(self):
        """
        Build pattern command.

        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 6
        Byte 2: Pattern ID: 0-8
        Byte 3: Repeat: 0-255

        """

        return [CMD_REPORT_NUM, MODE_PATTERN, self.pattern, self.repeat, 0, 0, 0, 0, 0]

    def cmd_strobe(self):
        """
        Build strobe command.

        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 3
        Byte 2: Pins: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: Speed: 0-255
        Byte 7: NA
        Byte 8: Repeat: 0-255

        """

        return [CMD_REPORT_NUM, MODE_STROBE, self.pins, self.red, self.green, self.blue, self.speed, 0, self.repeat]

    def cmd_wave(self):
        """
        Build wave command.

        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 4
        Byte 2: Wave type: 1-5
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: NA
        Byte 7: Repeat: 0-255
        Byte 8: Speed: 0-255

        """

        return [CMD_REPORT_NUM, MODE_WAVE, self.wave, self.red, self.green, self.blue, 0, self.repeat, self.speed]

    def cmd_fade(self):
        """
        Build fade command.

        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 2
        Byte 2: Pins: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: Fade duration: 0-255
        Byte 7: NA
        Byte 8: NA

        """

        return [CMD_REPORT_NUM, MODE_FADE, self.pins, self.red, self.green, self.blue, self.speed, 0, 0]

    def cmd_static(self):
        """
        Build static command.

        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 1
        Byte 2: Pins: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: Fade duration: 0-255
        Byte 7: NA
        Byte 8: NA

        """

        return [CMD_REPORT_NUM, MODE_STATIC, self.pins, self.red, self.green, self.blue, 0, 0, 0]


class LuxFlag:
    """Class to controll luxflag."""

    def __init__(self):
        """Initialize."""

        self._device = hid.Device(vid=LUXAFOR_VENDOR, pid=LUXAFOR_PRODUCT)

    def __enter__(self):
        """Enter."""

        return self

    def __exit__(self, type, value, traceback):  # noqa: A002
        """Exit."""

        return self.close()

    def close(self):
        """Close luxafor device."""

        return self._device.close()

    def set_red(self, **kwargs):
        """Set color red."""

        self.set_color(COLOR_RED, **kwargs)

    def set_orange(self, **kwargs):
        """Set color orange."""

        self.set_color(COLOR_ORANGE, **kwargs)

    def set_yellow(self, **kwargs):
        """Set color yellow."""

        self.set_color(COLOR_YELLOW, **kwargs)

    def set_green(self, **kwargs):
        """Set color green."""

        self.set_color(COLOR_GREEN, **kwargs)

    def set_blue(self, **kwargs):
        """Set color blue."""

        self.set_color(COLOR_BLUE, **kwargs)

    def set_purple(self, **kwargs):
        """Set color purple."""

        self.set_color(COLOR_PURPLE, **kwargs)

    def set_pink(self, **kwargs):
        """Set color pink."""

        self.set_color(COLOR_PINK, **kwargs)

    def set_cyan(self, **kwargs):
        """Set color cyan."""

        self.set_color(COLOR_CYAN, **kwargs)

    def set_white(self, **kwargs):
        """Set color white."""

        self.set_color(COLOR_WHITE, **kwargs)

    def set_off(self, **kwargs):
        """Set color off."""

        mode = kwargs.get('mode', 'static').lower()
        if mode not in ("static", "fade"):
            mode = "static"
        self.set_color(COLOR_OFF, mode=mode, pins=kwargs.get('pins', "all"), speed=kwargs.get('speed', 1))

    def set_color(self, color, *, mode="static", pins="all", speed=1, repeat=1, wave=1):
        """Set color."""

        # Validate inputs
        red, green, blue = color
        pins = resolve_pins(pins)
        mode = MODE_MAP.get(mode.lower(), MODE_INVALID)
        if mode == MODE_WAVE and not (1 <= wave <= 5):
            raise ValueError('Wave must be a positive integer between 1-5, {} was given'.format(wave))
        elif not (0 <= red <= 255):
            raise ValueError('Red channel must be a positive integer between 0-255, {} was given'.format(red))
        elif not (0 <= green <= 255):
            raise ValueError('Green channel must be a positive integer between 0-255, {} was given'.format(green))
        elif not (0 <= blue <= 255):
            raise ValueError('Blue channel must be a positive integer between 0-255, {} was given'.format(blue))
        elif not (1 <= speed <= 255):
            raise ValueError('Speed channel must be a positive integer between 1-255, {} was given'.format(speed))
        elif not (1 <= repeat <= 255):
            raise ValueError('Repeat channel must be a positive integer between 1-255, {} was given'.format(repeat))
        elif mode not in MODE_VALID or mode == MODE_PATTERN:
            raise ValueError('Mode {} is an invalid value'.format(mode))
        elif pins not in PINS_VALID:
            raise ValueError('Pins {} is not a valid value'.format(pins))

        self._execute(red, green, blue, mode=mode, pins=pins, speed=speed, repeat=repeat, wave=wave)

    def set_pattern(self, pattern, *, repeat=1):
        """Set pattern."""

        # Validate inputs
        if not (1 <= pattern <= 9):
            raise ValueError('Pattern must be a positive integer between 1-9, {} was given'.format(pattern))
        elif not (1 <= repeat <= 255):
            raise ValueError('Repeat channel must be a positive integer between 1-255, {} was given'.format(repeat))

        if pattern == PAT_RAINBOW:
            self._pattern_rainbow(repeat=repeat)
        else:
            self._execute(*COLOR_OFF, mode=MODE_PATTERN, repeat=repeat, pattern=pattern)

    def _pattern_rainbow(self, *, repeat=1):
        """Pattern rainbow."""

        for x in range(repeat):
            self.set_pink(mode="fade", speed=100)
            self.set_red(mode="fade", speed=100)
            self.set_orange(mode="fade", speed=100)
            self.set_yellow(mode="fade", speed=100)
            self.set_green(mode="fade", speed=100)
            self.set_cyan(mode="fade", speed=100)
            self.set_blue(mode="fade", speed=100)
            self.set_purple(mode="fade", speed=100)
        self.set_off(mode="fade", speed=100)

    def _execute(self, red, green, blue, *, mode=MODE_STATIC, pins=PINS_ALL, speed=1, repeat=1, wave=1, pattern=1):
        """Set color."""

        if not (red or green or blue):
            # We don't support strobe of waving on turning off
            strobe = False
            wave = 0

        # Execute the command
        lc = _LuxCmd(red, green, blue, mode, pins, speed, repeat, wave, pattern)
        self._device.write(lc.cmd)

        # Wait for commands that take time to complete
        if lc.mode != MODE_STATIC:
            while self._device.read(MSG_SIZE, 100) != MSG_NON_IMMEDIATE_COMPLETE:
                pass
