"""Luxafor server."""
from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPTokenAuth
from gevent.pywsgi import WSGIServer
from . import usb
from . import common as cmn
from . import __meta__

app = Flask(__name__)
auth = HTTPTokenAuth('Bearer')
tokens = set()
luxafor = None
HOST = '0.0.0.0'
PORT = 5000


def get_api_ver_path():
    """Get the API path."""

    return '/pyluxa4/api/v%s.%s' % __meta__.__version_info__[:2]


def is_bool(name, value):
    """Check if bool."""

    if not isinstance(value, bool):
        raise TypeError("'{}' must be a boolean".format(name))


def is_str(name, value):
    """Check if bool."""

    if not isinstance(value, str):
        raise TypeError("'{}' must be a string".format(name))


def is_int(name, value):
    """Check if bool."""

    if not isinstance(value, int):
        raise TypeError("'{}' must be a integer".format(name))


@auth.verify_token
def verify_token(token):
    """Verify incoming token."""

    if token in tokens:
        return True
    return False


def color():
    """Set colors."""

    try:
        error = ''
        led = request.json.get("led", cmn.LED_ALL)
        is_int('led', led)
        color = request.json.get('color', '')
        is_str('color', color)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxafor.color(color, led=led)
        except Exception as e:
            error = str(e)

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success' if not error else 'fail',
            "code": 200,
            "error": error
        }
    )


def fade():
    """Fade colors."""

    try:
        error = ''
        led = request.json.get("led", cmn.LED_ALL)
        is_int('led', led)
        color = request.json.get('color', '')
        is_str('color', color)
        speed = request.json.get('speed', 0)
        is_int('speed', speed)
        wait = request.json.get('wait', False)
        is_bool('wait', wait)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxafor.fade(color, led=led, speed=speed, wait=wait)
        except Exception as e:
            error = str(e)

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success' if not error else 'fail',
            "code": 200,
            "error": error
        }
    )


def strobe():
    """Strobe colors."""

    try:
        error = ''
        led = request.json.get("led", cmn.LED_ALL)
        is_int('led', led)
        color = request.json.get('color', '')
        is_str('color', color)
        speed = request.json.get('speed', 0)
        is_int('speed', speed)
        repeat = request.json.get('repeat', 0)
        is_int('repeat', repeat)
        wait = request.json.get('wait', False)
        is_bool('wait', wait)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxafor.strobe(color, led=led, speed=speed, repeat=repeat, wait=wait)
        except Exception as e:
            error = str(e)

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success' if not error else 'fail',
            "code": 200,
            "error": error
        }
    )


def wave():
    """Wave colors."""

    try:
        error = ''
        color = request.json.get('color', '')
        is_str('color', color)
        wave = request.json.get('wave', cmn.WAVE_SHORT)
        is_int('wave', wave)
        speed = request.json.get('speed', 0)
        is_int('speed', speed)
        repeat = request.json.get('repeat', 0)
        is_int('repeat', repeat)
        wait = request.json.get('wait', False)
        is_bool('wait', wait)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxafor.wave(color, wave=wave, speed=speed, repeat=repeat, wait=wait)
        except Exception as e:
            error = str(e)

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success' if not error else 'fail',
            "code": 200,
            "error": error
        }
    )


def pattern():
    """Set pattern."""

    try:
        error = ''
        pattern = request.json.get('pattern', 0)
        is_int('pattern', pattern)
        repeat = request.json.get('repeat', 0)
        is_int('repeat', repeat)
        wait = request.json.get('wait', False)
        is_bool('wait', wait)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxafor.pattern(pattern, repeat=repeat, wait=wait)
        except Exception as e:
            error = str(e)

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success' if not error else 'fail',
            "code": 200,
            "error": error
        }
    )


def off():
    """Set off."""

    error = ''
    try:
        luxafor.off()
    except Exception as e:
        error = str(e)

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success' if not error else 'fail',
            "code": 200,
            "error": error
        }
    )


def kill():
    """Kill."""

    try:
        error = ''
        http_server.close()
        http_server.stop(timeout=10)
    except Exception as e:
        error = str(e)

    if error:
        abort(400, error)

    return {
        "path": request.path,
        "status": 'success' if not error else 'fail',
        "code": 200,
        "error": error
    }


@app.route('/')
def index():
    """
    Print out some text for main page.

    This is really only here so we
    can quickly, visually check if server
    is running.
    """
    return "RESTful Luxafor server!"


@app.route('%s/command/<string:command>' % get_api_ver_path(), methods=['POST'])
@auth.login_required
def execute_command(command):
    """Executes a given command GET or POST command."""
    if request.method == 'POST':
        if command == 'color':
            results = color()
        elif command == 'fade':
            results = fade()
        elif command == 'strobe':
            results = strobe()
        elif command == 'wave':
            results = wave()
        elif command == 'pattern':
            results = pattern()
        elif command == 'off':
            results = off()
        elif command == 'kill':
            # Results won't make it back if successful
            results = kill()
        else:
            abort(404)

    return results


@app.route('/pyluxa4/api/version', methods=['GET'])
def version():
    """Return version."""
    return jsonify(
        {
            "path": request.path,
            'status': 'success',
            'error': '',
            'version': __meta__.__version__,
            'version_path': get_api_ver_path()
        }
    )


@app.errorhandler(400)
def bad_request(error):
    """Return 400 error."""

    return make_response(
        jsonify(
            {
                "path": request.path,
                "status": "fail",
                "code": 400,
                "error": str(error)
            }
        ),
        400
    )


@app.errorhandler(404)
def not_found(error):
    """Return 404 error."""
    return make_response(
        jsonify(
            {
                "path": request.path,
                "status": "fail",
                "code": 404,
                "error": 'Request not found'
            }
        ),
        404
    )


@app.errorhandler(500)
def server_error(error):
    """Return 500 error."""
    return make_response(
        jsonify(
            {
                "path": request.path,
                "status": "fail",
                "code": 500,
                "error": 'Internal server error'
            }
        ),
        500
    )


def run(host=HOST, port=PORT, device_index=0, device_path=None, token=None, ssl=None, debug=False, **kwargs):
    """Run server."""

    global luxafor
    global http_server
    global tokens

    with usb.Luxafor(device_index, device_path, token) as lf:
        luxafor = lf
        tokens = set([token])

        try:
            http_server = WSGIServer((host, port), app, **kwargs)
            http_server.serve_forever()
        except KeyboardInterrupt:
            pass
