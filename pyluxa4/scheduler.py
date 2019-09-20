"""Scheduler."""
import time
import copy
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

    def __init__(self, handle, logger):
        """Initialize."""

        self.logger = logger
        self.handle = handle
        self.day_end = self.end_of_day()
        self.mode_map = {
            "color": handle.color,
            "strobe": handle.strobe,
            "fade": handle.fade,
            "wave": handle.wave,
            "pattern": handle.pattern,
            "off": handle.off
        }
        self.events = []
        self.cmds = []

    def clear_timers(self):
        """Clear the timers."""

        remove = []
        for index, event in enumerate(self.events):
            timer = event.get('timer')
            if timer is not None:
                remove.append(index)

        for index in reversed(remove):
            del self.events[index]
            del self.cmds[index]

    def clear_schedule(self):
        """Clear the schedule."""

        remove = []
        for index, event in enumerate(self.events):
            timer = event.get('timer')
            if timer is None:
                remove.append(index)

        for index in reversed(remove):
            del self.events[index]
            del self.cmds[index]

    def end_of_day(self):
        """End of day time."""
        tm = time.strptime("23:59:59", '%H:%M:%S')
        return self.total_seconds(timedelta(hours=tm.tm_hour, minutes=tm.tm_min, seconds=tm.tm_sec))

    def total_seconds(self, t):
        """Get the total seconds."""

        return (t.microseconds + (t.seconds + t.days * 24 * 3600) * 10 ** 6) / 10 ** 6

    def get_current_time(self):
        """Get the current time."""

        now = datetime.now()
        seconds = self.total_seconds(timedelta(hours=now.hour, minutes=now.minute, seconds=now.second))
        return seconds, now.weekday()

    def resolve_times(self, times, timer, timer_start=None):
        """
        Convert convert time to seconds for easy comparison.

        Seconds are relative to a day.
        """

        if not isinstance(times, list):
            times = [times]

        resolved = []
        if timer:
            if timer_start is None:
                now = time.localtime()
                seconds = self.total_seconds(timedelta(hours=now.tm_hour, minutes=now.tm_min, seconds=now.tm_sec))
            else:
                seconds = timer_start
            accum = 0
            for t in sorted(set(times)):
                hours, minutes = [int(part) for part in t.split(':')]
                relative_time = accum = hours * 60 * 60 + minutes * 60 + accum
                relative_time += seconds
                while relative_time > self.day_end:
                    relative_time -= self.day_end + 1
                resolved.append(relative_time)
        else:
            for t in sorted(set(times)):
                tm = time.strptime(t, '%H:%M')
                resolved.append(self.total_seconds(timedelta(hours=tm.tm_hour, minutes=tm.tm_min, seconds=tm.tm_sec)))
            if not resolved:
                raise ValueError('No valid times found')
        return resolved

    def resolve_days(self, days):
        """
        Resolve days.

        Days are numbers from 0-6 where Monday is 0.
        """

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

    def parse_timer(self, obj):
        """Parse timer."""

        timer = obj['timer']
        cmn.is_int('timer', timer)
        cmn.validate_timer_cycle(timer)
        return timer

    def parse_timer_boundary(self, obj, name):
        """Parse timer boundary."""

        value = obj.get(name)
        return self.resolve_times(value, False)[0] if value is not None else None

    def time_in_range(self, day, seconds, delta, event_days):
        """
        Check if day is in range.

        Day should equal the current day, but if seconds
        is less than a minute into the next day, we could
        match 12:59 PM.
        """

        yesterday = day - 1 if day > 0 else 6

        return (
            (day in event_days and 0 <= delta < 60) or
            (seconds < 60 and yesterday in event_days and 0 <= delta < 60)
        )

    def read_schedule(self, records):
        """Read schedule."""

        if not isinstance(records, list):
            err = "Schedule should be of type list, not {}.".format(type(records))
            self.logger.error(err)
            return err

        err = ''

        events = []
        cmds = []

        for entry in records:
            start = None
            end = None
            try:
                allowed = set(['cmd', 'days', 'times', 'args', 'timer'])
                if 'timer' in entry:
                    allowed.add('start')
                    allowed.add('end')
                # Throw an error for unexpected parameters
                for k in entry.keys():
                    if k not in allowed:
                        raise ValueError('Unexpected event parameter {}'.format(k))

                cmd_type = entry['cmd']

                # Handle timer variables
                timer = self.parse_timer(entry) if 'timer' in entry else None
                if timer is not None:
                    start = self.parse_timer_boundary(entry, 'start')
                    end = self.parse_timer_boundary(entry, 'end')

                args = []
                kwargs = {}
                if cmd_type in self.mode_map:
                    cmd = self.mode_map[cmd_type]
                    if timer is not None:
                        days = ALL
                    else:
                        days = self.resolve_days(entry['days'])
                    times = self.resolve_times(entry['times'], timer is not None, timer_start=start)
                    arguments = entry.get('args', {})
                    expected = set()
                    if cmd_type in ('color', 'strobe', 'fade', 'wave'):
                        expected.add('color')
                        self.parse_color(arguments, args)

                        if cmd_type in ('color', 'strobe', 'fade'):
                            expected.add('led')
                            self.parse_led(arguments, kwargs)

                        if cmd_type in ('strobe', 'fade', 'wave'):
                            expected.add('speed')
                            self.parse_speed(arguments, kwargs)

                        if cmd_type in ('strobe', 'wave'):
                            expected.add('repeat')
                            self.parse_repeat(arguments, kwargs)

                        if cmd_type == 'wave':
                            expected.add('wave')
                            self.parse_wave(arguments, kwargs)

                    elif cmd_type == 'pattern':
                        expected.add('pattern')
                        expected.add('repeat')
                        self.parse_pattern(arguments, args)
                        self.parse_repeat(arguments, kwargs)

                    # Throw an error for unexpected arguments
                    for k in arguments.keys():
                        if k not in expected:
                            raise ValueError('Unexpected command argument {}'.format(k))

                else:
                    raise ValueError("Unrecognized command {}".format(cmd_type))

            except Exception as e:
                self.logger.error(e)
                err = str(e)
                break

            events.append(entry)
            cmds.append(
                {
                    'cmd': cmd,
                    'args': args,
                    'kwargs': kwargs,
                    'days': days,
                    'next': times[0],
                    'index': 0,
                    'times': times,
                    'ran': False,
                    'timer': timer,
                    'start': start,
                    'end': end
                }
            )
        if not err:
            self.events.extend(events)
            self.cmds.extend(cmds)

        return err

    def get_schedule(self):
        """Get the schedule."""

        records = []
        for event in self.events:
            timer = event.get('timer')
            if timer is None:
                records.append(copy.deepcopy(event))
        return records

    def get_timers(self):
        """Get the timers."""

        records = []
        for event in self.events:
            timer = event.get('timer')
            if timer is not None:
                records.append(copy.deepcopy(event))
        return records

    def get_delta(self, current, target):
        """Get the delta between the current seconds and the target."""

        delta = current - target

        # Account for day rollover with delta
        if current < 60 and delta < 0:
            delta2 = (self.day_end + current + 1) - target
            if delta2 > 0:
                delta = delta2

        return delta

    def check_records(self):
        """Check events."""

        seconds, day = self.get_current_time()
        indexes = []
        timers = []
        expired = []

        for index, cmd in enumerate(self.cmds):

            delta = self.get_delta(seconds, cmd['next'])

            if cmd['timer'] is not None and cmd['start'] is not None:
                timer_delta = self.get_delta(seconds, cmd['start'])
                if not self.time_in_range(day, seconds, timer_delta, cmd['days']):
                    continue
                # Okay to start timer
                cmd['start'] = None

            if cmd['timer'] is not None and cmd['start'] is None and cmd['end'] is not None:
                timer_delta = self.get_delta(seconds, cmd['end'])
                if self.time_in_range(day, seconds, timer_delta, cmd['days']):
                    # Timer has now expired
                    expired.append(index)
                    continue

            # See if the current day and time matches
            if self.time_in_range(day, seconds, delta, cmd['days']):
                # "ran" is true if an event has only one time, this prevents it from
                # matching repeatedly. Once it no longer matches, it will be
                # set to false.
                if not cmd['ran']:
                    # Increment time index accounting for rollover.
                    i = cmd['index'] + 1
                    if i >= len(cmd['times']):
                        i = 0
                        if cmd['timer'] is not None:
                            if cmd['timer'] != 1:
                                cmd['times'] = self.resolve_times(self.events[index]['times'], True)
                                if cmd['timer'] != 0:
                                    cmd['timer'] -= 1
                            else:
                                expired.append(index)
                    if i == cmd['index'] and cmd['timer'] is None:
                        # Next index is last index, there is only one time
                        # Mark event as "ran".
                        cmd['ran'] = True
                    else:
                        # Point to next time in the list
                        cmd['next'] = cmd['times'][i]
                        cmd['index'] = i
                    if cmd['timer'] is not None:
                        timers.append(index)
                    else:
                        indexes.append(index)
            elif cmd['ran']:
                # Event with single time instance no longer matches, set "False"
                cmd['ran'] = False

        indexes.extend(timers)

        # Run the matched event
        for index in indexes:
            cmd = self.cmds[index]
            try:
                cmd['cmd'](*cmd['args'], **cmd['kwargs'])
            except Exception as e:
                self.logger.error(e)

        # Remove expired timers
        for index in reversed(expired):
            del self.cmds[index]
            del self.events[index]
