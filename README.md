# cindergrace_netman

> Hinweis: Dieses Repository ist ein Hobby-/Experimentierprojekt. Es handelt sich nicht um ein gewerbliches Angebot (keine Auftragsannahme, keine Garantien, kein Supportversprechen).

![Status](https://img.shields.io/badge/Status-Alpha-red)

> ⚠️ **Alpha** - In aktiver Entwicklung, nicht für Produktion geeignet.

Netzwerk-Management Tool

## Installation

```bash
pip install cindergrace-netman
```

## Verwendung

```bash
# Gradio UI starten
cindergrace-netman ui

# Download-Limit auf 60% einer 100 Mbit Leitung setzen
sudo cindergrace-netman limit --percent 60 --base-mbit 100

# Limit entfernen
sudo cindergrace-netman clear

# Tray-Icon starten
cindergrace-netman tray
```

> Hinweis: Das Setzen von Limits via `tc` erfordert Root-Rechte.
> Fuer Download-Limits wird ein IFB-Device (`ifb0`) erstellt.

## Entwicklung

```bash
# Repository klonen
git clone https://github.com/goettemar/cindergrace_netman.git
cd cindergrace_netman

# Virtual Environment erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -e ".[dev]"
```

## Lizenz

Dieses Projekt steht unter der [PolyForm Noncommercial License 1.0.0](LICENSE).

---

Erstellt am 2026-01-03 | [goettemar](https://github.com/goettemar)
