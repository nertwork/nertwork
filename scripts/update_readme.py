#!/usr/bin/env python3
"""Nertwork GitHub Open Source Attribution & Profile Sync CLI (`github-oss` / `sync_github_profile.py`).

Queries live status of all upstream Open Source Pull Requests and companion Issues authored by
`@nertwork` (James Farr Gomez <james@nertwork.com>) across Home Assistant, Smart Home & Clean Energy,
Omarchy Linux / Hyprland / Quickshell, and Cloud/Network Infrastructure:

Subcommands (<150 tokens by default):
  summary     Compact <150-token summary of @nertwork merged & open upstream PRs and companion Issues
  prs         Detailed table of tracked upstream PRs (state, head SHA, issue link, comments, merge status)
  issues      Detailed status of companion upstream GitHub Issues filed by @nertwork
  comments    Show recent maintainer/bot comments & reviews on tracked PRs and Issues
  sync        Regenerate and push https://github.com/nertwork/nertwork (README.md + 6h GitHub Action)
  add         Register a new upstream PR/Issue in TRACKED_CONTRIBUTIONS (and optionally link Fixes #<issue> & push)
  ha-patches  Run ops/smarthome/tools/check_upstream_fixes.py to audit all 14 live HA patches & upstream PRs

Also embedded inside `nertwork/nertwork/scripts/update_readme.py` so GitHub Actions
(`.github/workflows/update-profile.yml`) auto-updates `https://github.com/nertwork` every 6 hours.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

GITHUB_USER = "nertwork"
USER_AGENT = "nertwork-profile-sync/1.1"

# BEGIN_TRACKED_CONTRIBUTIONS
TRACKED_CONTRIBUTIONS: list[dict[str, Any]] = [
    # --- Category 1: Home Assistant Core Libraries & Energy / Smart Home Ecosystem ---
    {
        "category": "smarthome",
        "repo": "home-assistant-libs/aiowebostv",
        "pr": 778,
        "issue": None,
        "component": "LG webOS TV (`aiowebostv`)",
        "summary": "Retrieve exceptions from all initial `subscribe_tasks` on failure to prevent unretrieved task warnings on Python 3.14 (shipped in `aiowebostv==1.0.0` / HA Core `2026.11.0`).",
    },
    {
        "category": "smarthome",
        "repo": "thomluther/anker-solix-api",
        "pr": 350,
        "issue": None,
        "component": "Anker SOLIX Python API",
        "summary": "Add Solarbank PPS (`F3000` / `A1782`) Home System MQTT telemetry (`0421` `a5`/`a6`/`d8`), realtime status requests, and PV channel mapping.",
    },
    {
        "category": "smarthome",
        "repo": "thomluther/anker-solix-api",
        "pr": 351,
        "issue": None,
        "component": "Anker SOLIX Python API",
        "summary": "Add Storm Guard (`disaster_backup`) and TOU usage mode schedule support (`modify_solix_use_time`) for Solarbank PPS `A1782` (`F3000`) & full 16-command MQTT hardware verification.",
    },
    {
        "category": "smarthome",
        "repo": "zabuldon/teslajsonpy",
        "pr": 524,
        "issue": None,
        "component": "Tesla JSON Python (`teslajsonpy`)",
        "summary": "Add Tesla Powerwall Storm Watch (`storm_mode_enabled`) properties and controller commands (released in `teslajsonpy==3.14.0`).",
    },
    {
        "category": "smarthome",
        "repo": "alandtse/tesla",
        "pr": 1247,
        "issue": None,
        "component": "Tesla Custom Integration (`tesla_custom`)",
        "summary": "Add Tesla Powerwall Storm Watch switch entity (`StormWatchSwitch`).",
    },
    {
        "category": "smarthome",
        "repo": "alandtse/tesla",
        "pr": 1256,
        "issue": 1255,
        "component": "Tesla Custom Integration (`tesla_custom`)",
        "summary": "Guard `teslamate.py` against empty/float MQTT payloads (`cast_int`) and validate `TeslaCarShiftState` enum options during concurrent streaming.",
    },
    {
        "category": "smarthome",
        "repo": "home-assistant-libs/aioeagle",
        "pr": 135,
        "issue": 136,
        "component": "Rainforest EAGLE-3 / EAGLE-200 (`aioeagle`)",
        "summary": "Handle empty `<Device/>` XML responses and omitted component/variable fields in `ElectricMeter` during Zigbee HAN congestion.",
    },
    {
        "category": "smarthome",
        "repo": "jbergler/hass-ttlock",
        "pr": 367,
        "issue": 366,
        "component": "TTLock Integration (`hass-ttlock`)",
        "summary": "Extend `REVERIFY_GRACE` to locks with an online G2 Wi-Fi gateway (`gateway_online`), reset retry grace on webhook push, and restore `Lock` state on startup via `RestoreEntity`.",
    },
    {
        "category": "smarthome",
        "repo": "xZetsubou/hass-localtuya",
        "pr": 904,
        "issue": 909,
        "component": "LocalTuya Integration (`hass-localtuya`)",
        "summary": "Fix `UnboundLocalError` (`prefix`) and `AffixData` set hashability in `pytuya/parser.py` when logging unknown 4-byte header prefixes.",
    },
    {
        "category": "smarthome",
        "repo": "FunkeyFlo/ps5-mqtt",
        "pr": 704,
        "issue": 703,
        "component": "PlayStation 5 MQTT (`ps5-mqtt`)",
        "summary": "Use `takeEvery` for per-device Redux sagas (`REGISTER_DEVICE`, `UPDATE_HOME_ASSISTANT`), `continue` past transitioning consoles, and support comma-separated DDP broadcast targets (shipped in `v1.9.0`).",
    },
    {
        "category": "smarthome",
        "repo": "tsightler/ring-mqtt-ha-addon",
        "pr": 128,
        "issue": None,
        "component": "Ring-MQTT Add-on (`ring-mqtt-ha-addon`)",
        "summary": "Use `str` schema for `disarm_code` in `config.yaml` so Home Assistant Supervisor's `addon_pwned` check does not flag 4-digit keypad PINs against HaveIBeenPwned.",
    },
    {
        "category": "smarthome",
        "repo": "JeffSteinbok/hass-dreo",
        "pr": 828,
        "issue": 22,
        "component": "Dreo Smart Device Integration (`hass-dreo`)",
        "summary": "Add support for `001` MCU revision of `DR-HAP003S` Air Purifier (shipped in `v1.11.11`).",
    },
    {
        "category": "smarthome",
        "repo": "thomluther/ha-anker-solix",
        "pr": 641,
        "issue": None,
        "component": "Anker SOLIX HA Integration (`ha-anker-solix`)",
        "summary": "Use `SolixPpsBatteryStatus` enum for `SOLARBANK_PPS` `battery_status` sensor (manually merged upstream by maintainer).",
        "manual_merge_note": "Merged Manually",
    },
    {
        "category": "smarthome",
        "repo": "thomluther/ha-anker-solix",
        "pr": 643,
        "issue": None,
        "component": "Anker SOLIX HA Integration (`ha-anker-solix`)",
        "summary": "Support Storm Guard and backup usage mode entities (`select.py`, `datetime.py`) for `A1782` (`F3000`, incorporated into upstream `SB_PPS` support).",
        "manual_merge_note": "Incorporated Upstream",
    },
    # --- Category 2: Omarchy Linux & Wayland / Hyprland Desktop Ecosystem ---
    {
        "category": "omarchy",
        "repo": "tmn73/omarchy-calendar",
        "pr": 46,
        "issue": None,
        "component": "Omarchy Calendar (`omarchy-calendar`)",
        "summary": "Resolve Google Calendar event `html_link` for Evolution Data Server (EDS) CalDAV sources.",
    },
    {
        "category": "omarchy",
        "repo": "meviusisback/omarchy-hw-monitor",
        "pr": 6,
        "issue": None,
        "component": "Omarchy Hardware Monitor (`omarchy-hw-monitor`)",
        "summary": "Identify browser tab domains and process roles in `proc_top` with `tmpfs` caching.",
    },
    {
        "category": "omarchy",
        "repo": "omacom/omarchy",
        "pr": 16008,
        "issue": 16006,
        "component": "Omarchy Linux (`omarchy`)",
        "summary": "Handle early enterprise Wi-Fi script failures in the Quickshell network panel so failed `nmcli` connection creation clears `actionKind`.",
    },
    {
        "category": "omarchy",
        "repo": "twiking/omasettings",
        "pr": 30,
        "issue": 36,
        "component": "OmaSettings (`omasettings`)",
        "summary": "Deduplicate numbered NetworkManager Wi-Fi profiles (`<SSID> 1`), clear stale interface bindings, and unescape colons in SSIDs.",
    },
    # --- Category 3: Cloud, Networking & Infrastructure Automation ---
    {
        "category": "infra",
        "repo": "HappyPathway/github-runner-image",
        "pr": 9,
        "issue": None,
        "component": "GitHub Actions Runner Image",
        "summary": "Add Python `venv` and workflow automation updates for self-hosted GitHub Actions runner image builds.",
    },
    {
        "category": "infra",
        "repo": "jarischaefer/docker-librenms",
        "pr": 123,
        "issue": 119,
        "component": "Docker LibreNMS (`docker-librenms`)",
        "summary": "Release version bumps (`1.68` / `1.69`) and distributed poller memcached support.",
    },
    {
        "category": "infra",
        "repo": "mrlesmithjr/ansible-frr",
        "pr": 56,
        "issue": 43,
        "component": "FRRouting Ansible Role (`ansible-frr`)",
        "summary": "Add BGP Listen Range support, OSPF distribute lists (`#28`), BGP neighbor timers (`#16`), Ubuntu 18/20 `iproute2` support (`#20`), and check-mode fixes (`#17`) across 9 merged PRs.",
    },
]
# END_TRACKED_CONTRIBUTIONS

PUBLISHED_PROJECTS: list[dict[str, str]] = [
    {
        "repo": "nertwork/omarchy-ai-agents",
        "plugin_id": "nertwork.agents",
        "title": "Omarchy AI Agents (`nertwork.agents`)",
        "description": "Real-time status, rate-limit, and token usage bar panel for AI coding assistants (Claude Code, OpenAI Codex, GitHub Copilot, Grok, Antigravity) on Omarchy Linux / Quickshell.",
    },
    {
        "repo": "nertwork/omarchy-network-info",
        "plugin_id": "nertwork.network-info",
        "title": "Omarchy Network Intelligence (`nertwork.network-info`)",
        "description": "Unified network intelligence, public/LAN IP telemetry, Wi-Fi RSSI, and live interface bandwidth monitor for Omarchy (`omarchy-shell`).",
    },
    {
        "repo": "nertwork/omarchy-battery-health",
        "plugin_id": "nertwork.power",
        "title": "Omarchy Battery Health & Power (`nertwork.power`)",
        "description": "Battery health diagnostics, 80% charge threshold limiting, and real-time power draw analytics for Omarchy Linux laptops.",
    },
    {
        "repo": "nertwork/omarchy-drawer",
        "plugin_id": "nertwork.drawer",
        "title": "Omarchy Foldable Bar Drawer (`nertwork.drawer`)",
        "description": "Foldable status bar drawer container for Omarchy widgets with smooth expand/collapse animations.",
    },
    {
        "repo": "nertwork/proxmox-image",
        "plugin_id": "Infrastructure",
        "title": "Proxmox Cloud-Init Image Builder (`proxmox-image`)",
        "description": "Automated Ubuntu & Rocky Linux Cloud-Init VM template builder for Proxmox VE clusters.",
    },
    {
        "repo": "nertwork/change-acs-password",
        "plugin_id": "Network Automation",
        "title": "Cisco ACS Automation (`change-acs-password` & `acsclient`)",
        "description": "Python automation toolkit and library for managing enterprise Cisco ACS appliances.",
    },
]


def _get_github_token() -> str:
    """Resolve GitHub token from environment (`GH_TOKEN` / `GITHUB_TOKEN`) or HashiCorp Vault."""
    for env_key in ("GH_TOKEN", "GITHUB_TOKEN", "PAT_TOKEN"):
        val = os.environ.get(env_key, "").strip()
        if val:
            return val
    try:
        env = dict(os.environ)
        env.setdefault("VAULT_ADDR", "https://vault.nertwork.com")
        vt_path = Path.home() / ".vault-token"
        if "VAULT_TOKEN" not in env and vt_path.exists():
            env["VAULT_TOKEN"] = vt_path.read_text(encoding="utf-8").strip()
        proc = subprocess.run(
            ["vault", "kv", "get", "-field=token", "terraform_keys/github_token"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            env=env,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception:
        pass
    return ""


def _gh_request(
    url: str,
    token: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as exc:
        return {"error": str(exc)}


def _gh_get(url: str, token: str) -> dict[str, Any]:
    return _gh_request(url, token, method="GET")


def fetch_live_contributions(token: str) -> dict[str, Any]:
    """Query GitHub API in parallel for all tracked PRs plus overall @nertwork search counts."""
    def _fetch_one(item: dict[str, Any]) -> dict[str, Any]:
        repo = item["repo"]
        pr_num = item["pr"]
        data = _gh_get(f"https://api.github.com/repos/{repo}/pulls/{pr_num}", token)
        merged = bool(data.get("merged"))
        raw_state = str(data.get("state", "open")).lower()
        head_sha = str((data.get("head") or {}).get("sha") or "")[:7]
        comments = int(data.get("comments", 0)) + int(data.get("review_comments", 0))
        mergeable_state = str(data.get("mergeable_state") or "unknown")
        if mergeable_state == "unstable" and data.get("mergeable") is True:
            mergeable_state = "clean (awaiting maintainer CI)"
        if merged:
            status = "MERGED"
            badge = f"![Merged](https://img.shields.io/badge/PR_%23{pr_num}-Merged-8957e5?style=flat-square&logo=github)"
        elif raw_state == "open":
            status = "OPEN"
            badge = f"![Open](https://img.shields.io/badge/PR_%23{pr_num}-Open-2ea043?style=flat-square&logo=github)"
        elif item.get("manual_merge_note"):
            status = "MERGED_MANUALLY"
            label = urllib.parse.quote(item["manual_merge_note"].replace(" ", "_"))
            badge = f"![{item['manual_merge_note']}](https://img.shields.io/badge/PR_%23{pr_num}-{label}-8957e5?style=flat-square&logo=github)"
        else:
            status = "CLOSED"
            badge = f"![Closed](https://img.shields.io/badge/PR_%23{pr_num}-Closed-6e7681?style=flat-square&logo=github)"

        created_at = str(data.get("created_at") or "")[:10]
        merged_at = str(data.get("merged_at") or "")[:10]
        updated_at = str(data.get("updated_at") or "")[:10]
        return {
            **item,
            "status": status,
            "badge": badge,
            "head_sha": head_sha,
            "comments": comments,
            "mergeable_state": mergeable_state,
            "title": data.get("title") or item["summary"],
            "created_at": created_at,
            "merged_at": merged_at,
            "updated_at": updated_at,
            "pr_url": f"https://github.com/{repo}/pull/{pr_num}",
            "issue_url": f"https://github.com/{repo}/issues/{item['issue']}" if item.get("issue") else None,
        }

    with ThreadPoolExecutor(max_workers=8) as ex:
        enriched = list(ex.map(_fetch_one, TRACKED_CONTRIBUTIONS))

    all_prs = _gh_get(
        f"https://api.github.com/search/issues?q=author:{GITHUB_USER}+is:pr&per_page=1",
        token,
    )
    merged_prs = _gh_get(
        f"https://api.github.com/search/issues?q=author:{GITHUB_USER}+is:pr+is:merged&per_page=1",
        token,
    )
    open_prs = _gh_get(
        f"https://api.github.com/search/issues?q=author:{GITHUB_USER}+is:pr+is:open&per_page=1",
        token,
    )
    all_issues = _gh_get(
        f"https://api.github.com/search/issues?q=author:{GITHUB_USER}+is:issue&per_page=1",
        token,
    )

    return {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "totals": {
            "total_prs": int(all_prs.get("total_count", len(enriched))),
            "merged_prs": int(merged_prs.get("total_count", 0)),
            "open_prs": int(open_prs.get("total_count", 0)),
            "total_issues": int(all_issues.get("total_count", 0)),
            "tracked_count": len(enriched),
            "tracked_merged": sum(1 for x in enriched if x["status"] in ("MERGED", "MERGED_MANUALLY")),
            "tracked_open": sum(1 for x in enriched if x["status"] == "OPEN"),
        },
        "items": enriched,
    }


def render_readme(data: dict[str, Any]) -> str:
    """Render the complete Markdown for `nertwork/nertwork/README.md`."""
    totals = data["totals"]
    items = data["items"]

    def _render_table(cat: str) -> str:
        rows = [
            "| Status | Upstream Repository & Component | Pull Request & Issue | Technical Summary |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for it in items:
            if it["category"] != cat:
                continue
            repo = it["repo"]
            pr_link = f"[`#{it['pr']}`]({it['pr_url']})"
            if it.get("issue") and it.get("issue_url"):
                pr_link += f" / [Issue `#{it['issue']}`]({it['issue_url']})"
            repo_col = f"**[{repo}](https://github.com/{repo})**<br><sub>{it['component']}</sub>"
            rows.append(f"| {it['badge']} | {repo_col} | {pr_link} | {it['summary']} |")
        return "\n".join(rows)

    proj_rows = [
        "| Repository | Category / Plugin ID | Description |",
        "| :--- | :--- | :--- |",
    ]
    for p in PUBLISHED_PROJECTS:
        proj_rows.append(
            f"| **[`{p['repo']}`](https://github.com/{p['repo']})** | `{p['plugin_id']}` | {p['description']} |"
        )
    proj_table = "\n".join(proj_rows)

    return f"""# James F. Gomez (`@nertwork`)

