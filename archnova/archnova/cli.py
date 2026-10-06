import argparse
import json
import os
import random
import sys
import time

from . import __version__, info as sysinfo
from .render import RESET, fg, gradtext, render
from .themes import DEFAULT_THEME, THEMES


def live(stops, icons, logo, speed):
    out = sys.stdout
    out.write("\x1b[?1049h\x1b[?25l")
    try:
        t0, last, data = time.time(), 0, None
        while True:
            now = time.time()
            if data is None or now - last >= 1:
                data, last = sysinfo.collect(), now
            frame = render(data, stops, (now - t0) * speed, icons, logo)
            hint = f"\n\n {fg((88, 88, 110))}Ctrl+C ile cik{RESET}"
            out.write("\x1b[H" + (frame + hint).replace("\n", "\x1b[K\n") + "\x1b[J")
            out.flush()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        out.write("\x1b[?25h\x1b[?1049l")
        out.flush()


def main():
    p = argparse.ArgumentParser(prog="archnova", description="Arch Linux icin goz alici sistem bilgisi araci")
    p.add_argument("-t", "--theme", default=os.environ.get("ARCHNOVA_THEME", DEFAULT_THEME),
                   help="tema adi veya 'random'")
    p.add_argument("-l", "--list-themes", action="store_true", help="temalari goster")
    p.add_argument("-L", "--live", action="store_true", help="canli animasyonlu mod")
    p.add_argument("--speed", type=float, default=0.08, help="canli mod gradient hizi")
    p.add_argument("--no-logo", action="store_true")
    p.add_argument("--no-icons", action="store_true", help="Nerd Font yoksa kullan")
    p.add_argument("--json", action="store_true", help="JSON cikti")
    p.add_argument("-V", "--version", action="version", version=f"archnova {__version__}")
    a = p.parse_args()

    if a.list_themes:
        for name, stops in THEMES.items():
            print(f"  {name:<11} {gradtext('\u2588' * 40, stops)}")
        return
    if a.json:
        d = sysinfo.collect()
        print(json.dumps(d, indent=2, ensure_ascii=False))
        return

    name = random.choice(list(THEMES)) if a.theme == "random" else a.theme
    if name not in THEMES:
        sys.exit(f"Bilinmeyen tema: {name}. 'archnova -l' ile listele.")
    stops, icons, logo = THEMES[name], not a.no_icons, not a.no_logo

    if a.live:
        live(stops, icons, logo, a.speed)
    else:
        print(render(sysinfo.collect(), stops, 0.0, icons, logo))
