"""Gradient, kutu ve logo cizimi."""
import re
import shutil

from .themes import LOGO

RESET = "\x1b[0m"
DIM = (88, 88, 110)
_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")

ICONS = {
    "os": "\uf303", "kernel": "\uf17c", "uptime": "\uf017", "packages": "\uf487",
    "shell": "\uf120", "desktop": "\uf108", "terminal": "\uf489", "cpu": "\uf2db",
    "gpu": "\uf26c", "memory": "\uf538", "disk": "\uf0a0", "ip": "\uf1eb", "battery": "\uf240",
}


def fg(c):
    return f"\x1b[38;2;{int(c[0])};{int(c[1])};{int(c[2])}m"


def vlen(s):
    return len(_ANSI.sub("", s))


def grad(stops, t):
    """Dongusel gradient: t herhangi bir float olabilir."""
    pts = list(stops) + [stops[0]]
    t = (t % 1.0) * (len(pts) - 1)
    i = min(int(t), len(pts) - 2)
    f = t - i
    a, b = pts[i], pts[i + 1]
    return tuple(a[k] + (b[k] - a[k]) * f for k in range(3))


def gradtext(text, stops, phase=0.0, span=None):
    span = span or max(len(text), 1)
    return "".join(fg(grad(stops, i / span + phase)) + ch for i, ch in enumerate(text)) + RESET


def bar(pct, width=22):
    filled = round(pct / 100 * width)
    ramp = [(80, 250, 123), (241, 250, 140), (255, 85, 85)]
    out = ""
    for i in range(width):
        if i < filled:
            t = i / max(width - 1, 1)
            seg = min(int(t * 2), 1)
            a, b, f = ramp[seg], ramp[seg + 1], t * 2 - seg
            out += fg([a[k] + (b[k] - a[k]) * f for k in range(3)]) + "\u2501"
        else:
            out += fg(DIM) + "\u2500"
    return out + RESET


def _rows(info, icons):
    spec = [("os", "OS"), ("kernel", "Kernel"), ("uptime", "Uptime"), ("packages", "Paket"),
            ("shell", "Shell"), ("desktop", "DE/WM"), ("terminal", "Terminal"),
            ("cpu", "CPU"), ("gpu", "GPU"), ("memory", "RAM"), ("disk", "Disk"), ("ip", "IP")]
    rows = [(k, l, info[k]) for k, l in spec if info.get(k) not in (None, "?")]
    if info.get("battery"):
        cap, st = info["battery"]
        rows.append(("battery", "Pil", f"%{cap} ({st})"))
    return rows


def render(info, stops, phase=0.0, icons=True, show_logo=True):
    acc, acc2 = grad(stops, phase), grad(stops, phase + 0.5)
    lines = [gradtext(f"{info['user']}@{info['host']}", stops, phase)]
    lines.append("")  # ayirici sonra doldurulur
    for key, label, val in _rows(info, icons):
        ic = ICONS[key] if icons else "\u25c6"
        lines.append(f"{fg(acc)}{ic}  {label:<9}{RESET}{val}")
    lines.append("")
    for label, key in (("CPU", "cpu_pct"), ("RAM", "mem_pct"), ("DSK", "disk_pct")):
        lines.append(f"{fg(acc2)}{label}{RESET} {bar(info[key])} {info[key]:5.1f}%")
    lines.append("")
    lines.append("".join(fg(grad(stops, i / 10 + phase)) + "\u2588\u2588" for i in range(10)) + RESET)

    w = max(vlen(l) for l in lines)
    lines[1] = gradtext("\u2500" * w, stops, phase)

    title = " archnova "
    top = "\u256d\u2500" + title + "\u2500" * max(0, w + 2 - 2 - len(title)) + "\u256e"
    box = [gradtext(top, stops, phase)]
    h = len(lines) + 2
    for r, l in enumerate(lines):
        c = fg(grad(stops, r / h + phase))
        box.append(f"{c}\u2502{RESET} {l}{' ' * (w - vlen(l))} {c}\u2502{RESET}")
    box.append(gradtext("\u2570" + "\u2500" * (w + 2) + "\u256f", stops, phase))

    logo = LOGO.splitlines()
    lw, bw = max(map(len, logo)), w + 4
    cols = shutil.get_terminal_size((100, 30)).columns
    if not show_logo or lw + 3 + bw > cols:
        return "\n".join(box)

    colored = []
    for r, line in enumerate(logo):
        s = "".join(
            fg(grad(stops, c / lw * 0.6 + r / len(logo) * 0.4 + phase)) + ch if ch != " " else " "
            for c, ch in enumerate(line.ljust(lw))
        )
        colored.append(s + RESET)

    height = max(len(colored), len(box))
    top_l, top_b = (height - len(colored)) // 2, (height - len(box)) // 2
    out = []
    for i in range(height):
        l = colored[i - top_l] if 0 <= i - top_l < len(colored) else " " * lw
        b = box[i - top_b] if 0 <= i - top_b < len(box) else ""
        out.append(f"{l}   {b}")
    return "\n".join(out)
