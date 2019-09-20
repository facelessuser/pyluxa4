"""Luxafor server."""
import logging
from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPTokenAuth
from gevent.pywsgi import WSGIServer
from gevent.lock import BoundedSemaphore
import gevent
from . import scheduler
from . import usb
from . import common as cmn
from . import __meta__

sem = BoundedSemaphore(1)

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)
app = Flask(__name__)
auth = HTTPTokenAuth('Bearer')
tokens = set()
luxafor = None
schedule = None
HOST = '0.0.0.0'
PORT = 5000
ERR_CMD_FAILED = "Command could not be excuted, possibly due to a disconnected device"


def get_api_ver_path():
    """Get the API path."""

    return '/pyluxa4/api/v%s.%s' % __meta__.__version_info__[:2]


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
        cmn.is_int('led', led)
        color = request.json.get('color', '')
        cmn.is_str('color', color)
    except Exception as e:
        logger.error(e)
        error = str(e)

    if not error:
        sem.acquire()
        try:
            if luxafor.color(color, led=led):
                raise RuntimeError(ERR_CMD_FAILED)
        except Exception as e:
            logger.error(e)
            error = str(e)
        sem.release()

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success',
            "code": 200,
            "error": error
        }
    )


def fade():
    """Fade colors."""

    try:
        error = ''
        led = request.json.get("led", cmn.LED_ALL)
        cmn.is_int('led', led)
        color = request.json.get('color', '')
        cmn.is_str('color', color)
        speed = request.json.get('speed', 0)
        cmn.is_int('speed', speed)
    except Exception as e:
        logger.error(e)
        error = str(e)

    if not error:
        sem.acquire()
        try:
            if luxafor.fade(color, led=led, speed=speed):
                raise RuntimeError(ERR_CMD_FAILED)
        except Exception as e:
            logger.error(e)
            error = str(e)
        sem.release()

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success',
            "code": 200,
            "error": error
        }
    )


def strobe():
    """Strobe colors."""

    try:
        error = ''
        led = request.json.get("led", cmn.LED_ALL)
        cmn.is_int('led', led)
        color = request.json.get('color', '')
        cmn.is_str('color', color)
        speed = request.json.get('speed', 0)
        cmn.is_int('speed', speed)
        repeat = request.json.get('repeat', 0)
        cmn.is_int('repeat', repeat)
    except Exception as e:
        logger.error(e)
        error = str(e)

    if not error:
        sem.acquire()
        try:
            if luxafor.strobe(color, led=led, speed=speed, repeat=repeat):
                raise RuntimeError(ERR_CMD_FAILED)
        except Exception as e:
            logger.error(e)
            error = str(e)
        sem.release()

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success',
            "code": 200,
            "error": error
        }
    )


def wave():
    """Wave colors."""

    try:
        error = ''
        color = request.json.get('color', '')
        cmn.is_str('color', color)
        wave = request.json.get('wave', cmn.WAVE_SHORT)
        cmn.is_int('wave', wave)
        speed = request.json.get('speed', 0)
        cmn.is_int('speed', speed)
        repeat = request.json.get('repeat', 0)
        cmn.is_int('repeat', repeat)
    except Exception as e:
        logger.error(e)
        error = str(e)

    if not error:
        sem.acquire()
        try:
            if luxafor.wave(color, wave=wave, speed=speed, repeat=repeat):
                raise RuntimeError(ERR_CMD_FAILED)
        except Exception as e:
            logger.error(e)
            error = str(e)
        sem.release()

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success',
            "code": 200,
            "error": error
        }
    )


def pattern():
    """Set pattern."""

    try:
        error = ''
        pattern = request.json.get('pattern', 0)
        cmn.is_int('pattern', pattern)
        repeat = request.json.get('repeat', 0)
        cmn.is_int('repeat', repeat)
    except Exception as e:
        logger.error(e)
        error = str(e)

    if not error:
        sem.acquire()
        try:
            if luxafor.pattern(pattern, repeat=repeat):
                raise RuntimeError(ERR_CMD_FAILED)
        except Exception as e:
            logger.error(e)
            error = str(e)
        sem.release()

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success',
            "code": 200,
            "error": error
        }
    )


def off():
    """Set off."""

    error = ''
    sem.acquire()
    try:
        if luxafor.off():
            raise RuntimeError(ERR_CMD_FAILED)
    except Exception as e:
        logger.error(e)
        error = str(e)
    sem.release()

    if error:
        abort(400, error)

    return jsonify(
        {
            "path": request.path,
            "status": 'success',
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
        background.kill()
    except Exception as e:
        logger.error(e)
        error = str(e)

    if error:
        abort(400, error)

    return {
        "path": request.path,
        "status": 'success',
        "code": 200,
        "error": error
    }


def get_records(timers=False):
    """Return the current schedule or timers from the scheduler."""

    sem.acquire()
    if timers:
        report = schedule.get_timers()
    else:
        report = schedule.get_schedule()
    sem.release()
    return {
        "path": request.path,
        "status": 'success',
        "code": 200,
        "schedule": report,
        "error": ''
    }


def setup_schedule():
    """Setup schedule."""

    err = ''
    sem.acquire()
    events = request.json.get('schedule')
    clear = request.json.get('clear', False)
    cancel = request.json.get('cancel', False)
    if cancel:
        schedule.clear_timers()
    if clear:
        schedule.clear_schedule()
    if events is not None:
        err = schedule.read_schedule(events)
    sem.release()
    if err:
        abort(400, err)
    return {
        "path": request.path,
        "status": 'success',
        'code': 200,
        "error": err
    }


def check_schedule():
    """Check schedule in the background."""

    while True:
        sem.acquire()
        schedule.check_records()
        sem.release()
        gevent.sleep(10)


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
        elif command == 'scheduler':
            results = setup_schedule()
        else:
            abort(404)
    else:
        abort(404)

    return results


@app.route('%s/scheduler/<string:command>' % get_api_ver_path(), methods=['GET'])
@auth.login_required
def get_scheduler(command):
    """Retrieve information from scheduler."""

    if request.method == 'GET':
        if command == 'schedule':
            results = get_records()
        elif command == 'timers':
            results = get_records(timers=True)
        else:
            abort(404)
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


def run(
    host=HOST, port=PORT, device_index=0, device_path=None, token=None, events=None,
    debug=False, **kwargs
):
    """Run server."""

    global luxafor
    global http_server
    global tokens
    global schedule
    global background

    log_handler.setFormatter(
        logging.Formatter(fmt='[%(asctime)s] %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    )

    with usb.Luxafor(device_index, device_path, token) as lf:
        luxafor = lf
        tokens = set([token])
        schedule = scheduler.Scheduler(luxafor, logger)
        if events is not None:
            err = schedule.read_schedule(events)
            if err:
                logger.error(err)
        http_server = WSGIServer((host, port), app, **kwargs)
        serve = gevent.spawn(http_server.start)
        background = gevent.spawn(check_schedule)

        try:
            logger.info('Starting Luxafor server...')
            gevent.joinall([serve, background])
        except KeyboardInterrupt:
            pass
        logger.info('Exiting Luxafor server...')
