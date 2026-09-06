# -*- coding: utf-8 -*-
"""Renderiza el plan de negocio KHC como documento HTML premium autocontenido."""
import base64
import os
import re
import html as _html

from plan_data import META, COLORS
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
        return (
            f'<section class="sec {"" if not sub else "sub"}" id="s{b["num"]}">'
            f'<header class="sechead"><div class="secnum">{b["num"]}</div>'
            f'<div class="sctext"><div class="kick">{b["kicker"]}</div><h2>{b["title"]}</h2></div></header>'
            + (f'<p class="intro">{inline(b["intro"])}</p>' if b.get("intro") else "")
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
  --serif:'Playfair-Regular','Playfair Display',Georgia,serif;
  --sans:'Inter-Regular',-apple-system,'Segoe UI',Roboto,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--sans);font-size:15.5px;line-height:1.62;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--serif);font-weight:600;margin:0}
svg text{font-family:'Inter-V',var(--sans)}
strong{font-weight:700;color:var(--navy)}
em{color:var(--navy2)}

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
.cover-mid{flex:1;display:flex;flex-direction:column;justify-content:center;padding:0 64px;max-width:900px}
.cover-kicker{font-size:12px;letter-spacing:.5em;color:var(--gold);text-transform:uppercase;margin-bottom:22px}
.cover h1{font-size:clamp(44px,7vw,86px);line-height:1.04;font-weight:800;color:#FBF7EE;margin:0 0 26px}
.cover h1 em{font-style:italic;font-weight:400;color:#E9D9BB}
.cover-sub{max-width:560px;font-size:17px;line-height:1.7;color:rgba(235,239,241,.82)}
.cover-rule{width:120px;height:3px;background:var(--gold);margin:34px 0 30px}
.cover-points{display:flex;gap:38px;flex-wrap:wrap}
.cp{min-width:150px;border-left:2px solid rgba(198,161,91,.5);padding-left:14px}
.cp b{display:block;font-family:var(--serif);font-size:21px;color:#F1E7D4;font-weight:700}
.cp span{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:rgba(235,239,241,.65)}
.cover-bottom{display:flex;gap:26px;flex-wrap:wrap;padding:0 64px 46px;font-size:11px;
  letter-spacing:.18em;text-transform:uppercase;color:rgba(235,239,241,.6)}
.cover-bottom span b{color:#E9D9BB;font-weight:600}

/* ---------------- ÍNDICE ---------------- */
.toc{background:#FDFBF6;border-bottom:1px solid var(--line)}
.toc-in{max-width:1020px;margin:0 auto;padding:70px 28px 80px}
.toc-title{font-size:34px;color:var(--navy);margin-bottom:6px}
.toc-kick{font-size:11px;letter-spacing:.4em;color:var(--gold2);text-transform:uppercase;margin-bottom:34px}
.toc-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 40px}
a.ti{display:flex;align-items:baseline;gap:16px;padding:11px 4px;text-decoration:none;
  color:var(--ink);border-bottom:1px dashed var(--line);transition:.18s}
a.ti:hover{background:var(--cream);padding-left:12px;color:var(--navy)}
.tn{font-family:var(--serif);font-weight:800;font-size:19px;color:var(--gold2);min-width:46px}
.tt{font-weight:600;color:var(--navy);font-size:14px;line-height:1.35}
.tk{font-size:10.5px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase;margin-top:2px}

/* ---------------- CONTENIDO ---------------- */
main{max-width:1020px;margin:0 auto;padding:56px 28px 90px}
.sec{padding:34px 0 46px;border-top:1px solid var(--line)}
.sec:first-child{border-top:0;padding-top:10px}
.sec.sub{padding-top:52px;padding-bottom:14px;border-top:0}
.sechead{display:flex;gap:26px;align-items:flex-start;margin-bottom:22px}
.secnum{font-family:var(--serif);font-weight:800;font-size:64px;line-height:.9;color:transparent;
  -webkit-text-stroke:1.4px var(--gold2);min-width:96px;padding-top:4px}
.sec.sub .secnum{font-size:38px;-webkit-text-stroke:1px var(--gold2);min-width:64px;padding-top:2px}
.kick{font-size:11px;letter-spacing:.38em;color:var(--gold2);text-transform:uppercase;margin-bottom:10px}
.sec h2{font-size:clamp(26px,3.4vw,40px);line-height:1.15;color:var(--navy);font-weight:800;max-width:820px}
.sec.sub h2{font-size:clamp(21px,2.4vw,28px)}
.intro{font-family:var(--serif);font-size:18.5px;line-height:1.72;color:var(--navy2);
  border-left:3px solid var(--gold);padding-left:22px;margin:4px 0 30px;font-style:italic}
.lead{font-size:17.5px;line-height:1.75;color:var(--navy2);background:var(--cream);
  border-radius:14px;padding:24px 28px;margin:8px 0 30px}
.lead strong{color:var(--gold2)}
.body{margin:0 0 18px;font-size:15.5px;line-height:1.7}
.quote{position:relative;margin:34px 0;padding:26px 34px 26px 74px;font-family:var(--serif);
  font-style:italic;font-size:21px;line-height:1.5;color:var(--navy);background:#FDFBF6;
  border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.quote::before{content:"“";position:absolute;left:22px;top:2px;font-size:84px;line-height:1;
  color:var(--gold);opacity:.55;font-style:normal}

/* KPI */
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:30px 0 34px}
.kpi{background:linear-gradient(160deg,#132A44,#0D1E32);border:1px solid rgba(198,161,91,.25);
  border-radius:16px;padding:20px 22px;position:relative;overflow:hidden}
.kpi::after{content:"";position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--gold),rgba(198,161,91,0))}
.kv{font-family:var(--serif);font-weight:800;font-size:27px;color:#EDDDBF;line-height:1.05}
.kl{font-size:10.5px;letter-spacing:.22em;color:var(--gold);text-transform:uppercase;margin:8px 0 7px}
.kd{font-size:12.5px;line-height:1.5;color:rgba(230,236,240,.78)}

/* TABLAS */
.tbl-wrap{overflow-x:auto;margin:22px 0 10px;border:1px solid var(--line);border-radius:14px;
  background:#fff;box-shadow:0 1px 0 rgba(16,35,58,.04)}
table.tbl{width:100%;border-collapse:collapse;font-size:13.8px}
.tbl thead th{background:var(--navy);color:#F3EEE3;text-align:left;font-weight:600;
  font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;padding:13px 14px}
.tbl tbody td{padding:11px 14px;border-top:1px solid #F0EAE0;vertical-align:top;line-height:1.5}
.tbl tbody tr:nth-child(even) td{background:#FBF8F1}
.tbl tbody tr.hl td{background:#F4EAD8;border-top:2px solid var(--gold);font-weight:700}
.tbl tbody tr.hl td:first-child{color:var(--navy)}
.tbl td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tnote{font-size:12.5px;color:var(--muted);font-style:italic;margin:2px 4px 22px}

/* CALLOUTS */
.callout{border-radius:14px;padding:20px 24px;margin:26px 0;border:1px solid;border-left-width:5px}
.callout .co-title{font-weight:700;color:var(--navy);margin-bottom:6px;font-size:15px}
.callout .co-body{font-size:14px;color:var(--ink)}
.callout .co-body li{margin:4px 0}
.callout.info{background:#EFF5FA;border-color:#BFD4E5;border-left-color:var(--blue)}
.callout.warn{background:#FCF3E5;border-color:#EBD7B5;border-left-color:var(--amber)}
.callout.success{background:#EEF5F0;border-color:#C6DCCC;border-left-color:var(--green)}
.callout.tip{background:#F8F2E6;border-color:#E9D8B4;border-left-color:var(--gold)}

/* GRID */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:28px 0 34px}
.gcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 22px 20px;
  position:relative;box-shadow:0 1px 2px rgba(16,35,58,.05)}
.gicon{font-size:24px;margin-bottom:12px}
.gcard h3{font-family:var(--sans);font-weight:700;font-size:14.5px;color:var(--navy);margin-bottom:8px;line-height:1.3}
.gcard p{font-size:13.2px;line-height:1.6;color:var(--muted);margin:0}

/* STEPS */
.steps{list-style:none;margin:26px 0;padding:0;counter-reset:none}
.steps li{display:flex;gap:18px;padding:13px 4px;border-bottom:1px dashed var(--line)}
.sn{font-family:var(--serif);font-weight:800;font-size:20px;color:transparent;
  -webkit-text-stroke:1px var(--gold2);min-width:40px;line-height:1.15}
.sb strong{display:block;font-size:15px;margin-bottom:3px}
.sb p{margin:2px 0 0;font-size:13.6px;color:var(--muted)}

/* CHECKLIST */
.checks{list-style:none;padding:0;margin:20px 0 28px;columns:2;column-gap:40px}
.checks li{display:flex;gap:12px;padding:8px 0;break-inside:avoid;font-size:14px}
.ck{min-width:20px;height:20px;border:1.5px solid var(--gold2);border-radius:6px;margin-top:2px;position:relative}
.ck::after{content:"✓";position:absolute;left:3px;top:-3px;color:var(--gold2);font-weight:800;font-size:14px}

/* CHART */
.chart{margin:30px 0 34px}
.chart figcaption{font-size:11.5px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold2);
  margin-bottom:18px;font-weight:600}
.donut-row{display:flex;align-items:center;gap:40px;flex-wrap:wrap}
.donut{width:250px;height:250px;border-radius:50%;position:relative;flex-shrink:0}
.donut::before{content:"";position:absolute;inset:0;border-radius:50%;background:var(--g);
  -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 44px),#000 calc(100% - 43px));
  mask:radial-gradient(farthest-side,transparent calc(100% - 44px),#000 calc(100% - 43px))}
.donut-in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;color:var(--navy)}
.dv{font-family:var(--serif);font-weight:800;font-size:22px;color:var(--navy)}
.dl{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:4px;max-width:130px}
.legend{list-style:none;margin:0;padding:0;flex:1;min-width:280px}
.legend li{display:flex;align-items:center;gap:12px;padding:7px 0;border-bottom:1px dashed var(--line);
  font-size:13.5px;color:var(--ink)}
.sw{width:12px;height:12px;border-radius:3px;flex-shrink:0}
.ll{flex:1}
.lp{font-weight:700;color:var(--navy);font-variant-numeric:tabular-nums}
.bars{display:flex;flex-direction:column;gap:13px}
.bar-row{display:grid;grid-template-columns:minmax(150px,34%) 1fr 110px;gap:14px;align-items:center}
.bar-label{font-size:12.8px;color:var(--muted);text-align:right;line-height:1.35}
.bar-track{height:20px;background:var(--cream);border-radius:8px;overflow:hidden}
.bar-fill{height:100%;border-radius:8px}
.bar-val{font-weight:700;color:var(--navy);font-size:13.5px;font-variant-numeric:tabular-nums}
.line-wrap{max-width:640px}
.line-wrap svg{width:100%;height:auto;display:block}

/* TIMELINE */
.timeline{list-style:none;margin:26px 0;padding:0;position:relative}
.timeline li{display:grid;grid-template-columns:110px 26px 1fr;gap:0 18px;padding:0 0 22px}
.period{font-size:11px;letter-spacing:.1em;color:#fff;background:var(--navy2);border-radius:999px;
  text-align:center;padding:7px 8px;height:fit-content;text-transform:uppercase;font-weight:600}
.tl-dot{width:13px;height:13px;border-radius:50%;background:var(--gold);margin-top:8px;
  box-shadow:0 0 0 4px #F3E9D6;position:relative;z-index:1}
.timeline li:not(:last-child)::before{content:"";position:absolute;left:126px;top:30px;bottom:0;
  width:1px;background:var(--line);margin-left:-6px}
.tl-body{padding-top:2px}
.tl-body strong{display:block;font-size:15px;color:var(--navy);margin-bottom:3px}
.tl-body p{margin:0;font-size:13.8px;color:var(--muted)}

/* TWOCOL */
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:26px 0}
.col{border:1px solid var(--line);border-radius:16px;padding:22px 24px;background:#fff}
.col h4{font-family:var(--sans);font-weight:700;font-size:14.5px;color:var(--navy);margin-bottom:12px}
.bullets{margin:0;padding:0;list-style:none}
.bullets li{position:relative;padding:6px 0 6px 20px;font-size:13.6px;color:var(--ink);line-height:1.55}
.bullets li::before{content:"•";position:absolute;left:4px;color:var(--gold2);font-weight:800}

/* PIE */
.colophon{border-top:1px solid var(--line);background:#FDFBF6}
.colophon-in{max-width:1020px;margin:0 auto;padding:44px 28px;display:flex;gap:28px;flex-wrap:wrap;
  justify-content:space-between;font-size:12.5px;color:var(--muted)}
.colophon b{color:var(--navy)}
.brk{page-break-after:always}
.toc{padding:0}

@media (max-width:860px){
  .kpis,.grid{grid-template-columns:1fr 1fr}
  .toc-grid{grid-template-columns:1fr}
  .checks{columns:1}
  .twocol{grid-template-columns:1fr}
  .bar-row{grid-template-columns:1fr;gap:5px}
  .bar-label{text-align:left}
  .secnum{font-size:44px;min-width:70px}
  .cover-mid,.cover-top,.cover-bottom{padding-left:34px;padding-right:34px}
}
@media (max-width:560px){
  .kpis,.grid{grid-template-columns:1fr}
  .cover-points{gap:20px}
}

/* BOTÓN imprimir/PDF */
.print-btn{position:fixed;right:22px;bottom:22px;z-index:50;background:var(--navy);color:#F3EEE3;
  border:1px solid rgba(198,161,91,.6);border-radius:999px;padding:13px 22px;font:600 13.5px var(--sans);
  letter-spacing:.06em;cursor:pointer;box-shadow:0 8px 24px rgba(16,35,58,.28);transition:.18s}
.print-btn:hover{background:var(--navy2);transform:translateY(-2px)}

@media print{
  body{background:#fff;font-size:11pt}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .print-btn{display:none}
  main{max-width:100%;padding:0}
  .cover{min-height:235mm;page-break-after:always}
  .toc{page-break-after:always}
  .toc-in{padding:12mm 0 10mm}
  .sec{page-break-before:always;padding:0 0 10mm}
  .sec,.sec.sub{padding-top:0}
  .kpis,.grid,.twocol,.donut-row{page-break-inside:avoid}
  .tbl-wrap,.callout,.quote,.chart{page-break-inside:avoid}
  .checks li{break-inside:avoid}
  .toc-grid{grid-template-columns:1fr 1fr}
  .kv{font-size:20pt}
  a{color:inherit;text-decoration:none}
  .cover::before{font-size:320px}
}
"""

def build_html():
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
  <div class="toc-grid">{toc_items}</div>
</div></nav>

<main>
{''.join(sections).replace('<div class="brk"></div>', '')}
</main>

<footer class="colophon"><div class="colophon-in">
  <div><b>KHC · Plan de Negocio</b><br>{m["subtitle"]} — {m["location"]}</div>
  <div><b>{m["edition"]}</b><br>Generado desde <code>scripts/</code> · cálculos en <code>calculos/</code></div>
  <div>{m["confidential"]}<br>Verificar convocatorias, normativa y precios antes de invertir.</div>
</div></footer>

<button class="print-btn" onclick="window.print()">🖨 Imprimir / Guardar PDF</button>
</body>
</html>"""
    return doc
