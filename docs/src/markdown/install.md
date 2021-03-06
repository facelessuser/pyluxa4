# Installation

## Prerequisites

`pyluxa4` requires [libusb/hidapi][hidapi] to be installed in order for the controller portion of the library to be
functional.

- macOS: the easiest way is to just install with brew.

    ```
    brew install hidapi
    ```

- Windows: simply download the [pre-built binaries][hidapi-binaries] and make them
  available in your path.

- Install via the provided package manager for your distro, or build from source. For Ubuntu:

    ```
    sudo apt install libhidapi-hidraw0
    ```

    or

    ```
    apt install libhidapi-libusb0
    ```

## Install

Once the prerequisites are installed, you can simply use pip to install the library:

```
pip install pyluxa4
```

After that, `pyluxa4` should be available from the command line (assuming Python's bin/Script folder is in your system
path).

```
$ pyluxa4 --version
pyluxa4 1.5
```

You can also run the module with:

```
$ python3 -m pyluxa4 --version
pyluxa4 1.5
```

--8<--
refs.txt
--8<--
