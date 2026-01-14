# Cindergrace NetMan Benutzerhandbuch

## Ueberblick

Cindergrace NetMan ist ein Linux-Tool zum Begrenzen der Download-Bandbreite.
Die Limits werden mit `tc` und einem IFB-Device (`ifb0`) umgesetzt.

## Schnellstart (UI)

1) Projekt starten:
```bash
./start.sh
```
2) UI oeffnen:
- Standard: `http://127.0.0.1:7863`

<!-- Screenshot: UI Startseite (Status + Limit-Steuerung) -->

Hinweis: Beim Start der UI werden Root-Rechte benoetigt, wenn ein Limit gesetzt wird.

## UI-Bedienung

Die UI bietet drei zentrale Bereiche:
- Status (aktuelles Limit, Interface, DSL-Geschwindigkeit)
- Limit setzen/entfernen
- Tests (Ping und Download)

<!-- Screenshot: UI Bereich "Limit setzen" -->
<!-- Screenshot: UI Bereich "Tests" (Ping/Download) -->
<!-- Screenshot: UI Einstellungen (Sprache, Autostart, Port) -->

In den Einstellungen kann der Server-Port dauerhaft gesetzt werden. Der neue Port
wird gespeichert und beim naechsten Start der UI verwendet.

## System Tray

Der Tray-Modus bietet einen schnellen Toggle fuer das Limit und einen Shortcut zur UI.

```bash
cindergrace-netman tray
```

<!-- Screenshot: System Tray Icon (aktiv/inaktiv) -->
<!-- Screenshot: Tray Kontextmenue -->

## Kommandozeile (CLI)

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

## Konfiguration und State

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

Der ueber die UI gesetzte Port hat Vorrang vor dem Standardwert und wird in der
State-Datei gespeichert.

## Sicherheitshinweise

- Das Setzen von Limits erfordert Root-Rechte.
- Externe UI-Freigabe ist riskant, da keine Authentisierung aktiv ist.
- Der Download-Test akzeptiert nur `http://` und `https://` URLs.

## Troubleshooting

Wenn keine Interfaces angezeigt werden:
- Pruefe, ob `ip` und `tc` installiert sind.
- Starte die UI/CLI mit ausreichenden Rechten.

Wenn das Limit nicht wirkt:
- Pruefe die Interface-Auswahl.
- Teste mit `cindergrace-netman status`.
