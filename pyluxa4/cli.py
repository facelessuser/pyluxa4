"""Command line."""
import argparse
import os
from .common import resolve_led, WAVE_SHORT
from . import __meta__
from . import client


def cmd_color(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 color', description="Set color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, front, or all")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).color(
        args.color,
        led=resolve_led(args.led),
        timeout=args.timeout
    )


def cmd_fade(argv):
    """Fade to color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 fade', description="Fade to color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).fade(
        args.color,
        led=resolve_led(args.led),
        duration=args.duration,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_strobe(argv):
    """Strobe color."""

    parser = argparse.ArgumentParser(prog='pyluxa4 strobe', description="Strobe color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, front, or all")
    parser.add_argument('--speed', action='store', type=int, default=0, help="Speed of strobe: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).strobe(
        args.color,
        led=resolve_led(args.led),
        speed=args.speed,
        repeat=args.repeat,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_wave(argv):
    """Show color with wave effect."""

    parser = argparse.ArgumentParser(prog='pyluxa4 wave', description="Wave effect")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--wave', action='store', type=int, default=WAVE_SHORT, help="Wave configuration: 1-5")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of wave effect: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Number of times to repeat: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).wave(
        args.color,
        duration=args.duration,
        repeat=args.repeat,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pyluxa4 pattern', description="Display pattern")
    parser.add_argument('pattern', action='store', type=int, help="Color value.")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).pattern(
        args.pattern,
        repeat=args.repeat,
        wait=args.wait,
        timeout=args.timeout
    )


def cmd_off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pyluxa4 off', description="Turn off")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).off(timeout=args.timeout)


def cmd_version(argv):
    """Get the server to respond with the version."""

    parser = argparse.ArgumentParser(prog='pyluxa4 api', description="Request version")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).version(timeout=args.timeout)


def cmd_kill(argv):
    """Kill the running server."""

    parser = argparse.ArgumentParser(prog='pyluxa4 kill', description="Kill server")
    parser.add_argument('--host', action='store', default=client.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=client.PORT, help="Port")
    parser.add_argument('--timeout', action='store', type=int, default=client.TIMEOUT, help="Timeout")
    args = parser.parse_args(argv)

    return client.LuxRest(args.host, args.port).kill(timeout=args.timeout)


def cmd_serve(argv):
    """Start the server."""
    from . import server

    parser = argparse.ArgumentParser(prog='pyluxa4 serve', description="Run server")
    parser.add_argument('--device-path', action='store', default=None, help="Luxafor device path")
    parser.add_argument('--device-index', action='store', type=int, default=0, help="Luxafor device index")
    parser.add_argument('--host', action='store', default=server.HOST, help="Host")
    parser.add_argument('--port', action='store', type=int, default=server.PORT, help="Port")
    args = parser.parse_args(argv)

    path = args.device_path
    index = args.device_index

    server.run(args.host, args.port, index, path)


def cmd_list(argv):
    """List Luxafor devices."""

    from . import usb

    parser = argparse.ArgumentParser(prog='pyluxa4 serve', description="List available Luxafor devices")
    args = parser.parse_args(argv)

    devices = usb.enumerate_luxafor()
    for index, device in enumerate(devices):
        print('{:d}> {}'.format(index, os.fsdecode(device['path'])))


def main(argv):
    """Main."""
    status = 0

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
