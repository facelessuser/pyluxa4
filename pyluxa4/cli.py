"""Command line."""
import argparse
import os
import sys
import json
from . import common as cmn
from . import __meta__
from . import client


def process_schedule(schedule):
    """Read JSON file."""

    config = None
    if schedule and os.path.exists(schedule) and os.path.isfile(schedule):
        with open(schedule, 'r') as f:
            config = json.loads(f.read())
        if not isinstance(config, list):
            raise ValueError('JSON file should contain a list of events')
    return config


class LedAction(argparse.Action):
    """Resolve LED options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        led = cmn.resolve_led(values)
        setattr(namespace, self.dest, led)


class PatternAction(argparse.Action):
    """Check pattern options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        p = cmn.resolve_pattern(values)
        setattr(namespace, self.dest, p)


class WaveAction(argparse.Action):
    """Check wave options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        w = cmn.resolve_wave(values)
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


class TimerAction(argparse.Action):
    """Check repeat options."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Handle the action call."""

        cmn.validate_timer_cycle(values)
        setattr(namespace, self.dest, values)


def connection_args(parser):
    """Connection arguments to control the request."""

    parser.add_argument('--host', default=client.HOST, help="Host")
    parser.add_argument('--port', type=int, default=client.PORT, help="Port")
    parser.add_argument(
        '--secure', default=None,
        help="Enable https requests: enable verification (1), disable verification(0), or specify a certificate."
    )
    parser.add_argument('--timeout', type=int, default=client.TIMEOUT, help="Timeout")


def cmd_color(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 color', description="Set color")
    parser.add_argument('color', help="Color value.")
    parser.add_argument('--led', action=LedAction, default=cmn.LED_ALL, help="LED: 1-6, back, front, or all")
    parser.add_argument('--token', default='', help="Send API token")
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
    parser.add_argument('color', help="Color value.")
    parser.add_argument('--led', action=LedAction, default=cmn.LED_ALL, help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action=SpeedAction, type=int, default=0, help="Speed of fade: 0-255")
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).fade(
        args.color,
        led=args.led,
        speed=args.speed,
        timeout=args.timeout
    )


