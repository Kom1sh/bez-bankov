#!/usr/bin/env python3
"""Генерирует src/slides.html — содержание деки.

    python3 src/make_slides.py && python3 src/build.py && python3 src/qa.py

Правится ТОЛЬКО этот файл (содержание) и src/deck.tpl.html (оформление).
index.html — результат сборки, руками его не трогать.

Ниже: словари брендов, штриховые иконки, помощники компонентов, генераторы графиков
и, в самом низу, сами слайды. Демо-слайды показывают каждый компонент в деле —
заменяйте их своими и удаляйте лишнее.
"""
import json, pathlib, math, html

HERE = pathlib.Path(__file__).resolve().parent
BR = json.load(open(HERE / "brands.json")) if (HERE / "brands.json").exists() else {}
# D = json.load(open(HERE / "data.json", encoding="utf-8"))   # снимок живых данных, если он есть

INK = "#1C1C1E"
# Фирменные цвета из Simple Icons. Белый и чёрный заменяем чернилами: на белой плитке
# фирменный белый невидим, а чистый чёрный выглядит грязно.
for _k, _v in list(BR.items()):
    if _v.upper() in ("#000000", "#FFFFFF", "#181717", "#191919"):
        BR[_k] = INK

# Подписи под плитками логотипов: слуг → как называть по-русски.
NAME = {}

# Бренды, которых нет в Simple Icons, рисуются текстовой плиткой: слуг → (надпись, цвет).
WORD = {}

UI = {
 "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
 "robot": '<rect x="4.5" y="8.5" width="15" height="11" rx="2.5"/><path d="M12 8.5V4.5"/><circle cx="12" cy="3.5" r="1.2"/><circle cx="9" cy="14" r="1.3"/><circle cx="15" cy="14" r="1.3"/><path d="M2 13v3M22 13v3"/>',
 "book": '<path d="M3.5 5h6.5a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H3.5z"/><path d="M20.5 5H14a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h6.5z"/>',
 "podium": '<rect x="2.5" y="12.5" width="5.5" height="8.5" rx="1"/><rect x="9.25" y="5.5" width="5.5" height="15.5" rx="1"/><rect x="16" y="9.5" width="5.5" height="11.5" rx="1"/>',
 "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l2.6-2.6a4.5 4.5 0 0 0-6.4-6.4L11.2 6.4"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0L5 12.6a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>',
 "sitemap": '<rect x="9" y="2.5" width="6" height="4.5" rx="1"/><rect x="2.5" y="17" width="6" height="4.5" rx="1"/><rect x="15.5" y="17" width="6" height="4.5" rx="1"/><path d="M12 7v4.5M5.5 17v-5.5h13V17"/>',
 "gauge": '<path d="M4 16a8 8 0 0 1 16 0"/><path d="M12 16l4.5-5.5"/><circle cx="12" cy="16" r="1.3"/><path d="M3 20h18"/>',
 "shield": '<path d="M12 2.5 4 6v6c0 5 3.4 8.4 8 9.5 4.6-1.1 8-4.5 8-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16.5 9"/>',
 "no": '<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/>',
 "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
 "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="18" r="1.2"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "quote": '<path d="M4 15V9a3 3 0 0 1 3-3h2v5H6v4H4z"/><path d="M14 15V9a3 3 0 0 1 3-3h2v5h-3v4h-2z"/>',
 "chat": '<path d="M4 5.5h16v10H10l-5 4v-4H4z"/>',
 "doc": '<path d="M6 2.5h8l4 4v15H6z"/><path d="M14 2.5v4h4"/><path d="M9 12h6M9 16h6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
 "megaphone": '<path d="M3 10v4l11 4V6z"/><path d="M14 6v12"/><path d="M17.5 9.5a3 3 0 0 1 0 5"/><path d="M6 14l1.5 5"/>',
 "pin": '<path d="M12 21.5s-7-6.2-7-11.3a7 7 0 0 1 14 0c0 5.1-7 11.3-7 11.3z"/><circle cx="12" cy="10" r="2.5"/>',
 "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 3.5v4.5h-4.5"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "zap": '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6z"/>',
 "eye": '<path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
 "pen": '<path d="M4 20l3.2-.7L20 6.5a2.1 2.1 0 0 0-3-3L4.2 16.3z"/><path d="M15.5 5.5l3 3"/>',
 "arrow": '<path d="M4 12h16"/><path d="M13 5l7 7-7 7"/>',
 "coins": '<circle cx="9" cy="9" r="6"/><path d="M15.5 8.2A6 6 0 1 1 8.2 15.5"/>',
 "share": '<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.6M8.2 13.2l7.6 4.6"/>',
 "star": '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1.1 6.3L12 17.4l-5.6 3 1.1-6.3L3 9.7l6.2-.9z"/>',
 "flag": '<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
 "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/>',
 "layers": '<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5"/><path d="M2.5 17 12 22l9.5-5"/>',
}

