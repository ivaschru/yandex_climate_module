# Yandex Climate Modules (IoT API)

Custom integration for Home Assistant that exposes Yandex Station climate module sensors
(CO2 / temperature / humidity) via Yandex IoT API.

## Install (HACS custom repo)
- HACS → Integrations → ⋮ → Custom repositories
- Add this repo as **Integration**
- Install, restart Home Assistant

## Setup
- Settings → Devices & services → Add integration → "Yandex Climate Modules (IoT API)"
- Paste OAuth token with `iot.view` scope
- Select modules found automatically
