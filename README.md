# YI Camera Connect

Custom Home Assistant integration for YI Home cameras used together with the **YI RTSP** Home Assistant App.

YI Camera Connect exposes the cameras managed by YI RTSP as Home Assistant camera devices, online/offline sensors, stream controls, runtime diagnostics, and ready-to-use RTSP endpoints for Frigate.

> This is an independent community project and is not affiliated with or endorsed by YI Technology.

## Requirements

- Home Assistant OS / Supervised with support for Home Assistant Apps.
- The companion **YI RTSP** App must be installed and running.
- A supported YI Home account and camera model.

## Installation with HACS

Until the repository is included in the default HACS catalog, add it as a custom repository:

1. Open **HACS → Integrations**.
2. Open the repository menu and choose **Custom repositories**.
3. Add `https://github.com/Dmxsir/yi-camera-connect` as category **Integration**.
4. Install **YI Camera Connect**.
5. Restart Home Assistant.
6. Install/start the companion YI RTSP App. The App publishes Home Assistant discovery data and YI Camera Connect completes setup from that discovery.

The integration intentionally cannot be configured as a standalone cloud client. Camera/cloud sessions and media transport are owned by YI RTSP; Home Assistant communicates with the App over its internal authenticated API.

## Entities

For each discovered camera the integration can provide:

- Camera entity backed by the App-owned RTSP stream.
- Connectivity binary sensor using the App's PPPP availability state.
- Stream on/off switch.
- Runtime-status sensor with restart/failure diagnostics.
- Frigate RTSP sensor with a ready-to-copy LAN RTSP URL and go2rtc example.

## Security model

- The YI account password is sent directly to YI RTSP during account setup/reconfigure and is not stored in the Home Assistant Config Entry.
- The Config Entry stores only the App connection metadata and the App-internal API credential needed for Home Assistant ↔ App communication.
- Camera account/session secrets are not exposed through Home Assistant entities.

## Compatibility

The internal Home Assistant domain remains `yi_home` for compatibility with the YI RTSP App discovery contract.

Current public integration version: **0.1.0**.

## Companion App

YI RTSP repository: https://github.com/Dmxsir/yi-rtsp

## Development

The integration was split from the main reverse-engineering/development repository after the App-owned cloud-session architecture and HA/Frigate integration gates were completed.

Issues and feature requests belong in this repository's GitHub Issues.
