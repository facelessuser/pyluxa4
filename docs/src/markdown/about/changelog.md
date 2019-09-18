# Changelog

## 1.2.0

- **NEW**: `--wait` removed from CLI as the server should not get hung while waiting. `wait` is still available when
  using `pyluxa4.usb` directly.
- **NEW**: Add new `schedule` command that takes a JSON and schedules lights by days and times.

## 1.1.0

- **NEW**: Allow `traffic-light`, `police`, `rainbow`, and `random<1 - 5>` as valid values on CLI along with numerical
  values.
- **NEW**: Allow `short`, `long`, `overlapping-short`, and `overlapping-long` as valid values on CLI along with
  numerical values.
- **NEW**: Provide more constants with friendly names in common library.
- **FIX**: Wave pattern not being sent properly.

## 1.0.0

- **NEW**: Initial release
