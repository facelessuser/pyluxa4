#!flask/bin/python
import argparse
import sys
import traceback
from flask import Flask, jsonify, abort, make_response, request
from . import controller
from . import __meta__
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
        color = request.json['color']
    except Exception:
        error = str(traceback.format_exc())

    if not error:
        try:
            luxflag.color(color, led=led)
        except Exception:
            error = str(traceback.format_exc())

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
    except Exception:
        error = str(traceback.format_exc())

    if not error:
        try:
            luxflag.fade(color, led=led, duration=duration, wait=wait)
        except Exception:
            error = str(traceback.format_exc())

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
    except Exception:
        error = str(traceback.format_exc())

    if not error:
        try:
            luxflag.strobe(color, led=led, speed=speed, repeat=repeat, wait=wait)
        except Exception:
            error = str(traceback.format_exc())

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
    except Exception:
        error = str(traceback.format_exc())

    if not error:
        try:
            luxflag.wave(color, led=led, wave=wv, duration=duration, repeat=repeat, wait=wait)
        except Exception:
            error = str(traceback.format_exc())

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
    except Exception:
        error = str(traceback.format_exc())

    if not error:
        try:
            luxflag.pattern(pat, repeat=repeat, wait=wait)
        except Exception:
            error = str(traceback.format_exc())

    return jsonify(
        {
            'command': 'pattern',
            "status": 'success' if not error else 'fail',
            "error":error
        }
    )


def pattern():
    """Set pattern."""

    error = ''
    try:
        luxflag.off()
    except Exception:
        error = str(traceback.format_exc())

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
        elif command == 'off':
            results = off()
        else:
            abort(404)

    return results


@app.route('/pylux/api/version', methods=['GET'])
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


def run(host='0.0.0.0', port=5000, debug=False):
    """Run server."""

    global luxflag

    with controller.LuxFlag() as lf:
        luxflag = lf

        try:
            http_server = WSGIServer((host, port), app)
            http_server.serve_forever()
        except KeyboardInterrupt:
            pass


def main(argv):
    """Main."""

    parser = argparse.ArgumentParser(prog='pylux server', description="Run server")
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __meta__.__version__))
    parser.add_argument('--host', action='store', default='0.0.0.0', help="Host")
    parser.add_argument('--port', action='store', type=int, default=5000, help="Port")
    args = parser.parse_args(argv)

    run(args.host, args.port)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
