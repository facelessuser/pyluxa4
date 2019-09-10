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

LUXAFOR_VENDOR = 0x04d8
LUXAFOR_PRODUCT = 0xf372

MODE_SIMPLE = 0x00
MODE_STATIC = 0x01
MODE_FADE = 0x02
MODE_STROBE = 0x03
MODE_WAVE = 0x04
MODE_PATTERN = 0x6

PINS_ALL = 0xff
PINS_BACK_SIDE = 0x42
PINS_TAB_SIDE = 0x41
PINS_VALID = (1, 2, 3, 4, 5, 6, 0x41, 0x42, 0xff)

# Message that is sent when a command, that cannont be completed immediatey,
# complets (such as fade).
MSG_SIZE = 8
MSG_NON_IMMEDIATE_COMPLETE = b'\x00\x01\x00\x00\x00\x00\x00\x00'

CMD_REPORT_NUM = 0


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
    """Luxafor command class."""

    def __init__(self, red, green, blue, pins=PINS_ALL, fade=0, strobe=False, wave=0, pattern=0, speed=1, repeat=1):
        """Initialize."""

        if not (0 <= wave <= 5):
            raise ValueError('Wave must be a positive integer between 1-5, {} was given'.format(wave))
        if not (0 <= pattern <= 8):
            raise ValueError("Pattern must be a positive integer between 0-8, {} was given".format(pattern))

        self.red = clamp(red)
        self.green = clamp(green)
        self.blue = clamp(blue)
        self.fade = clamp(fade)
        self.strobe = strobe
        self.wave = wave
        self.pattern = pattern
        self.speed = clamp(speed)
        self.repeat = clamp(repeat)
        self.pins = PINS_ALL if pins not in PINS_VALID else pins

    def construct(self):
        """
        Construct the command.

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

        - Static

          Byte 0: Report number: 0 (Luxafor flag only has 0)
          Byte 1: Command Mode: 1
          Byte 2: Pins: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
          Byte 3: Red channel: 0-255
          Byte 4: Green channel: 0-255
          Byte 5: Blue channel: 0-255
          Byte 6: Fade duration: 0-255
          Byte 7: NA
          Byte 8: NA

        - Fade

          Byte 0: Report number: 0 (Luxafor flag only has 0)
          Byte 1: Command Mode: 2
          Byte 2: Pins: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
          Byte 3: Red channel: 0-255
          Byte 4: Green channel: 0-255
          Byte 5: Blue channel: 0-255
          Byte 6: Fade duration: 0-255
          Byte 7: NA
          Byte 8: NA

        - Strobe

          Byte 0: Report number: 0 (Luxafor flag only has 0)
          Byte 1: Command Mode: 3
          Byte 2: Pins: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
          Byte 3: Red channel: 0-255
          Byte 4: Green channel: 0-255
          Byte 5: Blue channel: 0-255
          Byte 6: Speed: 0-255
          Byte 7: NA
          Byte 8: Repeat: 0-255

        - Wave

          Byte 0: Report number: 0 (Luxafor flag only has 0)
          Byte 1: Command Mode: 4
          Byte 2: Wave type: 1-5
          Byte 3: Red channel: 0-255
          Byte 4: Green channel: 0-255
          Byte 5: Blue channel: 0-255
          Byte 6: NA
          Byte 7: Repeat: 0-255
          Byte 8: Speed: 0-255

        - Built in

          Byte 0: Report number: 0 (Luxafor flag only has 0)
          Byte 1: Command Mode: 6
          Byte 2: Pattern ID: 0-8
          Byte 3: Repeat: 0-255

        - Productivity

          Byte 0: Report number: 0 (Luxafor flag only has 0)
          Byte 1: Command Mode: 10
          Byte 2: Command: E (enable), D (Disable), R, G, B, C, Y, M, W, O (colors)

        """

        if self.fade:
            mode = MODE_FADE
        elif self.strobe:
            mode = MODE_STROBE
        elif self.wave:
            mode = MODE_WAVE
        elif self.pattern:
            mode = MODE_PATTERN
        else:
            mode = MODE_STATIC

        byte2 = self.pins
        byte3 = self.red
        byte4 = self.green
        byte5 = self.blue
        byte6 = self.fade
        byte7 = 0
        byte8 = 0

        if self.pattern:
            byte2 = self.pattern
            byte3 = self.repeat
            byte4 = 0
            byte5 = 0
            byte6 = 0
        elif self.strobe:
            byte6 = self.speed
            byte8 = self.repeat
        elif self.wave:
            byte2 = self.wave
            byte6 = 0
            byte7 = self.repeat
            byte8 = self.speed

        print(bytes([CMD_REPORT_NUM, mode, byte2, byte3, byte4, byte5, byte6, byte7, byte8]))
        return bytes([CMD_REPORT_NUM, mode, byte2, byte3, byte4, byte5, byte6, byte7, byte8])


