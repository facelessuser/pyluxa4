# Installation

## Prerequisites

`pyluxa4` requires [libusb/hidapi][hidapi] to be installed in order for the controller portion of the library to be
functional. The hidapi path must be included in the systems appropriate environmental variable or the `--hidapi` option
of the `serve` command must be specified with an absolute path to the library.

-   macOS: the easiest way is to just install with brew.

    ```console
    $ brew install hidapi
    ```

    Update environment variables to include the path in `DYLD_LIBRARY_PATH` if not available. As an example:

    ```bash
    DYLD_LIBRARY_PATH="${DYLD_LIBRARY_PATH}:/usr/local/Cellar/hidapi/0.14.0/lib"
    export DYLD_LIBRARY_PATH
    ```

-   Windows: simply download the [pre-built binaries][hidapi-binaries] and make them available in your path. The
    pre-built binaries include 32 bit and 64 bit architecture. Make sure to use the correct one for your system and
    Python.

-   Install via the provided package manager for your distro, or build from source. For Ubuntu:

    ```console
    $ sudo apt install libhidapi-hidraw0
    ```

    or

    ```console
    $ apt install libhidapi-libusb0
    ```

## Install

Once the prerequisites are installed, you can simply use pip to install the library:

```console
$ pip install pyluxa4
```

After that, `pyluxa4` should be available from the command line (assuming Python's bin/Script folder is in your system
path).

```console
$ pyluxa4 --version
pyluxa4 1.7
```

You can also run the module with:

```console
$ python3 -m pyluxa4 --version
pyluxa4 1.7
```