**Principal Cloud (GCP & AWS), Network Security (`JNCIP-SEC`) & Agentic AI Infrastructure Architect (`ai-ops`)** • **15+ years** of production experience architecting global multi-cloud platforms (`GCP`, `AWS`, `OpenStack`, `Proxmox VE`, `Kubernetes`), global golden-image & IaC CI/CD pipelines (`Terraform Enterprise` across 500+ workspaces, `Ansible`, `Puppet`, `Pulumi`, `Packer`, `GitLab CI`, `GitHub Actions`), carrier & data center routing/switching (`1,000+` devices • `BGP`, `OSPF`, `EVPN-VXLAN`, `Juniper Junos`, `Cisco IOS-XE/NX-OS`, `Cumulus Linux`), and autonomous Zero-Trust SecOps (`Wazuh SIEM/XDR`, `HashiCorp Vault`, `MCP`, `Graphify`).

📍 **Location & Mobility:** `Remote (US)` • `Los Angeles Metro` • `San Francisco Bay Area` • `Austin, TX` • `New York City Metro` *(Open to Relocation w/ Package)*

[![Portfolio & Executive Resume](https://img.shields.io/badge/Architect_Dossier_%26_Resume-nertwork.com%2Fabout-38bdf8?style=for-the-badge&logo=cloudflare&logoColor=white)](https://www.nertwork.com/about/)
[![Technical Blog](https://img.shields.io/badge/Engineering_Dispatches-nertwork.com-818cf8?style=for-the-badge&logo=rss&logoColor=white)](https://www.nertwork.com/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-James_Gomez-0a66c2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/james-farr/)
[![X / Twitter](https://img.shields.io/badge/X-nertwork-111827?style=for-the-badge&logo=x&logoColor=white)](https://x.com/nertwork)

[![Total Pull Requests](https://img.shields.io/badge/Pull_Requests_Authored-{totals['total_prs']}-2ea043?style=for-the-badge&logo=github)](https://github.com/pulls?q=is%3Apr+author%3Anertwork)
[![Merged Pull Requests](https://img.shields.io/badge/Merged_PRs-{totals['merged_prs']}-8957e5?style=for-the-badge&logo=git)](https://github.com/pulls?q=is%3Apr+author%3Anertwork+is%3Amerged)
[![Active Open PRs](https://img.shields.io/badge/Open_Upstream_PRs-{totals['open_prs']}-1f6feb?style=for-the-badge&logo=githubactions)](https://github.com/pulls?q=is%3Apr+author%3Anertwork+is%3Aopen)
[![Issues Reported](https://img.shields.io/badge/Upstream_Issues_Filed-{totals['total_issues']}-d29922?style=for-the-badge&logo=github)](https://github.com/issues?q=is%3Aissue+author%3Anertwork)

---

## Core Architecture Stack & Certifications (15+ Years Production Leadership)

| Domain | Technologies & Production Capabilities |
| :--- | :--- |
| **Agentic AI & Autonomous SecOps (`ai-ops`)** | Two-Tier Orchestrator/Sub-Agent Architecture (`Vertex AI`, `Google Agentspace`, `AI Agent Gateways`, `Bedrock`, `OpenAI`, `Gemini`), `LLMOps`/`MLOps` Governance, Model Context Protocol (`MCP`), `Graphify` Topological Knowledge Graphs (`<150-token` queries), Autonomous `Wazuh` & CI/CD Remediation (`Hermes`), Candidate Diff Staging |
| **Google Cloud (GCP) & AWS Architecture** | **GCP:** `GKE`, `Cloud Run`, `Vertex AI`, `Agentspace`, `Shared VPC`, `Cloud Router` & `NCC` HA BGP/IPsec, `Cloud Armor` WAF, `Workload Identity Federation`, `BigQuery`/`GMP` • **AWS:** `1,000+` VM Migrations, `Transit Gateway (TGW)`, `Direct Connect`, `EKS`/`ECS`, `GuardDuty`, `Security Hub`, `Network Firewall`, Cloud FinOps |
| **Multi-Cloud IaC & Global CI/CD** | Terraform & Terraform Enterprise (`500+` Workspaces), Pulumi (`Python`/`TypeScript`), Ansible, Puppet, Packer Golden Images, GitLab CI/CD, GitHub Actions, Jenkins across `NA`, `LATAM`, `EU` & `APAC` |
| **Carrier & Data Center Networking** | `1,000+` Managed Devices • `BGP` (95th-Percentile TE), `OSPF`, `EVPN-VXLAN`, `VRF-Lite`, `ECMP`, `VRRP`, `LACP`; Juniper `Junos` (`MX`/`EX`/`QFX`/`SRX`, `PyEZ`, `NETCONF`), Cisco (`IOS-XE`/`NX-OS`/`ASA`), `Cumulus Linux` (`FRRouting`), `MikroTik RouterOS` |
| **Zero-Trust Security, SIEM/XDR & SSOT** | `Wazuh` SIEM/XDR (`OpenSearch` CVE Indexing, MITRE ATT&CK, CIS Benchmarks), `HashiCorp Vault` Dynamic Secrets/PKI, `Authentik` SAML/OIDC SSO, Enterprise `RADIUS`/`TACACS+` AAA, Global Factory `IPsec`/`VTI`, `NetBox` SSOT, `Grafana Cloud` (`Prometheus`/`Mimir`/`Loki`) |
| **Industry Certifications & Education** | **`JNCIP-SEC`** • **`JNCIP-DC`** • **`JNCIP-ENT`** • **`JNCDA`** • **Juniper SE Champion** • **`CCNP`** • **`CCNA`** • **`VMware VCP5-DCV`** • **Mitel CVE** • **Cypress College** (Cisco Network & Security Lab, *Grade: A*) • **Victor Valley College** (Linux Administration, *Grade: A*) |

### Featured Technical Publications on [`nertwork.com`](https://www.nertwork.com/)
- [**Autonomous Cloud & Infrastructure SecOps: Integrating Wazuh SIEM/XDR, HashiCorp Vault, and Agentic AI Across AWS, GCP, and Proxmox Fleets**](https://www.nertwork.com/2026/11/10/autonomous-cloud-and-infrastructure-secops-wazuh-siem-xdr-hashicorp-vault-and-agentic-ai/)
- [**Leveraging AI for a Homelab: Declarative Proxmox VE Infrastructure with Terraform, Pulumi & GitLab CI/CD**](https://www.nertwork.com/2026/11/10/leveraging-ai-for-a-homelab-declarative-proxmox-ve-infrastructure-with-terraform-pulumi-and-gitlab-ci-cd/)
- [**Enforcing Network Standards Across a 1,000+ Device Fleet with Agentic AI**](https://www.nertwork.com/2026/10/30/enforcing-network-standards-across-a-1000-device-fleet-with-agentic-ai/)
- [**Full Architect Resume, Experience Timeline & All 37 Articles (`/about/`)**](https://www.nertwork.com/about/)

---

## Upstream Open Source Contributions (Auto-Updated)

> *Automatically synchronized via GitHub Actions (`.github/workflows/update-profile.yml`) and `sync_github_profile.py`. Last verified: **{data['updated_at']}***

### 1. Home Assistant Core Libraries, Smart Home & Clean Energy Integrations

{_render_table("smarthome")}

---

### 2. Omarchy Linux, Hyprland & Quickshell Desktop Ecosystem

{_render_table("omarchy")}

---

### 3. Cloud, Routing (`FRRouting` / BGP) & Network Monitoring (`LibreNMS`)

{_render_table("infra")}

---

## Published Open Source Projects & Omarchy Plugins

{proj_table}
"""


WORKFLOW_YAML = """name: Auto-Update Open Source Contributions README

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:
  push:
    branches:
      - main
    paths:
      - 'scripts/update_readme.py'
      - '.github/workflows/update-profile.yml'

permissions:
  contents: write

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout profile repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Update README with live GitHub PR & Issue statuses
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python3 scripts/update_readme.py --output README.md

      - name: Commit and push if changed
        run: |
          git config user.name "James Farr Gomez"
          git config user.email "james@nertwork.com"
          git add README.md
          if ! git diff --cached --quiet; then
            git commit -m "chore(profile): auto-update upstream PR and issue statuses [skip ci]"
            git push
          fi
"""


def sync_to_github_repo(readme_text: str, script_text: str, token: str) -> dict[str, Any]:
    """Clone `nertwork/nertwork`, write `README.md`, `scripts/update_readme.py`, and `.github/workflows/update-profile.yml`, and push."""
    work_dir = Path("/tmp/nertwork_profile_repo")
    subprocess.run(["rm", "-rf", str(work_dir)], check=False)
    clone_url = f"https://{GITHUB_USER}:{token}@github.com/{GITHUB_USER}/{GITHUB_USER}.git"
    git_env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "James Farr Gomez",
        "GIT_AUTHOR_EMAIL": "james@nertwork.com",
        "GIT_COMMITTER_NAME": "James Farr Gomez",
        "GIT_COMMITTER_EMAIL": "james@nertwork.com",
        "GIT_TERMINAL_PROMPT": "0",
    }
    try:
        res = subprocess.run(
            ["git", "clone", clone_url, str(work_dir)],
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
            env=git_env,
        )
        if res.returncode != 0:
            return {"pushed": False, "error": res.stderr.strip()}

        (work_dir / "README.md").write_text(readme_text, encoding="utf-8")
        scripts_dir = work_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        (scripts_dir / "update_readme.py").write_text(script_text, encoding="utf-8")
        wf_dir = work_dir / ".github" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        (wf_dir / "update-profile.yml").write_text(WORKFLOW_YAML, encoding="utf-8")

        subprocess.run(["git", "-C", str(work_dir), "add", "-A"], check=True, env=git_env)
        diff_check = subprocess.run(
            ["git", "-C", str(work_dir), "diff", "--cached", "--quiet"],
            check=False,
            env=git_env,
        )
        if diff_check.returncode == 0:
            return {"pushed": False, "status": "up_to_date", "url": f"https://github.com/{GITHUB_USER}"}

        subprocess.run(
            [
                "git",
                "-C",
                str(work_dir),
                "commit",
                "-m",
                "feat(profile): sync upstream Open Source PR & issue attribution showcase",
            ],
            check=True,
            env=git_env,
        )
        push_res = subprocess.run(
            ["git", "-C", str(work_dir), "push", "origin", "HEAD:main"],
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
            env=git_env,
        )
        return {
            "pushed": push_res.returncode == 0,
            "status": "updated" if push_res.returncode == 0 else "push_failed",
            "url": f"https://github.com/{GITHUB_USER}",
            "error": None if push_res.returncode == 0 else push_res.stderr.strip(),
        }
    finally:
        subprocess.run(["rm", "-rf", str(work_dir)], check=False)


def print_compact_summary(data: dict[str, Any]) -> None:
    """Print <150-token compact summary of @nertwork upstream contributions."""
    t = data["totals"]
    items = data["items"]
    print(
        f"@nertwork GitHub OSS Attribution (https://github.com/nertwork | {data['updated_at']}):\n"
        f"  Totals : {t['total_prs']} PRs Authored ({t['merged_prs']} Merged, {t['open_prs']} Open) | "
        f"{t['total_issues']} Issues Filed | Tracked Showcase: {t['tracked_merged']} Merged, {t['tracked_open']} Open"
    )
    merged_list = [
        f"{it['repo'].split('/')[-1]}#{it['pr']}"
        for it in items
        if it["status"] in ("MERGED", "MERGED_MANUALLY")
    ]
    print(f"  Merged : {', '.join(merged_list)}")
    print("  Open PRs & Companion Issues:")
    for it in items:
        if it["status"] == "OPEN":
            iss_str = f" (Fixes #{it['issue']})" if it.get("issue") else ""
            print(
                f"    • {it['repo']}#{it['pr']}{iss_str} [{it['head_sha']}] "
                f"(mergeable={it['mergeable_state']}, comments={it['comments']})"
            )


def print_detailed_prs(data: dict[str, Any], state_filter: str = "all", cat_filter: str = "all") -> None:
    """Print detailed table of tracked upstream PRs."""
    print(f"=== @nertwork Tracked Upstream PRs ({data['updated_at']}) ===")
    for it in data["items"]:
        if state_filter != "all" and state_filter.upper() not in it["status"]:
            continue
        if cat_filter != "all" and it["category"] != cat_filter:
            continue
        iss = f" | Issue #{it['issue']} ({it['issue_url']})" if it.get("issue") else ""
        print(
            f"[{it['status']}] {it['repo']}#{it['pr']} ({it['category']}) — {it['component']}\n"
            f"  URL     : {it['pr_url']}{iss}\n"
            f"  Head/CI : sha={it['head_sha']} | mergeable={it['mergeable_state']} | comments={it['comments']} | updated={it['updated_at']}\n"
            f"  Summary : {it['summary']}"
        )


def print_detailed_issues(token: str) -> None:
    """Fetch and print live status of companion upstream GitHub Issues filed by @nertwork."""
    issue_items = [it for it in TRACKED_CONTRIBUTIONS if it.get("issue")]
    print("=== @nertwork Upstream Companion Issues ===")
    for it in issue_items:
        repo = it["repo"]
        iss_num = it["issue"]
        iss_data = _gh_get(f"https://api.github.com/repos/{repo}/issues/{iss_num}", token)
        state = str(iss_data.get("state", "unknown")).upper()
        title = iss_data.get("title") or it["summary"]
        comments = iss_data.get("comments", 0)
        print(
            f"[{state}] {repo}#{iss_num} (linked to PR #{it['pr']}) — comments={comments}\n"
            f"  Title : {title}\n"
            f"  URL   : https://github.com/{repo}/issues/{iss_num}"
        )


def print_recent_comments(token: str, repo_filter: str = "") -> None:
    """Fetch and print recent comments on tracked PRs and companion Issues."""
    print("=== Recent Comments on @nertwork Upstream PRs & Companion Issues ===")
    for it in TRACKED_CONTRIBUTIONS:
        repo = it["repo"]
        if repo_filter and repo_filter.lower() not in repo.lower():
            continue
        pr_num = it["pr"]
        iss_num = it.get("issue")
        for kind, num in [("PR", pr_num)] + ([("Issue", iss_num)] if iss_num else []):
            comments = _gh_get(f"https://api.github.com/repos/{repo}/issues/{num}/comments?per_page=5", token)
            if isinstance(comments, list) and comments:
                for c in comments[-3:]:
                    user = (c.get("user") or {}).get("login", "unknown")
                    dt = str(c.get("created_at") or "")[:16].replace("T", " ")
                    body = " ".join(str(c.get("body") or "").strip().splitlines())[:220]
                    print(f"[{repo} {kind} #{num}] @{user} ({dt}): {body}")


def add_tracked_contribution(
    repo: str,
    pr_num: int,
    issue_num: int | None,
    category: str,
    component: str,
    summary: str,
    link_issue: bool,
    token: str,
) -> dict[str, Any]:
    """Add or update an entry in TRACKED_CONTRIBUTIONS in this script file (and mirror copies)."""
    pr_data = _gh_get(f"https://api.github.com/repos/{repo}/pulls/{pr_num}", token)
    if not summary:
        summary = str(pr_data.get("title") or f"Upstream contribution to {repo}#{pr_num}").strip()
    if not component:
        component = repo.split("/")[-1]

    if link_issue and issue_num and token:
        body = str(pr_data.get("body") or "")
        if f"#{issue_num}" not in body:
            new_body = f"Fixes #{issue_num}\n\n{body}".strip()
            _gh_request(
                f"https://api.github.com/repos/{repo}/pulls/{pr_num}",
                token,
                method="PATCH",
                payload={"body": new_body},
            )

    # Update in-memory list
    updated_existing = False
    for item in TRACKED_CONTRIBUTIONS:
        if item["repo"].lower() == repo.lower() and int(item["pr"]) == int(pr_num):
            item["issue"] = issue_num
            item["category"] = category
            item["component"] = component
            item["summary"] = summary
            updated_existing = True
            break
    if not updated_existing:
        TRACKED_CONTRIBUTIONS.append(
            {
                "category": category,
                "repo": repo,
                "pr": int(pr_num),
                "issue": int(issue_num) if issue_num else None,
                "component": component,
                "summary": summary,
            }
        )

    # Persist into canonical script files so update_readme.py stays 100% self-contained
    formatted_items = ["TRACKED_CONTRIBUTIONS: list[dict[str, Any]] = ["]
    for it in TRACKED_CONTRIBUTIONS:
        formatted_items.append("    {")
        formatted_items.append(f'        "category": {json.dumps(it["category"])},')
        formatted_items.append(f'        "repo": {json.dumps(it["repo"])},')
        formatted_items.append(f'        "pr": {int(it["pr"])},')
        formatted_items.append(f'        "issue": {json.dumps(it.get("issue"))},')
        formatted_items.append(f'        "component": {json.dumps(it["component"])},')
        formatted_items.append(f'        "summary": {json.dumps(it["summary"])},')
        if it.get("manual_merge_note"):
            formatted_items.append(f'        "manual_merge_note": {json.dumps(it["manual_merge_note"])},')
        formatted_items.append("    },")
    formatted_items.append("]")
    new_block = "# BEGIN_TRACKED_CONTRIBUTIONS\n" + "\n".join(formatted_items) + "\n# END_TRACKED_CONTRIBUTIONS"

    target_paths = [
        Path("/home/jfarr/projects/nertwork-ai-ops/tools/github/sync_github_profile.py"),
        Path("/home/jfarr/projects/nertwork-ai-ops/ops/registry/skills/github-oss/scripts/oss_cli.py"),
        Path("/home/jfarr/projects/nertwork-ai-registry/skills/github-oss/scripts/oss_cli.py"),
    ]
    for p in target_paths:
        if p.exists() and not p.is_symlink():
            src = p.read_text(encoding="utf-8")
            updated_src = re.sub(
                r"# BEGIN_TRACKED_CONTRIBUTIONS.*?# END_TRACKED_CONTRIBUTIONS",
                new_block,
                src,
                flags=re.DOTALL,
            )
            p.write_text(updated_src, encoding="utf-8")

    return {
        "action": "updated" if updated_existing else "added",
        "repo": repo,
        "pr": pr_num,
        "issue": issue_num,
        "category": category,
    }


def inspect_pr(repo: str, pr_num: int, token: str) -> None:
    """Inspect a specific upstream PR's state, check-runs, reviews, and inline comments."""
    pr = _gh_get(f"https://api.github.com/repos/{repo}/pulls/{pr_num}", token)
    head_sha = (pr.get("head") or {}).get("sha", "")
    mergeable = pr.get("mergeable")
    m_state = pr.get("mergeable_state")
    if m_state == "unstable" and mergeable is True:
        m_state = "clean (awaiting maintainer CI)"
    print(f"=== {repo}#{pr_num}: {pr.get('title')} ===")
    print(f"State: {pr.get('state')} | Merged: {pr.get('merged')} | Mergeable: {mergeable} ({m_state}) | Head: {head_sha[:7]}")
    if head_sha:
        checks = _gh_get(f"https://api.github.com/repos/{repo}/commits/{head_sha}/check-runs", token)
        runs = checks.get("check_runs", []) if isinstance(checks, dict) else []
        if runs:
            print("Check Runs:")
            for r in runs:
                print(f"  • {r.get('name')}: status={r.get('status')} conclusion={r.get('conclusion')}")
    reviews = _gh_get(f"https://api.github.com/repos/{repo}/pulls/{pr_num}/reviews", token)
    if isinstance(reviews, list) and reviews:
        print("Reviews:")
        for rv in reviews:
            u = (rv.get("user") or {}).get("login")
            st = rv.get("state")
            sub = str(rv.get("submitted_at") or "")[:19]
            print(f"  • [{sub}] @{u} ({st})")
    inline = _gh_get(f"https://api.github.com/repos/{repo}/pulls/{pr_num}/comments", token)
    if isinstance(inline, list) and inline:
        print("Inline Review Comments:")
        for ic in inline:
            u = (ic.get("user") or {}).get("login")
            sub = str(ic.get("created_at") or "")[:19]
            body = " ".join(str(ic.get("body") or "").split())[:180]
            print(f"  • [{sub}] @{u} ({ic.get('path')}:{ic.get('line')}): {body}")
    comments = _gh_get(f"https://api.github.com/repos/{repo}/issues/{pr_num}/comments", token)
    if isinstance(comments, list) and comments:
        print("Issue Comments:")
        for c in comments:
            u = (c.get("user") or {}).get("login")
            sub = str(c.get("created_at") or "")[:19]
            body = " ".join(str(c.get("body") or "").split())[:180]
            print(f"  • [{sub}] @{u}: {body}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Nertwork GitHub Open Source Attribution & Profile Sync CLI (github-oss)."
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="summary",
        choices=["summary", "prs", "issues", "comments", "inspect", "sync", "add", "ha-patches"],
        help="Subcommand to execute (default: summary)",
    )
    parser.add_argument("--output", help="Write generated README.md to this file path without pushing")
    parser.add_argument("--json", action="store_true", help="Output structured JSON")
    parser.add_argument("--push", action="store_true", help="Push updated README and workflow to nertwork/nertwork")
    parser.add_argument("--state", default="all", choices=["all", "open", "merged"], help="Filter PRs by state")
    parser.add_argument(
        "--category",
        default="all",
        choices=["all", "smarthome", "omarchy", "infra"],
        help="Filter or assign category (smarthome, omarchy, infra)",
    )
    parser.add_argument("--repo", help="Upstream owner/repo for `add` (e.g. alandtse/tesla)")
    parser.add_argument("--pr", type=int, help="Upstream PR number for `add`")
    parser.add_argument("--issue", type=int, help="Companion Issue number for `add`")
    parser.add_argument("--component", default="", help="Component display name for `add`")
    parser.add_argument("--summary", default="", help="Technical summary for `add`")
    parser.add_argument(
        "--link-issue",
        action="store_true",
        help="When running `add`, also prepend `Fixes #<issue>` to the upstream PR body",
    )
    args = parser.parse_args()

    token = _get_github_token()

    # Backwards-compatible flags (`--output` or `--push` without explicit subcommand)
    if args.output or (args.push and args.command == "summary"):
        args.command = "sync"

    if args.command == "ha-patches":
        checker = Path("/home/jfarr/projects/nertwork-ai-ops/ops/smarthome/tools/check_upstream_fixes.py")
        cmd = [sys.executable, str(checker)]
        if args.push:
            cmd.append("--sync-profile")
        if args.json:
            cmd.append("--json")
        return subprocess.run(cmd, check=False).returncode

    if args.command == "issues":
        print_detailed_issues(token)
        return 0

    if args.command == "inspect":
        if not args.repo or not args.pr:
            parser.error("`inspect` requires `--repo <owner/repo>` and `--pr <number>`")
        inspect_pr(args.repo, args.pr, token)
        return 0

    if args.command == "comments":
        print_recent_comments(token, repo_filter=args.repo or "")
        return 0

    if args.command == "add":
        if not args.repo or not args.pr:
            parser.error("`add` requires `--repo <owner/repo>` and `--pr <number>`")
        cat = args.category if args.category != "all" else "smarthome"
        res = add_tracked_contribution(
            repo=args.repo,
            pr_num=args.pr,
            issue_num=args.issue,
            category=cat,
            component=args.component,
            summary=args.summary,
            link_issue=args.link_issue,
            token=token,
        )
        print(f"Registered contribution: {json.dumps(res)}")
        if not args.push:
            return 0
        args.command = "sync"

    data = fetch_live_contributions(token)

    if args.command == "summary":
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print_compact_summary(data)
        return 0

    if args.command == "prs":
        if args.json:
            print(json.dumps(data["items"], indent=2))
        else:
            print_detailed_prs(data, state_filter=args.state, cat_filter=args.category)
        return 0

    # args.command == "sync"
    readme_md = render_readme(data)
    if args.output:
        Path(args.output).write_text(readme_md, encoding="utf-8")

    push_result = None
    if args.push or not args.output:
        self_src = Path(__file__).read_text(encoding="utf-8")
        push_result = sync_to_github_repo(readme_md, self_src, token)

    if args.json:
        print(json.dumps({"data": data, "push": push_result}, indent=2))
    elif not args.output:
        print(
            f"Synced @nertwork GitHub Profile ({data['totals']['tracked_merged']} merged / "
            f"{data['totals']['tracked_open']} open tracked upstream PRs, "
            f"{data['totals']['total_prs']} total PRs, {data['totals']['total_issues']} total issues)."
        )
        if push_result:
            print(f"Profile Repo Status: {push_result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
