# Cindergrace NetMan User Guide

## Overview

Cindergrace NetMan is a Linux tool for limiting download bandwidth.
Limits are applied with `tc` and an IFB device (`ifb0`).

## Quick Start (UI)

1) Start the project:
```bash
./start.sh
```
2) Open the UI:
- Default: `http://127.0.0.1:7863`

<!-- Screenshot: UI home (status + limit controls) -->

Note: Setting limits requires root privileges.

## UI Usage

The UI provides three main areas:
- Status (current limit, interface, DSL speed)
- Apply/remove limit
- Tests (ping and download)

<!-- Screenshot: UI "Apply limit" section -->
<!-- Screenshot: UI "Tests" section (ping/download) -->
<!-- Screenshot: UI settings (language, autostart, port) -->

In settings, you can set the server port permanently. The new port is saved and
used the next time the UI starts.

## System Tray

The tray mode offers a quick toggle and a shortcut to the UI.

```bash
cindergrace-netman tray
```

<!-- Screenshot: System tray icon (active/inactive) -->
<!-- Screenshot: Tray context menu -->

## Command Line (CLI)

```bash
# Start the UI
cindergrace-netman ui

# Apply limit (root required)
sudo cindergrace-netman limit --percent 60 --base-mbit 100

# Clear limit
sudo cindergrace-netman clear

# Show status
cindergrace-netman status

# Ping test
cindergrace-netman ping --host 8.8.8.8 --count 4 --interval 0.2

# Download test (max data in MB)
cindergrace-netman download --url https://ash-speed.hetzner.com/100MB.bin --max-mb 10
```

## Configuration and State

Settings are stored in:
- `~/.config/cindergrace_netman/state.json`

Key fields:
- `enabled`: limit on/off
- `percent`: percentage of base speed
- `base_mbit`: DSL/fiber speed
- `iface`: network interface
- `download_url`, `ping_host`
- `language` (en/de), `autostart`, `port`

Optional port override:
- `NETMAN_PORT` (default: 7863)

The port set in the UI overrides the default and is stored in the state file.

## Security Notes

- Applying limits requires root privileges.
- Exposing the UI externally is risky (no authentication).
- Download tests only allow `http://` and `https://` URLs.

## Troubleshooting

If no interfaces appear:
- Ensure `ip` and `tc` are installed.
- Run the UI/CLI with sufficient privileges.

If the limit does not apply:
- Verify the selected interface.
- Check with `cindergrace-netman status`.
