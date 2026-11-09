# James Farr Gomez (`@nertwork`)

**Infrastructure, Network & AI Systems Engineer** • Building autonomous infrastructure, local-first Smart Home & Energy systems, and Wayland/Hyprland desktop tooling.

[![Total Pull Requests](https://img.shields.io/badge/Pull_Requests_Authored-168-2ea043?style=for-the-badge&logo=github)](https://github.com/pulls?q=is%3Apr+author%3Anertwork)
[![Merged Pull Requests](https://img.shields.io/badge/Merged_PRs-142-8957e5?style=for-the-badge&logo=git)](https://github.com/pulls?q=is%3Apr+author%3Anertwork+is%3Amerged)
[![Active Open PRs](https://img.shields.io/badge/Open_Upstream_PRs-10-1f6feb?style=for-the-badge&logo=githubactions)](https://github.com/pulls?q=is%3Apr+author%3Anertwork+is%3Aopen)
[![Issues Reported](https://img.shields.io/badge/Upstream_Issues_Filed-43-d29922?style=for-the-badge&logo=github)](https://github.com/issues?q=is%3Aissue+author%3Anertwork)

---

## Upstream Open Source Contributions (Auto-Updated)

> *Automatically synchronized via GitHub Actions (`.github/workflows/update-profile.yml`) and `sync_github_profile.py`. Last verified: **2026-11-09 23:16 UTC***

### 1. Home Assistant Core Libraries, Smart Home & Clean Energy Integrations

| Status | Upstream Repository & Component | Pull Request & Issue | Technical Summary |
| :--- | :--- | :--- | :--- |
| ![Merged](https://img.shields.io/badge/PR_%23778-Merged-8957e5?style=flat-square&logo=github) | **[home-assistant-libs/aiowebostv](https://github.com/home-assistant-libs/aiowebostv)**<br><sub>LG webOS TV (`aiowebostv`)</sub> | [`#778`](https://github.com/home-assistant-libs/aiowebostv/pull/778) | Retrieve exceptions from all initial `subscribe_tasks` on failure to prevent unretrieved task warnings on Python 3.14 (shipped in `aiowebostv==1.0.0` / HA Core `2026.11.0`). |
| ![Merged](https://img.shields.io/badge/PR_%23350-Merged-8957e5?style=flat-square&logo=github) | **[thomluther/anker-solix-api](https://github.com/thomluther/anker-solix-api)**<br><sub>Anker SOLIX Python API</sub> | [`#350`](https://github.com/thomluther/anker-solix-api/pull/350) | Add Solarbank PPS (`F3000` / `A1782`) Home System MQTT telemetry (`0421` `a5`/`a6`/`d8`), realtime status requests, and PV channel mapping. |
| ![Open](https://img.shields.io/badge/PR_%23351-Open-2ea043?style=flat-square&logo=github) | **[thomluther/anker-solix-api](https://github.com/thomluther/anker-solix-api)**<br><sub>Anker SOLIX Python API</sub> | [`#351`](https://github.com/thomluther/anker-solix-api/pull/351) | Add Storm Guard (`disaster_backup`) and TOU usage mode schedule support (`modify_solix_use_time`) for Solarbank PPS `A1782` (`F3000`) & full 16-command MQTT hardware verification. |
| ![Merged](https://img.shields.io/badge/PR_%23524-Merged-8957e5?style=flat-square&logo=github) | **[zabuldon/teslajsonpy](https://github.com/zabuldon/teslajsonpy)**<br><sub>Tesla JSON Python (`teslajsonpy`)</sub> | [`#524`](https://github.com/zabuldon/teslajsonpy/pull/524) | Add Tesla Powerwall Storm Watch (`storm_mode_enabled`) properties and controller commands (released in `teslajsonpy==3.14.0`). |
| ![Merged](https://img.shields.io/badge/PR_%231247-Merged-8957e5?style=flat-square&logo=github) | **[alandtse/tesla](https://github.com/alandtse/tesla)**<br><sub>Tesla Custom Integration (`tesla_custom`)</sub> | [`#1247`](https://github.com/alandtse/tesla/pull/1247) | Add Tesla Powerwall Storm Watch switch entity (`StormWatchSwitch`). |
| ![Open](https://img.shields.io/badge/PR_%231256-Open-2ea043?style=flat-square&logo=github) | **[alandtse/tesla](https://github.com/alandtse/tesla)**<br><sub>Tesla Custom Integration (`tesla_custom`)</sub> | [`#1256`](https://github.com/alandtse/tesla/pull/1256) / [Issue `#1255`](https://github.com/alandtse/tesla/issues/1255) | Guard `teslamate.py` against empty/float MQTT payloads (`cast_int`) and validate `TeslaCarShiftState` enum options during concurrent streaming. |
| ![Open](https://img.shields.io/badge/PR_%23135-Open-2ea043?style=flat-square&logo=github) | **[home-assistant-libs/aioeagle](https://github.com/home-assistant-libs/aioeagle)**<br><sub>Rainforest EAGLE-3 / EAGLE-200 (`aioeagle`)</sub> | [`#135`](https://github.com/home-assistant-libs/aioeagle/pull/135) / [Issue `#136`](https://github.com/home-assistant-libs/aioeagle/issues/136) | Handle empty `<Device/>` XML responses and omitted component/variable fields in `ElectricMeter` during Zigbee HAN congestion. |
| ![Open](https://img.shields.io/badge/PR_%23367-Open-2ea043?style=flat-square&logo=github) | **[jbergler/hass-ttlock](https://github.com/jbergler/hass-ttlock)**<br><sub>TTLock Integration (`hass-ttlock`)</sub> | [`#367`](https://github.com/jbergler/hass-ttlock/pull/367) / [Issue `#366`](https://github.com/jbergler/hass-ttlock/issues/366) | Extend `REVERIFY_GRACE` to locks with an online G2 Wi-Fi gateway (`gateway_online`), reset retry grace on webhook push, and restore `Lock` state on startup via `RestoreEntity`. |
| ![Open](https://img.shields.io/badge/PR_%23904-Open-2ea043?style=flat-square&logo=github) | **[xZetsubou/hass-localtuya](https://github.com/xZetsubou/hass-localtuya)**<br><sub>LocalTuya Integration (`hass-localtuya`)</sub> | [`#904`](https://github.com/xZetsubou/hass-localtuya/pull/904) / [Issue `#909`](https://github.com/xZetsubou/hass-localtuya/issues/909) | Fix `UnboundLocalError` (`prefix`) and `AffixData` set hashability in `pytuya/parser.py` when logging unknown 4-byte header prefixes. |
| ![Open](https://img.shields.io/badge/PR_%23704-Open-2ea043?style=flat-square&logo=github) | **[FunkeyFlo/ps5-mqtt](https://github.com/FunkeyFlo/ps5-mqtt)**<br><sub>PlayStation 5 MQTT (`ps5-mqtt`)</sub> | [`#704`](https://github.com/FunkeyFlo/ps5-mqtt/pull/704) / [Issue `#703`](https://github.com/FunkeyFlo/ps5-mqtt/issues/703) | Use `takeEvery` for per-device Redux sagas (`REGISTER_DEVICE`, `UPDATE_HOME_ASSISTANT`), `continue` past transitioning consoles, and support comma-separated DDP broadcast targets. |
| ![Open](https://img.shields.io/badge/PR_%23128-Open-2ea043?style=flat-square&logo=github) | **[tsightler/ring-mqtt-ha-addon](https://github.com/tsightler/ring-mqtt-ha-addon)**<br><sub>Ring-MQTT Add-on (`ring-mqtt-ha-addon`)</sub> | [`#128`](https://github.com/tsightler/ring-mqtt-ha-addon/pull/128) | Use `str` schema for `disarm_code` in `config.yaml` so Home Assistant Supervisor's `addon_pwned` check does not flag 4-digit keypad PINs against HaveIBeenPwned. |
| ![Merged](https://img.shields.io/badge/PR_%23828-Merged-8957e5?style=flat-square&logo=github) | **[JeffSteinbok/hass-dreo](https://github.com/JeffSteinbok/hass-dreo)**<br><sub>Dreo Smart Device Integration (`hass-dreo`)</sub> | [`#828`](https://github.com/JeffSteinbok/hass-dreo/pull/828) / [Issue `#22`](https://github.com/JeffSteinbok/hass-dreo/issues/22) | Add support for `001` MCU revision of `DR-HAP003S` Air Purifier (shipped in `v1.11.11`). |
| ![Merged Manually](https://img.shields.io/badge/PR_%23641-Merged_Manually-8957e5?style=flat-square&logo=github) | **[thomluther/ha-anker-solix](https://github.com/thomluther/ha-anker-solix)**<br><sub>Anker SOLIX HA Integration (`ha-anker-solix`)</sub> | [`#641`](https://github.com/thomluther/ha-anker-solix/pull/641) | Use `SolixPpsBatteryStatus` enum for `SOLARBANK_PPS` `battery_status` sensor (manually merged upstream by maintainer). |
| ![Incorporated Upstream](https://img.shields.io/badge/PR_%23643-Incorporated_Upstream-8957e5?style=flat-square&logo=github) | **[thomluther/ha-anker-solix](https://github.com/thomluther/ha-anker-solix)**<br><sub>Anker SOLIX HA Integration (`ha-anker-solix`)</sub> | [`#643`](https://github.com/thomluther/ha-anker-solix/pull/643) | Support Storm Guard and backup usage mode entities (`select.py`, `datetime.py`) for `A1782` (`F3000`, incorporated into upstream `SB_PPS` support). |

---

### 2. Omarchy Linux, Hyprland & Quickshell Desktop Ecosystem

| Status | Upstream Repository & Component | Pull Request & Issue | Technical Summary |
| :--- | :--- | :--- | :--- |
| ![Merged](https://img.shields.io/badge/PR_%2346-Merged-8957e5?style=flat-square&logo=github) | **[tmn73/omarchy-calendar](https://github.com/tmn73/omarchy-calendar)**<br><sub>Omarchy Calendar (`omarchy-calendar`)</sub> | [`#46`](https://github.com/tmn73/omarchy-calendar/pull/46) | Resolve Google Calendar event `html_link` for Evolution Data Server (EDS) CalDAV sources. |
| ![Merged](https://img.shields.io/badge/PR_%236-Merged-8957e5?style=flat-square&logo=github) | **[meviusisback/omarchy-hw-monitor](https://github.com/meviusisback/omarchy-hw-monitor)**<br><sub>Omarchy Hardware Monitor (`omarchy-hw-monitor`)</sub> | [`#6`](https://github.com/meviusisback/omarchy-hw-monitor/pull/6) | Identify browser tab domains and process roles in `proc_top` with `tmpfs` caching. |
| ![Open](https://img.shields.io/badge/PR_%2316008-Open-2ea043?style=flat-square&logo=github) | **[omacom/omarchy](https://github.com/omacom/omarchy)**<br><sub>Omarchy Linux (`omarchy`)</sub> | [`#16008`](https://github.com/omacom/omarchy/pull/16008) / [Issue `#16006`](https://github.com/omacom/omarchy/issues/16006) | Handle early enterprise Wi-Fi script failures in the Quickshell network panel so failed `nmcli` connection creation clears `actionKind`. |
| ![Open](https://img.shields.io/badge/PR_%2330-Open-2ea043?style=flat-square&logo=github) | **[twiking/omasettings](https://github.com/twiking/omasettings)**<br><sub>OmaSettings (`omasettings`)</sub> | [`#30`](https://github.com/twiking/omasettings/pull/30) / [Issue `#36`](https://github.com/twiking/omasettings/issues/36) | Deduplicate numbered NetworkManager Wi-Fi profiles (`<SSID> 1`), clear stale interface bindings, and unescape colons in SSIDs. |

---

### 3. Cloud, Routing (`FRRouting` / BGP) & Network Monitoring (`LibreNMS`)

| Status | Upstream Repository & Component | Pull Request & Issue | Technical Summary |
| :--- | :--- | :--- | :--- |
| ![Open](https://img.shields.io/badge/PR_%239-Open-2ea043?style=flat-square&logo=github) | **[HappyPathway/github-runner-image](https://github.com/HappyPathway/github-runner-image)**<br><sub>GitHub Actions Runner Image</sub> | [`#9`](https://github.com/HappyPathway/github-runner-image/pull/9) | Add Python `venv` and workflow automation updates for self-hosted GitHub Actions runner image builds. |
| ![Merged](https://img.shields.io/badge/PR_%23123-Merged-8957e5?style=flat-square&logo=github) | **[jarischaefer/docker-librenms](https://github.com/jarischaefer/docker-librenms)**<br><sub>Docker LibreNMS (`docker-librenms`)</sub> | [`#123`](https://github.com/jarischaefer/docker-librenms/pull/123) / [Issue `#119`](https://github.com/jarischaefer/docker-librenms/issues/119) | Release version bumps (`1.68` / `1.69`) and distributed poller memcached support. |
| ![Merged](https://img.shields.io/badge/PR_%2356-Merged-8957e5?style=flat-square&logo=github) | **[mrlesmithjr/ansible-frr](https://github.com/mrlesmithjr/ansible-frr)**<br><sub>FRRouting Ansible Role (`ansible-frr`)</sub> | [`#56`](https://github.com/mrlesmithjr/ansible-frr/pull/56) / [Issue `#43`](https://github.com/mrlesmithjr/ansible-frr/issues/43) | Add BGP Listen Range support, OSPF distribute lists (`#28`), BGP neighbor timers (`#16`), Ubuntu 18/20 `iproute2` support (`#20`), and check-mode fixes (`#17`) across 9 merged PRs. |

---

## Published Open Source Projects & Omarchy Plugins

| Repository | Category / Plugin ID | Description |
| :--- | :--- | :--- |
| **[`nertwork/omarchy-ai-agents`](https://github.com/nertwork/omarchy-ai-agents)** | `nertwork.agents` | Real-time status, rate-limit, and token usage bar panel for AI coding assistants (Claude Code, OpenAI Codex, GitHub Copilot, Grok, Antigravity) on Omarchy Linux / Quickshell. |
| **[`nertwork/omarchy-network-info`](https://github.com/nertwork/omarchy-network-info)** | `nertwork.network-info` | Unified network intelligence, public/LAN IP telemetry, Wi-Fi RSSI, and live interface bandwidth monitor for Omarchy (`omarchy-shell`). |
| **[`nertwork/omarchy-battery-health`](https://github.com/nertwork/omarchy-battery-health)** | `nertwork.power` | Battery health diagnostics, 80% charge threshold limiting, and real-time power draw analytics for Omarchy Linux laptops. |
| **[`nertwork/omarchy-drawer`](https://github.com/nertwork/omarchy-drawer)** | `nertwork.drawer` | Foldable status bar drawer container for Omarchy widgets with smooth expand/collapse animations. |
| **[`nertwork/proxmox-image`](https://github.com/nertwork/proxmox-image)** | `Infrastructure` | Automated Ubuntu & Rocky Linux Cloud-Init VM template builder for Proxmox VE clusters. |
| **[`nertwork/change-acs-password`](https://github.com/nertwork/change-acs-password)** | `Network Automation` | Python automation toolkit and library for managing enterprise Cisco ACS appliances. |
