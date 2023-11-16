# Usage

## Overview

`pyluxa4` is mainly designed to be used from command line. When installed, it provides a command line tool called
`pyluxa4`. When installing the module, a tool will be added called `pyluxa4`. Assuming your Python installation's
bin/Script folder is added to your system's path, you will be able to access it from the command line:

```console
$ pyluxa4 --version
pyluxa4 1.5
```

You can also access it via:

```console
$ python3 -m pyluxa4 --version
pyluxa4 1.5
```

## Starting the Server

Generally, `pyluxa4` is designed to be used by running a server, and then executing commands:

1.  Start the server:

    ```console
    $ pyluxa4 serve
    [2019-09-21 15:21:49] INFO: Starting Luxafor server...
    ```

2.  Run a command:

    ```console
    $ pyluxa4 api
    {'error': '', 'path': '/pyluxa4/api/version', 'status': 'success', 'version': '1.5.1', 'version_path': '/pyluxa4/api/v1.5'}
    ```

If you have multiple devices connected, and you want to specify a specific one, you can run the `list` command to see
the connected devices. Devices are listed in the form `index> path`.

```console
$ pyluxa4 list
0> \\?\hid#vid_04d8&pid_f372#6&38a95344&1&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
```

Then we can then specify from the command line which device to use when we start the server. Using the index, it would
be:

```console
$ pyluxa4 serve --device-index 0
```

Using the path, it would be:

```console
$ pyluxa4 serve --device-path "\\?\hid#vid_04d8&pid_f372#6&38a95344&1&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}"
```

Normally, the serve command will find the `hidapi` library as long as its path is found in the systems appropriate
environmental variable, but if it is not, or you'd like to explicitly specify the path to avoid any DLL hijacking, then
you can specify the absolute path to the hidapi library with the `--hidapi`.

```console
$ python3 -m pyluxa4 serve --hidapi /usr/local/Cellar/hidapi/0.14.0/lib/libhidapi.dylib
```

## Killing a Server

If the server is running in a console, you can always press ++ctrl+c++, but if your server is running in the background,
you can kill the server with the `kill` command.

```console
$ pyluxa4 kill
```

## Sending Commands

Once the server is up and running, you can send a variety of commands to set the LEDs to a specific color, to fade
colors in or out, to strobe colors, to apply a wave effect to a color, or to simply run one of the built-in patterns.

More advanced commands are also available. The `scheduler` command can send JSON content to the server with a list of
commands to run at different times. The `timer` command can initiate a timer to initiate a command after a set amount of
time.

To run the commands, simply call `pyluxa4` with the command, followed by the commands arguments:

To set a color, simply specify the `color` command with the desired color:

```console
$ pyluxa4 color red
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/command/color', 'status': 'success'}
```

There are a variety of commands, check out [Commands](./commands.md) to learn more.

## Scheduling Commands

`pyluxa4` provides a command scheduler that allows you to specify a number of commands to run at different times.

For instance, if you wanted to automatically turn your light red at 3:00 PM for an hour, then turn it back green at
4:00 PM, we could construct a couple of scheduled events. Schedules are done as JSON files, the file should contain a
list of events where each event is a hash of key value pairs that describes the event:

```js
[
  {
    "cmd": "color",
    "days": "wkd",
    "times": ["15:00"],
    "args": {
      "color": "red"
    }
  },
  {
    "cmd": "color",
    "days": "wkd",
    "times": ["16:00"],
    "args": {
      "color": "green"
    }
  }
]
```

Then we can send the command to the server:

```console
$ pyluxa4 scheduler --schedule myschedule.json
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/command/scheduler', 'status': 'success'}
```

If we want to clear existing scheduling events while sending our new schedule, simply add the `--clear` command.

```console
$ pyluxa4 scheduler --schedule myschedule.json --clear
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/command/scheduler', 'status': 'success'}
```

If desired, you can also just run `--clear` without a schedule remove all scheduled events.

