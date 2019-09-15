"""Luxafor client API."""
import requests
import json
from .common import LED_ALL, LED_BACK, LED_FRONT, LED_VALID, LED_1, LED_2, LED_3, LED_4, LED_5, LED_6
from .common import WAVE_SHORT, WAVE_LONG, WAVE_OVERLAPPING_SHORT, WAVE_OVERLAPPING_LONG
from .common import PATTERN_LUXAFOR, PATTERN_RANDOM1, PATTERN_RANDOM2, PATTERN_RANDOM3
from .common import PATTERN_POLICE, PATTERN_RANDOM4, PATTERN_RANDOM5, PATTERN_RAINBOW
from . import __meta__

__all__ = (
    'LuxRest',
    'LED_ALL', 'LED_BACK', 'LED_FRONT', 'LED_1', 'LED_2', 'LED_3', 'LED_4', 'LED_5', 'LED_6',
    'WAVE_SHORT', 'WAVE_LONG', 'WAVE_OVERLAPPING_SHORT', 'WAVE_OVERLAPPING_LONG',
    'PATTERN_LUXAFOR', 'PATTERN_RANDOM1', 'PATTERN_RANDOM2', 'PATTERN_RANDOM3',
    'PATTERN_POLICE', 'PATTERN_RANDOM4', 'PATTERN_RANDOM5', 'PATTERN_RAINBOW'
)

HOST = "127.0.0.1"
PORT = 5000
TIMEOUT = 5


class LuxRest:
    """Class to post commands to the REST API."""

    def __init__(self, host=HOST, port=PORT):
        """Initialize."""

        self.host = host
        self.port = port

    def _format_respose(self, resp):
        """Format the response."""

        try:
            r = json.loads(resp.text)
        except Exception:
            r = {"status": "fail", "code": resp.status_code, "error": resp.text}
        return r

    def _post(self, command, payload, timeout, no_response=False):
        """Post a REST command."""

        if timeout == 0:
            timeout = None

        if payload is not None:
            payload = json.dumps(payload)
            headers = {'content-type': 'application/json'}
        else:
            headers = None

        try:
            resp = requests.post(
                'http://%s:%d/pyluxa4/api/v%s.%s/command/%s' % (
                    self.host,
                    self.port,
                    __meta__.__version_info__[0],
                    __meta__.__version_info__[1],
                    command
                ),
                data=payload,
                headers=headers,
                timeout=timeout
            )
        except requests.exceptions.ConnectionError:
            return {"status": "fail", "code": 0, "error": "Server does not appear to be running"}
        except Exception as e:
            return {"status": "fail", "code": 0, "error": str(e)}

        return self._format_respose(resp)

    def _get_version(self, timeout):
        """Perform a GET request."""

        if timeout == 0:
            timeout = None

        try:
            resp = requests.get(
                'http://%s:%d/pyluxa4/api/version' % (
                    self.host,
                    self.port
                ),
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

    def fade(self, color, *, led=LED_ALL, duration=0, wait=False, timeout=TIMEOUT):
        """Create command to fade colors."""

        return self._post(
            "fade",
            {
                "color": color,
                "led": led,
                "duration": duration,
                "wait": wait
            },
            timeout
        )

    def strobe(self, color, *, led=LED_ALL, speed=0, repeat=0, wait=False, timeout=TIMEOUT):
        """Create command to strobe colors."""

        return self._post(
            "strobe",
            {
                "color": color,
                "led": led,
                "speed": speed,
                "repeat": repeat,
                "wait": wait
            },
            timeout
        )

    def wave(self, color, *, wave=WAVE_SHORT, duration=0, repeat=0, wait=False, timeout=TIMEOUT):
        """Create command to use the wave effect."""

        return self._post(
            "wave",
            {
                "color": color,
                "wave": wave,
                "duration": duration,
                "repeat": repeat,
                "wait": wait
            },
            timeout
        )

    def pattern(self, pattern, *, led=LED_ALL, repeat=0, wait=False, timeout=TIMEOUT):
        """Create command to use the wave effect."""

        return self._post(
            "pattern",
            {
                "pattern": pattern,
                "repeat": repeat,
                "wait": wait
            },
            timeout
        )

    def off(self, timeout=TIMEOUT):
        """Turn off all lights."""

        return self._post(
            "off",
            None,
            timeout
        )

    def kill(self, timeout=TIMEOUT):
        """Kill the server."""

        return self._post(
            "kill",
            None,
            timeout
        )

    def version(self, timeout=TIMEOUT):
        """Request the version from the running server."""

        return self._get_version(timeout)
