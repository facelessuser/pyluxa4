"""
Luxafor USB controller via the Python hid wrapper around libusb/hidapi.

apmorton/pyhidapi: https://github.com/apmorton/pyhidapi
libusb/hidapi: https://github.com/libusb/hidapi

"""
import hid
import os
from .common import (
    LED_ALL, LED_BACK, LED_FRONT, LED_1, LED_2, LED_3, LED_4, LED_5, LED_6,
    WAVE_SHORT, WAVE_LONG, WAVE_OVERLAPPING_SHORT, WAVE_OVERLAPPING_LONG,
    WAVE_1, WAVE_2, WAVE_3, WAVE_4, WAVE_5,
    PATTERN_TRAFFIC_LIGHT, PATTERN_RANDOM1, PATTERN_RANDOM2, PATTERN_RANDOM3,
    PATTERN_POLICE, PATTERN_RANDOM4, PATTERN_RANDOM5, PATTERN_RAINBOW,
    PATTERN_1, PATTERN_2, PATTERN_3, PATTERN_4, PATTERN_5, PATTERN_6, PATTERN_7, PATTERN_8
)
from .import common as cmn
from .csscolors import name2hex

__version__ = '0.1'

__all__ = (
    'Luxafor', 'enumerate_luxafor',
    'LED_ALL', 'LED_BACK', 'LED_FRONT', 'LED_1', 'LED_2', 'LED_3', 'LED_4', 'LED_5', 'LED_6',
    'WAVE_SHORT', 'WAVE_LONG', 'WAVE_OVERLAPPING_SHORT', 'WAVE_OVERLAPPING_LONG',
    'WAVE_1', 'WAVE_2', 'WAVE_3', 'WAVE_4', 'WAVE_5',
    'PATTERN_TRAFFIC_LIGHT', 'PATTERN_RANDOM1', 'PATTERN_RANDOM2', 'PATTERN_RANDOM3',
    'PATTERN_POLICE', 'PATTERN_RANDOM4', 'PATTERN_RANDOM5', 'PATTERN_RAINBOW',
    'PATTERN_1', 'PATTERN_2', 'PATTERN_3', 'PATTERN_4', 'PATTERN_5', 'PATTERN_6', 'PATTERN_7', 'PATTERN_8'
)

LUXAFOR_VENDOR = 0x04d8
LUXAFOR_PRODUCT = 0xf372

MODE_BASIC = 0x00
MODE_STATIC = 0x01
MODE_FADE = 0x02
MODE_STROBE = 0x03
MODE_WAVE = 0x04
MODE_PATTERN = 0x6

# Message that is sent when a command, that cannot be completed immediately,
# completes (such as fade).
MSG_NON_IMMEDIATE_COMPLETE = b'\x00\x01\x00\x00\x00\x00\x00\x00'
MSG_NONE = b''
MSG_SIZE = 8

CMD_REPORT_NUM = 0


def clamp(value, mn=0, mx=255):
    """Clamp the value to the the given minimum and maximum."""

    return max(min(value, mx), mn)


def resolve_color(color):
    """Resolve color."""

    orig = color = color.lower()
    if color == 'off':
        color = 'black'
    if not color.startswith('#'):
        color = name2hex(color)
        if color is None:
            raise ValueError('{} is not a valid color name'.format(orig))

    if len(color) == 7:
        color = (
            int(color[1:3], 16),
            int(color[3:5], 16),
            int(color[5:7], 16)
        )
    elif len(color) == 4:
        color = (
            int(color[1:2] * 2, 16),
            int(color[2:3] * 2, 16),
            int(color[3:4] * 2, 16)
        )
    else:
        raise ValueError('{} is not a valid color code'.format(orig))

    return color


def enumerate_luxafor():
    """Enumerate all Luxafor devices."""

    return hid.enumerate(vid=LUXAFOR_VENDOR, pid=LUXAFOR_PRODUCT)


