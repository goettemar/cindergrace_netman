# cindergrace_netman

Netzwerk-Management Tool mit Bandwidth-Limiting, Ping und Speed-Tests.

## Workspace-Integration

Dieses Projekt ist Teil des KI-CLI Workspace. Wichtige Befehle:

```bash
# FAQ für schnellen Kontext (Token-sparend!)
ki-workspace faq --json

# Projekt-Status
ki-workspace status cindergrace_netman

# Issues von Codacy holen
ki-workspace sync cindergrace_netman

# Issues anzeigen
ki-workspace issues cindergrace_netman --json

# Release-Readiness prüfen
ki-workspace check cindergrace_netman
```

## Issue-Review Workflow

1. `ki-workspace faq issue_review_workflow` lesen
2. Issues mit `--json` laden
3. Wenn `ki_recommendation` gesetzt: SKIP (bereits bewertet)
4. Code prüfen, dann: `ki-workspace recommend-ignore <ID> -c <CATEGORY> -r "Grund" --reviewer codex`

## Architektur

```
src/cindergrace_netman/
├── cli.py           # argparse CLI Entry-Point
├── net.py           # Linux TC (qdisc) for bandwidth limiting
├── checks.py        # Ping + download speedtest
├── ui.py            # Gradio Web-UI with i18n
├── tray.py          # System tray icon
├── state.py         # XDG-compliant persistence
└── translations/
    └── ui.yaml      # UI translations (en/de)
```

## i18n

UI is multilingual (English/German), auto-detected from browser.

```python
from gradio_i18n import Translate, gettext as _

with Translate("translations/ui.yaml", placeholder_langs=["en", "de"]) as lang:
    gr.Button(_("apply"))  # -> "Apply" or "Uebernehmen"
```

Translation keys in `translations/ui.yaml`.

## Hinweise

- Braucht root für `tc`-Befehle
- State in `~/.config/cindergrace_netman/state.json`
- Gradio UI auf Port 7863 (siehe cindergrace_projects/gradio_ports.json)
