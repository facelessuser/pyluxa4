"""Command line."""
import argparse
import os
import sys
from . import common as cmn
from . import __meta__
from . import client

LED_MAP = {
    "all": cmn.LED_ALL,
    "back": cmn.LED_BACK,
    "front": cmn.LED_FRONT
}

PATTERN_MAP = {
    'traffic-light': cmn.PATTERN_TRAFFIC_LIGHT,
    'police': cmn.PATTERN_POLICE,
    'rainbow': cmn.PATTERN_RAINBOW,
    'random1': cmn.PATTERN_RANDOM1,
    'random2': cmn.PATTERN_RANDOM2,
    'random3': cmn.PATTERN_RANDOM3,
    'random4': cmn.PATTERN_RANDOM4,
    'random5': cmn.PATTERN_RANDOM5
}

WAVE_MAP = {
    "short": cmn.WAVE_SHORT,
    "long": cmn.WAVE_LONG,
    "overlapping-short": cmn.WAVE_OVERLAPPING_SHORT,
    "overlapping-long": cmn.WAVE_OVERLAPPING_LONG
}


class LedAction(argparse.Action):
    """Resolve LED options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        led = values.lower()
        if led in LED_MAP:
            led = LED_MAP[led]
        else:
            try:
                led = int(led)
                cmn.validate_led(led)
            except Exception:
                raise ValueError('Invalid LED value of {}'.format(led))

        setattr(namespace, self.dest, led)


class PatternAction(argparse.Action):
    """Check pattern options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        p = values.lower()
        if p in PATTERN_MAP:
            p = PATTERN_MAP[p]
        else:
            try:
                p = int(p)
                cmn.validate_pattern(p)
            except Exception:
                raise ValueError('Invalid pattern value of {}'.format(p))

        setattr(namespace, self.dest, p)


class WaveAction(argparse.Action):
    """Check wave options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        w = values.lower()
        if w in WAVE_MAP:
            w = WAVE_MAP[w]
        else:
            try:
                w = int(w)
                cmn.validate_wave(w)
            except Exception as e:
                print(e)
                raise ValueError('Invalid wave value of {}'.format(w))

        setattr(namespace, self.dest, w)


class SpeedAction(argparse.Action):
    """Check speed options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        cmn.validate_speed(values)
        setattr(namespace, self.dest, values)


