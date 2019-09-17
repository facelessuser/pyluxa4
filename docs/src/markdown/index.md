# Python Luxafor

`pyluxa4` is a Python library for controlling [Luxafor][luxafor] devices. You can set colors, blink them, fade them,
apply a wave effect, and even run its built-in patterns. All of this is done by running a small server that is accessed
locally on port 5000 (the port can be changed). Once running, you can issue commands from the CLI tool, which in turns
communicates with the server using a REST API.

Since the server uses a REST API, you could easily write scripts in other languages to control the device once running.

If desired, you can import the `pyluxa4.usb` library in a script and control the device directly without running a
server. Or you could import `pyluxa4.client` and write your own application that uses the REST API to control the device
through the server.

--8<--
refs.txt
--8<--