class Luxafor:
    """
    Class to control Luxafor device.

    This is not implemented.

    - Productivity

      ```
      Byte 0: Report number: 0 (Luxafor flag only has 0)
      Byte 1: Command Mode: 10
      Byte 2: Command: E (enable), D (Disable), R, G, B, C, Y, M, W, O (colors)
      ```

    """

    def __init__(self, index=0, path=None, token=None):
        """Initialize."""

        device = None
        devices = enumerate_luxafor()
        if not devices:
            raise RuntimeError('Cannot find a valid connected Luxafor device')
        if path is not None:
            target = os.fsencode(path)
            for d in devices:
                if d['path'] == target:
                    device = d['path']
                    break
            if device is None:
                raise RuntimeError('The Luxfor device with path {} could not be found'.format(path))
        if device is None:
            if index < 0 or index >= len(devices):
                raise RuntimeError('The Luxafor device at index {} cannot be found'.format(index))
            device = devices[index]['path']
        self._path = device
        self._token = token
        self._device = hid.Device(path=self._path)
        self._closed = False
        self._disconnected = False
        self._serial = self._get_serial()

    def _get_serial(self):
        """Get serial number."""

        self._device.write(b'\x00\x80')
        return self._device.read(MSG_SIZE, 3)

    def __enter__(self):
        """Enter."""

        return self

    def __exit__(self, type, value, traceback):  # noqa: A002
        """Exit."""

        return self.close()

    def _disconnect(self):
        """Disconnect the device."""

        if self._device is not None:
            self._device.close()
            self._disconnected = True
            self._device = None

    def _reconnect(self):
        """Reconnect device."""

        devices = enumerate_luxafor()
        for device in devices:
            path = device['path']
            try:
                self._device = hid.Device(path=path)
                if self._get_serial() == self._serial:
                    self._path = path
                    self._disconnected = False
                    break
                else:
                    self._disconnect()
            except Exception:
                self._disconnect()

        return not self._disconnected

    def close(self):
        """Close Luxafor device."""

        self._closed = True
        return self._device.close()

    def get_token(self):
        """Get the API ID."""

        return self._token

    def off(self):
        """Set all LEDs to off."""

        return self.basic_color('O')

    def basic_color(self, color):
        """
        Build basic color command.

        ```
        Byte 0: Report number (Luxafor flag only has 0)
        Byte 1: Color: R, G, B, C, M, Y, W, O
        Byte 2: NA
        Byte 3: NA
        Byte 4: NA
        Byte 5: NA
        Byte 6: NA
        Byte 7: NA
        Byte 8: NA
        ```

        """

        color = ord(color.upper())
        cmn.validate_simple_color(color)
        return self._execute([CMD_REPORT_NUM, MODE_BASIC, color])

    def color(self, color, *, led=LED_ALL):
        """
        Build static color command.

        ```
        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 1
        Byte 2: LED: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: NA
        Byte 7: NA
        Byte 8: NA
        ```

        """

        if isinstance(color, str) and len(color) == 1:
            return self.basic_color(color)
        else:
            red, green, blue = resolve_color(color)
            cmn.validate_led(led)
            return self._execute([CMD_REPORT_NUM, MODE_STATIC, led, red, green, blue, 0, 0, 0])

    def fade(self, color, *, led=LED_ALL, speed=1, wait=False):
        """
        Build fade command.

        ```
        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 2
        Byte 2: LED: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: Fade speed: 0-255
        Byte 7: NA
        Byte 8: NA
        ```

        """

        red, green, blue = resolve_color(color)
        cmn.validate_led(led)
        cmn.validate_speed(speed)
        return self._execute([CMD_REPORT_NUM, MODE_FADE, led, red, green, blue, speed, 0, 0], wait=wait)

    def wave(self, color, *, wave=WAVE_SHORT, speed=0, repeat=0, wait=False):
        """
        Build wave command.

        ```
        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 4
        Byte 2: Wave type: 1-5
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: NA
        Byte 7: Repeat: 0-255
        Byte 8: Speed: 0-255
        ```

        """

        # We cannot wait when repeat is set to go on forever.
        if repeat == 0:
            wait = False
        red, green, blue = resolve_color(color)
        cmn.validate_wave(wave)
        cmn.validate_speed(speed)
        cmn.validate_repeat(repeat)
        return self._execute([CMD_REPORT_NUM, MODE_WAVE, wave, red, green, blue, 0, repeat, speed], wait=wait)

    def strobe(self, color, *, led=LED_ALL, speed=0, repeat=0, wait=False):
        """
        Build strobe command.

        ```
        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 3
        Byte 2: LED: 1-6, 0x42 (back), 0x41 (tab), 0xFF (all)
        Byte 3: Red channel: 0-255
        Byte 4: Green channel: 0-255
        Byte 5: Blue channel: 0-255
        Byte 6: Speed: 0-255
        Byte 7: NA
        Byte 8: Repeat: 0-255
        ```

        """

        # We cannot wait when repeat is set to go on forever.
        if repeat == 0:
            wait = False
        red, green, blue = resolve_color(color)
        cmn.validate_led(led)
        cmn.validate_speed(speed)
        cmn.validate_repeat(repeat)
        return self._execute([CMD_REPORT_NUM, MODE_STROBE, led, red, green, blue, speed, 0, repeat], wait=wait)

    def pattern(self, pattern, *, repeat=0, wait=False):
        """
        Build pattern command.

        ```
        Byte 0: Report number: 0 (Luxafor flag only has 0)
        Byte 1: Command Mode: 6
        Byte 2: Pattern ID: 0-8
        Byte 3: Repeat: 0-255
        ```

        """

        # We cannot wait when repeat is set to go on forever.
        if repeat == 0:
            wait = False
        cmn.validate_pattern(pattern)
        cmn.validate_repeat(repeat)
        return self._execute([CMD_REPORT_NUM, MODE_PATTERN, pattern, repeat, 0, 0, 0, 0, 0], wait=wait)

    def _execute(self, cmd, wait=False):
        """
        Set color.

        Return false if there was an error.
        """

        if self._disconnected and not self._reconnect():
            return True
        elif self._closed:
            return True

        try:
            self._device.write(bytes(cmd))
        except hid.HIDException:
            # Failed to connect
            self._disconnect()

        # Attempt to reconnect and try again
        if self._disconnected:
            if not self._reconnect():
                return True
            self._device.write(bytes(cmd))

        # Wait for commands that take time to complete.
        # When the `hid` is released on Windows, the current
        # command may not complete. Using wait before the
        # script exits will help ensure the command completes.
        if wait:
            try:
                while self._device.read(MSG_SIZE, 100) != MSG_NON_IMMEDIATE_COMPLETE:
                    pass
            except hid.HIDException:
                self._disconnect()
                return True
        return False
