"""Luxafor client API."""
import requests
import json
from .common import (
    LED_ALL, LED_BACK, LED_FRONT, LED_1, LED_2, LED_3, LED_4, LED_5, LED_6,
    WAVE_SHORT, WAVE_LONG, WAVE_OVERLAPPING_SHORT, WAVE_OVERLAPPING_LONG,
    WAVE_1, WAVE_2, WAVE_3, WAVE_4, WAVE_5,
    PATTERN_TRAFFIC_LIGHT, PATTERN_RANDOM1, PATTERN_RANDOM2, PATTERN_RANDOM3,
    PATTERN_POLICE, PATTERN_RANDOM4, PATTERN_RANDOM5, PATTERN_RAINBOW,
    PATTERN_1, PATTERN_2, PATTERN_3, PATTERN_4, PATTERN_5, PATTERN_6, PATTERN_7, PATTERN_8
)

from . import __meta__

__all__ = (
    'LuxRest',
    'LED_ALL', 'LED_BACK', 'LED_FRONT', 'LED_1', 'LED_2', 'LED_3', 'LED_4', 'LED_5', 'LED_6',
    'WAVE_SHORT', 'WAVE_LONG', 'WAVE_OVERLAPPING_SHORT', 'WAVE_OVERLAPPING_LONG',
    'WAVE_1', 'WAVE_2', 'WAVE_3', 'WAVE_4', 'WAVE_5',
    'PATTERN_TRAFFIC_LIGHT', 'PATTERN_RANDOM1', 'PATTERN_RANDOM2', 'PATTERN_RANDOM3',
    'PATTERN_POLICE', 'PATTERN_RANDOM4', 'PATTERN_RANDOM5', 'PATTERN_RAINBOW',
    'PATTERN_1', 'PATTERN_2', 'PATTERN_3', 'PATTERN_4', 'PATTERN_5', 'PATTERN_6', 'PATTERN_7', 'PATTERN_8'
)

HOST = "127.0.0.1"
PORT = 5000
TIMEOUT = 5


class LuxRest:
    """Class to post commands to the REST API."""

    def __init__(self, host=HOST, port=PORT, verify=None, token=''):
        """Initialize."""

        self.host = host
        self.port = port
        self.http = 'http'
        self.verify = True
        self.token = token
        if verify:
            self.http = 'https'
            if verify == '0':
                self.verify = False
            elif verify != '1':
                self.verify = verify

    def _format_respose(self, resp):
        """Format the response."""

        try:
            r = json.loads(resp.text)
        except Exception:
            r = {"status": "fail", "code": resp.status_code, "error": resp.text}
        return r

    def _post(self, command, payload, timeout):
        """Post a REST command."""

        if timeout == 0:
            timeout = None

        headers = {'Authorization': 'Bearer {}'.format(self.token)}

        if payload is not None:
            payload = json.dumps(payload)
            headers['content-type'] = 'application/json'

        try:
            resp = requests.post(
                '%s://%s:%d/pyluxa4/api/v%s.%s/command/%s' % (
                    self.http,
                    self.host,
                    self.port,
                    __meta__.__version_info__[0],
                    __meta__.__version_info__[1],
                    command
                ),
                data=payload,
                headers=headers,
                timeout=timeout,
                verify=self.verify
            )
        except requests.exceptions.ConnectionError:
            return {"status": "fail", "code": 0, "error": "Server does not appear to be running"}
        except Exception as e:
            return {"status": "fail", "code": 0, "error": str(e)}

        return self._format_respose(resp)

    def _get(self, command, timeout):
        """Perform a REST request."""

        if timeout == 0:
            timeout = None

        headers = {'Authorization': 'Bearer {}'.format(self.token)}

        try:
            resp = requests.get(
                '%s://%s:%d/pyluxa4/api/v%s.%s/%s' % (
                    self.http,
                    self.host,
                    self.port,
                    __meta__.__version_info__[0],
                    __meta__.__version_info__[1],
                    command
                ),
                headers=headers,
                timeout=timeout,
                verify=self.verify
            )
        except requests.exceptions.ConnectionError:
            return {"status": "fail", "code": 0, "error": "Server does not appear to be running"}
        except Exception as e:
            return {"status": "fail", "code": 0, "error": str(e)}

        return self._format_respose(resp)

    def _get_version(self, timeout):
        """Perform a GET request for version."""

        if timeout == 0:
            timeout = None

        try:
            resp = requests.get(
                '%s://%s:%d/pyluxa4/api/version' % (
                    self.http,
                    self.host,
                    self.port
                ),
                verify=self.verify,
                timeout=timeout
            )
        except requests.exceptions.ConnectionError:
            return {"status": "fail", "code": 0, "error": "Server does not appear to be running"}
        except Exception as e:
            return {"status": "fail", "code": 0, "error": str(e)}

        return self._format_respose(resp)

    def color(self, color, *, led=LED_ALL, timeout=TIMEOUT):
        """Create command to set colors."""

        return self._post(
            "color",
            {
                "color": color,
                "led": led
            },
            timeout
        )

    def fade(self, color, *, led=LED_ALL, speed=0, timeout=TIMEOUT):
        """Create command to fade colors."""

        return self._post(
            "fade",
            {
                "color": color,
                "led": led,
                "speed": speed
            },
            timeout
        )

    def strobe(self, color, *, led=LED_ALL, speed=0, repeat=0, timeout=TIMEOUT):
        """Create command to strobe colors."""

        return self._post(
            "strobe",
            {
                "color": color,
                "led": led,
                "speed": speed,
                "repeat": repeat
            },
            timeout
        )

    def wave(self, color, *, wave=WAVE_SHORT, speed=0, repeat=0, timeout=TIMEOUT):
        """Create command to use the wave effect."""

        return self._post(
            "wave",
            {
                "color": color,
                "wave": wave,
                "speed": speed,
                "repeat": repeat
            },
            timeout
        )

    def pattern(self, pattern, *, led=LED_ALL, repeat=0, timeout=TIMEOUT):
        """Create command to use the wave effect."""

        return self._post(
            "pattern",
            {
                "pattern": pattern,
                "repeat": repeat
            },
            timeout
        )

    def off(self, *, timeout=TIMEOUT):
        """Turn off all lights."""

        return self._post(
            "off",
            None,
            timeout
        )

    def scheduler(self, *, schedule=None, clear=False, cancel=False, timeout=TIMEOUT):
        """Scheduler command."""

        return self._post(
            "scheduler",
            {
                "schedule": schedule,
                "clear": clear,
                "cancel": cancel
            },
            timeout
        )

    def get_schedule(self, *, timeout=TIMEOUT):
        """Get schedule from scheduler."""

        return self._get(
            "scheduler/schedule",
            timeout
        )

    def get_timers(self, *, timeout=TIMEOUT):
        """Get timers from scheduler."""

        return self._get(
            "scheduler/timers",
            timeout
        )

    def kill(self, *, timeout=TIMEOUT):
        """Kill the server."""

        return self._post(
            "kill",
            None,
            timeout
        )

    def version(self, *, timeout=TIMEOUT):
        """Request the version from the running server."""

        return self._get_version(timeout)
