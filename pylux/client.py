"""Main."""
import sys
import argparse
import requests
import json
from .common import resolve_led
from . import __meta__
import traceback

def post(host, port, command, payload):
    """Post a REST command."""

    try:
        resp = requests.post(
            '%s:%d/pylux/api/v%s.%s/command/%s' % (
                host,
                port,
                __meta__.__version_info__[0],
                __meta__.__version_info__[1],
                command
            ),
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
            timeout=1000
        )
    except Exception:
        return {"status": "fail", "error": traceback.format_exc()}

    return json.loads(resp.text)


def set(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pylux set', description="Set color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--host', action='store', default="http://127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return post(
        args.host, args.port,
        'set',
        {
            'color': args.color.lower(),
            'led': resolve_led(args.led)
        }
    )


def fade(argv):
    """Fade to color."""

    parser = argparse.ArgumentParser(prog='pylux fade', description="Fade to color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="http://127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return post(
        args.host, args.port,
        'fade',
        {
            'color': args.color.lower(),
            'led': resolve_led(args.led),
            'duration': args.duration,
            'wait': args.wait
        }
    )


def strobe(argv):
    """Strobe color."""

    parser = argparse.ArgumentParser(prog='pylux strobe', description="Strobe color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action='store', type=int, default=0, help="Speed of strobe: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="http://127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return post(
        args.host, args.port,
        'strobe',
        {
            'color': args.color.lower(),
            'led': resolve_led(args.led),
            'speed': args.speed,
            'repeat': args.repeat,
            'wait': args.wait
        }
    )


def wave(argv):
    """Show color with wave effect."""

    parser = argparse.ArgumentParser(prog='pylux wave', description="Wave effect")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--wave', action='store', type=int, default=1, help="Wave configuration: 1-5")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of wave effect: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="http://127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return post(
        args.host, args.port,
        'strobe',
        {
            'color': args.color.lower(),
            'led': resolve_led(args.led),
            'wave': args.wave,
            'duration': args.duration,
            'repeat': args.repeat,
            'wait': args.wait
        }
    )


def pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pylux pattern', description="Display pattern")
    parser.add_argument('pattern', action='store', type=int, help="Color value.")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="http://127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return post(
        args.host, args.port,
        'strobe',
        {
            'pattern': args.pattern,
            'repeat': args.repeat,
            'wait': args.wait
        }
    )


def off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pylux off', description="Turn off")
    parser.add_argument('--host', action='store', default="http://127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv[1:])

    return post(
        args.host, args.port,
        'off'
    )


def main(argv):
    """Main."""
    parser = argparse.ArgumentParser(prog='pylux', description='Luxafor control tool.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __meta__.__version__))
    parser.add_argument(
        'command', action='store', help="Command to send: set, off, fade, strobe, wave, pattern, and server"
    )
    args = parser.parse_args(argv[0:1])

    if args.command == 'set':
        resp = set(argv[1:])

    elif args.command == 'off':
        resp = off(argv[1:])

    elif args.command == 'fade':
        resp = fade(argv[1:])

    elif args.command == 'strobe':
        resp = strobe(argv[1:])

    elif args.command == 'wave':
        resp = wave(argv[1:])

    elif args.command == 'pattern':
        resp = pattern(argv[1:])

    else:
        raise ValueError('{} is not a recognized commad'.format(args.command))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
