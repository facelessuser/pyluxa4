"""Scheduler."""
import json
import time
from datetime import datetime, timedelta
from . import common as cmn

MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6
WEEKDAY = (MON, TUE, WED, THU, FRI)
WEEKEND = (SAT, SUN)
ALL = WEEKDAY + WEEKEND

DAY_MAP = {
    "mon": (MON,),
    "tue": (TUE,),
    "wed": (WED,),
    "thu": (THU,),
    "fri": (FRI,),
    "sat": (SAT,),
    "sun": (SUN,),
    "wke": WEEKEND,
    "wkd": WEEKDAY,
    "all": ALL
}


class Scheduler:
    """Scheduler."""

    def __init__(self, handle):
        """Initialize."""

        self.handle = handle
        self.mode_map = {
            "color": handle.color,
            "strobe": handle.strobe,
            "fade": handle.fade,
            "wave": handle.wave,
            "pattern": handle.pattern,
            "off": handle.off
        }
        self.events = []

    def clear_schedule(self):
        """Clear the schedule."""

        self.events = []

    def total_seconds(self, t):
        """Get the total seconds."""

        return (t.microseconds + (t.seconds + t.days * 24 * 3600) * 10 ** 6) / 10 ** 6

    def get_current_time(self):
        """Get the current time."""

        now = datetime.now()
        seconds = self.total_seconds(timedelta(hours=now.hour, minutes=now.minute, seconds=now.second))
        return seconds, now.weekday()

    def resolve_times(self, times):
        """Convert datetime to seconds."""

        if not isinstance(times, list):
            times = [times]

        resolved = []
        for t in sorted(set(times)):
            tm = time.strptime(t, '%H:%M')
            resolved.append(self.total_seconds(timedelta(hours=tm.tm_hour, minutes=tm.tm_min, seconds=tm.tm_sec)))
        if not resolved:
            raise ValueError('No valid times found')
        return resolved

    def resolve_days(self, days):
        """Resolve days."""

        if not isinstance(days, list):
            days = [days]

        resolved = []
        for day in days:
            value = DAY_MAP.get(day.lower())
            if value is not None:
                resolved.extend(value)
        if not resolved:
            raise ValueError('No valid days found')
        return set(resolved)

    def parse_led(self, arguments, kwargs):
        """Parse led."""

        led = arguments.get('led', cmn.LED_ALL)
        if isinstance(led, str):
            led = cmn.resolve_led(led)
        else:
            cmn.validate_led(led)
        kwargs['led'] = led

    def parse_speed(self, arguments, kwargs):
        """Parses speed."""

        speed = arguments.get('speed', 0)
        cmn.validate_speed(speed)
        kwargs['speed'] = speed

    def parse_repeat(self, arguments, kwargs):
        """Parse repeat."""

        repeat = arguments.get('repeat', 0)
        cmn.validate_repeat(repeat)
        kwargs['repeat'] = repeat

    def parse_wave(self, arguments, kwargs):
        """Parse wave."""

        wave = arguments.get('wave', 1)
        if isinstance(wave, str):
            wave = cmn.resolve_wave(wave)
        else:
            cmn.validate_wave(wave)
        kwargs['wave'] = wave

    def parse_pattern(self, arguments, args):
        """Parse pattern."""

        pattern = arguments['pattern']
        if isinstance(pattern, str):
            pattern = cmn.resolve_pattern(pattern)
        else:
            cmn.validate_pattern(pattern)
        args.append(pattern)

    def parse_color(self, arguments, args):
        """Parse colors."""

        color = arguments['color']
        cmn.is_str('color', color)
        args.append(color)

    def read_schedule(self, schedule):
        """Read schedule."""

        try:
            with open(schedule, 'r') as f:
                config = json.loads(f.read())
            assert isinstance(config, list)
        except Exception:
            return "Could not open file or file content was invalid {}".format(schedule)

        err = ''

        for entry in config:
            try:
                cmd_type = entry['type']
                args = []
                kwargs = {}
                if cmd_type in self.mode_map:
                    cmd = self.mode_map[cmd_type]
                    days = self.resolve_days(entry['days'])
                    times = self.resolve_times(entry['times'])
                    arguments = entry.get('args', {})
                    if cmd_type in ('color', 'strobe', 'fade', 'wave'):
                        self.parse_color(arguments, args)

                        if cmd_type in ('color', 'strobe', 'fade'):
                            self.parse_led(arguments, kwargs)

                        if cmd_type in ('strobe', 'fade', 'wave'):
                            self.parse_speed(arguments, kwargs)

                        if cmd_type in ('strobe', 'wave'):
                            self.parse_repeat(arguments, kwargs)

                        if cmd_type == 'wave':
                            self.parse_wave(arguments, kwargs)

                    elif cmd_type == 'pattern':
                        self.parse_pattern(arguments, args)
                        self.parse_repeat(arguments, kwargs)

                else:
                    err = "Unrecognized command type {}".format(cmd_type)
                    break
            except Exception as e:
                err = str(e)
                break

            self.events.append(
                {
                    'cmd': cmd,
                    'args': args,
                    'kwargs': kwargs,
                    'days': days,
                    'next': times[0],
                    'index': 0,
                    'times': times,
                    'ran': False
                }
            )
        if err:
            self.clear_schedule()

        return err

    def check_schedule(self):
        """Check events."""

        seconds, day = self.get_current_time()
        closest = -1
        for index, event in enumerate(self.events):
            delta = seconds - event['next']
            if seconds < 60:
                delta = abs(delta)
            if day in event['days'] and 0 <= delta < 60:
                if not event['ran']:
                    i = event['index'] + 1
                    if i >= len(event['times']):
                        i = 0
                    if i == event['index']:
                        event['ran'] = True
                    else:
                        event['next'] = event['times'][i]
                        event['index'] = i
                    closest = index
            elif event['ran']:
                event['ran'] = False
        if closest > -1:
            event = self.events[closest]
            try:
                event['cmd'](*event['args'], **event['kwargs'])
            except Exception:
                # Remove bad commands
                print('Failed to execute command...')
                del self.events[closest]