class RepeatAction(argparse.Action):
    """Check repeat options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        cmn.validate_repeat(values)
        setattr(namespace, self.dest, values)


def connection_args(parser):
    """Connection arguments to control the request."""

    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument(
        '--secure', action='store', default=None,
        help="Enable https requests: enable verification (1), disable verification(0), or specify a certificate."
    )
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")


def cmd_color(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 color', description="Set color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action=LedAction, default=cmn.LED_ALL, help="LED: 1-6, back, front, or all")
    parser.add_argument('--token', action='store', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).color(
        args.color,
        led=args.led,
        timeout=args.timeout
    )


def cmd_fade(argv):
    """Fade to color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 fade', description="Fade to color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action=LedAction, default=cmn.LED_ALL, help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action=SpeedAction, type=int, default=0, help="Speed of fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--token', action='store', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).fade(
        args.color,
        led=args.led,
        speed=args.speed,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_strobe(argv):
    """Strobe color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 strobe', description="Strobe color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action=LedAction, default=cmn.LED_ALL, help="LED: 1-6, back, front, or all")
    parser.add_argument('--speed', action=SpeedAction, type=int, default=0, help="Speed of strobe: 0-255")
    parser.add_argument('--repeat', action=RepeatAction, type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--token', action='store', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).strobe(
        args.color,
        led=args.led,
        speed=args.speed,
        repeat=args.repeat,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_wave(argv):
    """Show color with wave effect."""

    parser = argparse.ArgumentParser(prog='pyluxa4 wave', description="Wave effect")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--wave', action=WaveAction, default=cmn.WAVE_SHORT, help="Wave configuration: 1-5")
    parser.add_argument('--speed', action=SpeedAction, type=int, default=0, help="Speed of wave effect: 0-255")
    parser.add_argument('--repeat', action=RepeatAction, type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--token', action='store', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).wave(
        args.color,
        wave=args.wave,
        speed=args.speed,
        repeat=args.repeat,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pyluxa4 pattern', description="Display pattern")
    parser.add_argument('pattern', action=PatternAction, help="Pattern value.")
    parser.add_argument('--repeat', action=RepeatAction, type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--token', action='store', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).pattern(
        args.pattern,
        repeat=args.repeat,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pyluxa4 off', description="Turn off")
    parser.add_argument('--token', action='store', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).off(
        timeout=args.timeout
    )


def cmd_version(argv):
    """Get the server to respond with the version."""

    parser = argparse.ArgumentParser(prog='pyluxa4 api', description="Request version")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure).version(timeout=args.timeout)


def cmd_kill(argv):
    """Kill the running server."""

    parser = argparse.ArgumentParser(prog='pyluxa4 kill', description="Kill server")
    parser.add_argument('--token', action='store', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).kill(
        timeout=args.timeout
    )


def cmd_serve(argv):
    """Start the server."""
    from . import server

    parser = argparse.ArgumentParser(prog='pyluxa4 serve', description="Run server")
    parser.add_argument('--device-path', action='store', default=None, help="Luxafor device path")
    parser.add_argument('--device-index', action='store', type=int, default=0, help="Luxafor device index")
    parser.add_argument('--host', action='store', default=server.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=server.PORT, help="Port")
    parser.add_argument('--ssl-key', action='store', default=None, help="SSL key file (for https://)")
    parser.add_argument('--ssl-cert', action='store', default=None, help="SSL cert file (for https://)")
    parser.add_argument(
        '--token', action='store', default='', help="Assign a token that must be used when sending commands"
    )
    args = parser.parse_args(argv)

    path = args.device_path
    index = args.device_index
    kwargs = {}
    if args.ssl_key:
        kwargs['keyfile'] = args.ssl_key
    if args.ssl_cert:
        kwargs['certfile'] = args.ssl_cert

    server.run(args.host, args.port, index, path, args.token, **kwargs)


def cmd_list(argv):
    """List Luxafor devices."""

    from . import usb

    parser = argparse.ArgumentParser(prog='pyluxa4 serve', description="List available Luxafor devices")
    parser.parse_args(argv)

    devices = usb.enumerate_luxafor()
    for index, device in enumerate(devices):
        print('{:d}> {}'.format(index, os.fsdecode(device['path'])))


def main():
    """Main."""
    status = 0
    argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog='pyluxa4', description='Luxafor control tool.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __meta__.__version__))
    parser.add_argument(
        'command', action='store', help="Command to send: color, off, fade, strobe, wave, pattern, api, serve, and kill"
    )
    args = parser.parse_args(argv[0:1])

    if args.command == 'serve':
        cmd_serve(argv[1:])
    elif args.command == 'list':
        cmd_list(argv[1:])
    else:
        if args.command == 'api':
            resp = cmd_version(argv[1:])

        elif args.command == 'kill':
            resp = cmd_kill(argv[1:])

        elif args.command == 'color':
            resp = cmd_color(argv[1:])

        elif args.command == 'off':
            resp = cmd_off(argv[1:])

        elif args.command == 'fade':
            resp = cmd_fade(argv[1:])

        elif args.command == 'strobe':
            resp = cmd_strobe(argv[1:])

        elif args.command == 'wave':
            resp = cmd_wave(argv[1:])

        elif args.command == 'pattern':
            resp = cmd_pattern(argv[1:])

        else:
            raise ValueError('{} is not a recognized commad'.format(args.command))

        print(resp)

        if resp['status'] == 'fail':
            status = 1

    return status
