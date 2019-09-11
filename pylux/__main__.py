"""Main."""
import sys
import argparse
import pylux

COLOR_NAMES = ('red', 'orange', 'yellow', 'green', 'blue', 'pink', 'purple', 'cyan', 'white', 'off')
COLOR_SIZE = 6


def main():
    """Main."""
    parser = argparse.ArgumentParser(prog='pylux', description='Luxafor control tool.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + pylux.__version__))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--set', action='store', default='000000', help="Set color")
    group.add_argument('--pattern', action='store', type=int, default=0, help="Patterns: 1-9")
    parser.add_argument('--pins', action='store', default='all', help="Pins: 1-6, back, tab, or all")
    parser.add_argument('--mode', action='store', default='static', help="Mode: static, fade, strobe, wave")
    parser.add_argument('--wave', action='store', type=int, default=1, help="Wave configuration: 1-5")
    parser.add_argument('--speed', action='store', type=int, default=1, help="Speed for strobe, wave, or fade: 1-255")
    parser.add_argument(
        '--repeat', action='store', type=int, default=1, help="Repeat for strobe, wave, or pattern: 1-255"
    )
    args = parser.parse_args()

    with pylux.LuxFlag() as lf:
        if args.pattern:
            pattern = args.pattern
            mode = 0
        elif args.mode:
            mode = args.mode
            pattern = 0
        pins = args.pins
        speed = args.speed
        repeat = args.repeat
        wave = args.wave
        color = args.set.lower()
        if pattern:
            lf.set_pattern(pattern, repeat=repeat)
        elif color in COLOR_NAMES:
            # Handle named colors
            getattr(lf, 'set_{}'.format(color))(pins=pins, mode=mode, speed=speed, repeat=repeat, wave=wave)
        elif len(color) == COLOR_SIZE:
            # Handle colors in the form RRGGBB
            try:
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4: 6], 16)
            except Exception:
                raise ValueError('Invalid color {}'.format(color))

            lf.set_color(r, g, b, pins=pins, mode=mode, speed=speed, repeat=repeat, wave=wave)
        else:
            raise ValueError('Invalid color {}'.format(color))

    return 0


if __name__ == '__main__':
    sys.exit(main())
