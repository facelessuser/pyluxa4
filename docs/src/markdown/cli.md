# CLI Usage

## List

The `list` command lists all the available Luxafor devices connected to the machine. It provides the index of the device
in the list and the path at which it is found. Either the index or path can be used in the `serve` command to specify
which device to connect to, the path will always take precedence.

```
$ pyluxa4 list --help
usage: pyluxa4 serve [-h]

List available Luxafor devices

optional arguments:
  -h, --help  show this help message and exit
```

## Serve

The `serve` command connects with your device and starts a server. By default, the first Luxafor device that is found is
the one that the server will connect to, but you can specify a specific device by either using `--device-path` or
`--device-index`. `--device-path` take precedence over `--device-index`.

You can restrict the incoming requests by using a token via the `--token` option, and only requests that provide the
token will be accepted. `--token` should really only be used over SSL.

You can also ensure the server only takes HTTPS requests by using `--ssl-key` and `--ssl-cert`. Support is limited.
`pyluxa4` is only really intended to be used on a local network, and probably with only self signed certificates.
Commands sent via the client should use the `--secure <option>` option to either send requests with verification (`1`),
requests with no verification (`0`), or to specify a certificate to validate against.

!!! warning "Linux"
    You may need to run the server as `sudo` in order to connect to the Luxafor device. If you get errors about not
    being able to connect, try `sudo`.

```
$ pyluxa4 serve --help
usage: pyluxa4 serve [-h] [--device-path DEVICE_PATH]
                     [--device-index DEVICE_INDEX] [--host HOST] [--port PORT]
                     [--ssl-key SSL_KEY] [--ssl-cert SSL_CERT]
                     [--token TOKEN]

Run server

optional arguments:
  -h, --help            show this help message and exit
  --device-path DEVICE_PATH
                        Luxafor device path
  --device-index DEVICE_INDEX
                        Luxafor device index
  --host HOST           Host
  --port PORT           Port
  --ssl-key SSL_KEY     SSL key file (for https://)
  --ssl-cert SSL_CERT   SSL cert file (for https://)
  --token TOKEN         Assign an token that must be used when sending commands
```

## Color

The `color` command sets the color on the device. The color is specified either in the form `#RRGGBB`, `#RGB`, or using
webcolor names. `off` is also accepted and is an alias for `black` which turns off the lights.

You can also use Luxafor's shorthand for the built-in color presets:

- `R` (red)
- `G` (green)
- `B` (blue)
- `C` (cyan)
- `Y` (yellow)
- `M` (magenta)
- `W` (white)
- `O` (off)

If needed, you can also control each LED individually, or by the groups front and back. Though, the `--led` option will
be ignored if you use Luxafor's built-in, color shorthand, as that is executed using a command that does not expose
single LED resolution.

```
$ pyluxa4 color --help
usage: pyluxa4 color [-h] [--led LED] [--token TOKEN] [--host HOST]
                     [--port PORT] [--secure SECURE] [--timeout TIMEOUT]
                     color

Set color

positional arguments:
  color              Color value.

optional arguments:
  -h, --help         show this help message and exit
  --led LED          LED: 1-6, back, front, or all
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## Fade

The `fade` command will fade a color in, or in the case of `off` out. You can specify the speed of the fade which
to increase how long it takes to fade the color. A low value will be faster than a big value.

Color can be any value excepted by the [`color`](#color) command except Luxafor shorthand for basic colors (e.g. `R`,
`G`, `B`, etc.).

If needed, you can also control each LED individually, or by the groups front and back.

```
$ pyluxa4 fade --help
usage: pyluxa4 fade [-h] [--led LED] [--speed SPEED] [--token TOKEN]
                    [--host HOST] [--port PORT] [--secure SECURE]
                    [--timeout TIMEOUT]
                    color

Fade to color

positional arguments:
  color              Color value.

optional arguments:
  -h, --help         show this help message and exit
  --led LED          LED: 1-6, back, tab, or all
  --speed SPEED      Speed of fade: 0-255
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## Strobe

The `strobe` command will cause a color to blink on and off. You can control how fast it blinks and how many times.

If needed, you can also control each LED individually, or by the groups front and back.

Color can be any value excepted by the [`color`](#color) command except Luxafor shorthand for basic colors (e.g. `R`,
`G`, `B`, etc.).

```
$ pyluxa4 strobe --help
usage: pyluxa4 strobe [-h] [--led LED] [--speed SPEED] [--repeat REPEAT]
                      [--token TOKEN] [--host HOST] [--port PORT]
                      [--secure SECURE] [--timeout TIMEOUT]
                      color

Strobe color

positional arguments:
  color              Color value.

optional arguments:
  -h, --help         show this help message and exit
  --led LED          LED: 1-6, back, front, or all
  --speed SPEED      Speed of strobe: 0-255
  --repeat REPEAT    Number of times to repeat: 0-255
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## Wave

The `wave` command provides a way to have a color perform a wave effect. The type of wave, speed of the wave, and how
many times it repeats can all be controlled. You can also use friendly names for 4 of the wave patterns instead of their
numerical patterns:

Wave | Alias
---- | -----
1    | `short`
2    | `long`
3    | `overlapping-short`
4    | `overlapping-long`
5    | NA

You cannot control individual LEDs with the wave command as all the LEDs are needed to perform the wave effect.

Color can be any value excepted by the [`color`](#color) command except Luxafor shorthand for basic colors (e.g. `R`,
`G`, `B`, etc.).

```
$ pyluxa4 wave --help
usage: pyluxa4 wave [-h] [--wave WAVE] [--speed SPEED] [--repeat REPEAT]
                    [--token TOKEN] [--host HOST] [--port PORT]
                    [--secure SECURE] [--timeout TIMEOUT]
                    color

