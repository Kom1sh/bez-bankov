#!/usr/bin/env python3
"""Собирает SVG-спрайт логотипов из Simple Icons (лицензия CC0) и словарь фирменных цветов.

    python3 src/fetch_icons.py google yandexcloud openai telegram vk

Слуги можно передать аргументами или списком в src/icons.txt (по одному в строке,
пустые строки и решётки игнорируются). Результат: src/sprite.html и src/brands.json.

Чего нет в Simple Icons (проверять заранее): Яндекс, ChatGPT, Bing, Ahrefs, Wildberries,
Ozon, Avito, 2GIS, Дзен, Microsoft. Такие бренды рисуются текстовой плиткой — см. WORD
в make_slides.py.
"""
import json, re, sys, urllib.request, pathlib

HERE = pathlib.Path(__file__).parent
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@latest"

def slugs_from_args():
    if len(sys.argv) > 1:
        return sys.argv[1:]
    f = HERE / "icons.txt"
    if not f.exists():
        raise SystemExit("передайте слуги аргументами или заполните src/icons.txt")
    return [l.strip() for l in f.read_text(encoding="utf-8").split("\n")
            if l.strip() and not l.strip().startswith("#")]

def main():
    slugs = slugs_from_args()
    data = json.loads(urllib.request.urlopen(f"{CDN}/data/simple-icons.json").read().decode())
    icons = data["icons"] if isinstance(data, dict) and "icons" in data else data
    hexmap = {}
    for i in icons:
        s = i.get("slug") or re.sub(r"[^a-z0-9]", "", i["title"].lower())
        hexmap[s] = i["hex"]
    sym, brands, miss = [], {}, []
    for s in slugs:
        try:
            svg = urllib.request.urlopen(f"{CDN}/icons/{s}.svg").read().decode()
        except Exception:
            miss.append(s)
            continue
        d = re.search(r'<path d="([^"]+)"', svg).group(1)
        sym.append(f'<symbol id="i-{s}" viewBox="0 0 24 24"><path d="{d}"/></symbol>')
        brands[s] = "#" + hexmap.get(s, "000000")
    (HERE / "sprite.html").write_text(
        '<svg id="sprite" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden">'
        "<defs>" + "".join(sym) + "</defs></svg>", encoding="utf-8")
    json.dump(brands, open(HERE / "brands.json", "w"), indent=1)
    print(f"иконок: {len(sym)}")
    if miss:
        print("НЕ НАЙДЕНЫ, рисовать текстовой плиткой:", ", ".join(miss))

if __name__ == "__main__":
    main()
