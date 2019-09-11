# pylux

Luxafor flag controller. Requires: libusb/hidapi: https://github.com/libusb/hidapi to be installed.

## Command Line

```
usage: pylux [-h] [--version] (--set SET | --pattern PATTERN) [--pins PINS]
             [--mode MODE] [--wave WAVE] [--speed SPEED] [--repeat REPEAT]

Luxafor control script.

optional arguments:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  --set SET          Set color
  --pattern PATTERN  Patterns: 1-9
  --pins PINS        Pins: 1-6, back, tab, or all
  --mode MODE        Mode: static, fade, strobe, wave
  --wave WAVE        Wave configuration: 1-5
  --speed SPEED      Speed for strobe, wave, or fade: 1-255
  --repeat REPEAT    Repeat for strobe, wave, or pattern: 1-255
```

- Generally, you would use `--set` and specify a color by either the form `RRGGBB` or one of the supported color names:
  `pink`, `red`, `orange`, `yellow`, `green`, `cyan`, `blue`, `purple`, `white`, and `off` (turns all colors off).
- You can specify the `--mode` with `strobe`, `wave`, or `fade` to enable the desired effect.
- `--wave` is used to change the wave pattern used when `--mode` is `wave`.
- `--speed` controls the speed of `strobe`, `fade`, and `wave` effects.
- `--repeat` is used to repeat periodic effects or patterns. `--repeat` works on `strobe`, `wave`, and `--pattern`.
- `--pattern` is used instead of `--set` and can select one of nine patterns. Patterns 1-8 trigger one of the built-in
  patterns, while pattern 9 triggers a custom rainbow pattern provided by `pylux`. `--repeat` will repeat a given
  pattern the specified number of times.
- When specifying the color as `off`, only the `--fade` affect is recognized.

## Library

The library can be pulled in and used as a library.

```py
import pylux

device = pylux.LuxFlag()
device.set_red(mode="fade", speed=100)
device.set_off()
device.close()
```

Or you can do custom colors directly:

```py
import pylux.LuxFlag()
device.set_color([255, 000, 000], mode="fade", speed=100)
device.set_off()
device.close()
```

You can also run some of the hardware, built-in patterns (1-8). We've also included a custom software pattern "rainbow"
that is accessible as pattern 9.

```py
import pylux.LuxFlag()
device.set_pattern(1, repeat=2)
device.set_off()
device.close()
```

You can also run with the `with` statement which will close the connection automatically:

```py
with pylux.LuxFlag() as device:
    device.set_red(mode="fade", speed=100)
    device.set_off()
```

## License

MIT License

Copyright (c) 2019 Isaac Muse
