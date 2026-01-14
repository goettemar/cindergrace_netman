# Cindergrace NetMan Benutzerhandbuch / User Guide

Dieses Dokument erklaert die Bedienung von Cindergrace NetMan in Deutsch und Englisch.

---

## Deutsch

### Ueberblick

Cindergrace NetMan ist ein Linux-Tool zum Begrenzen der Download-Bandbreite.
Die Limits werden mit `tc` und einem IFB-Device (`ifb0`) umgesetzt.

### Schnellstart (UI)

1) Projekt starten:
```bash
./start.sh
```
2) UI oeffnen:
- Standard: `http://127.0.0.1:7863`

<!-- Screenshot: UI Startseite (Status + Limit-Steuerung) -->

Hinweis: Beim Start der UI werden Root-Rechte benoetigt, wenn ein Limit gesetzt wird.

### UI-Bedienung

Die UI bietet drei zentrale Bereiche:
- Status (aktuelles Limit, Interface, DSL-Geschwindigkeit)
- Limit setzen/entfernen
- Tests (Ping und Download)

<!-- Screenshot: UI Bereich "Limit setzen" -->
<!-- Screenshot: UI Bereich "Tests" (Ping/Download) -->
<!-- Screenshot: UI Einstellungen (Sprache, Autostart, Port) -->

### System Tray

Der Tray-Modus bietet einen schnellen Toggle fuer das Limit und einen Shortcut zur UI.

```bash
cindergrace-netman tray
```

<!-- Screenshot: System Tray Icon (aktiv/inaktiv) -->
<!-- Screenshot: Tray Kontextmenue -->

### Kommandozeile (CLI)

```bash
# UI starten
cindergrace-netman ui

# Limit setzen (Root erforderlich)
sudo cindergrace-netman limit --percent 60 --base-mbit 100

# Limit entfernen
sudo cindergrace-netman clear

# Status anzeigen
cindergrace-netman status

# Ping-Test
cindergrace-netman ping --host 8.8.8.8 --count 4 --interval 0.2

# Download-Test (maximale Datenmenge in MB)
cindergrace-netman download --url https://ash-speed.hetzner.com/100MB.bin --max-mb 10
```

### Konfiguration und State

Die Einstellungen werden in der State-Datei gespeichert:
- `~/.config/cindergrace_netman/state.json`

Wichtige Felder:
- `enabled`: Limit aktiv/inaktiv
- `percent`: Prozent vom Basiswert
- `base_mbit`: DSL/Fiber Geschwindigkeit
- `iface`: Netzwerk-Interface
- `download_url`, `ping_host`
- `language` (en/de), `autostart`, `port`

Optional kann der Port per Umgebungsvariable gesetzt werden:
- `NETMAN_PORT` (Standard: 7863)

### Sicherheitshinweise

- Das Setzen von Limits erfordert Root-Rechte.
- Externe UI-Freigabe ist riskant, da keine Authentisierung aktiv ist.
- Der Download-Test akzeptiert nur `http://` und `https://` URLs.

### Troubleshooting

Wenn keine Interfaces angezeigt werden:
- Pruefe, ob `ip` und `tc` installiert sind.
- Starte die UI/CLI mit ausreichenden Rechten.

Wenn das Limit nicht wirkt:
- Pruefe die Interface-Auswahl.
- Teste mit `cindergrace-netman status`.

---

## English

### Overview

Cindergrace NetMan is a Linux tool for limiting download bandwidth.
Limits are applied with `tc` and an IFB device (`ifb0`).

### Quick Start (UI)

1) Start the project:
```bash
./start.sh
```
2) Open the UI:
- Default: `http://127.0.0.1:7863`

<!-- Screenshot: UI home (status + limit controls) -->

Note: Setting limits requires root privileges.

### UI Usage

The UI provides three main areas:
- Status (current limit, interface, DSL speed)
- Apply/remove limit
- Tests (ping and download)

<!-- Screenshot: UI "Apply limit" section -->
<!-- Screenshot: UI "Tests" section (ping/download) -->
<!-- Screenshot: UI settings (language, autostart, port) -->

### System Tray

The tray mode offers a quick toggle and a shortcut to the UI.

```bash
cindergrace-netman tray
```

<!-- Screenshot: System tray icon (active/inactive) -->
<!-- Screenshot: Tray context menu -->

### Command Line (CLI)

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

### Configuration and State

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

### Security Notes

- Applying limits requires root privileges.
- Exposing the UI externally is risky (no authentication).
- Download tests only allow `http://` and `https://` URLs.

### Troubleshooting

If no interfaces appear:
- Ensure `ip` and `tc` are installed.
- Run the UI/CLI with sufficient privileges.

If the limit does not apply:
- Verify the selected interface.
- Check with `cindergrace-netman status`.
