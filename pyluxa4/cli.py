"""Command line."""
import argparse
from .common import resolve_led
from . import __meta__
from . import client


def cmd_set(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 set', description="Set color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host.")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port.")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).set(
        args.color,
        led=resolve_led(args.led)
    )


def cmd_fade(argv):
    """Fade to color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 fade', description="Fade to color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host.")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port.")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).fade(
        args.color,
        led=resolve_led(args.led),
        duration=args.duration,
        wait=args.wait
    )


def cmd_strobe(argv):
    """Strobe color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 strobe', description="Strobe color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action='store', type=int, default=0, help="Speed of strobe: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host.")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port.")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).strobe(
        args.color,
        led=resolve_led(args.led),
        speed=args.speed,
        repeat=args.repeat,
        wait=args.wait
    )


def cmd_wave(argv):
    """Show color with wave effect."""

    parser = argparse.ArgumentParser(prog='pyluxa4 wave', description="Wave effect")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--wave', action='store', type=int, default=1, help="Wave configuration: 1-5")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of wave effect: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host.")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port.")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).wave(
        args.color,
        led=resolve_led(args.led),
        duration=args.duration,
        repeat=args.repeat,
        wait=args.wait
    )


def cmd_pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pyluxa4 pattern', description="Display pattern")
    parser.add_argument('pattern', action='store', type=int, help="Color value.")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host.")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port.")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).pattern(
        args.pattern,
        repeat=args.repeat,
        wait=args.wait
    )


def cmd_off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pyluxa4 off', description="Turn off")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host.")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port.")
    args = parser.parse_args(argv[1:])

    return client.LuxRest(args.host, args.port).off()


def cmd_server(argv):
    """Start the server."""
    from . import server

    parser = argparse.ArgumentParser(prog='pyluxa4 server', description="Run server")
    parser.add_argument('--host', action='store', default=server.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=server.PORT, help="Port")
    args = parser.parse_args(argv)

    server.run(args.host, args.port)


def main(argv):
    """Main."""
    status = 0

    parser = argparse.ArgumentParser(prog='pyluxa4', description='Luxafor control tool.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __meta__.__version__))
    parser.add_argument(
        'command', action='store', help="Command to send: set, off, fade, strobe, wave, and pattern"
    )
    args = parser.parse_args(argv[0:1])

    if args.command == 'server':
        cmd_server(argv[1:])
    else:
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
            status = 1

    return status
