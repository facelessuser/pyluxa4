# Python Luxafor

/// warning
This library has only been tested on the [Luxafor Flag](https://luxafor.com/product/flag/). It may or may not work on
other devices.
///

`pyluxa4` is a Python library for controlling [Luxafor][luxafor] devices and is cross platform. It runs on Windows,
macOS, and Linux. You can set colors, strobe them, fade them, apply wave effects, and even run its built-in patterns.
All of this is done by running a small server that is accessed locally on port 5000 (the port can be changed).

Once the server is running, you can issue commands from the CLI tool, which in turns communicates with the server using
a REST API. Since the server uses a REST API, you could easily write scripts in other languages to control the device
once running.

If desired, you can import the `pyluxa4.usb` library in a script and control the device directly without running a
server. Or you could import `pyluxa4.client` and write your own application that uses the REST API to control the device
through the server.

There are already various other libraries out that control the Luxafor devices. Some worked better than others, and
while many did exactly as advertised, none really did all that I was looking for. `pyluxa4` is a simple solution that
works on all operating systems, is easily controlled from anywhere on a local network, provides a scheduler so you can
setup lights to run at specific times, and an interface for setting timers.
