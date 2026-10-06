"""Sistem bilgisi toplayicilar (sadece standart kutuphane)."""
import glob
import os
import platform
import re
import shutil
import socket
import subprocess
from functools import lru_cache

_prev_cpu = None


def _read(path, default=""):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return default


def _gib(kib):
    return kib / 1024 / 1024


def os_name():
    m = re.search(r'^PRETTY_NAME="?([^"\n]+)', _read("/etc/os-release"), re.M)
    return m.group(1) if m else platform.system()


def uptime():
    try:
        s = int(float(_read("/proc/uptime").split()[0]))
    except (IndexError, ValueError):
        return "?"
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m = s // 60
    return " ".join(p for p in (f"{d}g" if d else "", f"{h}s" if h else "", f"{m}dk") if p)


@lru_cache(maxsize=1)
def packages():
    parts = []
    try:
        n = len(os.listdir("/var/lib/pacman/local")) - 1
        if n > 0:
            parts.append(f"{n} (pacman)")
    except OSError:
        pass
    try:
        out = subprocess.run(["flatpak", "list"], capture_output=True, text=True, timeout=3).stdout
        n = len([l for l in out.splitlines() if l.strip()])
        if n:
            parts.append(f"{n} (flatpak)")
    except (OSError, subprocess.SubprocessError):
        pass
    return ", ".join(parts) or "?"


def shell():
    return os.path.basename(os.environ.get("SHELL", "?"))


def desktop():
    de = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or "?"
    st = os.environ.get("XDG_SESSION_TYPE", "")
    return f"{de} ({st})" if st and de != "?" else de


def terminal():
    for var, name in (("KITTY_WINDOW_ID", "kitty"), ("ALACRITTY_SOCKET", "alacritty"),
                      ("WEZTERM_EXECUTABLE", "wezterm"), ("GHOSTTY_RESOURCES_DIR", "ghostty")):
        if os.environ.get(var):
            return name
    return os.environ.get("TERM_PROGRAM") or os.environ.get("TERM", "?")


@lru_cache(maxsize=1)
def cpu_model():
    m = re.search(r"model name\s*:\s*(.+)", _read("/proc/cpuinfo"))
    name = m.group(1) if m else platform.processor() or "?"
    name = re.sub(r"\((R|TM)\)|CPU|\d+-Core Processor|@.*", "", name)
    return f"{' '.join(name.split())} ({os.cpu_count()})"


@lru_cache(maxsize=1)
def gpu():
    try:
        out = subprocess.run(["lspci", "-mm"], capture_output=True, text=True, timeout=3).stdout
    except (OSError, subprocess.SubprocessError):
        return "?"
    for line in out.splitlines():
        if re.search(r"VGA|3D|Display", line):
            q = re.findall(r'"([^"]*)"', line)
            if len(q) >= 3:
                dev = re.search(r"\[(.+?)\]", q[2])
                return (dev.group(1) if dev else q[2])[:42]
    return "?"


def _cpu_times():
    f = _read("/proc/stat").splitlines()[0].split()[1:]
    v = list(map(int, f))
    return sum(v), v[3] + (v[4] if len(v) > 4 else 0)


def cpu_percent():
    global _prev_cpu
    import time
    if _prev_cpu is None:
        _prev_cpu = _cpu_times()
        time.sleep(0.12)
    t, i = _cpu_times()
    pt, pi = _prev_cpu
    _prev_cpu = (t, i)
    return 0.0 if t == pt else max(0.0, min(100.0, 100 * (1 - (i - pi) / (t - pt))))


def memory():
    d = {}
    for l in _read("/proc/meminfo").splitlines():
        k, _, v = l.partition(":")
        d[k] = int(v.split()[0]) if v.split() else 0
    total = d.get("MemTotal", 1)
    used = total - d.get("MemAvailable", 0)
    return used, total


def disk():
    u = shutil.disk_usage("/")
    return u.used, u.total


def battery():
    for p in glob.glob("/sys/class/power_supply/BAT*"):
        cap = _read(p + "/capacity").strip()
        if cap.isdigit():
            return int(cap), _read(p + "/status").strip() or "?"
    return None


def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "?"


def collect():
    mu, mt = memory()
    du, dt = disk()
    return {
        "user": os.environ.get("USER", "user"),
        "host": socket.gethostname(),
        "os": os_name(),
        "kernel": platform.release(),
        "uptime": uptime(),
        "packages": packages(),
        "shell": shell(),
        "desktop": desktop(),
        "terminal": terminal(),
        "cpu": cpu_model(),
        "gpu": gpu(),
        "memory": f"{_gib(mu):.1f} / {_gib(mt):.1f} GiB",
        "disk": f"{du / 1024**3:.0f} / {dt / 1024**3:.0f} GiB",
        "ip": local_ip(),
        "battery": battery(),
        "cpu_pct": cpu_percent(),
        "mem_pct": 100 * mu / mt,
        "disk_pct": 100 * du / dt,
    }
