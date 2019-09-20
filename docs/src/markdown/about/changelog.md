# Changelog

## 1.4.0

- **NEW**: Schedule should not be sent as a file name, but as a JSON object.

## 1.3.0

- **NEW**: API for USB library now returns whether it passed or failed. This can indicate a disconnected device.
- **FIX**: A command may fail for various reasons, so don't remove a command from schedule just because it fails.
- **FIX**: Add logic to reconnect to a device if it appears the device was disconnected.

## 1.2.0

- **NEW**: `--wait` removed from CLI as the server should not get hung while waiting. `wait` is still available when
  using `pyluxa4.usb` directly.
- **NEW**: Add new `scheduler` command that allows scheduling command events based on day and time and clearing
  scheduled events.
- **NEW**: Add new `get` command which can be used to retrieve currently loaded schedules via `pyluxa4 get schedule`.

## 1.1.0

- **NEW**: Allow `traffic-light`, `police`, `rainbow`, and `random<1 - 5>` as valid values on CLI along with numerical
  values.
- **NEW**: Allow `short`, `long`, `overlapping-short`, and `overlapping-long` as valid values on CLI along with
  numerical values.
- **NEW**: Provide more constants with friendly names in common library.
- **FIX**: Wave pattern not being sent properly.

## 1.0.0

- **NEW**: Initial release
