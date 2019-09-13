# Python Luxafor

Luxafor flag controller.

Luxafor provides software for macOS and Windows, but it does not provide any for Linux. This library was written to
allow easy scripting in Python for all operating systems: Linux, macOS, and Windows.

## Installation

1. `luxa4` requires [libusb/hidapi](https://github.com/libusb/hidapi) to be installed.

    - macOS: the easiest way is to just install with brew.

        ```
        brew install hidapi
        ```

    - Windows: simply download the [pre-built binaries](https://github.com/libusb/hidapi/releases) and make them
      available in your path.

    - Linux: TBD

2. Install `pylux`.

## License

MIT License

Copyright (c) 2019 Isaac Muse