Wave effect

positional arguments:
  color              Color value.

optional arguments:
  -h, --help         show this help message and exit
  --wave WAVE        Wave configuration: 1-5
  --speed SPEED      Speed of wave effect: 0-255
  --repeat REPEAT    Number of times to repeat: 0-255
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## Pattern

The `pattern` command initiates one of 8 built-in patterns on the Luxafor device. You can control which pattern is
displayed along with how many times it repeats. You can also use friendly names for patterns instead of their numerical
values:

Pattern | Alias
------- | -----
1       | `traffic-light`
2       | `random1`
3       | `random2`
4       | `random3`
5       | `police`
6       | `random4`
7       | `random5`
8       | `rainbow`

You cannot control individual LEDs with the pattern command as all the LEDs are needed to perform the patterns.


```
$ pyluxa4 pattern --help
usage: pyluxa4 pattern [-h] [--repeat REPEAT] [--token TOKEN] [--host HOST]
                       [--port PORT] [--secure SECURE] [--timeout TIMEOUT]
                       pattern

Display pattern

positional arguments:
  pattern            Pattern value.

optional arguments:
  -h, --help         show this help message and exit
  --repeat REPEAT    Number of times to repeat: 0-255
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## Off

The `off` command turns off all lights on the Luxafor device.

You cannot control which LED is turned off with this command. If you need per LED resolution, simply use `pyluxa4 color
off --led <led>` to control individual LEDs.

```
$ pyluxa4 off --help
usage: pyluxa4 off [-h] [--token TOKEN] [--host HOST] [--port PORT]
                   [--secure SECURE] [--timeout TIMEOUT]

Turn off

optional arguments:
  -h, --help         show this help message and exit
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## Kill

The `kill` command is used to kill an already running server.

```
$ pyluxa4 kill --help
usage: pyluxa4 kill [-h] [--token TOKEN] [--host HOST] [--port PORT]
                    [--secure SECURE] [--timeout TIMEOUT]

Kill server

optional arguments:
  -h, --help         show this help message and exit
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## Schedule

The `schedule` command takes a JSON file with either commands for either [color](#color), [fade](#fade),
[strobe](#strobe), [wave](#wave), [pattern](#pattern), or [off](#off).

Commands must contain:

- `type` which is the command type, and is the name of the commands mentioned above.
- `days` which can be either a single string or list of string values representing days of the week: `mon`, `tue`,
  `wen`, `thu`, `fri`, `sat`, or `sun`. You can also use `wke` to specify the weekend or `wkd` to specify weekdays.
  `all` would mean all days.
- `times` which can be either a single string or a list of string values representing the hour and minute for the light
  to trigger on. The format should be `H:M` where `H` is the hour from 0 - 23 and `M` is the minute from 0 - 59.

Lastly, you can specify the arguments for the command under the `args` keyword. For commands like `color`, `fade`,
`strobe`, and `wave`, you must specify the color under `color`. For `pattern` you must specify the pattern under
`pattern`. All other options such as `speed`, `repeat`, or `wave` (for the wave pattern) are optional.

For values that are numbers you can use integers. For values that are strings, you can use strings.

Example JSON (`schedule.json`):

```js
[
    {
        "type": "pattern",
        "days": ["all"],
        "times": "20:21",
        "args": {
            "pattern": "police",
            "repeat": 3
        }
    },

    {
        "type": "fade",
        "days": "all",
        "times": ["20:20", "20:22"],
        "args": {
            "color": "red",
            "speed": 100
        }
    }
]
```

Command load the schedule:

```
$ pyluxa4 schedule schedule.json
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.1/command/schedule', 'status': 'success'}
```

```
$ pyluxa4 schedule --help
usage: pyluxa4 kill [-h] [--token TOKEN] [--host HOST] [--port PORT]
                    [--secure SECURE] [--timeout TIMEOUT]
                    file

Kill server

positional arguments:
  file               JSON schedule file.

optional arguments:
  -h, --help         show this help message and exit
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

## API

The `api` command simply returns the API for the current running server.

```
$ pyluxa4 api --help
usage: pyluxa4 api [-h] [--host HOST] [--port PORT] [--secure SECURE]
                   [--timeout TIMEOUT]

Request version

optional arguments:
  -h, --help         show this help message and exit
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

--8<--
refs.txt
--8<--
