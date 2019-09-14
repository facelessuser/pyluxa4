"""Luxafor client API."""
import sys
import argparse
import requests
import json
from .common import resolve_led, LED_ALL, LED_BACK, LED_FRONT
from . import __meta__
import traceback

__all__ = ('LuxRest', 'LED_ALL', 'LED_BACK', 'LED_FRONT')

HOST = "127.0.0.1"
PORT = 5000


class LuxRest:
    """Class to post commands to the REST API."""

    def __init__(self, host=HOST, port=PORT):
        """Initialize."""

        self.host = host
        self.port = port

    def _post(self, command, payload=None):
        """Post a REST command."""

        try:
            resp = requests.post(
                'http://%s:%d/pylux/api/v%s.%s/command/%s' % (
                    self.host,
                    self.port,
                    __meta__.__version_info__[0],
                    __meta__.__version_info__[1],
                    command
                ),
                data=json.dumps(payload) if payload is not None else None,
                headers={'content-type': 'application/json'} if payload is not None else None,
                timeout=1000
            )
        except Exception:
            return {"status": "fail", "error": traceback.format_exc()}

        return json.loads(resp.text)

    def set(self, color, *, led=LED_ALL):
        """Create command to set colors."""

        return self._post(
            "set",
            {
                "color": color,
                "led": led
            }
        )

    def fade(self, color, *, led=LED_ALL, duration=0, wait=False):
        """Create command to fade colors."""

        return self._post(
            "fade",
            {
                "color": color,
                "led": led,
                "duration": duration,
                "wait": wait
            }
        )

    def strobe(self, color, *, led=LED_ALL, speed=0, repeat=0, wait=False):
        """Create command to strobe colors."""

        return self._post(
            "strobe",
            {
                "color": color,
                "led": led,
                "speed": speed,
                "repeat": repeat,
                "wait": wait
            }
        )

    def wave(self, color, *, led=LED_ALL, wave=1, duration=0, repeat=0, wait=False):
        """Create command to use the wave effect."""

        return self._post(
            "wave",
            {
                "color": color,
                "led": led,
                "wave": wave,
                "duration": duration,
                "repeat": repeat,
                "wait": wait
            }
        )

    def pattern(self, pattern, *, led=LED_ALL, repeat=0, wait=False):
        """Create command to use the wave effect."""

        return self._post(
            "pattern",
            {
                "pattern": pattern,
                "repeat": repeat,
                "wait": wait
            }
        )

    def off(self):
        """Turn off all lights."""

        return self._post(
            "off",
            {}
        )


def cmd_set(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pylux set', description="Set color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--host', action='store', default="127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return LuxRest(args.host, args.port).set(
        args.color,
        led=resolve_led(args.led)
    )


def cmd_fade(argv):
    """Fade to color."""

    parser = argparse.ArgumentParser(prog='pylux fade', description="Fade to color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return LuxRest(args.host, args.port).fade(
        args.color,
        led=resolve_led(args.led),
        duration=args.duration,
        wait=args.wait
    )


def cmd_strobe(argv):
    """Strobe color."""

    parser = argparse.ArgumentParser(prog='pylux strobe', description="Strobe color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action='store', type=int, default=0, help="Speed of strobe: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return LuxRest(args.host, args.port).strobe(
        args.color,
        led=resolve_led(args.led),
        speed=args.speed,
        repeat=args.repeat,
        wait=args.wait
    )


def cmd_wave(argv):
    """Show color with wave effect."""

    parser = argparse.ArgumentParser(prog='pylux wave', description="Wave effect")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--wave', action='store', type=int, default=1, help="Wave configuration: 1-5")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of wave effect: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return LuxRest(args.host, args.port).wave(
        args.color,
        led=resolve_led(args.led),
        duration=args.duration,
        repeat=args.repeat,
        wait=args.wait
    )


def cmd_pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pylux pattern', description="Display pattern")
    parser.add_argument('pattern', action='store', type=int, help="Color value.")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default="127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv)

    return LuxRest(args.host, args.port).pattern(
        args.pattern,
        repeat=args.repeat,
        wait=args.wait
    )


def cmd_off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pylux off', description="Turn off")
    parser.add_argument('--host', action='store', default="127.0.0.1", help="Host.")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port.")
    args = parser.parse_args(argv[1:])

    return LuxRest(args.host, args.port).off()


def main(argv):
    """Main."""
    parser = argparse.ArgumentParser(prog='pylux', description='Luxafor control tool.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __meta__.__version__))
    parser.add_argument(
        'command', action='store', help="Command to send: set, off, fade, strobe, wave, and pattern"
    )
    args = parser.parse_args(argv[0:1])

    if args.command == 'set':
        resp = cmd_set(argv[1:])

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

    if resp['status'] == 'fail':
        print(resp)

    return 1 if resp['status'] == 'fail' else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
