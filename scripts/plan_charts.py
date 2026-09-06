# -*- coding: utf-8 -*-
"""Generadores SVG para gráficos del plan (reutilizados en PDF y HTML)."""
import math

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def donut_svg(data, cx, cy, r, ring=30, c0=0.0, c1=360.0):
    """data: [(value, color)] -> SVG path del anillo (donut)."""
    total = sum(v for v, _ in data) or 1
    start = c0
    parts = []
    for val, col in data:
        frac = val / total * (c1 - c0)
        if frac <= 0.05 and v > 0:
            frac = max(frac, 0.05)  # mantener línea visible
        end = start + frac
        large = 1 if (end - start) > 180 else 0
        a0 = math.radians(start - 90)
        a1 = math.radians(end - 90)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x0i, y0i = cx + (r - ring) * math.cos(a0), cy + (r - ring) * math.sin(a0)
        x1i, y1i = cx + (r - ring) * math.cos(a1), cy + (r - ring) * math.sin(a1)
        parts.append(
            f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} '
            f'L {x1i:.1f} {y1i:.1f} A {r - ring} {r - ring} 0 {large} 0 {x0i:.1f} {y0i:.1f} Z" fill="{esc(col)}"/>'
        )
        start = end
    return "".join(parts)

def donut_svg_doc(data, width, ring_color="#F6F1E7"):
    """Donut completo para documento (invertido, ya que SVG Y baja)."""
    cx, cy, r = width / 2, 118, 88
    bg = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{ring_color}"/>'
    seg = donut_svg(data, cx, cy, r, ring=34)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{cy + r + 6}">'
        f'{bg}{seg}</svg>'
    )

def bars_svg(data, width, bar_h=20, gap=14, label_w=196, font="Inter-Regular", vfont=None):
    """data: [(label, value, color)] — barras horizontales con valor al final."""
    n = len(data)
    height = n * (bar_h + gap) - gap + 8
    maxv = max(v for _, v, _ in data) or 1
    rows = []
    y = 4
    for label, value, color in data:
        w = (value / maxv) * (width - label_w - 58)
        rows.append(
            f'<text x="{label_w - 8}" y="{y + bar_h / 2 + 3.5}" text-anchor="end" '
            f'font-family="{font}" font-size="8.6" fill="#5B6875">{esc(label)}</text>'
            f'<rect x="{label_w}" y="{y}" width="{max(w, 2):.1f}" height="{bar_h}" rx="4" fill="{esc(color)}"/>'
            f'<text x="{label_w + w + 7:.1f}" y="{y + bar_h / 2 + 3.5}" '
            f'font-family="{vfont or font}" font-size="8.6" font-weight="600" fill="#10233A">{esc(value)}</text>'
        )
        y += bar_h + gap
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'{"".join(rows)}</svg>'
    )

def line_svg(labels, series, width, height=190, unit="€", font="Inter-Regular"):
    """series: [(nombre, valores)] — línea con área y puntos."""
    import math
    n = len(labels)
    pad_l, pad_r, pad_t, pad_b = 34, 14, 14, 26
    iw = width - pad_l - pad_r
    ih = height - pad_t - pad_b
    allv = [v for _, vs in series for v in vs]
    maxv = max(allv) or 1
    minv = min(allv)
    # dejar aire alrededor y escalar desde ~82% del mínimo para leer la curva
    span = (maxv - minv) or 1
    minv = max(0, minv - span * 0.18)
    maxv = maxv + span * 0.18
    def X(i):
        return pad_l + iw * (i / (n - 1)) if n > 1 else pad_l + iw / 2
    def Y(v):
        return pad_t + ih * (1 - (v - minv) / (maxv - minv))
    out = []
    # gridlines horizontales
    for g in range(0, 5):
        v = minv + (maxv - minv) * g / 4
        yy = Y(v)
        out.append(f'<line x1="{pad_l}" y1="{yy:.1f}" x2="{width - pad_r}" y2="{yy:.1f}" stroke="#E3DACB" stroke-width="0.6"/>')
        out.append(f'<text x="{pad_l - 5}" y="{yy + 3:.1f}" text-anchor="end" font-family="{font}" font-size="7.2" fill="#9AA5B1">{int(v)}</text>')
    colors = ["#C6A15B", "#7C9A8C", "#7FA8C9"]
    for si, (name, vals) in enumerate(series):
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
        col = colors[si % len(colors)]
        base = pad_t + ih  # fondo del área de dibujo
        area = f"{X(0):.1f},{base:.1f} " + " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals)) + f" {X(n - 1):.1f},{base:.1f}"
        out.append(f'<polygon points="{area}" fill="{col}" opacity="0.10"/>')
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(vals):
            out.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="3.1" fill="#FFFFFF" stroke="{col}" stroke-width="1.8"/>')
    for i, lb in enumerate(labels):
        out.append(f'<text x="{X(i):.1f}" y="{height - 8}" text-anchor="middle" font-family="{font}" font-size="8" fill="#5B6875">{esc(lb)}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">{"".join(out)}</svg>'
