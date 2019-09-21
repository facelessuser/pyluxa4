"""Scheduler."""
import time
import copy
from datetime import datetime
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

    def get_timer_increment(self, times):
        """Calculate timer increments."""

        if not isinstance(times, list):
            times = [times]

        accum = 0
        for t in times:
            h, m = t.split(':')
            accum += int(h) * 60 * 60 + int(m) * 60
        if accum == 0:
            accum = 1
        return accum

    def resolve_times(self, ref, times, timer=False):
        """
        Resolve times.

        Timers should relative the current time.

        Non-timers should be relative to the current day.
        If a non-timer's time is less than the current time,
        we should add a day.
        """

        if not isinstance(times, list):
            times = [times]

        seconds = ref.timestamp()
        if timer:
            new_times = []
            ts = ref.timestamp()
            for t in times:
                h, m = t.split(':')
                new_times.append(ts + int(h) * 60 * 60 + int(m) * 60)
                ts = new_times[-1]
        else:
            new_times = []
            for t in times:
                h, m = t.split(':')
                dt = ref.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
                t = dt.timestamp()
                if t < seconds:
                    t += 24 * 60 * 60
                new_times.append(dt.timestamp())
        return new_times

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

    def parse_timer_boundary(self, ref, value, now):
        """Parse timer boundary."""

        t = self.resolve_times(ref, [value], False)[0] if value is not None else None
        # Time is already passed for today, assume tomorrow
        if t is not None and t < now.timestamp():
            t += 24 * 60 * 60
        return t

    def read_schedule(self, records):
        """Read schedule."""

        if not isinstance(records, list):
            err = "Schedule should be of type list, not {}.".format(type(records))
            self.logger.error(err)
            return err

        err = ''

        events = []
        cmds = []

        now = datetime.now()

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
                    start = self.parse_timer_boundary(now, entry.get('start'), now)
                    end = self.parse_timer_boundary(now, entry.get('end'), now)

                args = []
                kwargs = {}
                if cmd_type in self.mode_map:
                    cmd = self.mode_map[cmd_type]
                    if timer is not None:
                        days = ALL
                    else:
                        days = self.resolve_days(entry['days'])
                    times = self.resolve_times(
                        (datetime.fromtimestamp(start) if start is not None else now),
                        entry['times'],
                        timer is not None
                    )
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
                err = str(e)
                break

            events.append(entry)
            cmds.append(
                {
                    'cmd': cmd,
                    'args': args,
                    'kwargs': kwargs,
                    'days': days,
                    'times': times,
                    'cycles': None if timer is None else [timer] * len(entry['times']),
                    'increment': 1 if timer is None else self.get_timer_increment(entry['times']),
                    'timer': timer is not None,
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

    def time_expired(self, now, target):
        """Check if target past any usable range."""

        return target is None or (now >= target and (now - target) >= 60)

    def time_in_range(self, now, target, day, days):
        """Evaluate if time is in range."""

        return target is not None and now >= target and day in days and (now - target) < 60

    def update_timer(self, cmd, event_index, time_index, dt_now, expired):
        """Update a timer."""

        timer_expired = False
        t = cmd['times'][time_index]

        if t is not None:
            cycle = cmd['cycles'][time_index]
            increment = cmd['increment']
            now = dt_now.timestamp()
            cycles = 0

            while t < now:
                t += increment
                cycles += 1

            if cycle == 0:
                cmd['times'][time_index] = t
            elif cycles < cycle:
                cmd['cycles'][time_index] -= cycles
                cmd['times'][time_index] = t
            else:
                cmd['times'][time_index] = None

        if cmd['times'][-1] is None:
            # All time slots have expired
            timer_expired = True
            expired.append(event_index)

        return timer_expired

    def update_time(self, cmd, event_index, time_index, dt_now):
        """Update a normal event time."""

        times = self.events[event_index]['times']
        t = cmd['times'][time_index]
        t2 = self.resolve_times(dt_now, times[time_index] if isinstance(times, list) else times, False)[0]
        if t2 == t:
            # We haven't rolled over to a new day, so we calculated the same time.
            # Add a day.
            t2 += 24 * 60 * 60
        cmd['times'][time_index] = t2

    def update_times(self, cmd, index, dt_now, expired):
        """Update any times that have expired."""

        timer_expired = False
        now = dt_now.timestamp()
        # Update expired times if required
        for i, t in enumerate(cmd['times']):
            if self.time_expired(now, t):
                is_timer = cmd['timer']
                if is_timer:
                    timer_expired = self.update_timer(cmd, index, i, dt_now, expired)
                    break
                else:
                    self.update_time(cmd, index, i, dt_now)

        return timer_expired

    def check_records(self):
        """Check events."""

        indexes = []
        timers = []
        expired = []

        now = time.time()
        dt_now = datetime.fromtimestamp(now)
        day = dt_now.weekday()

        for index, cmd in enumerate(self.cmds):

            if cmd['timer'] and cmd['start'] is not None:
                if now < cmd['start']:
                    continue
                # Okay to start timer
                cmd['start'] = None

            if cmd['timer'] and cmd['start'] is None and cmd['end'] is not None:
                if now >= cmd['end']:
                    expired.append(index)
                    continue

            # We don't know if the computer just woke up and all are times are bad.
            # Refresh stale times.
            if self.update_times(cmd, index, dt_now, expired):
                # We found an timer which is completely expired. No need to explore this entry further.
                continue

            # Capture events whose time we match.
            for i, t in enumerate(cmd['times']):
                if self.time_in_range(now, t, day, cmd['days']):
                    if cmd['timer']:
                        timers.append(index)
                        self.update_timer(cmd, index, i, dt_now, expired)
                    else:
                        indexes.append(index)
                        self.update_time(cmd, index, i, dt_now)

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