class LuxFlag:
    """Class to controll luxflag."""

    def __init__(self):
        """Initialize."""

        self.ignore = False
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

        self.set_color(255, 0, 0, **kwargs)

    def set_orange(self, **kwargs):
        """Set color orange."""

        self.set_color(255, 102, 0, **kwargs)

    def set_yellow(self, **kwargs):
        """Set color yellow."""

        self.set_color(255, 255, 0, **kwargs)

    def set_green(self, **kwargs):
        """Set color green."""

        self.set_color(0, 255, 0, **kwargs)

    def set_blue(self, **kwargs):
        """Set color blue."""

        self.set_color(0, 0, 255, **kwargs)

    def set_purple(self, **kwargs):
        """Set color purple."""

        self.set_color(75, 0, 130, **kwargs)

    def set_pink(self, **kwargs):
        """Set color pink."""

        self.set_color(255, 0, 255, **kwags)

    def set_cyan(self, **kwags):
        """Set color cyan."""

        self.set_color(0, 255, 255, **kwargs)

    def set_white(self, **kwargs):
        """Set color white."""

        self.set_color(255, 255, 255, **kwargs)

    def set_off(self, **kwargs):
        """Set color off."""

        self.set_color(0, 0, 0, pins=kwargs.get('pins', PINS_ALL), fade=kwargs.get('fade', 0))

    def set_color(
            self, red, green, blue, *,
            pins=PINS_ALL, fade=0, strobe=False, wave=0, pattern=0, speed=1, repeat=1
        ):
        """Set color."""

        is_on = (red or green or blue or pattern)

        if is_on:
            # If we fade in to a color while a color is showing,
            # the color will simply turn off, so turn it off, then fade in.
            self.ignore = True
            self.set_off(pins=pins, fade=(fade if not pattern else 0))
            self.ignore = False
        else:
            # We don't support strobe of waving on turning off
            strobe = False
            wave = 0

        lc = LuxCmd(red, green, blue, pins, fade, strobe, wave, pattern, speed, repeat)
        self._device.write(lc.construct())

        # Move this
        if (fade or ((strobe or wave or pattern) and repeat)) and not self.ignore:
            # Wait for fade to complete
            while self._device.read(MSG_SIZE) != MSG_NON_IMMEDIATE_COMPLETE:
                pass

            if not pattern:
                # The fading in won't hold unless we bombard the flag with requests to stay on
                lc = LuxCmd(red, green, blue, pins)
                past = time.time()
                while (time.time() - past) < 1:
                    self._device.write(lc.construct())


def main():
    """Main."""
    parser = argparse.ArgumentParser(prog='lux', description='Luxafor control script.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))
    parser.add_argument('--set', action='store', help="Set pins.")
    parser.add_argument('--pins', action='store', default='all', help="Pins 1-6 or 'back', 'tab', or 'all'")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fade', action='store', type=int, default=0, help="Time to fade in.")
    group.add_argument('--strobe', action='store_true', help="Time to fade in.")
    group.add_argument('--wave', action='store', type=int, default=0, help="Wave.")
    group.add_argument('--pattern', action='store', type=int, default=0, help="Pattern.")
    parser.add_argument('--speed', action='store', type=int, default=1, help="Speed for strobe or wave.")
    parser.add_argument('--repeat', action='store', type=int, default=1, help="Repeat for strobe or wave.")
    group.add_argument('--rainbow', action='store', type=int, default=0, help="Rainbow")
    args = parser.parse_args()

    with LuxFlag() as lf:

        if args.rainbow:
            pins = resolve_pins(args.pins)
            lf.set_white(pins, args.rainbow)
            lf.set_pink(pins, args.rainbow)
            lf.set_red(pins, args.rainbow)
            lf.set_orange(pins, args.rainbow)
            lf.set_yellow(pins, args.rainbow)
            lf.set_green(pins, args.rainbow)
            lf.set_cyan(pins, args.rainbow)
            lf.set_blue(pins, args.rainbow)
            lf.set_purple(pins, args.rainbow)
            lf.set_off(pins, args.rainbow)
        else:
            pins = resolve_pins(args.pins)
            speed = args.speed
            repeat = args.repeat
            wave = args.wave
            strobe = args.strobe
            fade = args.fade
            pattern = args.pattern
            color = args.set.lower() if args.set else '000000'
            if color in COLOR_NAMES:
                # Handle named colors
                getattr(lf, 'set_{}'.format(color))(
                    pins=pins, fade=fade, strobe=strobe, wave=wave, pattern=pattern, speed=speed, repeat=repeat
                )
            elif len(color) == COLOR_SIZE:
                # Handle colors in the form RRGGBB
                try:
                    r = int(color[0:2], 16)
                    g = int(color[2:4], 16)
                    b = int(color[4: 6], 16)
                except Exception:
                    raise ValueError('Invalid color {}'.format(color))

                lf.set_color(
                    r, g, b,
                    pins=pins, fade=fade, strobe=strobe, wave=wave, pattern=pattern, speed=speed, repeat=repeat
                )
            else:
                raise ValueError('Invalid color {}'.format(color))

    return 0


if __name__ == '__main__':
    sys.exit(main())
