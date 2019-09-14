"""Main."""
import sys
import argparse
from . import usb
from .common import resolve_led
from . import __meta__


def cmd_set(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pylux set', description="Set color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    args = parser.parse_args(argv)

    with usb.LuxFlag() as lf:
        lf.color(
            args.color.lower(),
            led=resolve_led(args.led)
        )


def cmd_fade(argv):
    """Fade to color."""

    parser = argparse.ArgumentParser(prog='pylux fade', description="Fade to color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--duration', action='store', type=int, default=0, help="Duration of fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    args = parser.parse_args(argv)

    with usb.LuxFlag() as lf:
        lf.fade(
            args.color.lower(),
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
    args = parser.parse_args(argv)

    with usb.LuxFlag() as lf:
        lf.strobe(
            args.color.lower(),
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
    args = parser.parse_args(argv)

    with usb.LuxFlag() as lf:
        lf.wave(
            args.color.lower(),
            led=resolve_led(args.led),
            wave=args.wave,
            druation=args.druation,
            repeat=args.repeat,
            wait=args.wait
        )


def cmd_pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pylux pattern', description="Display pattern")
    parser.add_argument('pattern', action='store', type=int, help="Color value.")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    parser.add_argument('--wait', action='store_true', help="Wait for sequence to complete")
    args = parser.parse_args(argv)

    with usb.LuxFlag() as lf:
        lf.pattern(
            args.pattern,
            repeat=args.repeat,
            wait=args.wait
        )


def cmd_off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pylux off', description="Turn off")
    args = parser.parse_args(argv[1:])
    with usb.LuxFlag() as lf:
        lf.off()


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
        cmd_set(argv[1:])

    elif args.command == 'off':
        cmd_off(argv[1:])

    elif args.command == 'fade':
        cmd_fade(argv[1:])

    elif args.command == 'strobe':
        cmd_strobe(argv[1:])

    elif args.command == 'wave':
        cmd_wave(argv[1:])

    elif args.command == 'pattern':
        cmd_pattern(argv[1:])

    else:
        raise ValueError('{} is not a recognized commad'.format(args.command))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