def cmd_strobe(argv):
    """Strobe color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 strobe', description="Strobe color")
    parser.add_argument('color', help="Color value.")
    parser.add_argument('--led', action=LedAction, default=cmn.LED_ALL, help="LED: 1-6, back, front, or all")
    parser.add_argument('--speed', action=SpeedAction, type=int, default=0, help="Speed of strobe: 0-255")
    parser.add_argument('--repeat', action=RepeatAction, type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).strobe(
        args.color,
        led=args.led,
        speed=args.speed,
        repeat=args.repeat,
        timeout=args.timeout
    )


def cmd_wave(argv):
    """Show color with wave effect."""

    parser = argparse.ArgumentParser(prog='pyluxa4 wave', description="Wave effect")
    parser.add_argument('color', help="Color value.")
    parser.add_argument('--wave', action=WaveAction, default=cmn.WAVE_SHORT, help="Wave configuration: 1-5")
    parser.add_argument('--speed', action=SpeedAction, type=int, default=0, help="Speed of wave effect: 0-255")
    parser.add_argument('--repeat', action=RepeatAction, type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).wave(
        args.color,
        wave=args.wave,
        speed=args.speed,
        repeat=args.repeat,
        timeout=args.timeout
    )


def cmd_pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pyluxa4 pattern', description="Display pattern")
    parser.add_argument('pattern', action=PatternAction, help="Pattern value.")
    parser.add_argument('--repeat', action=RepeatAction, type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).pattern(
        args.pattern,
        repeat=args.repeat,
        timeout=args.timeout
    )


def cmd_off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pyluxa4 off', description="Turn off")
    parser.add_argument('--token', default='', help="Send API token")
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
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).kill(
        timeout=args.timeout
    )


def cmd_scheduler(argv):
    """Send a schedule to execute patterns and/or clear existing schedules."""

    parser = argparse.ArgumentParser(prog='pyluxa4 scheduler', description="Schedule events")
    parser.add_argument('--schedule', help="JSON schedule file.")
    parser.add_argument('--clear', action='store_true', help="Clear all scheduled events")
    parser.add_argument('--cancel', action='store_true', help="Cancel timers.")
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port, args.secure, args.token).scheduler(
        schedule=process_schedule(args.schedule),
        clear=args.clear,
        cancel=args.cancel,
        timeout=args.timeout
    )


def cmd_timer(argv):
    """Setup timers."""

    parser = argparse.ArgumentParser(prog='pyluxa4 timer', description="Setup timers")
    parser.add_argument(
        '--times', help="List of relative times (<num hours>:<num minutes>) separated by commas.", required=True
    )
    parser.add_argument('--type', help="Timer event type: color, strobe, fade, wave, pattern, or off", required=True)
    parser.add_argument('--led', action=LedAction, default=cmn.LED_ALL, help="LED: 1-6, back, tab, or all")
    parser.add_argument('--color', help="Color of timer alerts.")
    parser.add_argument('--pattern', action=PatternAction, help="Pattern of timer alerts.")
    parser.add_argument(
        '--wave', action=WaveAction, default=cmn.WAVE_SHORT, help="Force a given wave effect instead of strobe."
    )
    parser.add_argument('--speed', action=SpeedAction, type=int, default=0, help="Speed of strobe or wave: 0-255")
    parser.add_argument('--repeat', action=RepeatAction, type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument(
        '--cycle', action=TimerAction, type=int, default=1, help="Number of times to cycle through the timers."
    )
    parser.add_argument('--start', help="Delay the timer to a specific time.")
    parser.add_argument('--end', help="End timer at a specific time.")
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    if args.type == "color":
        cmd = "color"
        color_key = "color"
        color_value = args.color
        led = args.led
        speed = None
        repeat = None
        wave = None
    elif args.type == "fade":
        cmd = "fade"
        color_key = "color"
        color_value = args.color
        led = args.led
        speed = args.speed
        repeat = None
        wave = None
    elif args.type == "strobe":
        cmd = "strobe"
        color_key = "color"
        color_value = args.color
        led = args.led
        speed = args.speed
        repeat = args.repeat
        wave = None
    elif args.type == "wave":
        cmd = "wave"
        color_key = "color"
        color_value = args.color
        led = None
        speed = args.speed
        repeat = args.repeat
        wave = args.wave
    elif args.type == "pattern":
        cmd = "pattern"
        color_key = "pattern"
        color_value = args.pattern
        led = None
        repeat = args.repeat
        speed = None
        wave = None
    elif args.type == "off":
        cmd = "off"
        color_key = None
        color_value = None
        led = None
        repeat = None
        speed = None
        wave = None
    else:
        parser.error('Unrecognized --type {}'.format(args.type))

    if cmd in ('color', 'fade', 'strobe', 'wave') and color_value is None:
        parser.error('--color is required with --type color')
    elif cmd == 'pattern' and color_value is None:
        parser.error('--pattern is required with --type {}'.format(cmd))

    schedule = {
        "cmd": cmd,
        "timer": args.cycle,
        "start": args.start,
        "end": args.end,
        "days": "all",
        "times": args.times.split(','),
        "args": {}
    }

    if color_key is not None:
        schedule['args'][color_key] = color_value
    if repeat is not None:
        schedule['args']['repeat'] = repeat
    if speed is not None:
        schedule['args']['speed'] = speed
    if wave is not None:
        schedule['args']['wave'] = wave
    if led is not None:
        schedule['args']['led'] = led

    return client.LuxRest(args.host, args.port, args.secure, args.token).scheduler(
        schedule=[schedule],
        clear=False,
        timeout=args.timeout
    )


def cmd_get(argv):
    """Get information."""

    parser = argparse.ArgumentParser(prog='pyluxa4 get', description="Get information")
    parser.add_argument('info', help="Request information: schedule or timers")
    parser.add_argument('--token', default='', help="Send API token")
    connection_args(parser)
    args = parser.parse_args(argv)

    if args.info == 'schedule':
        return client.LuxRest(args.host, args.port, args.secure, args.token).get_schedule(
            timeout=args.timeout
        )
    elif args.info == 'timers':
        return client.LuxRest(args.host, args.port, args.secure, args.token).get_timers(
            timeout=args.timeout
        )
    else:
        parser.error('Unrecognized requested data {}'.format(args.info))


def cmd_serve(argv):
    """Start the server."""
    from . import server

    parser = argparse.ArgumentParser(prog='pyluxa4 serve', description="Run server")
    parser.add_argument('--schedule', default='', help="JSON schedule file.")
    parser.add_argument('--device-path', default=None, help="Luxafor device path")
    parser.add_argument('--device-index', type=int, default=0, help="Luxafor device index")
    parser.add_argument('--host', default=server.HOST, help="Host")
    parser.add_argument('--port', type=int, default=server.PORT, help="Port")
    parser.add_argument('--ssl-key', default=None, help="SSL key file (for https://)")
    parser.add_argument('--ssl-cert', default=None, help="SSL cert file (for https://)")
    parser.add_argument(
        '--token', default='', help="Assign a token that must be used when sending commands"
    )
    args = parser.parse_args(argv)

    path = args.device_path
    index = args.device_index
    kwargs = {}
    if args.ssl_key:
        kwargs['keyfile'] = args.ssl_key
    if args.ssl_cert:
        kwargs['certfile'] = args.ssl_cert

    server.run(args.host, args.port, index, path, args.token, process_schedule(args.schedule), **kwargs)


def cmd_list(argv):
    """List Luxafor devices."""

    from . import usb

    parser = argparse.ArgumentParser(prog='pyluxa4 list', description="List available Luxafor devices")
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
        'command',
        action='store',
        help=(
            "Command to send: color, off, fade, strobe, wave, pattern, api, serve, "
            "kill, get, schedule, and timer"
        )
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

        elif args.command == 'scheduler':
            resp = cmd_scheduler(argv[1:])

        elif args.command == 'timer':
            resp = cmd_timer(argv[1:])

        elif args.command == 'get':
            resp = cmd_get(argv[1:])

        else:
            parser.error('{} is not a recognized commad'.format(args.command))

        print(resp)

        if resp['status'] == 'fail':
            status = 1

    return status
