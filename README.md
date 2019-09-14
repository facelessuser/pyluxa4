# Python Luxafor

Luxafor flag controller.

Luxafor provides software for macOS and Windows, but it does not provide any for Linux. This library was written to
allow easy scripting in Python for all operating systems: Linux, macOS, and Windows.

`pyluxa4` allows for a couple of ways to control your Luxafor device.

1. You can use `pyluxa4-server` to start a server and use `pyluxa4-client` (or any other REST client) to control the
  device using the REST API. This works well with all platforms. This also gives you flexibility to send commands from
  more than just Python scripts.

3. You can also import `pyluxa4.client` and build your own script around the REST API, or import `pyluxa4.usb` and
  control the device directly via the USB interface from your own Python library.

## Installation

1. `luxa4` requires [libusb/hidapi](https://github.com/libusb/hidapi) to be installed.

    - macOS: the easiest way is to just install with brew.

        ```
        brew install hidapi
        ```

    - Windows: simply download the [pre-built binaries](https://github.com/libusb/hidapi/releases) and make them
      available in your path.

    - Linux: TBD

2. Install `pyluxa4`.

## License

MIT License

Copyright (c) 2019 Isaac Muse
