# USB API

## Overview

While `pyluxa4` provides a CLI interface for starting a server and commands that control a Luxafor device, you can also
use `pyluxa4` to control the device directly through the USB without the server directly using. If you wish to control
the device directly from your own Python scripts, simply import the `usb` library:

```py3
from pyluxa4 import usb
```

Then you can connect to a Luxafor device:

```py3
with usb.Luxafor(index=0) as luxafor:
    luxafor.fade("red", speed=10, wait=True)
    luxafor.fade("green", speed=10, wait=True)
```

You can also use it without `with`:

```py3
device = usb.Luxafor(index=0)
luxafor.fade("red", speed=10, wait=True)
luxafor.fade("green", speed=10, wait=True)
device.close()
```

## Constants

### LEDs
Constant  | Alias                  | Value
--------- | ---------------------- | -----
LED_ALL   |                        | `0xff`
LED_FRONT |                        | `0x41`
LED_BACK  |                        | `0x42`
LED_1     |                        | `1`
LED_2     |                        | `2`
LED_3     |                        | `3`
LED_4     |                        | `4`
LED_5     |                        | `5`
LED_6     |                        | `6`

### Waves

Constant  | Alias                  | Value
--------- | ---------------------- | -----
WAVE_1    | WAVE_SHORT             | `1`
WAVE_2    | WAVE_LONG              | `2`
WAVE_3    | WAVE_OVERLAPPING_SHORT | `3`
WAVE_4    | WAVE_OVERLAPPING_LONG  | `4`
WAVE_5    |                        | `5`

### Patterns

Constant  | Alias                  | Value
--------- | ---------------------- | -----
PATTERN_1 | PATTERN_TRAFFIC_LIGHT  | `1`
PATTERN_2 | PATTERN_RANDOM1        | `2`
PATTERN_3 | PATTERN_RANDOM2        | `3`
PATTERN_4 | PATTERN_RANDOM3        | `4`
PATTERN_5 | PATTERN_POLICE         | `5`
PATTERN_6 | PATTERN_RANDOM4        | `6`
PATTERN_7 | PATTERN_RANDOM5        | `7`
PATTERN_8 | PATTERN_RAINBOW        | `8`

## `enumerate_luxafor()`

Enumerate Luxafor devices returning a list of the available devices:

```pycon3
>>> import pyluxa4.usb as usb
>>> usb.enumerate_luxafor()
[{'path': b'\\\\?\\hid#vid_04d8&pid_f372#6&38a95344&1&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}', 'vendor_id': 1240, 'product_id': 62322, 'serial_number': None, 'release_number': 256, 'manufacturer_string': 'Microchip Technology Inc.', 'product_string': 'LUXAFOR FLAG', 'usage_page': 65280, 'usage': 1, 'interface_number': -1}]
```

## Luxafor()

```py3
class Luxafor:
    """Class to control Luxafor device."""

    def __init__(self, index=0, path=None):
```

Luxafor is the class that connects to the Luxafor USB device.

