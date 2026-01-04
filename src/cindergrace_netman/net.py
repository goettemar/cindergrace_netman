import re
import subprocess


IFB_DEVICE = "ifb0"


class NetmanError(RuntimeError):
    pass


def _run(cmd: list[str]) -> str:
    try:
        completed = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        raise NetmanError(stderr or "Command failed") from exc
    return completed.stdout.strip()

def _run_ignore(cmd: list[str]) -> None:
    try:
        _run(cmd)
    except NetmanError:
        return


def list_interfaces() -> list[str]:
    output = _run(["ip", "-o", "link", "show"])
    interfaces: list[str] = []
    for line in output.splitlines():
        parts = line.split(": ", 2)
        if len(parts) < 2:
            continue
        name = parts[1].split("@", 1)[0].strip()
        if name:
            interfaces.append(name)
    return interfaces


def get_default_interface() -> str | None:
    output = _run(["ip", "route", "show", "default"])
    for line in output.splitlines():
        match = re.search(r"\bdev\s+(\S+)", line)
        if match:
            return match.group(1)
    return None


def get_interface_speed(iface: str) -> int | None:
    """Gibt die Link-Geschwindigkeit in Mbit/s zurueck, oder None wenn nicht verfuegbar."""
    # Methode 1: /sys/class/net/<iface>/speed
    speed_file = f"/sys/class/net/{iface}/speed"
    try:
        with open(speed_file) as f:
            speed = int(f.read().strip())
            if speed > 0:
                return speed
    except (FileNotFoundError, ValueError, PermissionError, OSError):
        # OSError kann bei virtuellen Interfaces auftreten
        pass

    # Methode 2: ethtool (falls verfuegbar)
    try:
        output = _run(["ethtool", iface])
        for line in output.splitlines():
            if "Speed:" in line:
                match = re.search(r"(\d+)\s*Mb", line)
                if match:
                    return int(match.group(1))
    except NetmanError:
        pass

    return None


def get_interface_state(iface: str) -> str:
    """Gibt den Verbindungsstatus zurueck: up, down, oder unknown."""
    state_file = f"/sys/class/net/{iface}/operstate"
    try:
        with open(state_file) as f:
            return f.read().strip()
    except (FileNotFoundError, PermissionError):
        return "unknown"


def list_interfaces_with_info() -> list[dict]:
    """Gibt alle Interfaces mit Speed und Status zurueck."""
    default_iface = get_default_interface()
    interfaces = []

    for iface in list_interfaces():
        # Virtuelle/System-Interfaces ueberspringen
        if iface in ("lo", "ifb0", "ifb1"):
            continue

        speed = get_interface_speed(iface)
        state = get_interface_state(iface)
        is_default = iface == default_iface

        interfaces.append({
            "name": iface,
            "speed_mbit": speed,
            "state": state,
            "is_default": is_default,
        })

    return interfaces


def _setup_ifb() -> None:
    _run_ignore(["modprobe", "ifb", "numifbs=1"])
    _run_ignore(["ip", "link", "add", IFB_DEVICE, "type", "ifb"])
    _run(["ip", "link", "set", "dev", IFB_DEVICE, "up"])


def apply_limit(iface: str, rate_mbit: float) -> None:
    if rate_mbit <= 0:
        raise NetmanError("Rate must be > 0")
    _setup_ifb()
    rate_text = f"{rate_mbit:.2f}".rstrip("0").rstrip(".")
    _run(["tc", "qdisc", "replace", "dev", iface, "handle", "ffff:", "ingress"])
    _run_ignore(["tc", "filter", "del", "dev", iface, "parent", "ffff:"])
    _run(
        [
            "tc",
            "filter",
            "add",
            "dev",
            iface,
            "parent",
            "ffff:",
            "protocol",
            "ip",
            "u32",
            "match",
            "u32",
            "0",
            "0",
            "action",
            "mirred",
            "egress",
            "redirect",
            "dev",
            IFB_DEVICE,
        ]
    )
    _run(
        [
            "tc",
            "qdisc",
            "replace",
            "dev",
            IFB_DEVICE,
            "root",
            "tbf",
            "rate",
            f"{rate_text}mbit",
            "burst",
            "64kb",
            "latency",
            "400ms",
        ]
    )


def clear_limit(iface: str) -> None:
    _run_ignore(["tc", "qdisc", "del", "dev", IFB_DEVICE, "root"])
    _run_ignore(["tc", "filter", "del", "dev", iface, "parent", "ffff:"])
    _run_ignore(["tc", "qdisc", "del", "dev", iface, "ingress"])
    _run_ignore(["ip", "link", "set", "dev", IFB_DEVICE, "down"])
    _run_ignore(["ip", "link", "delete", IFB_DEVICE, "type", "ifb"])
