# -*- coding: utf-8 -*-
"""Renderiza el plan de negocio KHC como documento HTML premium autocontenido."""
import base64
import os
import re
import html as _html

from plan_data import META, COLORS, estimate_minutes
from plan_data import (SECTION_1, SECTION_2, SECTION_3, SECTION_4, SECTION_5)
from plan_data2 import (SECTION_6, SECTION_7, SECTION_8, SECTION_9, SECTION_15,
                        SECTION_16, SECTION_17, SECTION_18, SECTION_19, SECTION_21)
from plan_data3 import (SECTION_10, SECTION_11, SECTION_12, SECTION_13,
                        SECTION_14, SECTION_20)
from plan_data4 import SECTION_22
from plan_charts import line_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIGHTS = {
    "Inter-Regular": "400", "Inter-Medium": "500", "Inter-SemiBold": "600",
    "Inter-Bold": "700", "Inter-ExtraBold": "800",
    "Playfair-Regular": "400", "Playfair-SemiBold": "600", "Playfair-ExtraBold": "800",
    "Playfair-Italic": "400",
}

def font_css():
    out = []
    inter = base64.b64encode(open(os.path.join(ROOT, "assets/fonts/woff2/Inter-latin-var.woff2"), "rb").read()).decode()
    play = base64.b64encode(open(os.path.join(ROOT, "assets/fonts/woff2/Playfair-latin-var.woff2"), "rb").read()).decode()
    out.append(f"@font-face{{font-family:'Inter-V';src:url(data:font/woff2;base64,{inter}) format('woff2');font-weight:100 900;font-style:normal;font-display:swap;}}")
    out.append(f"@font-face{{font-family:'Playfair-V';src:url(data:font/woff2;base64,{play}) format('woff2');font-weight:400 900;font-style:normal;font-display:swap;}}")
    for name, w in WEIGHTS.items():
        if name.startswith("Inter"):
            path = os.path.join(ROOT, "assets/fonts/woff2/Inter-latin-var.woff2")
            fam = name
        else:
            path = os.path.join(ROOT, "assets/fonts/woff2/Playfair-latin-var.woff2")
            fam = name
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        out.append(
            f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b64}) format('woff2');"
            f"font-weight:{w};font-style:{'italic' if name=='Playfair-Italic' else 'normal'};font-display:swap;}}"
        )
    return "\n".join(out)

