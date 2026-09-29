#!/usr/bin/env python3
"""Качает вариативные шрифты с Google Fonts и вшивает их в src/fonts.css как base64.

    python3 src/fetch_fonts.py "Unbounded:wght@200..900" "Golos Text:wght@400..900" "JetBrains Mono:wght@400..700"

Без аргументов берёт набор по умолчанию. Диапазон весов через две точки обязателен:
на список отдельных весов Google отдаёт статические начертания, и жирный станет
синтетическим. Забираются только подмножества latin и cyrillic, иначе файл раздувается.
"""
import re, sys, urllib.request, base64, pathlib

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
KEEP = ("latin", "cyrillic")
DEFAULT = ["Unbounded:wght@200..900", "Golos Text:wght@400..900", "JetBrains Mono:wght@400..700"]

def main(families):
    out = []
    for fam in families:
        q = fam.replace(" ", "+")
        css = urllib.request.urlopen(
            urllib.request.Request(f"https://fonts.googleapis.com/css2?family={q}&display=block", headers=UA)
        ).read().decode()
        got = False
        for m in re.finditer(r"/\* (\S+) \*/\s*@font-face\s*{(.*?)}", css, re.S):
            subset, body = m.group(1), m.group(2)
            if subset not in KEEP:
                continue
            url = re.search(r"url\((\S+?)\)", body).group(1)
            data = base64.b64encode(urllib.request.urlopen(url).read()).decode()
            body = re.sub(r"src:\s*url\(\S+?\)\s*format\('woff2'\);",
                          f"src:url(data:font/woff2;base64,{data}) format('woff2');", body)
            out.append("@font-face{" + re.sub(r"\s+", " ", body).strip() + "}")
            print(f"  {fam} · {subset} · {len(data) // 1024} КБ")
            got = True
        if not got:
            print(f"  ВНИМАНИЕ: у «{fam}» нет ни latin, ни cyrillic. Кириллицы нет у многих "
                  f"узких гротесков; из вариативных с кириллицей есть Onest, Manrope, Golos Text, "
                  f"Unbounded, Geologica.")
    path = pathlib.Path(__file__).with_name("fonts.css")
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"fonts.css: {path.stat().st_size // 1024} КБ")

if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT)