Parameters | Description
---------- | -----------
`index`    | Index of the HID USB device as returned by [`enumerate_luxafor()`](#enumerate_luxafor).
`path`     | The path of the HID USB device as returned by [`enumerate_luxafor()`](#enumerate_luxafor).


## Luxafor.close()

```py3
def close(self):
    """Close Luxafor device."""
```

Close the connection to the Luxafor device.

## Luxafor.off()

```py3
def off(self):
    """Set all LEDs to off."""
```

Sets all the LEDs of the Luxafor device off.

## Luxafor.basic_color()

````py3
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
````

Using the built-in color codes, set all the LEDs to the color.

Parameters | Description
---------- | -----------
`color`    | A string with either the values `R` (red), `G` (green), `B` (blue), `C` (cyan), `M` (magenta), `Y` (yellow), or `O` (off).


## Luxafor.color()

````py3
def color(self, color, *, led=LED_ALL):
    """
    Build static color command.

    ```
    Byte 0: Report number: 0 (Luxafor flag only has 0)
    Byte 1: Command Mode: 1
    Byte 2: LED: 1-6, 0x42 (back), 0x41 (front), 0xFF (all)
    Byte 3: Red channel: 0-255
    Byte 4: Green channel: 0-255
    Byte 5: Blue channel: 0-255
    Byte 6: NA
    Byte 7: NA
    Byte 8: NA
    ```

    """
````

Set LEDs to the specified colors. Each LED can be controlled individually. If a built-in color code is used, the command
will revert to `basic_color` functionality, which means `led` specifics will be ignored and all LED will be set.

Parameters | Description
---------- | -----------
`color`    | Color is specified by a string with hex RGB color codes in the form of `#RRGGBB` or `#RGB`. You can also use any CSS webcolor name, such as `red`, `green`, etc. `off` is treated like `black` which turns all LEDs off.
`led`      | Specific LEDs can be specified to control (1-6). You can also set all the front LEDs with `0x41`, all the back LEDs with `0x42`, or all the LEDs with `0xff`. See [LED constants](#leds).

## Luxafor.fade()

````py3
def fade(self, color, *, led=LED_ALL, speed=1, wait=False):
    """
    Build fade command.

    ```
    Byte 0: Report number: 0 (Luxafor flag only has 0)
    Byte 1: Command Mode: 2
    Byte 2: LED: 1-6, 0x42 (back), 0x41 (front), 0xFF (all)
    Byte 3: Red channel: 0-255
    Byte 4: Green channel: 0-255
    Byte 5: Blue channel: 0-255
    Byte 6: Fade speed: 0-255
    Byte 7: NA
    Byte 8: NA
    ```

    """
````

Fade a color in (or out if the color is `off` or `black`). Each LED can be controlled individually via `led`. The
duration/speed of the fade can also be controlled. If desired, you can wait for the command to complete as well.
Commands that employ `repeat=0` will continue forever, so wait will not be considered for infinite loops.

Parameters | Description
---------- | -----------
`color`    | Color is specified by a string with hex RGB color codes in the form of `#RRGGBB` or `#RGB`. You can also use any CSS webcolor name, such as `red`, `green`, etc. `off` is treated like `black` which turns all LEDs off.
`led`      | Specific LEDs can be specified to control (1-6). You can also set all the front LEDs with `0x41`, all the back LEDs with `0x42`, or all the LEDs with `0xff`. See [LED constants](#leds).
`speed`    | Speed at which the color will be faded (0-255). Lower is generally faster.
`repeat`   | How many times to repeat the fade effect (0-255). 0 will cause the effect to repeat forever.
`wait`     | Wait for the command to complete. Wait will be ignored if `repeat` is 0.

## Luxafor.strobe()

````py3
def strobe(self, color, *, led=LED_ALL, speed=0, repeat=0, wait=False):
    """
    Build strobe command.

    ```
    Byte 0: Report number: 0 (Luxafor flag only has 0)
    Byte 1: Command Mode: 3
    Byte 2: LED: 1-6, 0x42 (back), 0x41 (front), 0xFF (all)
    Byte 3: Red channel: 0-255
    Byte 4: Green channel: 0-255
    Byte 5: Blue channel: 0-255
    Byte 6: Speed: 0-255
    Byte 7: NA
    Byte 8: Repeat: 0-255
    ```

    """
````

Strobe the LEDs with the specified color. Each LED can be controlled individually via `led`. You can also control the
speed and how many times the strobe repeats. If desired, you can wait for the command to complete as well. Commands
that employ `repeat=0` will continue forever, so wait will not be considered for infinite loops.

Parameters | Description
---------- | -----------
`color`    | Color is specified by a string with hex RGB color codes in the form of `#RRGGBB` or `#RGB`. You can also use any CSS webcolor name, such as `red`, `green`, etc. `off` is treated like `black` which turns all LEDs off.
`led`      | Specific LEDs can be specified to control (1-6). You can also set all the front LEDs with `0x41`, all the back LEDs with `0x42`, or all the LEDs with `0xff`. See [LED constants](#leds).
`speed`    | Speed at which the color will strobe (0-255). Lower is generally faster.
`repeat`   | How many times to repeat the strobe effect (0-255). 0 will cause the effect to repeat forever.
`wait`     | Wait for the command to complete. Wait will be ignored if `repeat` is 0.

## Luxafor.wave()

````py3
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
````

Apply a wave effect using the specified color across the LEDs. You can control the speed and how many times the wave
is repeated. If desired, you can wait for the command to complete as well. Commands that employ `repeat=0` will continue
forever, so wait will not be considered for infinite loops.

Parameters | Description
---------- | -----------
`color`    | Color is specified by a string with hex RGB color codes in the form of `#RRGGBB` or `#RGB`. You can also use any CSS webcolor name, such as `red`, `green`, etc. `off` is treated like `black` which turns all LEDs off.
`wave`     | Specify the desired wave pattern. See the [wave constants](#waves).
`speed`    | Speed at which the color will apply the wave effect (0-255). Lower is generally faster.
`repeat`   | How many times to repeat the wave effect (0-255). 0 will cause the effect to repeat forever.
`wait`     | Wait for the command to complete. Wait will be ignored if `repeat` is 0.

## Luxafor.pattern()

````py3
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
````

Initiate one of the built-in patterns in the Luxafor device. You can also control how man times the pattern repeats. If
desired, you can wait for the command to complete as well. Commands that employ `repeat=0` will continue forever, so
wait will not be considered for infinite loops.

Parameters | Description
---------- | -----------
`pattern`  | Pattern code (1-8). See the [pattern constants](#patterns).
`repeat`   | How many times to repeat the pattern (0-255). 0 will cause the effect to repeat forever.
`wait`     | Wait for the command to complete. Wait will be ignored if `repeat` is 0.
