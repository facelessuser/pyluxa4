## List

The `list` command lists all the available Luxafor devices connected to the machine. It provides the index of the device
in the list and the path at which it is found. Either the index or path can be used in the `serve` command to specify
which device to connect to, the path will always take precedence.

```console
$ pyluxa4 list --help
usage: pyluxa4 list [-h]

List available Luxafor devices

optional arguments:
  -h, --help  show this help message and exit
```

## Serve

The `serve` command connects with your device and starts a server. By default, the first Luxafor device that is found is
the one that the server will connect to, but you can specify a specific device by either using `--device-path` or
`--device-index`. `--device-path` take precedence over `--device-index`.

If desired, you can schedule events by specifying a schedule file via the `--schedule` option. See
[Scheduler](#scheduler) for more information.

You can restrict the incoming requests by using a token via the `--token` option, and only requests that provide the
token will be accepted. `--token` should really only be used over SSL.

You can also ensure the server only takes HTTPS requests by using `--ssl-key` and `--ssl-cert`. Support is limited.
`pyluxa4` is only really intended to be used on a local network, and probably with only self signed certificates.
Commands sent via the client should use the `--secure <option>` option to either send requests with verification (`1`),
requests with no verification (`0`), or to specify a certificate to validate against.

/// warning | Linux
You may need to run the server as `sudo` in order to connect to the Luxafor device. If you get errors about not
being able to connect, try `sudo`.
///

```console
$ pyluxa4 serve --help
usage: pyluxa4 serve [-h] [--schedule SCHEDULE] [--device-path DEVICE_PATH] [--device-index DEVICE_INDEX] [--hidapi HIDAPI] [--host HOST]
                     [--port PORT] [--ssl-key SSL_KEY] [--ssl-cert SSL_CERT] [--token TOKEN]

Run server.

options:
  -h, --help            show this help message and exit
  --schedule SCHEDULE   JSON schedule file.
  --device-path DEVICE_PATH
                        Luxafor device path.
  --device-index DEVICE_INDEX
                        Luxafor device index.
  --hidapi HIDAPI       Explicit, absolute path to where the hidapi library can be found.
  --host HOST           Host
  --port PORT           Port.
  --ssl-key SSL_KEY     SSL key file (for https://).
  --ssl-cert SSL_CERT   SSL cert file (for https://).
  --token TOKEN         Assign a token that must be used when sending commands.
```

## Color

The `color` command sets the color on the device. The color can be specified via CSS color syntax including, but not
limited to, hex colors, RGB syntax, webcolor names, HSL, etc. Alpha will be ignored and out of gamut colors will be
gamut mapped into sRGB.

You can also use Luxafor's shorthand for the built-in color presets:

-   `R` (red)
-   `G` (green)
-   `B` (blue)
-   `C` (cyan)
-   `Y` (yellow)
-   `M` (magenta)
-   `W` (white)
-   `O` (off)

If needed, you can also control each LED individually, or by the groups front and back. Though, the `--led` option will
be ignored if you use Luxafor's built-in, color shorthand, as that is executed using a command that does not expose
single LED resolution.

```console
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

Color can be any value accepted by the [`color`](#color) command except Luxafor shorthand for basic colors (e.g. `R`,
`G`, `B`, etc.).

If needed, you can also control each LED individually, or by the groups front and back.

```console
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

Color can be any value accepted by the [`color`](#color) command except Luxafor shorthand for basic colors (e.g. `R`,
`G`, `B`, etc.).

```console
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

Color can be any value accepted by the [`color`](#color) command except Luxafor shorthand for basic colors (e.g. `R`,
`G`, `B`, etc.).

```console
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


```console
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

```console
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

```console
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

## Scheduler

The `scheduler` command takes a JSON file via `--schedule` with commands for either [color](#color),
[fade](#fade), [strobe](#strobe), [wave](#wave), [pattern](#pattern), or [off](#off), and schedules them to be executed
at the specified times on the specified days. Events are appended to previously scheduled events unless `--clear` is
provided. If desired, you can run `--clear` without `--schedule` which will simply clear all events. `--clear` does not
cancel timers, it only removes normal, scheduled events. To cancel timers, use `--cancel`.

```console
$ pyluxa4 scheduler --help
usage: pyluxa4 scheduler [-h] [--schedule SCHEDULE] [--clear] [--cancel]
                         [--token TOKEN] [--host HOST] [--port PORT]
                         [--secure SECURE] [--timeout TIMEOUT]

Schedule events

optional arguments:
  -h, --help           show this help message and exit
  --schedule SCHEDULE  JSON schedule file.
  --clear              Clear all scheduled events
  --cancel             Cancel timers.
  --token TOKEN        Send API token
  --host HOST          Host
  --port PORT          Port
  --secure SECURE      Enable https requests: enable verification (1), disable
                       verification(0), or specify a certificate.
  --timeout TIMEOUT    Timeout
```

To learn more about using the scheduler see [Scheduling Commands](./usage.md#scheduling-commands).

## Timer

The `timer` command provides a way to set off a timer that will execute a command based on a relative time.

```console
$ pyluxa4 timer --help
usage: pyluxa4 timer [-h] --times TIMES --cmd CMD [--led LED] [--color COLOR]
                     [--pattern PATTERN] [--wave WAVE] [--speed SPEED]
                     [--repeat REPEAT] [--cycle CYCLE] [--start START]
                     [--end END] [--token TOKEN] [--host HOST] [--port PORT]
                     [--secure SECURE] [--timeout TIMEOUT]

Setup timers

optional arguments:
  -h, --help         show this help message and exit
  --times TIMES      List of relative times (<num hours>:<num minutes>)
                     separated by commas.
  --cmd CMD          Timer event cmd: color, strobe, fade, wave, pattern, or
                     off
  --led LED          LED: 1-6, back, tab, or all
  --color COLOR      Color of timer alerts.
  --pattern PATTERN  Pattern of timer alerts.
  --wave WAVE        Force a given wave effect instead of strobe.
  --speed SPEED      Speed of strobe or wave: 0-255
  --repeat REPEAT    Number of times to repeat: 0-255
  --cycle CYCLE      Number of times to cycle through the timers.
  --start START      Delay the timer to a specific time.
  --end END          End timer at a specific time.
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

To learn more about setting timers, see [Setting Timers](./usage.md#setting-timers).

## Get

The `get` command allows you to retrieve information. Currently you can only retrieve the loaded `schedule` (scheduled
non-timer events) or scheduled `timers`:

```console
$ pyluxa4 get schedule
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.2/scheduler/schedule', 'schedule': [{'args': {'pattern': 'police', 'repeat': 3}, 'cmd': 'pattern', 'days': ['all'], 'times': '20:16'}, {'args': {'color': 'red', 'speed': 100}, 'cmd': 'fade', 'days': 'all', 'times': ['20:15', '20:17']}], 'status': 'success'}
```

```
pyluxa4 get --help
usage: pyluxa4 get [-h] [--token TOKEN] [--host HOST] [--port PORT]
                   [--secure SECURE] [--timeout TIMEOUT]
                   info

Get information

positional arguments:
  info               Request information: schedule or timers

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

```console
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
