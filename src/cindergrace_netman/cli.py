import argparse

from .checks import download_test, ping
from .net import NetmanError, apply_limit, clear_limit, get_default_interface
from .state import load_state, save_state
from .tray import run_tray
from .ui import build_app


def _resolve_iface(iface: str | None) -> str:
    if iface:
        return iface
    detected = get_default_interface()
    if not detected:
        raise NetmanError("Kein Default-Interface gefunden")
    return detected


def _cmd_ui(args: argparse.Namespace) -> None:
    app = build_app()
    app.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
    )


def _cmd_limit(args: argparse.Namespace) -> None:
    iface = _resolve_iface(args.iface)
    rate = args.base_mbit * args.percent / 100
    apply_limit(iface, rate)
    state = load_state()
    state.update(
        {
            "enabled": True,
            "percent": args.percent,
            "base_mbit": args.base_mbit,
            "iface": iface,
        }
    )
    save_state(state)
    print(f"Limit aktiv: {args.percent}% ({rate:.2f} Mbit/s) auf {iface}")


def _cmd_clear(args: argparse.Namespace) -> None:
    iface = _resolve_iface(args.iface)
    clear_limit(iface)
    state = load_state()
    state["enabled"] = False
    state["iface"] = iface
    save_state(state)
    print(f"Limit deaktiviert auf {iface}")


def _cmd_status(_args: argparse.Namespace) -> None:
    state = load_state()
    iface = state["iface"] or get_default_interface() or "?"
    rate = state["base_mbit"] * state["percent"] / 100
    status = "aktiv" if state["enabled"] else "aus"
    print(f"Status: {status}")
    print(f"Interface: {iface}")
    print(f"Limit: {state['percent']}% von {state['base_mbit']} Mbit/s = {rate:.2f} Mbit/s")


def _cmd_ping(args: argparse.Namespace) -> None:
    result = ping(args.host, count=args.count, interval=args.interval)
    print(result)


def _cmd_download(args: argparse.Namespace) -> None:
    result = download_test(args.url, max_mb=args.max_mb)
    print(result)


def _cmd_tray(_args: argparse.Namespace) -> None:
    run_tray()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cindergrace-netman")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ui_parser = subparsers.add_parser("ui", help="Gradio UI starten")
    ui_parser.add_argument("--host", default="127.0.0.1")
    ui_parser.add_argument("--port", type=int, default=7863)  # Siehe gradio_ports.json
    ui_parser.add_argument("--share", action="store_true")
    ui_parser.set_defaults(func=_cmd_ui)

    limit_parser = subparsers.add_parser("limit", help="Download-Limit setzen")
    limit_parser.add_argument("--percent", type=int, default=100)
    limit_parser.add_argument("--base-mbit", type=int, default=100)
    limit_parser.add_argument("--iface")
    limit_parser.set_defaults(func=_cmd_limit)

    clear_parser = subparsers.add_parser("clear", help="Download-Limit entfernen")
    clear_parser.add_argument("--iface")
    clear_parser.set_defaults(func=_cmd_clear)

    status_parser = subparsers.add_parser("status", help="Aktuellen Status anzeigen")
    status_parser.set_defaults(func=_cmd_status)

    ping_parser = subparsers.add_parser("ping", help="Ping-Test ausfuehren")
    ping_parser.add_argument("--host", default="8.8.8.8")
    ping_parser.add_argument("--count", type=int, default=4)
    ping_parser.add_argument("--interval", type=float, default=0.2)
    ping_parser.set_defaults(func=_cmd_ping)

    download_parser = subparsers.add_parser("download", help="Download-Test ausfuehren")
    download_parser.add_argument("--url", default="https://speed.hetzner.de/10MB.bin")
    download_parser.add_argument("--max-mb", type=int, default=10)
    download_parser.set_defaults(func=_cmd_download)

    tray_parser = subparsers.add_parser("tray", help="Tray-Icon starten")
    tray_parser.set_defaults(func=_cmd_tray)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except NetmanError as exc:
        raise SystemExit(f"Fehler: {exc}") from exc


if __name__ == "__main__":
    main()
