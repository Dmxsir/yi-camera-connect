# Changelog

All notable changes to **YI Camera Connect** will be documented in this file.

## 0.1.0 - 2026-09-05

Initial public HACS-ready release.

### Added

- Home Assistant camera entities backed by the companion YI RTSP App.
- Authoritative online/offline connectivity sensors.
- Stream start/stop switches.
- Runtime status and failure diagnostics.
- Frigate-ready RTSP endpoint sensors with go2rtc configuration examples.
- Supervisor App discovery based configuration flow.
- Secure handoff of YI account credentials to the YI RTSP App without storing the YI password in the Home Assistant Config Entry.
- English and Hebrew translations.
- HACS and Hassfest validation workflow.

### Notes

- Requires the companion **YI RTSP** Home Assistant App.
- Internal integration domain remains `yi_home` for compatibility with the App discovery contract.
- This is an independent community project and is not affiliated with or endorsed by YI Technology.
