# Changelog

## 1.7

-   **NEW**: Update supported Python versions to Python 3.8 - 3.12.
-   **NEW**: Use `coloraide` to handle color parsing.
-   **NEW**: Add `--hdiapi` option to the `serve` command to explicitly define an absolute path to the hidapi library.
-   **FIX**: Vendor `hid` and provide fixes for loading the libraries on Windows with Python 3.8+.

## 1.6

-   **NEW**: Deprecate the timer argument `--type` in favor of `--cmd` which corresponds to how it is stored in the
    scheduler.

## 1.5.1

-   **FIX**: Better scheduler algorithm. Handles lapse in time (computer sleeping), more efficient, etc.

## 1.5

-   **NEW**: Add `timer` command.
-   **NEW**: Add `--cancel` option to `scheduler` command that cancels timers in the scheduler. `--clear` will not
    remove timers, only traditional scheduled events.
-   **FIX**: Better day rollover logic.
-   **FIX**: LED resolution from CLI.

## 1.4

-   **NEW**: Schedule should not be sent as a file name, but as a JSON object.

## 1.3

-   **NEW**: API for USB library now returns whether it passed or failed. This can indicate a disconnected device.
-   **FIX**: A command may fail for various reasons, so don't remove a command from schedule just because it fails.
-   **FIX**: Add logic to reconnect to a device if it appears the device was disconnected.

## 1.2

-   **NEW**: `--wait` removed from CLI as the server should not get hung while waiting. `wait` is still available when
    using `pyluxa4.usb` directly.
-   **NEW**: Add new `scheduler` command that allows scheduling command events based on day and time and clearing
    scheduled events.
-   **NEW**: Add new `get` command which can be used to retrieve currently loaded schedules via `pyluxa4 get schedule`.

## 1.1

-   **NEW**: Allow `traffic-light`, `police`, `rainbow`, and `random<1 - 5>` as valid values on CLI along with numerical
    values.
-   **NEW**: Allow `short`, `long`, `overlapping-short`, and `overlapping-long` as valid values on CLI along with
    numerical values.
-   **NEW**: Provide more constants with friendly names in common library.
-   **FIX**: Wave pattern not being sent properly.

## 1.0

-   **NEW**: Initial release