UI.update({
 "card": '<rect x="2.5" y="5.5" width="19" height="13" rx="2.2"/><path d="M2.5 10h19"/><path d="M6 15h4"/>',
 "cash": '<rect x="2.5" y="6" width="19" height="12" rx="1.8"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/>',
 "bag": '<path d="M5 8h14l-1 12.5H6z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
 "car": '<path d="M4 16.5V12l2-5h12l2 5v4.5"/><path d="M3 16.5h18"/><circle cx="7.5" cy="16.5" r="1.8"/><circle cx="16.5" cy="16.5" r="1.8"/><path d="M4.5 12h15"/>',
 "park": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M9.5 17V7.5h3.5a3 3 0 0 1 0 6H9.5"/>',
 "wallet": '<path d="M3.5 7.5h15a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-15z"/><path d="M3.5 7.5 15 3.5v4"/><circle cx="16.5" cy="14" r="1.2"/>',
 "qr": '<rect x="3.5" y="3.5" width="7" height="7" rx="1"/><rect x="13.5" y="3.5" width="7" height="7" rx="1"/><rect x="3.5" y="13.5" width="7" height="7" rx="1"/><path d="M13.5 13.5h3v3M20.5 13.5v7h-4M13.5 17.5v3"/>',
 "shop": '<path d="M3.5 9.5 5 4.5h14l1.5 5"/><path d="M3.5 9.5h17v2a2.8 2.8 0 0 1-5.6 0 2.8 2.8 0 0 1-5.8 0 2.8 2.8 0 0 1-5.6 0z"/><path d="M5 12.5v8h14v-8"/>',
 "tax": '<path d="M6 2.5h9l3 3v16H6z"/><path d="M9 10h6M9 14h6M9 18h3"/>',
})

def ui(name, cls=""): return f'<svg class="ui {cls}" viewBox="0 0 24 24" aria-hidden="true">{UI[name]}</svg>'

def ico(slug):
    return f'<svg class="ic" style="color:{BR.get(slug, INK)}"><use href="#i-{slug}"/></svg>'

def tile(slug, label=None, size="", extra=""):
    if slug in WORD:
        t, c = WORD[slug]; inner = f'<div class="tile word {size}" style="color:{c};{extra}">{t}</div>'
    else:
        inner = f'<div class="tile {size}" style="{extra}">{ico(slug)}</div>'
    if label is None or (slug in WORD and label == WORD[slug][0]): return inner
    return f'<div class="tl{" w" if slug in WORD else ""}">{inner}<span>{label}</span></div>'

def top(pill): return f'<div class="top"><span class="pill">{pill}</span><span class="cnt"></span></div>'

def slide(inner, title, cls=""): return f'<section class="s {cls}" data-t="{html.escape(title)}">{inner}</section>'

def sticky(kind, h, p, extra=""): return f'<div class="sticky {kind}">{extra}<h4>{h}</h4><p>{p}</p></div>'

