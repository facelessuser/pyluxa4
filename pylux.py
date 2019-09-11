"""
Luxafor control via the Python hid wrapper around libusb/hidapi.

apmorton/pyhidapi: https://github.com/apmorton/pyhidapi
libusb/hidapi: https://github.com/libusb/hidapi

"""
import hid
import argparse
import sys
import time

__version__ = '0.1'

COLOR_NAMES = ('red', 'orange', 'yellow', 'green', 'blue', 'pink', 'purple', 'cyan', 'white', 'off')
COLOR_SIZE = 6
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


class LuxCmd:
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

    def __init__(self, red, green, blue, mode=MODE_STATIC, pins=PINS_ALL, speed=1, repeat=1, wave=0, pattern=0):
        """Initialize."""

        if mode == MODE_WAVE and not (0 < wave <= 5):
            raise ValueError('Wave must be a positive integer between 1-5, {} was given'.format(wave))
        if mode == MODE_PATTERN and not (1 <= pattern <= 8):
            raise ValueError("Pattern must be a positive integer between 0-8, {} was given".format(pattern))

        self.mode = mode
        self.red = clamp(red)
        self.green = clamp(green)
        self.blue = clamp(blue)
        self.wave = wave
        self.pattern = pattern
        self.speed = clamp(speed, 1, 255)
        self.repeat = clamp(repeat, 1, 255)
        self.pins = PINS_ALL if pins not in PINS_VALID else pins

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

        mode = kwargs.get('mode', MODE_STATIC)
        if mode not in (MODE_STATIC, MODE_FADE):
            mode = MODE_STATIC
        speed = kwargs.get('speed', 1) if mode == MODE_FADE else 0
        self.set_color(COLOR_OFF, mode=mode, pins=kwargs.get('pins', PINS_ALL), speed=speed)

    def set_color(self, color, *, mode=MODE_STATIC, pins=PINS_ALL, speed=1, repeat=1, wave=0):
        """Set color."""

        # Ignore pattern mode
        if mode == MODE_PATTERN:
            mode = MODE_STATIC

        self._execute(color, mode=mode, pins=pins, speed=speed, repeat=repeat, wave=wave)

    def set_pattern(self, pattern, *, repeat=1):
        """Set pattern."""

        if pattern == PAT_RAINBOW:
            self._pattern_rainbow(repeat=repeat)
        else:
            self._execute(COLOR_OFF, mode=MODE_PATTERN, repeat=repeat, pattern=pattern)

    def _pattern_rainbow(self, *, repeat=1):
        """Pattern rainbow."""

        for x in range(repeat):
            self.set_pink(mode=MODE_FADE, speed=100)
            self.set_red(mode=MODE_FADE, speed=100)
            self.set_orange(mode=MODE_FADE, speed=100)
            self.set_yellow(mode=MODE_FADE, speed=100)
            self.set_green(mode=MODE_FADE, speed=100)
            self.set_cyan(mode=MODE_FADE, speed=100)
            self.set_blue(mode=MODE_FADE, speed=100)
            self.set_purple(mode=MODE_FADE, speed=100)
        self.set_off(mode=MODE_FADE, speed=100)

    def _execute(self, color, *, mode=MODE_STATIC, pins=PINS_ALL, speed=1, repeat=1, wave=0, pattern=0):
        """Set color."""

        red, green, blue = color
        if not (red or green or blue):
            # We don't support strobe of waving on turning off
            strobe = False
            wave = 0

        # Execute the command
        lc = LuxCmd(red, green, blue, mode, pins, speed, repeat, wave, pattern)
        self._device.write(lc.cmd)

        # Wait for commands that take time to complete
        if lc.mode != MODE_STATIC:
            while self._device.read(MSG_SIZE, 100) != MSG_NON_IMMEDIATE_COMPLETE:
                pass


def main():
    """Main."""
    parser = argparse.ArgumentParser(prog='lux', description='Luxafor control script.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--set', action='store', default='000000', help="Set color")
    group.add_argument('--pattern', action='store', type=int, default=0, help="Patterns: 1-9")
    parser.add_argument('--pins', action='store', default='all', help="Pins: 1-6, back, tab, or all")
    parser.add_argument('--mode', action='store', default='static', help="Mode: static, fade, strobe, wave")
    parser.add_argument('--wave', action='store', type=int, default=1, help="Wave configuration: 1-5")
    parser.add_argument('--speed', action='store', type=int, default=1, help="Speed for strobe, wave, or fade: 1-255")
    parser.add_argument(
        '--repeat', action='store', type=int, default=1, help="Repeat for strobe, wave, or pattern: 1-255"
    )
    args = parser.parse_args()

    with LuxFlag() as lf:

        pins = resolve_pins(args.pins)
        if args.pattern:
            pattern = args.pattern
            mode = 0
        elif args.mode:
            mode = MODE_MAP.get(args.mode.lower(), MODE_STATIC)
            pattern = 0
        speed = args.speed
        repeat = args.repeat
        wave = args.wave
        color = args.set.lower()
        if pattern:
            lf.set_pattern(pattern, repeat=repeat)
        elif color in COLOR_NAMES:
            # Handle named colors
            getattr(lf, 'set_{}'.format(color))(pins=pins, mode=mode, speed=speed, repeat=repeat, wave=wave)
        elif len(color) == COLOR_SIZE:
            # Handle colors in the form RRGGBB
            try:
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4: 6], 16)
            except Exception:
                raise ValueError('Invalid color {}'.format(color))

            lf.set_color(r, g, b, pins=pins, mode=mode, speed=speed, repeat=repeat, wave=wave)
        else:
            raise ValueError('Invalid color {}'.format(color))

    return 0


if __name__ == '__main__':
    sys.exit(main())