```console
$ pyluxa4 scheduler --clear
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/command/scheduler', 'status': 'success'}
```

To get an output of loaded events in the schedule (timers not included), we can run:

```console
$ pyluxa4 get schedule
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/scheduler/schedule', 'schedule': [{'args': {'color': 'red'}, 'cmd': 'color', 'days': ['wkd'], 'times': ['15:00']}, {'args': {'color': 'green'}, 'cmd': 'color', 'days': ['wkd'], 'times': ['16:00']}], 'status': 'success'}
```

Parameters | Description
---------- | -----------
`cmd`      | Name of the command to run
`days`     | A list of days: `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, or `sun`. You can also specify `wkd` for weekdays, `wke` for the weekend, and `all` for all days.
`times`    | A list of times that the even will be run on. Times are specified as 24 hour time format.
`args`     | Is a hash of key value pairs of arguments to pass the the specified command.

/// tip | Sending Schedule on Server Start
You can also load a schedule while starting the server via the `--schedule` parameter:

```console
$ pyluxa4 serve --schedule myschedule.json
[2019-09-22 14:05:10] INFO: Starting Luxafor server...
```
///

## Setting Timers

`pyluxa4` allows for setting timers. Timers are essentially a special kind of scheduled event. One that ignores `days`
and will destroy itself after the number of specified cycles has run to completion (unless it specified to run forever).

Additionally, timers are unique as the `times` list does not contain specific times, but contains relative times in the
form `<number of hours>:<number of minutes>`. For instance, if we wanted to have the timer go off in 3 hours and
30 minutes, we would specify the time as `3:30`. This does **not** represent `3:30 AM`, but 3 hours and 30 minutes
from the time the timer was added.

For instance, if we wanted to strobe a red light in an hour and 30 minutes, we could use the following command:

```console
$ pyluxa4 timer --cmd strobe --color red --speed 10 --repeat 10 --times 1:30
```

If we wanted to do it at ten minutes from now followed by another 5 minutes after that:

```console
$ pyluxa4 timer --cmd strobe --color red --speed 10 --repeat 10 --times 0:10,0:5
```

We could even repeat the cycle to flash to iterate through the timers twice, essentially flashing the red light at
10 minutes, 5 minutes, 10 minutes, and 5 minutes

```console
$ pyluxa4 timer --cmd strobe --color red --speed 10 --repeat 10 --times 0:10,0:5 --cycle 2
```

We could even do it continuously every 30 minutes by specifying the cycle as 0 (meaning forever):

```console
$ pyluxa4 timer --cmd strobe --color red --speed 10 --repeat 10 --times 0:30 --cycle 0
```

You can also delay when the times start by specifying a specific time to wait for before starting the timer. For
instance, here we start flashing the light every 30 minutes starting at 9:00 AM:

```console
$ pyluxa4 timer --cmd strobe --color red --speed 10 --repeat 10 --times 0:30 --cycle 0 --start 9:00
```

You could also terminate a timer after at a specific time, for example 5:00 PM:

```console
$ pyluxa4 timer --cmd strobe --color red --speed 10 --repeat 10 --times 0:30 --cycle 0 --start 9:00 --end 17:00
```

As mentioned, times are just a special kind of scheduled event, you can actually put them in a schedule file and they
will be recognized. You *must* add `timer` with the number of times to cycle through the timers. You also *must* make
times relative. The key `days` will be ignored in timers and can be omitted. You can also use two one or both timer
specific keys (`start` and `end`) to specify a respective start and end time for the timers.

For a simple example of a timer represented in a schedule file, consider a case where we'd like to turn off lights as
soon as a schedule is loaded. We could specify a timer with a relative time of `0:0`, which means right away:

```js
[
  {
      "cmd": "off",
      "timer": 1,
      "times": ["0:0"]
  }
]
```

You can clear all running timers by calling the `scheduler` command with the `--cancel` parameter:

```console
$ pyluxa4 scheduler --cancel
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/command/scheduler', 'status': 'success'}
```

To get an output of loaded timers, we can run:

```console
$ pyluxa4 get timers
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/scheduler/timers', 'schedule': [{'args': {}, 'cmd': 'off', 'days': 'all', 'end': None, 'start': None, 'timer': 1, 'times': ['0:10']}], 'status': 'success'}
```

## Enabling HTTPS

`pyluxa4` is mainly meant to be used on a local network, so these instructions are from that perspective.

In order to enable HTTPS, we need to have a certificate. In our local network case, using a simple self signed
certificate is more than sufficient.

To create a certificate, we will assume you have [OpenSSL][openssl] installed. If you are on Windows
using Git Bash, it will likely be available in your Bash terminal. We use OpenSSL to generate a x509v3 certificate. You
can create a simple configuration template like the one shown below which adds in the v3 parameters. Replace the IP with
the one from your machine. We will call this file `cert.conf`.

```ini
[ req ]
default_bits               = 4096
distinguished_name         = req_distinguished_name
[ req_distinguished_name ]
countryName                = Country Name (2 letter code)
stateOrProvinceName        = State or Province Name (full name)
localityName               = Locality Name (eg, city)
organizationName           = Organization Name (eg, company)
organizationalUnitName     = Organizational Unit Name (eg, section)
commonName                 = Common Name (e.g. server FQDN or YOUR name)
emailAddress               = Email Address
[ v3_req  ]
subjectAltName             = @alt_names
[alt_names]
DNS.1                      = localhost
IP.1                       = 127.0.0.1
IP.2                       = 192.168.1.2
```

Afterwards, run the following command. Enter the information that you'd like:

```console
$ openssl req -x509 -out pyluxa4.cer -newkey rsa:4096 -nodes -keyout private.key -extensions v3_req -days 3650 -config cert.conf
```

You should now have a certificate `pyluxa4.cer` and a private key file `private.key`.


Afterwards, you we can use the `--ssl-cert` and `--ssl-key` parameters to enable HTTPS in the server:

```console
$ pyluxa4 serve --ssl-cert pyluxa4.cer --ssl-key private.key
```

Now the server will only accept commands over HTTPS.

```console
$ pyluxa4 api
{'status': 'fail', 'code': 0, 'error': 'Server does not appear to be running'}
```

To send commands with over HTTPS to the server, simply use the `--secure` parameter. If you send the command with `0`,
it will ignore verifying the certificate:

```console
$ pyluxa4 api --secure 0
c:\Python36\lib\site-packages\urllib3\connectionpool.py:851: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
{'error': '', 'path': '/pyluxa4/api/version', 'status': 'success', 'version': '1.5.1', 'version_path': '/pyluxa4/api/v1.5'}
```

If you provide the certificate instead, it will verify the certificate:

```console
$ pyluxa4 api --secure pyluxa4.cer
{'error': '', 'path': '/pyluxa4/api/version', 'status': 'success', 'version': '1.5.1', 'version_path': '/pyluxa4/api/v1.5'}
```

## Token Authentication

In addition to using SSL for HTTPS, using token authentication can help make it more difficult for anyone to send
commands to your Luxafor device. Tokens should really only be used with SSL.

Simply specify your desired token using the the `--token` parameter when initiating the server:

```console
$ pyluxa4 serve --ssl-cert pyluxa4.cer --ssl-key private.key --token secret
```

Now the server will reject commands that require authentication if they are sent without the token.

```console
$ pyluxa4 color red --secure pyluxa4.cer
{'status': 'fail', 'code': 401, 'error': 'Unauthorized Access'}
```

But when we provide the token, the command passes:

```console
$ pyluxa4 color red --secure pyluxa4.cer --token secret
{'code': 200, 'error': '', 'path': '/pyluxa4/api/v1.5/command/color', 'status': 'success'}
```

/// note | Commands that Don't Require Authentication
`api` is the one command that does not require authentication. It will accept commands with or without tokens.
///