def stat(n, l, cls=""): return f'<div class="stat {cls}"><div class="n">{n}</div><div class="l">{l}</div></div>'

def browser(url, img, w=None):
    """Окно браузера. Высота выводится из пропорций снимка, поэтому страница видна целиком."""
    st = f' style="max-width:{w}px"' if w else ""
    return f'<div class="browser"{st}><div class="bar"><i></i><i></i><i></i><span class="url">{url}</span></div><div class="shot"><img src="assets/{img}" alt=""></div></div>'

def arrow(): return '<div class="arr"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>'

def step(n, h, p, kind="", icon=None, i=0):
    ic = ui(icon, "sm") if icon else ""
    return f'<div class="step {kind} r" style="--i:{i}"><div class="hd"><span class="num">{n}</span>{ic}</div><h4>{h}</h4><p>{p}</p></div>'

def fmt(n): return f"{int(round(n)):,}".replace(",", " ")

def nice(v):
    """Округляет потолок оси до «красивого» числа: 1621 → 2000, 537 → 600, 38 → 40."""
    if v <= 0: return 1
    import math as _m
    mag = 10 ** _m.floor(_m.log10(v)); f = v / mag
    for step in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if f <= step: return step * mag
    return 10 * mag

def line_chart(points, w=760, h=330, color="#0FBCB0", fill="#C3FAF5", every=1, vline=None, ymax=None, mark_last=True, mark_peak=False, xfmt=None, dot_r=5):
    L, R, T, B = 74, 24, 28, 44
    vals = [v for _, v in points]; ymax = ymax or nice(max(vals) * 1.12) or 1
    n = len(points); xs = [L + (w - L - R) * i / max(1, n - 1) for i in range(n)]
    ys = [T + (h - T - B) * (1 - v / ymax) for v in vals]
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    ticks = 4
    for k in range(ticks + 1):
        yy = T + (h - T - B) * k / ticks; vv = ymax * (1 - k / ticks)
        out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8" stroke-width="1"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{fmt(vv)}</text>')
    area = f"M{xs[0]:.1f},{h-B} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in zip(xs, ys)) + f" L{xs[-1]:.1f},{h-B} Z"
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out.append(f'<path d="{area}" fill="{fill}"/>'); out.append(f'<path d="{line}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (lab, v) in enumerate(points):
        if i == n - 1 or (i % every == 0 and n - 1 - i >= max(2, every // 2)):
            out.append(f'<text class="ax" x="{xs[i]:.1f}" y="{h-14}" text-anchor="middle">{xfmt(lab) if xfmt else lab}</text>')
    if vline is not None:
        i, txt = vline; out.append(f'<line x1="{xs[i]:.1f}" x2="{xs[i]:.1f}" y1="{T-8}" y2="{h-B}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>')
        out.append(f'<text class="val" x="{xs[i]+10:.1f}" y="{T+8}" text-anchor="start">{txt}</text>')
    if mark_last:
        out.append(f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="{dot_r+2}" fill="#fff" stroke="{color}" stroke-width="4"/>')
        out.append(f'<text class="val" x="{xs[-1]-14:.1f}" y="{ys[-1]-16:.1f}" text-anchor="end" style="font-size:22px">{fmt(vals[-1])}</text>')
    if mark_peak and n > 1:
        out.append(f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{dot_r}" fill="#fff" stroke="{color}" stroke-width="3"/>')
        out.append(f'<text class="val" x="{xs[0]+12:.1f}" y="{ys[0]-14:.1f}" text-anchor="start">{fmt(vals[0])}</text>')
    out.append("</svg>"); return "".join(out)

def bars(cats, series, w=760, h=330, suffix="", ymax=None):
    L, R, T, B = 60, 16, 30, 44
    allv = [v for _, _, vals in series for v in vals]; ymax = ymax or nice(max(allv) * 1.15) or 1
    n, m = len(cats), len(series); gw = (w - L - R) / n; bw = min(78, gw * 0.7 / m); gap = 8
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for k in range(5):
        yy = T + (h - T - B) * k / 4; out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{ymax*(1-k/4):.0f}{suffix}</text>')
    for ci, c in enumerate(cats):
        cx = L + gw * ci + gw / 2; total = m * bw + (m - 1) * gap; x0 = cx - total / 2
        for si, (name, color, vals) in enumerate(series):
            v = vals[ci]; x = x0 + si * (bw + gap); hh = (h - T - B) * v / ymax; y = h - B - hh
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(hh,2):.1f}" rx="8" fill="{color}"/>')
            lab = ("—" if v is None else f"{v:g}{suffix}")
            out.append(f'<text class="val" x="{x+bw/2:.1f}" y="{y-10:.1f}" text-anchor="middle">{lab}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{h-14}" text-anchor="middle" style="font-size:17px;fill:{INK};font-weight:500">{c}</text>')
    out.append("</svg>"); return "".join(out)

def hbars(items, w=700, rowh=52, maxv=None, labw=300, color="#0FBCB0", fmtv=fmt, mono=False):
    maxv = maxv or max(v for _, v, *_ in items)
    h = rowh * len(items); out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for i, it in enumerate(items):
        lab, v = it[0], it[1]; col = it[2] if len(it) > 2 else color
        y = i * rowh; bw = (w - labw - 110) * v / maxv
        fam = "font-family:var(--fm);font-weight:500;font-size:16px" if mono else "font-size:18px;font-weight:500"
        out.append(f'<text x="{labw-14}" y="{y+rowh/2+6}" text-anchor="end" style="{fam};fill:{INK}">{html.escape(lab)}</text>')
        out.append(f'<rect x="{labw}" y="{y+rowh/2-14}" width="{max(bw,3):.1f}" height="28" rx="8" fill="{col}"/>')
        out.append(f'<text class="val" x="{labw+bw+12:.1f}" y="{y+rowh/2+6}">{fmtv(v)}</text>')
    out.append("</svg>"); return "".join(out)

def donut(parts, size=300, thick=46, center=""):
    r = (size - thick) / 2; c = math.pi * 2 * r; tot = sum(v for _, v, _ in parts); off = 0
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" aria-hidden="true"><g transform="rotate(-90 {size/2} {size/2})">']
    for lab, v, col in parts:
        seg = c * v / tot
        out.append(f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{thick}" stroke-dasharray="{seg:.2f} {c-seg:.2f}" stroke-dashoffset="{-off:.2f}"/>')
        off += seg
    out.append("</g>")
    if center: out.append(f'<text x="{size/2}" y="{size/2+12}" text-anchor="middle" class="val" style="font-size:34px">{center}</text>')
    out.append("</svg>"); return "".join(out)

def plist(items, icon):
    return '<ul class="plist">' + "".join(
        f'<li>{ui(icon, "xs")}<div><b>{h}</b><i>{p}</i></div></li>' for h, p in items) + '</ul>'

def divider(n, title, sub, items):
    return slide(top("Раздел " + n) + f'<div class="body"><div class="row fill" style="gap:60px;align-items:flex-end"><div style="flex:1.2;display:flex;flex-direction:column;height:100%">'
      f'<div class="divn">{n}</div><div style="margin-top:auto"><div class="divt">{title}</div><div class="divs">{sub}</div></div></div>'
      f'<div class="divlist" style="flex:1;padding-bottom:12px">{"".join(f"<span>{x}</span>" for x in items)}</div></div></div>', f"Раздел {n}: {title}", "dark")

def qcard(kind, label, q, meta, page, win=None):
    tail = f'<span class="pill" style="margin-top:auto;align-self:flex-start">{win}</span>' if win else ""
    return f'<div class="sticky {kind}"><span class="lab">{label}</span><div class="qcard"><div class="q">{q}</div><div class="meta">{meta}</div></div><p>{page}</p>{tail}</div>'


# ═══════════════════════════════════════════════════════════════════════════
#  СЛАЙДЫ
#  Одна мысль на слайд. Заголовок — утверждение, а не тема раздела.
#  Каждая цифра с источником и датой. Разделители ставят ритм.
# ═══════════════════════════════════════════════════════════════════════════
S = []
# ── ЦИФРЫ: каждая с источником и датой, подставляются из проверенной таблицы ──
F = {}

def pct(v): return f"{v:.1f}".replace(".", ",")

def share_chart(points, w=860, h=470, lo=50, hi=100):
    """Доля безнала по годам: ось с 50%, подпись у каждой точки."""
    L, R, T, B = 64, 30, 30, 50
    n = len(points); xs = [L + (w - L - R) * i / (n - 1) for i in range(n)]
    ys = [T + (h - T - B) * (1 - (v - lo) / (hi - lo)) for _, v in points]
    o = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for k in range(0, 6):
        v = lo + (hi - lo) * k / 5; y = T + (h - T - B) * (1 - k / 5)
        o.append(f'<line x1="{L}" x2="{w-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#C9D0C3" stroke-width="1"/>')
        o.append(f'<text class="ax" x="{L-10}" y="{y+5:.1f}" text-anchor="end">{int(v)}%</text>')
    area = f"M{xs[0]:.1f},{h-B} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in zip(xs, ys)) + f" L{xs[-1]:.1f},{h-B} Z"
    o.append(f'<path d="{area}" fill="#E2F6D5"/>')
    o.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys)) + '" fill="none" stroke="#163300" stroke-width="4" stroke-linejoin="round"/>')
    for i, ((lab, v), x, y) in enumerate(zip(points, xs, ys)):
        last = i == n - 1
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 if last else 6}" fill="{"#9FE870" if last else "#fff"}" stroke="#163300" stroke-width="3"/>')
        lab_v = "≈73%" if lab == "2021" else f"{pct(v)}%"
        o.append(f'<text class="val" x="{x + (6 if last else 0):.1f}" y="{y-18:.1f}" text-anchor="{"end" if last else "middle"}" style="font-size:{24 if last else 18}px">{lab_v}</text>')
        o.append(f'<text class="ax" x="{x:.1f}" y="{h-16}" text-anchor="middle" style="font-size:17px">{lab}</text>')
    o.append("</svg>"); return "".join(o)

def plist2(items):
    return '<div class="facts">' + "".join(f'<div class="fi">{ui(i, "sm")}<div><b>{h}</b><i>{t}</i></div></div>' for i, h, t in items) + '</div>'

SHARE = [("2019", 64.7), ("2020", 70.3), ("2021", 73.0), ("2022", 78.1), ("2023", 83.4), ("2024", 85.8), ("2025", 88.0)]
F["h2"] = "Наличными просто проходят два платежа из восьми. Ещё три — только в отделении"
F["f2"] = ("ТК РФ ст. 136, НК РФ ст. 45, ГК РФ ст. 140, КоАП ст. 14.8; Почта России; АМПП (2023); РБК и iXBT — Ozon, 28.09.2026; "
           "X5 (2023); доход на карту — опрос Банка России о платёжном поведении, 2025.")
F["h3"] = "Безнал за шесть лет вырос с 65 до 88% розничных покупок, банкоматов стало на треть меньше"
F["chart3"] = share_chart(SHARE) + '<div class="leg"><span>доля безналичных платежей в розничном обороте, Банк России</span></div>'
F["side3"] = plist2([
    ("card", "94% взрослых с картой", "86% получают доход сразу на карту."),
    ("cash", "Банкоматов −32%", "Было 202,6 тыс. в начале 2020 года, стало 137,9 тыс."),
    ("home", "Офисов банков всё меньше", "22 355 в начале 2026 года, 20 869 на 1 сентября."),
    ("zap", "СБП: 18,3 млрд переводов", "За 2025 год на 103 трлн ₽, в 1,4 раза больше, чем годом раньше.")])
F["f3"] = ("Банк России: стратегии НПС 2021–2023, итоги 2022 и 2023 годов; 2024–2025 — Интерфакс со ссылкой на ЦБ; 2021 — около 73%, округлено ЦБ. "
           "Банкоматы и офисы — статистика НПС и банковского сектора; СБП — обзор за IV кв. 2025; карты — опрос ЦБ и НАФИ, 2025.")
F["h4"] = "Государство ведёт платежи в цифру, а наличных на руках вдвое больше, чем в 2020 году"
F["push"] = plist2([
    ("wallet", "Цифровой рубль с 1 сентября 2026", "Крупнейшие банки и магазины с выручкой от 120 млн ₽. За три недели почти 200 тыс. счетов. С 2027 и 2028 года — остальные."),
    ("qr", "QR и биометрия", "1,1 млрд оплат за второй квартал 2026 года на 1,7 трлн ₽."),
    ("card", "Кассы самообслуживания", "У X5 это 69 тыс. касс из 140 тыс. Их предпочитают 55% покупателей.")])
F["hold"] = plist2([
    ("cash", "20,7 трлн ₽ наличными", "В 2,1 раза больше, чем в начале 2020 года, и +20,9% за год."),
    ("user", "48% не могут без наличных", "27% прямо их предпочитают, 36% хранят сбережения в купюрах."),
    ("flag", "Первый рост наличных платежей", "Банк России в 2026 году впервые отметил, что платежей наличными стало больше.")])
F["f4"] = ("Закон 248-ФЗ и Банк России; Интерфакс, 23.09.2026 — счета цифрового рубля; обзор НПС за II кв. 2026; X5 (2026), SuperJob (09.2026); "
           "денежные агрегаты ЦБ на 1.09.2026; опрос ЦБ о платёжном поведении, 2025; Коммерсантъ, 04.09.2026.")
F["f5"] = "Кассы самообслуживания принимают карты и СБП, наличные — нет (X5). Их предпочитают 55% покупателей, SuperJob, сентябрь 2026."

def vd(kind, text): return f'<span class="vd v{kind}"><i></i>{text}</span>'

# 1 обложка
S.append(slide(top("Банковские инструменты, доклад на 3 минуты") +
  '<div class="body cover"><div class="row fill" style="gap:48px">'
  '<div style="flex:1;display:flex;flex-direction:column;min-width:0">'
  '<h1 style="font-size:84px;line-height:1">Финансовая свобода без банков</h1>'
  '<p class="sub">Можно ли в 2026 году жить на наличные: без карт, переводов и кредитов</p>'
  '<div class="who"><div><b>Протасов Егор</b><br><span>Банковские инструменты</span></div></div></div>'
  '<div style="width:560px;flex:none;display:flex;flex-direction:column;gap:18px;justify-content:center">'
  f'<div class="card" style="padding:30px 32px;gap:14px"><span class="lab" style="font:500 18px/1.3 var(--ft);color:var(--slate)">Мой ответ</span>'
  '<p style="font:700 34px/1.2 var(--fd);color:var(--ink)">Частично — да. Полностью — почти нет.</p>'
  '<p style="font:400 21px/1.4 var(--ft)">Наличными можно платить в магазине, но зарплата, налоги, ЖКХ и штрафы всё равно проходят через банк.</p></div>'
  + '</div></div></div>', "Обложка", "cover"))

# 2 один день без карты
DAY = [("wallet", "Зарплата", "Законно в кассе (ст. 136 ТК), но 86% получают доход на карту", "cash", "можно, но редко"),
       ("home", "ЖКХ", "На почте или в кассе банка, обычно с комиссией", "bank", "только в отделении"),
       ("tax", "Налоги", "По квитанции в банке, на почте или в МФЦ", "bank", "только в отделении"),
       ("car", "Штрафы ГИБДД", "В кассе банка или на почте, возможна комиссия", "bank", "только в отделении"),
       ("park", "Парковка в Москве", "Паркоматы наличные не берут, 95% платят в приложении", "card", "только через банк"),
       ("bag", "Маркетплейс", "WB — только онлайн, Ozon — через свои банкоматы до 15 тыс. ₽", "card", "только через банк"),
       ("card", "Касса самообслуживания", "Только карта и СБП, наличные не принимает", "card", "только через банк"),
       ("shop", "Касса с кассиром", "Обязана принять наличные: ст. 140 ГК, штраф до 50 тыс. ₽", "cash", "наличными можно")]
S.append(slide(top("Один день без карты") + f'<h1>{F.get("h2", "Заголовок слайда 2")}</h1>'
  '<div class="body"><div class="day" style="margin:auto 0">'
  '<div class="h">Платёж</div><div class="h">Как заплатить без карты</div><div class="h">Итог</div>'
  + "".join(f'<div class="k">{ui(i)}{t}</div><div>{d}</div><div>{vd(k, v)}</div>' for i, t, d, k, v in DAY)
  + f'</div><p class="foot">{F.get("f2", "")}</p></div>', "Один день без карты"))

# 3 безнал растёт
S.append(slide(top("Куда движется") + f'<h1>{F.get("h3", "Заголовок слайда 3")}</h1>'
  '<div class="body"><div class="row fill" style="gap:34px;align-items:center">'
  f'<div class="chart" style="flex:1.3">{F.get("chart3", "")}</div>'
  f'<div style="flex:1;display:flex;flex-direction:column;gap:16px">{F.get("side3", "")}</div>'
  f'</div><p class="foot">{F.get("f3", "")}</p></div>', "Безнал растёт"))

# 4 что толкает и что держит
S.append(slide(top("Что дальше") + f'<h1>{F.get("h4", "Заголовок слайда 4")}</h1>'
  '<div class="body"><div class="g2" style="margin:auto 0;align-items:stretch">'
  f'<div class="sticky teal tight"><span class="lab">Толкает в безнал</span>{F.get("push", "")}</div>'
  f'<div class="sticky tight" style="background:var(--orange-l)"><span class="lab" style="color:var(--orange-d)">Держит наличные</span>{F.get("hold", "")}</div>'
  f'</div><p class="foot">{F.get("f4", "")}</p></div>', "Что дальше"))

# 5 мой вывод: кассы
def lane(kind, queue, label, cap):
    ppl = "".join(f'<div class="person">{ui("user")}</div>' for _ in range(queue)) if queue else ""
    ic = ui("cash") if kind == "cash" else ui("card")
    return (f'<div class="lane"><div class="queue">{ppl}</div>'
            f'<div class="till {kind}">{ic}<span>{label}</span></div><span class="cap">{cap}</span></div>')
LANES = lane("cash", 5, "Кассир", "очередь") + "".join(lane("self", 0, "Карта или QR", "свободна") for _ in range(6))
S.append(slide(top("Мой вывод") + '<h1>Наличные мне нравятся, но в очередь к одной кассе, когда шесть свободны, я не встану</h1>'
  '<div class="body"><div class="row fill" style="gap:40px;align-items:flex-end">'
  f'<div style="flex:1.45;min-width:0"><div class="lanes">{LANES}</div></div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
  + f'<div class="sticky tight" style="background:var(--orange-l)"><span class="lab" style="color:var(--orange-d)">Наличными</span><h4>Еда и мелкие траты</h4><p>Купюры в кошельке — видно, сколько ушло за неделю. Это и есть чувство контроля.</p></div>'
  + f'<div class="sticky teal tight"><span class="lab">Через банк</span><h4>Всё обязательное</h4><p>Зарплата, ЖКХ, налоги, штрафы, парковка, заказы. Здесь без карты либо нельзя, либо очередь и комиссия.</p></div>'
  + f'</div></div><p class="foot">{F.get("f5", "")}</p></div>', "Мой вывод"))

out = "\n".join(S)
(HERE / "slides.html").write_text(out, encoding="utf-8")
print(f"slides.html: {len(S)} слайдов, {len(out.encode()) // 1024} КБ")
