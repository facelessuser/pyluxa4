#!flask/bin/python
import argparse
import sys
from flask import Flask, jsonify, abort, make_response, request
from . import controller
from . import __meta__
from .common import resolve_led
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

luxflag = None


def get_api_ver_path():
    return '/pylux/api/v%s.%s' % __meta__.__version_info__[:2]


def set():
    """Set colors."""

    try:
        error = ''
        led = request.json.get("led", 'all')
        color = request.json['color'].lower()
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxflag.color(color, led=resolve_led(led))
        except Exception as e:
            error = str(e)

    return jsonify(
        {
            'command': 'set',
            "status": 'success' if not error else 'fail',
            "error":error
        }
    )


def fade():
    """Fade colors."""

    try:
        error = ''
        led = request.json.get("led", 'all')
        color = request.json['color'].lower()
        duration = request.json.get('duration', 0)
        wait = request.json.get('wait', False)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxflag.fade(color, led=resolve_led(led), duration=duration, wait=wait)
        except Exception as e:
            error = str(e)

    return jsonify(
        {
            'command': 'fade',
            "status": 'success' if not error else 'fail',
            "error":error
        }
    )


def strobe():
    """Strobe colors."""

    try:
        error = ''
        led = request.json.get("led", 'all')
        color = request.json['color'].lower()
        speed = request.json.get('speed', 0)
        repeat = request.json.get('repeat', 0)
        wait = request.json.get('wait', False)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxflag.strobe(color, led=resolve_led(led), speed=speed, repeat=repeat, wait=wait)
        except Exception as e:
            error = str(e)

    return jsonify(
        {
            'command': 'strobe',
            "status": 'success' if not error else 'fail',
            "error":error
        }
    )


def wave():
    """Wave colors."""

    try:
        error = ''
        led = request.json.get("led", 'all')
        color = request.json['color'].lower()
        wv = request.json.get('wave', 1)
        duration = request.json.get('duration', 0)
        repeat = request.json.get('repeat', 0)
        wait = request.json.get('wait', False)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxflag.wave(color, led=resolve_led(led), wave=wv, duration=duration, repeat=repeat, wait=wait)
        except Exception as e:
            error = str(e)

    return jsonify(
        {
            'command': 'wave',
            "status": 'success' if not error else 'fail',
            "error":error
        }
    )


def pattern():
    """Set pattern."""

    try:
        error = ''
        pat = request.json['pattern']
        repeat = request.json.get('repeat', 0)
        wait = request.json.get('wait', False)
    except Exception as e:
        error = str(e)

    if not error:
        try:
            luxflag.pattern(pat, repeat=repeat, wait=wait)
        except Exception as e:
            error = str(e)

    return jsonify(
        {
            'command': 'pattern',
            "status": 'success' if not error else 'fail',
            "error":error
        }
    )


@app.route('/')
def index():
    """
    Just print out a statement.
    This is really only here so I
    can quickly, visually check if server
    is running.
    """
    return "RESTful Luxafor server!"


@app.route('%s/command/<string:command>' % get_api_ver_path(), methods=['POST'])
def execute_command(command):
    """ Executes a given command GET or POST command. """
    if request.method == 'POST':
        print(command)
        if command == 'set':
            results = set()
        elif command == 'fade':
            results = fade()
        elif command == 'strobe':
            results = strobe()
        elif command == 'wave':
            results = wave()
        elif command == 'pattern':
            results = pattern()
        else:
            print(command)
            abort(404)

    return results


@app.route('/automate/api/version', methods=['GET'])
def version():
    """
    Return version.
    """
    return jsonify(
        {
            'status': 'success',
            'error': '',
            'version': __meta__.__version__,
            'version_path': get_api_ver_path()
        }
    )


@app.errorhandler(404)
def not_found(error):
    """
    Return 404 error.
    """
    return make_response(
        jsonify(
            {
                'status': 'fail', 'error': 'Not found'
            }
        ),
        404
    )


def run(port, debug=False):
    """Run server."""

    global luxflag

    with pylux.LuxFlag() as lf:
        luxflag = lf

        try:
            http_server = WSGIServer(('', port), app)
            http_server.serve_forever()
        except KeyboardInterrupt:
            pass


def main(argv):
    """Main."""

    parser = argparse.ArgumentParser(prog='pylux server', description="Run server")
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __meta__.__version__))
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port")
    args = parser.parse_args(argv)

    server.run(args.port)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
