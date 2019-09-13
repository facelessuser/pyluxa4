"""Main."""
import sys
import argparse
import pylux


MODE_MAP = {
    'static': pylux.MODE_STATIC,
    'fade': pylux.MODE_FADE,
    'strobe': pylux.MODE_STROBE,
    'wave': pylux.MODE_WAVE,
    'pattern': pylux.MODE_PATTERN
}


def resolve_led(option):
    """Resolve the LED option to the actual required value."""

    led = option.lower()
    if led == 'all':
        led = pylux.LED_ALL
    elif led == 'back':
        led = pylux.LED_BACK
    elif led == 'front':
        led = pylux.LED_FRONT
    else:
        try:
            led = int(led)
        except Exception:
            raise ValueError('Invalid LED value of {}'.format(led))
    return led


def set(argv):
    """Set to color."""

    parser = argparse.ArgumentParser(prog='pylux set', description="Set color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    args = parser.parse_args(argv)

    with pylux.LuxFlag() as lf:
        lf.color(
            args.color.lower(),
            led=resolve_led(args.led)
        )


def fade(argv):
    """Fade to color."""

    parser = argparse.ArgumentParser(prog='pylux fade', description="Fade to color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    args = parser.parse_args(argv)

    with pylux.LuxFlag() as lf:
        lf.fade(
            args.color.lower(),
            led=resolve_led(args.led),
            speed=args.speed
        )


def strobe(argv):
    """Strobe color."""

    parser = argparse.ArgumentParser(prog='pylux strobe', description="Strobe color")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    args = parser.parse_args(argv)

    with pylux.LuxFlag() as lf:
        lf.strobe(
            args.color.lower(),
            led=resolve_led(args.led),
            speed=args.speed,
            repeat=args.repeat
        )


def wave(argv):
    """Show color with wave effect."""

    parser = argparse.ArgumentParser(prog='pylux wave', description="Wave effect")
    parser.add_argument('color', action='store', help="Color value.")
    parser.add_argument('--wave', action='store', type=int, default=1, help="Wave configuration: 1-5")
    parser.add_argument('--led', action='store', default='all', help="LED: 1-6, back, tab, or all")
    parser.add_argument('--speed', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    args = parser.parse_args(argv)

    with pylux.LuxFlag() as lf:
        lf.wave(
            args.color.lower(),
            led=resolve_led(args.led),
            wave=args.wave,
            speed=args.speed,
            repeat=args.repeat
        )


def pattern(argv):
    """Show pattern."""

    parser = argparse.ArgumentParser(prog='pylux pattern', description="Display pattern")
    parser.add_argument('pattern', action='store', type=int, help="Color value.")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Speed for strobe, wave, or fade: 0-255")
    args = parser.parse_args(argv)

    with pylux.LuxFlag() as lf:
        lf.pattern(
            args.pattern,
            repeat=args.repeat
        )


def off(argv):
    """Set off."""

    parser = argparse.ArgumentParser(prog='pylux off', description="Turn off")
    args = parser.parse_args(argv[1:])
    with pylux.LuxFlag() as lf:
        lf.off()


def rainbow(argv):
    """Show rainbow."""

    parser = argparse.ArgumentParser(prog='pylux rainbow', description="Display rainbow")
    parser.add_argument('--repeat', action='store', type=int, default=0, help="Repeat 0-255, 0 is treated as 1")
    args = parser.parse_args(argv)

    with pylux.LuxFlag() as lf:
        repeat = 1 if args.repeat == 0 else args.repeat

        for x in range(repeat):
            lf.fade("magenta", speed=100)
            lf.fade("red", speed=100)
            lf.fade("orange", speed=100)
            lf.fade("yellow", speed=100)
            lf.fade("green", speed=100)
            lf.fade("cyan", speed=100)
            lf.fade("blue", speed=100)
            lf.fade("purple", speed=100)
        lf.fade("off", speed=100)


def main(argv):
    """Main."""
    parser = argparse.ArgumentParser(prog='pylux', description='Luxafor control tool.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + pylux.__version__))
    parser.add_argument('command', action='store', help="Command to send: set, off, fade, strobe, wave, pattern")
    args = parser.parse_args(argv[0:1])

    if args.command == 'set':
        set(argv[1:])

    elif args.command == 'off':
        off(argv[1:])

    elif args.command == 'fade':
        fade(argv[1:])

    elif args.command == 'strobe':
        strobe(argv[1:])

    elif args.command == 'wave':
        wave(argv[1:])

    elif args.command == 'pattern':
        pattern(argv[1:])

    elif args.command == 'rainbow':
        rainbow(argv[1:])

    else:
        raise ValueError('{} is not a recognized commad'.format(args.command))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