def inline(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    return s

def pct(vals):
    total = sum(vals) or 1
    return [v / total * 100 for v in vals]

# ---------------------------------------------------------------- bloques HTML

_NUM_RE = re.compile(r"^[\d\s.,€%×x−\-–+—/·~≈]*\d[\d\s.,€%×x−\-–+—/·~≈]*$")

def _is_num(cell):
    c = re.sub(r"[*<>]", "", cell).strip()
    return bool(c) and _NUM_RE.match(c) is not None

def render_table(b):
    widths = b.get("widths")
    colgroup = ""
    if widths:
        colgroup = "<colgroup>" + "".join(f'<col style="width:{w * 100:.1f}%">' for w in widths) + "</colgroup>"
    head = "".join(f"<th>{inline(c)}</th>" for c in b["cols"])
    left = set(b.get("left") or [])
    rows = []
    for i, row in enumerate(b["rows"]):
        cls = " hl" if (i in (b.get("hl") or [])) else ""
        tds = []
        for j, c in enumerate(row):
            klass = ' class="num"' if (_is_num(c) and j not in left) else ""
            tds.append(f"<td{klass}>{inline(c)}</td>")
        rows.append(f"<tr class='{cls.strip()}'>{''.join(tds)}</tr>")
    note = f'<p class="tnote">{inline(b["note"])}</p>' if b.get("note") else ""
    return (f'<div class="tbl-wrap"><table class="tbl">{colgroup}<thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>{note}')

def render_donut(b):
    data = b["data"]
    vals = [v for _, v, _ in data]
    per = pct(vals)
    stops = []
    acc = 0.0
    for (label, v, color), p in zip(data, per):
        stops.append(f"{color} {acc:.2f}% {acc + p:.2f}%")
        acc += p
    swatches = "".join(
        f'<li><span class="sw" style="background:{c}"></span><span class="ll">{inline(l)}</span>'
        f'<span class="lp">{p:.1f}%</span></li>'
        for (l, v, c), p in zip(data, per)
    )
    inner = f'<div class="donut-in"><div class="dv">{b["cv"]}</div><div class="dl">{b["cl"]}</div></div>'
    return (
        f'<figure class="chart donut-fig"><figcaption>{b["title"]}</figcaption>'
        f'<div class="donut-row"><div class="donut" style="--g:conic-gradient({",".join(stops)})">{inner}</div>'
        f'<ul class="legend">{swatches}</ul></div>'
        + (f'<p class="tnote">{inline(b["note"])}</p>' if b.get("note") else "")
        + "</figure>")

def render_bars(b):
    maxv = max(v for _, v, _ in b["data"]) or 1
    rows = []
    for label, value, color in b["data"]:
        w = value / maxv * 100
        rows.append(
            f'<div class="bar-row"><div class="bar-label">{inline(label)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{w:.1f}%;background:{color}"></div></div>'
            f'<div class="bar-val">{value:,}'.replace(",", ".") + f' {b["unit"]}</div></div>')
    return (
        f'<figure class="chart"><figcaption>{b["title"]}</figcaption><div class="bars">{"".join(rows)}</div>'
        + (f'<p class="tnote">{inline(b["note"])}</p>' if b.get("note") else "")
        + "</figure>")

def render_line(b):
    svg = line_svg(b["labels"], b["series"], 620)
    return (
        f'<figure class="chart"><figcaption>{b["title"]}</figcaption>'
        f'<div class="line-wrap">{svg}</div>'
        + (f'<p class="tnote">{inline(b["note"])}</p>' if b.get("note") else "")
        + "</figure>")

def render_callout(b):
    return (f'<aside class="callout {b["tone"]}"><div class="co-title">{inline(b["title"])}</div>'
            f'<div class="co-body">{inline(b["html"])}</div></aside>')

def render_grid(b):
    cards = "".join(
        f'<div class="gcard"><div class="gicon">{icon}</div><h3>{inline(t)}</h3><p>{inline(txt)}</p></div>'
        for icon, t, txt in b["items"]
    )
    return f'<div class="grid">{cards}</div>'

def render_steps(b):
    items = "".join(
        f'<li><span class="sn">{i:02d}</span><div class="sb"><strong>{t}</strong>'
        + (f'<p>{inline(txt)}</p>' if txt else "")
        + "</div></li>" for i, (t, txt) in enumerate(b["items"], 1)
    )
    return f'<ol class="steps">{items}</ol>'

def render_check(b):
    items = "".join(f'<li><span class="ck"></span><div>{inline(t)}</div></li>' for t in b["items"])
    return f'<ul class="checks">{items}</ul>'

def render_timeline(b):
    items = "".join(
        f'<li><div class="period">{p}</div><div class="tl-dot"></div><div class="tl-body">'
        f'<strong>{t}</strong><p>{inline(txt)}</p></div></li>'
        for p, t, txt in b["items"]
    )
    return f'<ol class="timeline">{items}</ol>'

def render_twocol(b):
    def col(title, items):
        lis = "".join(f"<li>{inline(i)}</li>" for i in items)
        return f'<div class="col"><h4>{title}</h4><ul class="bullets">{lis}</ul></div>'
    return f'<div class="twocol">{col(b["lt"], b["li"])}{col(b["rt"], b["ri"])}</div>'

def render_block(b):
    t = b["t"]
    if t == "section":
        sub = b.get("num", "").count(".") > 0
        mins = _MINS.get(b["num"])
        dur = f'<span class="dur">⏱ ~{mins} min</span>' if (mins and not sub) else ""
        ess = ""
        if b.get("ess") and not sub:
            items = "".join(f"<li>{inline(x)}</li>" for x in b["ess"])
            ess = (f'<aside class="ess"><div class="ess-title">Lo esencial · en 20 segundos</div>'
                   f'<ul>{items}</ul></aside>')
        return (
            f'<section class="sec {"" if not sub else "sub"}" id="s{b["num"]}">'
            f'<header class="sechead"><div class="secnum">{b["num"]}</div>'
            f'<div class="sctext"><div class="kick">{b["kicker"]}</div><h2>{b["title"]}</h2></div>'
            f'{dur}</header>'
            + (f'<p class="intro">{inline(b["intro"])}</p>' if b.get("intro") else "")
            + ess
            + "</section>")
    if t == "lead":
        return f'<p class="lead">{inline(b["html"])}</p>'
    if t == "p":
        return f'<p class="body">{inline(b["html"])}</p>'
    if t == "quote":
        return f'<blockquote class="quote">{inline(b["text"])}</blockquote>'
    if t == "kpis":
        cards = "".join(
            f'<div class="kpi"><div class="kv">{v}</div><div class="kl">{l}</div>'
            f'<div class="kd">{inline(d)}</div></div>'
            for v, l, d in b["items"])
        return f'<div class="kpis">{cards}</div>'
    if t == "table":
        return render_table(b)
    if t == "donut":
        return render_donut(b)
    if t == "bars":
        return render_bars(b)
    if t == "line":
        return render_line(b)
    if t == "callout":
        return render_callout(b)
    if t == "grid":
        return render_grid(b)
    if t == "steps":
        return render_steps(b)
    if t == "check":
        return render_check(b)
    if t == "timeline":
        return render_timeline(b)
    if t == "twocol":
        return render_twocol(b)
    if t == "pagebreak":
        return '<div class="brk"></div>'
    if t == "spacer":
        return f'<div style="height:{b["pts"]}px"></div>'
    return ""

_MINS = {}

def toc_entries():
    out = []
    for secs in [SECTION_1, SECTION_2, SECTION_3, SECTION_4, SECTION_5, SECTION_6,
                 SECTION_7, SECTION_8, SECTION_9, SECTION_10, SECTION_11, SECTION_12,
                 SECTION_13, SECTION_14, SECTION_15, SECTION_16, SECTION_17, SECTION_18,
                 SECTION_19, SECTION_20, SECTION_21, SECTION_22]:
        for b in secs:
            if b["t"] == "section":
                out.append((b["num"], b["kicker"], b["title"]))
    return out

CSS = """
:root{
  --navy:#10233A;--navy2:#1B3A5C;--ink:#1D2733;--muted:#5B6875;
  --gold:#C6A15B;--gold2:#A58142;--cream:#F6F1E7;--paper:#FBF9F4;
  --line:#E7DECF;--line2:#D8CDBA;--sage:#7C9A8C;--terra:#C97B5A;
  --blush:#D9A79B;--blue:#7FA8C9;--green:#4E8A6E;--red:#B4502E;--amber:#C88A2E;
  --serif:'Playfair-V','Playfair Display',Georgia,serif;
  --sans:'Inter-V',-apple-system,'Segoe UI',Roboto,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--sans);font-size:16px;line-height:1.72;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--serif);font-weight:600;margin:0}
svg text{font-family:'Inter-V',var(--sans)}
strong{font-weight:700;color:var(--navy)}
em{color:var(--navy2)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
  background:var(--cream);border:1px solid #EDE3D2;border-radius:6px;padding:1px 6px;color:var(--navy2)}

/* ---------------- PORTADA ---------------- */
.cover{min-height:100vh;position:relative;display:flex;flex-direction:column;color:#F8F4EC;
  background:radial-gradient(1200px 700px at 80% -10%,#24476B 0%,transparent 60%),
             radial-gradient(900px 600px at -10% 110%,#1B3A5C 0%,transparent 55%),var(--navy);
  overflow:hidden}
.cover::before{content:"KHC";position:absolute;right:-40px;bottom:-90px;font-family:var(--serif);
  font-size:420px;font-weight:800;color:transparent;-webkit-text-stroke:1px rgba(198,161,91,.14);line-height:1;pointer-events:none}
.cover-frame{position:absolute;inset:26px;border:1px solid rgba(198,161,91,.35);pointer-events:none}
.cover-top{display:flex;justify-content:space-between;align-items:center;padding:58px 64px 0}
.cover-brand{display:flex;align-items:center;gap:14px;font-family:var(--serif);font-weight:800;
  letter-spacing:.22em;font-size:17px;color:#F1E7D4}
.cover-brand .dot{width:38px;height:38px;border:1px solid var(--gold);border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:14px;letter-spacing:.05em}
.cover-tag{font-size:11.5px;letter-spacing:.34em;color:rgba(241,231,212,.72);text-transform:uppercase}
.cover-mid{flex:1;display:flex;flex-direction:column;justify-content:center;padding:0 64px;max-width:920px}
.cover-kicker{font-size:12px;letter-spacing:.5em;color:var(--gold);text-transform:uppercase;margin-bottom:22px}
.cover h1{font-size:clamp(44px,7vw,84px);line-height:1.04;font-weight:800;color:#FBF7EE;margin:0 0 26px}
.cover h1 em{font-style:italic;font-weight:400;color:#E9D9BB}
.cover-sub{max-width:580px;font-size:17.5px;line-height:1.72;color:rgba(235,239,241,.84)}
.cover-rule{width:120px;height:3px;background:var(--gold);margin:34px 0 30px}
.cover-points{display:flex;gap:38px;flex-wrap:wrap}
.cp{min-width:150px;border-left:2px solid rgba(198,161,91,.5);padding-left:14px}
.cp b{display:block;font-family:var(--serif);font-size:21px;color:#F1E7D4;font-weight:700}
.cp span{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:rgba(235,239,241,.65)}
.cover-scope{font-family:var(--serif);font-style:italic;font-size:14px;color:rgba(201,191,169,.9);
  margin:44px 0 0}
.cover-bottom{display:flex;gap:26px;flex-wrap:wrap;padding:0 64px 46px;font-size:11px;
  letter-spacing:.18em;text-transform:uppercase;color:rgba(235,239,241,.6)}
.cover-bottom span b{color:#E9D9BB;font-weight:600}

/* ---------------- ÍNDICE ---------------- */
.toc{background:#FDFBF6;border-bottom:1px solid var(--line)}
.toc-in{max-width:1020px;margin:0 auto;padding:70px 28px 80px}
.toc-title{font-size:34px;color:var(--navy);margin-bottom:6px}
.toc-kick{font-size:11px;letter-spacing:.4em;color:var(--gold2);text-transform:uppercase;margin-bottom:34px}
.toc-stats{font-family:var(--serif);font-style:italic;font-size:15.5px;color:var(--gold2);margin:0 0 30px}
.toc-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 40px}
a.ti{display:flex;align-items:baseline;gap:16px;padding:11px 4px;text-decoration:none;
  color:var(--ink);border-bottom:1px dashed var(--line);transition:.18s}
a.ti:hover{background:var(--cream);padding-left:12px;color:var(--navy)}
.tn{font-family:var(--serif);font-weight:800;font-size:19px;color:var(--gold2);min-width:46px}
.tt{font-weight:600;color:var(--navy);font-size:14px;line-height:1.35}
.tk{font-size:10.5px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase;margin-top:2px}

/* rutas de lectura */
.paths{margin-top:44px}
.paths-title{font-size:11px;letter-spacing:.4em;color:var(--gold2);text-transform:uppercase;
  margin-bottom:18px;font-weight:700}
.paths-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
a.path{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);
  border-top:3px solid var(--gold);border-radius:14px;padding:18px 18px 16px;
  box-shadow:0 1px 2px rgba(16,35,58,.04);transition:.18s}
a.path:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(16,35,58,.10)}
a.path b{display:block;font-size:13.5px;color:var(--navy);margin-bottom:6px}
a.path span{display:block;font-family:var(--serif);font-size:15px;color:var(--gold2);margin-bottom:7px}
a.path em{display:block;font-style:normal;font-size:12.5px;line-height:1.5;color:var(--muted)}

/* ---------------- CONTENIDO ---------------- */
main{max-width:1020px;margin:0 auto;padding:64px 28px 100px}
section.sec{scroll-margin-top:20px}
.sec{padding:38px 0 52px;border-top:1px solid var(--line)}
.sec:first-child{border-top:0;padding-top:14px}
.sec.sub{padding-top:58px;padding-bottom:14px;border-top:0}
.sechead{display:flex;gap:26px;align-items:flex-start;margin-bottom:24px}
.secnum{font-family:var(--serif);font-weight:800;font-size:64px;line-height:.9;color:transparent;
  -webkit-text-stroke:1.4px var(--gold2);min-width:96px;padding-top:4px}
.sec.sub .secnum{font-size:38px;-webkit-text-stroke:1px var(--gold2);min-width:64px;padding-top:2px}
.sctext{flex:1}
.kick{font-size:11px;letter-spacing:.38em;color:var(--gold2);text-transform:uppercase;margin-bottom:10px}
.sec h2{font-size:clamp(26px,3.4vw,40px);line-height:1.15;color:var(--navy);font-weight:800;max-width:760px}
.sec.sub h2{font-size:clamp(21px,2.4vw,28px)}
.dur{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold2);
  border:1px solid var(--line2);border-radius:999px;padding:7px 13px;white-space:nowrap;margin-top:6px;
  background:#fff}
.intro{font-family:var(--serif);font-size:19px;line-height:1.72;color:var(--navy2);
  border-left:3px solid var(--gold);padding-left:24px;margin:4px 0 30px;font-style:italic;max-width:820px}
.lead{font-size:18px;line-height:1.78;color:var(--navy2);background:var(--cream);
  border-radius:16px;padding:26px 30px;margin:8px 0 32px}
.lead strong{color:var(--gold2)}
.body{margin:0 0 20px;font-size:16px;line-height:1.74;max-width:880px}
.quote{position:relative;margin:38px 0;padding:28px 38px 28px 78px;font-family:var(--serif);
  font-style:italic;font-size:21.5px;line-height:1.55;color:var(--navy);background:#FDFBF6;
  border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.quote::before{content:"“";position:absolute;left:22px;top:2px;font-size:90px;line-height:1;
  color:var(--gold);opacity:.55;font-style:normal}

/* lo esencial */
.ess{background:linear-gradient(180deg,#FCF8EE,#F9F2E3);border:1px solid #E8DCC3;
  border-left:4px solid var(--gold);border-radius:16px;padding:20px 26px 16px;margin:2px 0 34px;
  break-inside:avoid}
.ess-title{font-size:10.5px;letter-spacing:.3em;color:var(--gold2);text-transform:uppercase;
  font-weight:700;margin-bottom:12px}
.ess ul{columns:2;column-gap:40px;margin:0;padding:0;list-style:none}
.ess li{break-inside:avoid;padding:6px 0 6px 24px;position:relative;font-size:14.2px;line-height:1.55;
  color:var(--ink)}
.ess li::before{content:"›";position:absolute;left:4px;top:6px;color:var(--gold2);font-weight:800;font-size:16px}

/* KPI */
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:32px 0 38px}
.kpi{background:linear-gradient(160deg,#132A44,#0D1E32);border:1px solid rgba(198,161,91,.25);
  border-radius:18px;padding:22px 24px;position:relative;overflow:hidden}
.kpi::after{content:"";position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--gold),rgba(198,161,91,0))}
.kv{font-family:var(--serif);font-weight:800;font-size:28px;color:#EDDDBF;line-height:1.05}
.kl{font-size:10.5px;letter-spacing:.22em;color:var(--gold);text-transform:uppercase;margin:9px 0 8px}
.kd{font-size:13px;line-height:1.55;color:rgba(230,236,240,.8)}

/* TABLAS */
.tbl-wrap{overflow-x:auto;margin:26px 0 12px;border:1px solid var(--line);border-radius:16px;
  background:#fff;box-shadow:0 1px 0 rgba(16,35,58,.04)}
table.tbl{width:100%;border-collapse:collapse;font-size:14.2px}
.tbl thead th{background:var(--navy);color:#F3EEE3;text-align:left;font-weight:600;
  font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;padding:14px 16px}
.tbl tbody td{padding:12.5px 16px;border-top:1px solid #F2ECE2;vertical-align:top;line-height:1.6}
.tbl tbody tr:nth-child(even) td{background:#FCFAF5}
.tbl tbody tr.hl td{background:#F6EDDB;border-top:2px solid var(--gold);font-weight:700}
.tbl tbody tr.hl td:first-child{color:var(--navy)}
.tbl td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--navy)}
.tnote{font-size:13px;color:var(--muted);font-style:italic;margin:4px 6px 26px}

/* CALLOUTS */
.callout{border-radius:16px;padding:24px 28px;margin:30px 0;border:1px solid;border-left-width:5px}
.callout .co-title{font-weight:700;color:var(--navy);margin-bottom:8px;font-size:16px}
.callout .co-body{font-size:15px;color:var(--ink)}
.callout .co-body li{margin:6px 0}
.callout.info{background:#F0F6FB;border-color:#C3D7E7;border-left-color:var(--blue)}
.callout.warn{background:#FCF4E6;border-color:#EDD9B8;border-left-color:var(--amber)}
.callout.success{background:#EFF6F1;border-color:#C9DECF;border-left-color:var(--green)}
.callout.tip{background:#F9F3E7;border-color:#EADBB8;border-left-color:var(--gold)}

/* GRID */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:30px 0 38px}
.gcard{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px 24px 22px;
  position:relative;box-shadow:0 1px 2px rgba(16,35,58,.05);transition:.18s}
.gcard:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(16,35,58,.08)}
.gicon{font-size:26px;margin-bottom:13px}
.gcard h3{font-family:var(--sans);font-weight:700;font-size:15px;color:var(--navy);margin-bottom:9px;line-height:1.35}
.gcard p{font-size:13.8px;line-height:1.65;color:var(--muted);margin:0}

/* STEPS */
.steps{list-style:none;margin:28px 0;padding:0}
.steps li{display:flex;gap:18px;padding:15px 4px;border-bottom:1px dashed var(--line)}
.sn{font-family:var(--serif);font-weight:800;font-size:21px;color:transparent;
  -webkit-text-stroke:1px var(--gold2);min-width:42px;line-height:1.15}
.sb strong{display:block;font-size:15.5px;margin-bottom:4px}
.sb p{margin:2px 0 0;font-size:14.2px;color:var(--muted)}

/* CHECKLIST */
.checks{list-style:none;padding:0;margin:22px 0 30px;columns:2;column-gap:44px}
.checks li{display:flex;gap:12px;padding:9px 0;break-inside:avoid;font-size:14.6px;line-height:1.6}
.ck{min-width:21px;height:21px;border:1.5px solid var(--gold2);border-radius:7px;margin-top:2px;position:relative}
.ck::after{content:"✓";position:absolute;left:3px;top:-3px;color:var(--gold2);font-weight:800;font-size:15px}

/* CHART */
.chart{margin:34px 0 38px}
.chart figcaption{font-size:11.5px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold2);
  margin-bottom:20px;font-weight:600}
.donut-row{display:flex;align-items:center;gap:44px;flex-wrap:wrap}
.donut{width:250px;height:250px;border-radius:50%;position:relative;flex-shrink:0}
.donut::before{content:"";position:absolute;inset:0;border-radius:50%;background:var(--g);
  -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 44px),#000 calc(100% - 43px));
  mask:radial-gradient(farthest-side,transparent calc(100% - 44px),#000 calc(100% - 43px))}
.donut-in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;color:var(--navy)}
.dv{font-family:var(--serif);font-weight:800;font-size:23px;color:var(--navy)}
.dl{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:5px;max-width:132px}
.legend{list-style:none;margin:0;padding:0;flex:1;min-width:280px}
.legend li{display:flex;align-items:center;gap:13px;padding:8px 0;border-bottom:1px dashed var(--line);
  font-size:14px;color:var(--ink)}
.sw{width:12px;height:12px;border-radius:3px;flex-shrink:0}
.ll{flex:1}
.lp{font-weight:700;color:var(--navy);font-variant-numeric:tabular-nums}
.bars{display:flex;flex-direction:column;gap:14px}
.bar-row{display:grid;grid-template-columns:minmax(150px,34%) 1fr 110px;gap:14px;align-items:center}
.bar-label{font-size:13.2px;color:var(--muted);text-align:right;line-height:1.4}
.bar-track{height:21px;background:var(--cream);border-radius:9px;overflow:hidden}
.bar-fill{height:100%;border-radius:9px}
.bar-val{font-weight:700;color:var(--navy);font-size:14px;font-variant-numeric:tabular-nums}
.line-wrap{max-width:650px}
.line-wrap svg{width:100%;height:auto;display:block}

/* TIMELINE */
.timeline{list-style:none;margin:28px 0;padding:0;position:relative}
.timeline li{display:grid;grid-template-columns:110px 26px 1fr;gap:0 18px;padding:0 0 24px}
.period{font-size:11px;letter-spacing:.1em;color:#fff;background:var(--navy2);border-radius:999px;
  text-align:center;padding:8px 8px;height:fit-content;text-transform:uppercase;font-weight:600}
.tl-dot{width:13px;height:13px;border-radius:50%;background:var(--gold);margin-top:9px;
  box-shadow:0 0 0 4px #F3E9D6;position:relative;z-index:1}
.timeline li:not(:last-child)::before{content:"";position:absolute;left:126px;top:32px;bottom:0;
  width:1px;background:var(--line);margin-left:-6px}
.tl-body{padding-top:2px}
.tl-body strong{display:block;font-size:15.5px;color:var(--navy);margin-bottom:4px}
.tl-body p{margin:0;font-size:14.2px;color:var(--muted)}

/* TWOCOL */
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:28px 0}
.col{border:1px solid var(--line);border-radius:18px;padding:24px 26px;background:#fff}
.col h4{font-family:var(--sans);font-weight:700;font-size:15px;color:var(--navy);margin-bottom:14px}
.bullets{margin:0;padding:0;list-style:none}
.bullets li{position:relative;padding:7px 0 7px 22px;font-size:14.4px;color:var(--ink);line-height:1.62}
.bullets li::before{content:"•";position:absolute;left:4px;color:var(--gold2);font-weight:800}

/* PIE */
.colophon{border-top:1px solid var(--line);background:#FDFBF6}
.colophon-in{max-width:1020px;margin:0 auto;padding:46px 28px;display:flex;gap:28px;flex-wrap:wrap;
  justify-content:space-between;font-size:13px;color:var(--muted)}
.colophon b{color:var(--navy)}
.brk{page-break-after:always}

/* BOTONES */
.print-btn{position:fixed;right:22px;bottom:22px;z-index:50;background:var(--navy);color:#F3EEE3;
  border:1px solid rgba(198,161,91,.6);border-radius:999px;padding:14px 24px;font:600 14px var(--sans);
  letter-spacing:.06em;cursor:pointer;box-shadow:0 8px 24px rgba(16,35,58,.28);transition:.18s}
.print-btn:hover{background:var(--navy2);transform:translateY(-2px)}
.top-btn{position:fixed;right:26px;bottom:84px;z-index:50;width:44px;height:44px;border-radius:50%;
  background:#fff;border:1px solid var(--line2);color:var(--navy);font-size:19px;font-weight:700;
  cursor:pointer;box-shadow:0 6px 18px rgba(16,35,58,.16);opacity:0;pointer-events:none;transition:.2s}
.top-btn.show{opacity:1;pointer-events:auto}
.top-btn:hover{background:var(--cream);transform:translateY(-2px)}
#pbar{position:fixed;top:0;left:0;height:3px;width:0;z-index:60;
  background:linear-gradient(90deg,var(--gold2),var(--gold));transition:width .12s}

@media (max-width:900px){
  .kpis,.grid{grid-template-columns:1fr 1fr}
  .toc-grid{grid-template-columns:1fr}
  .paths-row{grid-template-columns:1fr 1fr}
  .checks{columns:1}
  .twocol{grid-template-columns:1fr}
  .bar-row{grid-template-columns:1fr;gap:5px}
  .bar-label{text-align:left}
  .secnum{font-size:44px;min-width:70px}
  .cover-mid,.cover-top,.cover-bottom{padding-left:34px;padding-right:34px}
}
@media (max-width:600px){
  .kpis,.grid,.paths-row{grid-template-columns:1fr}
  .cover-points{gap:20px}
  .ess ul{columns:1}
}

@media print{
  body{background:#fff;font-size:11pt}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .print-btn,.top-btn,#pbar{display:none}
  main{max-width:100%;padding:0}
  .cover{min-height:235mm;page-break-after:always}
  .toc{page-break-after:always}
  .toc-in{padding:12mm 0 10mm}
  .sec{page-break-before:always;padding:0 0 10mm}
  .sec,.sec.sub{padding-top:0}
  .kpis,.grid,.twocol,.donut-row,.ess{page-break-inside:avoid}
  .tbl-wrap,.callout,.quote,.chart{page-break-inside:avoid}
  .checks li{break-inside:avoid}
  .toc-grid{grid-template-columns:1fr 1fr}
  .paths-row{grid-template-columns:1fr 1fr;page-break-inside:avoid}
  .kv{font-size:20pt}
  a{color:inherit;text-decoration:none}
  .cover::before{font-size:320px}
}
"""

def build_html():
    global _MINS
    _MINS = {}
    for secs in [SECTION_1, SECTION_2, SECTION_3, SECTION_4, SECTION_5, SECTION_6,
                 SECTION_7, SECTION_8, SECTION_9, SECTION_10, SECTION_11, SECTION_12,
                 SECTION_13, SECTION_14, SECTION_15, SECTION_16, SECTION_17, SECTION_18,
                 SECTION_19, SECTION_20, SECTION_21, SECTION_22]:
        _MINS.update(estimate_minutes(secs))
    entries = toc_entries()
    toc_items = "".join(
        f'<a class="ti" href="#s{num}"><span class="tn">{num}</span><span>'
        f'<span class="tt">{_html.escape(title)}</span><div class="tk">{_html.escape(kicker)}</div></span></a>'
        for num, kicker, title in entries)
    sections = []
    for secs in [SECTION_1, SECTION_2, SECTION_3, SECTION_4, SECTION_5, SECTION_6,
                 SECTION_7, SECTION_8, SECTION_9, SECTION_10, SECTION_11, SECTION_12,
                 SECTION_13, SECTION_14, SECTION_15, SECTION_16, SECTION_17, SECTION_18,
                 SECTION_19, SECTION_20, SECTION_21, SECTION_22]:
        sections.append("".join(render_block(b) for b in secs))
    m = META
    total_min = sum(v for k, v in _MINS.items() if k.count(".") == 0)
    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KHC · Plan de Negocio — Tienda de moda infantil, Oleiros</title>
<style>{font_css()}
{CSS}
</style>
</head>
<body>
<div class="cover">
  <div class="cover-frame"></div>
  <div class="cover-top">
    <div class="cover-brand"><span class="dot">KHC</span> KHC · MARCA PROPIA</div>
    <div class="cover-tag">Oleiros — A Coruña</div>
  </div>
  <div class="cover-mid">
    <div class="cover-kicker">Plan de negocio</div>
    <h1>Una tienda de ropa infantil<br>con <em>marca propia</em></h1>
    <div class="cover-rule"></div>
    <p class="cover-sub">{m["subtitle"]} · fabricación directa con etiqueta KHC, rotación rápida,
    e-commerce propio y marketing local desde el primer día. Todo el plan, los números y el
    calendario para abrir en {m["location"]}.</p>
    <div class="cover-points">
      <div class="cp"><b>21.010 €</b><span>inversión total</span></div>
      <div class="cp"><b>~70 %</b><span>margen bruto</span></div>
      <div class="cp"><b>1.670 €/mes</b><span>gastos fijos</span></div>
      <div class="cp"><b>92 €/día</b><span>punto de equilibrio</span></div>
    </div>
    <p class="cover-scope">Incluye proyección de ingresos a 5 años, plan de tesorería,
    análisis de sensibilidad, DAFO y cuadro de mando.</p>
  </div>
  <div class="cover-bottom">
    <span><b>{m["edition"]}</b></span>
    <span>{m["location"]}</span>
    <span>{m["confidential"]}</span>
  </div>
</div>

<nav class="toc"><div class="toc-in">
  <div class="toc-kick">Contenido</div>
  <h3 class="toc-title">Índice del plan</h3>
  <p class="toc-stats">22 secciones · {total_min} min de lectura · cada sección abre con su resumen de 20 segundos</p>
  <div class="toc-grid">{toc_items}</div>
  <div class="paths">
    <div class="paths-title">Cómo leer este plan</div>
    <div class="paths-row">
      <a href="#s06" class="path"><b>📊 Solo números</b><span>06 · 07 · 08 · 10 · 11 · 12 · 13</span><em>Revisar cifras, decidir inversión o preparar financiación</em></a>
      <a href="#s22" class="path"><b>🏛 Para la solicitud de ayudas</b><span>02.2 · 02.3 · 05 · 17 · 22</span><em>Lo que evalúan IGAPE, Consellería y Emigración</em></a>
      <a href="#s18" class="path"><b>🚀 Para arrancar esta semana</b><span>02.1 · 17 · 18 · 19 · 21</span><em>Local, ayudas, pedido a China y plan B</em></a>
      <a href="#s01" class="path"><b>📖 Lectura completa</b><span>01 → 22</span><em>Todo el plan, para vosotros y como documento adjunto</em></a>
    </div>
  </div>
</div></nav>

<main>
{''.join(sections).replace('<div class="brk"></div>', '')}
</main>

<footer class="colophon"><div class="colophon-in">
  <div><b>KHC · Plan de Negocio</b><br>{m["subtitle"]} — {m["location"]}</div>
  <div><b>{m["edition"]}</b><br>Generado desde <code>scripts/</code> · cálculos en <code>calculos/</code></div>
  <div>{m["confidential"]}<br>Verificar convocatorias, normativa y precios antes de invertir.</div>
</div></footer>

<div id="pbar"></div>
<button class="print-btn" onclick="window.print()">🖨 Imprimir / Guardar PDF</button>
<button class="top-btn" id="topBtn" aria-label="Volver arriba">↑</button>
<script>
const pbar = document.getElementById('pbar');
const topBtn = document.getElementById('topBtn');
const onScroll = () => {{
  const h = document.documentElement;
  const max = h.scrollHeight - h.clientHeight;
  pbar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  topBtn.classList.toggle('show', h.scrollTop > 700);
}};
document.addEventListener('scroll', onScroll, {{passive:true}}); onScroll();
topBtn.addEventListener('click', () => window.scrollTo({{top:0, behavior:'smooth'}}));
</script>
</body>
</html>"""
    return doc
