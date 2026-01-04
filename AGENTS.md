# Repository Guidelines

## Project Structure & Module Organization
- Source code lives in `src/cindergrace_netman/` (package entry, CLI, UI, network helpers).
- Tests live in `tests/` and follow `test_*.py` naming.
- Top-level docs are in `README.md` and `CHANGELOG.md`.
- Runtime state is stored under `~/.config/cindergrace_netman/state.json` (created automatically).

## Build, Test, and Development Commands
- `python -m venv .venv` creates a local virtualenv.
- `source .venv/bin/activate` activates it.
- `python -m pip install -e ".[dev]"` installs editable deps plus dev tools.
- `pytest` runs the test suite from `tests/`.
- `cindergrace-netman ui` starts the Gradio UI.
- `sudo cindergrace-netman limit --percent 60 --base-mbit 100` applies a download cap using `tc`.
- `cindergrace-netman tray` starts the system tray toggle.
- `./start.sh` bootstraps `.venv`, installs deps, and launches the UI.

## Coding Style & Naming Conventions
- Python 3.10+ only; keep code ASCII unless the file already uses Unicode.
- Follow Ruff defaults defined in `pyproject.toml` (line length 100).
- Modules use `snake_case.py`; functions/vars `snake_case`; classes `PascalCase`.
- Prefer small, focused modules; add brief comments only when logic is non-obvious.

## Testing Guidelines
- Framework: `pytest` (configured in `pyproject.toml`).
- Test files: `tests/test_*.py`; test functions: `test_*`.
- Add tests for new network helpers and CLI parsing where practical.

## Commit & Pull Request Guidelines
- Current history has a single “Initial commit”; no established commit message convention.
- Use clear, imperative commit messages (e.g., “Add tray tooltip refresh”).
- PRs should describe behavior changes, mention OS assumptions (Linux/`tc`), and include screenshots for UI changes.

## Security & Configuration Tips
- Download limiting uses `tc` + IFB and requires root privileges.
- Avoid storing secrets in the repo; configuration belongs in user config files or environment variables.

## KI-CLI Workspace Integration

Dieses Projekt ist Teil des zentralen KI-Workspaces. Nutze diese Befehle:

```bash
# FAQ für schnellen Kontext (Token-sparend!)
ki-workspace faq --json

# Projekt-Status und Issues
ki-workspace status cindergrace_netman
ki-workspace issues cindergrace_netman --json
ki-workspace sync cindergrace_netman      # Von Codacy holen

# Issue-Review Workflow
ki-workspace faq issue_review_workflow    # Workflow lesen
ki-workspace recommend-ignore <ID> -c <CATEGORY> -r "Grund" --reviewer codex
```

**Kategorien:** `accepted_use`, `false_positive`, `not_exploitable`, `test_code`, `external_code`

**Wichtig:** Wenn `ki_recommendation` bereits gesetzt → Issue NICHT erneut bewerten!
