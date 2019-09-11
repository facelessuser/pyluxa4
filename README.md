# pylux

Luxafor flag controller.

```
usage: lux [-h] [--version] (--set SET | --pattern PATTERN) [--pins PINS]
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
  `pink`, `red`, `orange`, `yellow`, `green`, `cyan`, `blue`, `purple`, and `white`.
- You can specify the `--mode` with `strobe`, `wave`, or `fade` to enable the desired effect.
- `--wave` is used to change the wave pattern used when `--mode` is `wave`.
- `--speed` controls the speed of `strobe`, `fade`, and `wave` effects.
- `--repeat` is used to repeat periodic effects or patterns. `--repeat` works on `strobe`, `wave`, and `--pattern`.
- `--pattern` is used instead of `--set` and can select one of nine patterns. Patterns 1-8 trigger one of the built-in
  patterns, while pattern 9 triggers a custom rainbow pattern provided by `pylux`. `--repeat` will repeat a given
  pattern the specified number of times.
