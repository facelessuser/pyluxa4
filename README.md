# Python Luxafor

`pyluxa4` is a Python library for controller Luxafor devices. You can set colors, blink them, fade them, apply a wave
effect, and even run its built-in patterns. All of this is done by running a small server that is accessed locally on
port 5000 (though the port can be changed). Once running, you can issue commands from the CLI tool, which in turns
communicates with the server using a REST API.

Since the server uses a REST API, you could easily write scripts in other languages to control the device once running.

If desired, you can import the `pyluxa4.usb` library in a script and control the device directly without running a
server. Or you could import `pyluxa4.client` and write your own application that uses the API to control the device
through the server.

## Installation

1. `luxa4` requires [libusb/hidapi](https://github.com/libusb/hidapi) to be installed.

    - macOS: the easiest way is to just install with brew.

        ```
        brew install hidapi
        ```

    - Windows: simply download the [pre-built binaries](https://github.com/libusb/hidapi/releases) and make them
      available in your path.

    - Install via the provided package manager for your distro, or build from source.

2. Lastly, install `pyluxa4`.

## CLI Usage

### List

The `list` command lists all the available Luxafor devices connected to the machine. It provides the index in the list
and the path at which it is found. Either the index or path can be used in the `serve` command to specify which device
to connect to.

```
$ pyluxa4 list --help
usage: pyluxa4 serve [-h]

List available Luxafor devices

optional arguments:
  -h, --help  show this help message and exit
```

### Serve

The `serve` connects with your device and starts a server. By default, the first Luxafor device found is the one that
the server will connect to, but you can specify a specific device by either using `--device-path` or `--device-index`.
`--device-path` take precedence over `--device-index`.

If you wish to restrict those making requests via the API, you can assign an ID with the `--token` option, and only
requests that provide the matching ID will be accepted. `--token` should really only be used over SSL.

You can also ensure the server only takes HTTPS requests by using `--ssl-key` and `--ssl-cert`. Support is limited.
`pyluxa4` is only really intended to be used on a local network, and probably with only self signed certificates.
Commands sent via the client should use the `--secure <option>` option to either send requests with verification (1),
requests with no verification (0), or to specify a certificate to validate against.

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

### Color

The `color` command sets the color on the device. The color is specified either in the form `#RRGGBB`, `#RGB`, or using
webcolor names. `off` is also accepted and which is an alias for `black` which turns off the lights.

You can also use Luxafor's shorthand for the built-in color presets:

- `R` (red)
- `G` (green)
- `B`(blue)
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

### Fade

The `fade` command will fade a color in, or in the case of `off`, out. You can specify the speed of the fade which
to increase how long it takes to fade the color.

If needed, you can also control each LED individually, or by the groups front and back. Though, the `--led` option will
be ignored if you use Luxafor's built-in, color shorthand, as that is executed using a command that does not expose
single LED resolution.

```
$ pyluxa4 fade --help
usage: pyluxa4 fade [-h] [--led LED] [--speed SPEED] [--wait]
                    [--token TOKEN] [--host HOST] [--port PORT]
                    [--secure SECURE] [--timeout TIMEOUT]
                    color

Fade to color

positional arguments:
  color                Color value.

optional arguments:
  -h, --help           show this help message and exit
  --led LED            LED: 1-6, back, tab, or all
  --speed SPEED        Speed of fade: 0-255
  --wait               Wait for sequence to complete
  --token TOKEN        Send API token
  --host HOST          Host
  --port PORT          Port
  --secure SECURE      Enable https requests: enable verification (1), disable
                       verification(0), or specify a certificate.
  --timeout TIMEOUT    Timeout
```

### Strobe

The `strobe` command will cause a color to blink on and off. You can control how fast it blinks, and how many times.

If needed, you can also control each LED individually, or by the groups front and back. Though, the `--led` option will
be ignored if you use Luxafor's built-in, color shorthand, as that is executed using a command that does not expose
single LED resolution.

```
$ pyluxa4 strobe --help
usage: pyluxa4 strobe [-h] [--led LED] [--speed SPEED] [--repeat REPEAT]
                      [--wait] [--token TOKEN] [--host HOST] [--port PORT]
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
  --wait             Wait for sequence to complete
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

### Wave

The `wave` command provides a way to have a color perform a wave effect. The type of wave, speed of the wave, and how
many times it repeats can all be controlled.

You cannot control individual LEDs with the wave command as all the LEDs are needed to perform the wave effect.

```
$ pyluxa4 wave --help
usage: pyluxa4 wave [-h] [--wave WAVE] [--speed SPEED] [--repeat REPEAT]
                    [--wait] [--token TOKEN] [--host HOST] [--port PORT]
                    [--secure SECURE] [--timeout TIMEOUT]
                    color

Wave effect

positional arguments:
  color                Color value.

optional arguments:
  -h, --help           show this help message and exit
  --wave WAVE          Wave configuration: 1-5
  --speed SPEED        Speed of wave effect: 0-255
  --repeat REPEAT      Number of times to repeat: 0-255
  --wait               Wait for sequence to complete
  --token TOKEN        Send API token
  --host HOST          Host
  --port PORT          Port
  --secure SECURE      Enable https requests: enable verification (1), disable
                       verification(0), or specify a certificate.
  --timeout TIMEOUT    Timeout
```

### Pattern

The `pattern` command initiates one of 8 built-in patterns on the Luxafor device. You can control which pattern is
displayed along with how many times it repeats.

You cannot control individual LEDs with the pattern command as all the LEDs are needed to perform the patterns.

```
$ pyluxa4 pattern --help
usage: pyluxa4 pattern [-h] [--repeat REPEAT] [--wait] [--token TOKEN]
                       [--host HOST] [--port PORT] [--secure SECURE]
                       [--timeout TIMEOUT]
                       pattern

Display pattern

positional arguments:
  pattern            Color value.

optional arguments:
  -h, --help         show this help message and exit
  --repeat REPEAT    Number of times to repeat: 0-255
  --wait             Wait for sequence to complete
  --token TOKEN      Send API token
  --host HOST        Host
  --port PORT        Port
  --secure SECURE    Enable https requests: enable verification (1), disable
                     verification(0), or specify a certificate.
  --timeout TIMEOUT  Timeout
```

### Off

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

### Kill

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

### API

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

## License

MIT License

Copyright (c) 2019 Isaac Muse
