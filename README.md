# Python Luxafor

> **warning**
> This library has only been tested on the [Luxafor Flag](https://luxafor.com/product/flag/). It may or may not work on
> other devices.

`pyluxa4` is a Python library for controlling [Luxafor](https://luxafor.com/) devices. You can set colors, blink them,
fade them, apply a wave effect, and even run its built-in patterns. All of this is done by running a small server that
is accessed locally on port 5000 (the port can be changed). Once running, you can issue commands from the CLI tool,
which in turns communicates with the server using a REST API.

Since the server uses a REST API, you could easily write scripts in other languages to control the device once running.

If desired, you can import the `pyluxa4.usb` library in a script and control the device directly without running a
server. Or you could import `pyluxa4.client` and write your own application that uses the REST API to control the device
through the server.

`pyluxa4` requires [libusb/hidapi](https://github.com/libusb/hidapi) to be installed in order for the controller portion
of the library to be functional.

## Documentation

Documentation is found here: https://facelessuser.github.io/pyluxa4/

## License

MIT License
