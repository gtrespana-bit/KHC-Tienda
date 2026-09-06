# -*- coding: utf-8 -*-
"""Renderiza el plan de negocio KHC como PDF premium A4 con reportlab + svglib."""
import io
import os
import re
import unicodedata

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, KeepTogether,
                                NextPageTemplate, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from svglib.svglib import svg2rlg

from plan_data import (META, COLORS, estimate_minutes,
                    SECTION_1, SECTION_2, SECTION_3, SECTION_4, SECTION_5)
from plan_data2 import (SECTION_6, SECTION_7, SECTION_8, SECTION_9, SECTION_15,
                        SECTION_16, SECTION_17, SECTION_18, SECTION_19, SECTION_21)
from plan_data3 import (SECTION_10, SECTION_11, SECTION_12, SECTION_13,
                        SECTION_14, SECTION_20)
from plan_data4 import SECTION_22
from plan_charts import donut_svg_doc, bars_svg, line_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")

PAGE_W, PAGE_H = A4
LM = RM = 18 * mm
TM = 20 * mm
BM = 17 * mm
FRAME_W = PAGE_W - LM - RM

C = {k: HexColor(v) for k, v in COLORS.items()}

# ------------------------------------------------------------------ utilidades

def register_fonts():
    ff = {
        "Inter": ("Inter-Regular.ttf", "Inter-Medium.ttf", "Inter-SemiBold.ttf", "Inter-Regular.ttf"),
        "InterB": ("Inter-Bold.ttf", "Inter-ExtraBold.ttf", "Inter-ExtraBold.ttf", "Inter-Bold.ttf"),
        "Playfair": ("Playfair-Regular.ttf", "Playfair-SemiBold.ttf", "Playfair-ExtraBold.ttf", "Playfair-Italic.ttf"),
        "InterSB": ("Inter-SemiBold.ttf", "Inter-Bold.ttf", "Inter-Bold.ttf", "Inter-SemiBold.ttf"),
    }
    names = {}
    for base, (normal, bold, bolditalic, italic) in ff.items():
        nrm = f"{base}-N"
        bld = f"{base}-B"
        bldit = f"{base}-BI"
        itl = f"{base}-I"
        pdfmetrics.registerFont(TTFont(nrm, os.path.join(FONTS, normal)))
        pdfmetrics.registerFont(TTFont(bld, os.path.join(FONTS, bold)))
        pdfmetrics.registerFont(TTFont(bldit, os.path.join(FONTS, bolditalic)))
        pdfmetrics.registerFont(TTFont(itl, os.path.join(FONTS, italic)))
        pdfmetrics.registerFontFamily(base, normal=nrm, bold=bld, italic=itl, boldItalic=bldit)
        names[base] = (nrm, bld, itl)
    return names

F = register_fonts()
FONT = "Inter"
FONTB = "InterB"
FONT_SB = "InterSB"
SERIF = "Playfair"
FN = "Inter-N"
FB = "InterB-N"
FSB = "InterSB-N"
PN = "Playfair-N"
PB = "Playfair-B"
PI = "Playfair-I"

EMOJI_MAP = {"✅": "(mejor)", "❌": "(no)", "🟡": "", "🟢": "", "🔴": "", "🎉": ""}

def clean(t):
    t = "".join(EMOJI_MAP.get(ch, ch) for ch in t)
    t = "".join(ch for ch in t
                if not (0x1F000 <= ord(ch) <= 0x1FAFF)
                and not (0x2600 <= ord(ch) <= 0x27BF)
                and not (0x1D100 <= ord(ch) <= 0x1DBFF))
    t = t.replace("\ufe0f", "")
    t = t.replace("≈", "~")
    t = re.sub(r"[ \t]{2,}", " ", t).strip()
    return t

NUM_RE = re.compile(r"^[\d\s.,€%×x−\-–+—/·~≈]*\d[\d\s.,€%×x−\-–+—/·~≈]*$")

def is_num_cell(cell):
    c = clean(cell).strip()
    return bool(c) and NUM_RE.match(c.replace("*", "").replace("<", "").replace(">", "")) is not None

def rl_markup(s):
    s = clean(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", s)
    s = s.replace("<ol>", "").replace("</ol>", "").replace("<ul>", "").replace("</ul>", "")
    s = s.replace("<li>", "<br/>• ").replace("</li>", "")
    s = s.replace("<strong>", "<b>").replace("</strong>", "</b>")
    s = s.replace("<em>", "<i>").replace("</em>", "</i>")
    s = s.replace("<code>", "").replace("</code>", "")
    return s

def style(name, **kw):
    base = dict(fontName=FN, fontSize=8.6, leading=12.6, textColor=C["ink"],
                alignment=TA_JUSTIFY, spaceAfter=5)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "body": style("body", fontSize=9.1, leading=13.6, alignment=TA_LEFT, spaceAfter=7),
    "lead": style("lead", fontName=PN, fontSize=12.2, leading=17.2, textColor=C["navy2"],
                  alignment=TA_LEFT, spaceAfter=11),
    "intro": style("intro", fontName=PN, fontSize=10.8, leading=15.6, textColor=C["navy2"],
                   alignment=TA_LEFT, spaceAfter=10),
    "cell": style("cell", fontSize=7.9, leading=11.2, alignment=TA_LEFT, spaceAfter=0),
    "cellc": style("cellc", fontSize=7.9, leading=11.2, alignment=TA_CENTER, spaceAfter=0),
    "cellr": style("cellr", fontSize=7.9, leading=11.2, alignment=TA_CENTER, spaceAfter=0),
    "head": style("head", fontName=FB, fontSize=7.1, leading=9.4, textColor=colors.white,
                  alignment=TA_LEFT, spaceAfter=0),
    "callout_t": style("callout_t", fontName=FN, fontSize=9.2, leading=12.2, textColor=C["navy"],
                       alignment=TA_LEFT, spaceAfter=2),
    "callout_b": style("callout_b", fontSize=8.3, leading=12.2, alignment=TA_LEFT, spaceAfter=0),
    "note": style("note", fontName=FN, fontSize=7.4, leading=10.4, textColor=C["muted"],
                  alignment=TA_LEFT, spaceAfter=9),
    "ess_title": style("ess_title", fontName=FB, fontSize=7.0, leading=9.4, textColor=C["gold2"],
                       alignment=TA_LEFT, spaceAfter=0),
    "ess_b": style("ess_b", fontSize=8.5, leading=12.4, alignment=TA_LEFT, spaceAfter=0),
    "quote": style("quote", fontName=f"{SERIF}-I", fontSize=12.4, leading=17, textColor=C["navy"],
                   alignment=TA_CENTER, spaceAfter=0),
    "chartcap": style("chartcap", fontName=FN, fontSize=6.9, leading=9.0, textColor=C["gold2"],
                      alignment=TA_LEFT, spaceAfter=7),
}

def P(text, st=S["body"]):
    return Paragraph(rl_markup(text), st)

# ------------------------------------------------------------ flowables propios

class SecHeader(Flowable):
    def __init__(self, num, kicker, title, sub=False, mins=None):
        super().__init__()
        self.num, self.kicker, self.title, self.sub, self.mins = num, kicker, title, sub, mins

    def wrap(self, aw, ah):
        self.width, self.height = aw, 40 if self.sub else 56
        return (aw, self.height)

    def draw(self):
        c = self.canv
        x0 = 0
        sp_text(c, x0, self.height - 8, clean(self.kicker).upper(), f"{FONT_SB}-N", 6.4, 1.8, C["gold2"])
        # número
        c.setFillColor(C["gold"])
        c.setFont(f"{SERIF}-B", 17 if self.sub else 21)
        c.drawString(x0, self.height - 28 if not self.sub else self.height - 30, self.num)
        # título
        c.setFillColor(C["navy"])
        c.setFont(f"{SERIF}-B", 15.5 if self.sub else 18.5)
        tw = c.stringWidth(clean(self.title), f"{SERIF}-B", 15.5 if self.sub else 18.5)
        msg = clean(self.title)
        maxw = self.width - 46
        if tw > maxw:
            lines = []
            cur = ""
            for word in msg.split(" "):
                if c.stringWidth((cur + " " + word).strip(), f"{SERIF}-B", 15.5 if self.sub else 18.5) > maxw and cur:
                    lines.append(cur)
                    cur = word
                else:
                    cur = (cur + " " + word).strip()
            lines.append(cur)
            y = self.height - 30
            for ln in lines[:2]:
                c.drawString(x0 + 46, y, ln)
                y -= 14
        else:
            c.drawString(x0 + 46, self.height - 30, msg)
        # chip de lectura
        if self.mins and not self.sub:
            sp_text(c, self.width, self.height - 8,
                    f"LECTURA  ~{self.mins} MIN", f"{FONT}-B", 5.9, 1.1, C["gold2"], align="r")
        # regla
        c.setStrokeColor(C["line"])
        c.setLineWidth(0.5)
        c.line(x0, 6, self.width, 6)

class KpiGrid(Flowable):
    def __init__(self, items, width):
        super().__init__()
        self.items = items
        self.full_w = width
        self.cols = 3
        self.gap = 9
        self.cw = (width - self.gap * (self.cols - 1)) / self.cols

    def wrap(self, aw, ah):
        rows = (len(self.items) + self.cols - 1) // self.cols
        lines = []
        for i in range(len(self.items)):
            det = clean(self.items[i][2])
            n = len(self._split(det, 7.0, self.cw - 22))
            lines.append(max(2, n))
        max_lines = max(lines)
        self.h = 58 + (max_lines - 2) * 9.2
        self.h *= rows
        self.h += self.gap * (rows - 1)
        self.height, self.width = self.h, aw
        return (aw, self.h)

    def _split(self, text, size, maxw):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            if pdfmetrics.stringWidth((cur + " " + w).strip(), f"{FONT}-N", size) > maxw and cur:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        return lines

    def draw(self):
        c = self.canv
        rh = self.h
        rows = (len(self.items) + self.cols - 1) // self.cols
        row_h = (rh - self.gap * (rows - 1)) / rows
        for idx, (val, lab, det) in enumerate(self.items):
            r, cc = divmod(idx, self.cols)
            x = cc * (self.cw + self.gap)
            y = self.height - (r + 1) * row_h - r * self.gap
            c.setFillColor(C["navy"])
            c.roundRect(x, y, self.cw, row_h, 5, stroke=0, fill=1)
            c.setFillColor(C["gold"])
            c.rect(x, y + row_h - 2.6, self.cw, 2.6, stroke=0, fill=1)
            c.setFillColor(HexColor("#EDDDBF"))
            c.setFont(f"{SERIF}-B", 13.6)
            c.drawString(x + 11, y + row_h - 22, clean(val))
            sp_text(c, x + 11, y + row_h - 31.5, clean(lab).upper(), f"{FONT}-B", 5.9, 0.7, C["gold"])
            c.setFillColor(HexColor("#D9E1E8"))
            c.setFont(f"{FONT}-N", 7.0)
            lines = self._split(clean(det), 7.0, self.cw - 22)[:3]
            ty = y + row_h - 41.5
            for ln in lines:
                c.drawString(x + 11, ty, ln)
                ty -= 9.2

class Quote(Flowable):
    def __init__(self, text, width):
        super().__init__()
        self.text, self.w = text, width

    def wrap(self, aw, ah):
        lines = self._split(clean(self.text), 12.4, aw - 60)
        self.height = 22 + len(lines) * 17
        self.width = aw
        return (aw, self.height)

    def _split(self, text, size, maxw):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            if pdfmetrics.stringWidth((cur + " " + w).strip(), f"{SERIF}-I", size) > maxw and cur:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        return lines

    def draw(self):
        c = self.canv
        c.setStrokeColor(C["line"])
        c.setLineWidth(0.6)
        c.line(0, 4, self.width, 4)
        c.line(0, self.height - 4, self.width, self.height - 4)
        c.setFillColor(C["gold"])
        c.setFont(f"{SERIF}-B", 22)
        c.drawString(6, self.height - 34, "“")
        c.setFillColor(C["navy"])
        c.setFont(f"{SERIF}-I", 12.4)
        y = self.height - 18
        for ln in self._split(clean(self.text), 12.4, self.width - 60):
            c.drawCentredString(self.width / 2 + 12, y, ln)
            y -= 17

def svg_to_flow(svg, width):
    drawing = svg2rlg(io.StringIO(svg))
    h = float(svg.split('height="')[1].split('"')[0])
    s = width / drawing.width
    drawing.scale(s, s)          # escalar el contenido (svglib no lo hace al fijar width/height)
    drawing.width = width
    drawing.height = h * s
    return drawing

# ------------------------------------------------------------------ contenido

def donut_block(b, aw):
    data = [(v, c) for l, v, c in b["data"]]
    svg = donut_svg_doc(data, 250)
    d = svg_to_flow(svg, 250)
    total = sum(v for _, v, _ in b["data"]) or 1
    rows = []
    for label, value, color in b["data"]:
        pct = value / total * 100
        rows.append([Paragraph(rl_markup(label), S["cell"]),
                     Paragraph(f"<b>{value:,.0f}</b>".replace(",", ".") + " €", S["cellr"]),
                     Paragraph(f"{pct:.1f} %", S["cellr"])])
    leg = Table(rows, colWidths=[aw - 264 - 106, 58, 48])
    leg.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, C["line"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    grid = Table([[d, leg]], colWidths=[250 + 14, aw - 250 - 14])
    grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    out = [Paragraph(clean(b["title"]).upper(), S["chartcap"]), grid]
    if b.get("note"):
        out.append(Spacer(1, 4)); out.append(P(b["note"], S["note"]))
    return out

def bars_block(b, aw):
    short = []
    for l, v, c in b["data"]:
        if len(l) > 44:
            l = l[:41] + "…"
        short.append((l, v, c))
    label_w = 258 if any(len(l) > 40 for l, _, _ in short) else 196
    svg = bars_svg(short, aw, label_w=label_w, font="Inter-N", vfont="InterB-N")
    out = [Paragraph(clean(b["title"]).upper(), S["chartcap"]), svg_to_flow(svg, aw)]
    if b.get("note"):
        out.append(Spacer(1, 4)); out.append(P(b["note"], S["note"]))
    return out

def line_block(b, aw):
    svg = line_svg(b["labels"], b["series"], aw, font="Inter-N")
    out = [Paragraph(clean(b["title"]).upper(), S["chartcap"]), svg_to_flow(svg, aw)]
    if b.get("note"):
        out.append(Spacer(1, 4)); out.append(P(b["note"], S["note"]))
    return out


def essence_block(b, aw):
    """Recuadro 'Lo esencial' — resumen de 20 segundos al inicio de cada sección."""
    items = [x for x in (b.get("ess") or [])]
    if not items:
        return []
    rows = []
    half = (len(items) + 1) // 2
    for i in range(half):
        left = items[i]
        right = items[i + half] if i + half < len(items) else ""
        lt = Paragraph(f"<font color='#A58142'>›</font>&nbsp;&nbsp;{rl_markup(left)}", S["ess_b"]) if left else ""
        rt = Paragraph(f"<font color='#A58142'>›</font>&nbsp;&nbsp;{rl_markup(right)}", S["ess_b"]) if right else ""
        rows.append([lt, rt])
    title = Paragraph("LO ESENCIAL — LEER EN 20 SEGUNDOS", S["ess_title"])
    t = Table([[title, ""], *rows], colWidths=[(aw - 26) / 2, (aw - 26) / 2])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FBF6EA")),
        ("BOX", (0, 0), (-1, -1), 0.6, HexColor("#E8DCC3")),
        ("LINEBEFORE", (0, 0), (0, -1), 3, C["gold"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("TOPPADDING", (0, 1), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 13),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, HexColor("#E8DCC3")),
        ("LINEBEFORE", (int((len(rows) or 1) > 0), 0), (int((len(rows) or 1) > 0), -1), 0.5, HexColor("#E8DCC3")),
    ]))
    return [KeepTogether([Spacer(1, 2), t, Spacer(1, 10)])]

def table_block(b, aw):
    cols = b["cols"]
    widths = b.get("widths")
    if widths:
        cw = [w * aw for w in widths]
    else:
        cw = [aw / len(cols)] * len(cols)
    data = [[Paragraph(clean(c).upper(), S["head"]) for c in cols]]
    for row in b["rows"]:
        cells = []
        for j, cell in enumerate(row):
            st = S["cellr"] if is_num_cell(cell) and j not in (b.get("left") or []) else S["cell"]
            cells.append(Paragraph(rl_markup(cell), st))
        data.append(cells)
    t = Table(data, colWidths=cw, repeatRows=1)
    sty = [
        ("BACKGROUND", (0, 0), (-1, 0), C["navy"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6.5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, C["line"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#FCFAF5")]),
    ]
    for r in b.get("hl") or []:
        sty += [("BACKGROUND", (0, r + 1), (-1, r + 1), HexColor("#F4EAD8")),
                ("LINEABOVE", (0, r + 1), (-1, r + 1), 1.2, C["gold"])]
    t.setStyle(TableStyle(sty))
    out = [t]
    if b.get("note"):
        out.append(Spacer(1, 4)); out.append(P(b["note"], S["note"]))
    else:
        out.append(Spacer(1, 6))
    return out

def callout_block(b, aw):
    tones = {"info": ("#EFF5FA", "#BFD4E5", C["blue"]),
             "warn": ("#FCF3E5", "#EBD7B5", C["amber"]),
             "success": ("#EEF5F0", "#C6DCCC", C["green"]),
             "tip": ("#F8F2E6", "#E9D8B4", C["gold"])}
    bg, edge, lc = tones.get(b["tone"], tones["info"])
    body = f"<b>{rl_markup(b['title'])}</b><br/>{rl_markup(b['html'])}"
    t = Table([[Paragraph(body, S["callout_b"])]], colWidths=[aw])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(bg)),
        ("BOX", (0, 0), (-1, -1), 0.6, HexColor(edge)),
        ("LINEBEFORE", (0, 0), (0, -1), 3, lc),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]

def grid_block(b, aw):
    items = b["items"]
    cols = 3
    cw = (aw - 14 * (cols - 1)) / cols
    rows = []
    for i in range(0, len(items), cols):
        row = []
        for icon, title, text in items[i:i + cols]:
            txt = f"<b>{rl_markup(title)}</b><br/><font color='#5B6875'>{rl_markup(text)}</font>"
            row.append(Paragraph(txt, S["cell"]))
        while len(row) < cols:
            row.append("")
        rows.append(row)
    t = Table(rows, colWidths=[cw] * cols)
    sty = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.5, C["line"]),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C["line"]),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ]
    t.setStyle(TableStyle(sty))
    return [Spacer(1, 4), t, Spacer(1, 8)]

def steps_block(b, aw):
    rows = []
    for i, (title, text) in enumerate(b["items"], 1):
        num = Paragraph(f"<font color='#A58142'><b>{i:02d}</b></font>", S["cellc"])
        body = f"<b>{rl_markup(title)}</b>" + (f"<br/><font color='#5B6875'>{rl_markup(text)}</font>" if text else "")
        rows.append([num, Paragraph(body, S["cell"])])
    t = Table(rows, colWidths=[26, aw - 26])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, C["line"]),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]

def check_block(b, aw):
    rows = [[Paragraph("<font color='#A58142'><b>•</b></font>", S["cell"]),
             Paragraph(rl_markup(item), S["cell"])] for item in b["items"]]
    t = Table(rows, colWidths=[13, aw - 13])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 6)]

def timeline_block(b, aw):
    rows = []
    for period, title, text in b["items"]:
        p = Paragraph(f"<b>{rl_markup(period).upper()}</b>", S["head"])
        body = f"<b>{rl_markup(title)}</b><br/><font color='#5B6875'>{rl_markup(text)}</font>"
        rows.append([p, Paragraph("<font color='#C6A15B'><b>•</b></font>", S["cell"]), Paragraph(body, S["cell"])])
    t = Table(rows, colWidths=[88, 18, aw - 106])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), C["navy2"]),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (0, -1), 6),
        ("RIGHTPADDING", (0, 0), (0, -1), 6),
        ("LEFTPADDING", (1, 0), (-1, -1), 8),
        ("RIGHTPADDING", (1, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, C["line"]),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]

def twocol_block(b, aw):
    def col(title, items):
        body = f"<b>{rl_markup(title)}</b>" + "".join(f"<br/>• {rl_markup(i)}" for i in items)
        return Paragraph(body, S["cell"])
    cw = (aw - 12) / 2
    t = Table([[col(b["lt"], b["li"]), col(b["rt"], b["ri"])]], colWidths=[cw, cw])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.5, C["line"]),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C["line"]),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]

def kpis_block(b):
    return [Spacer(1, 4), KpiGrid(b["items"], FRAME_W - 4), Spacer(1, 10)]

def quote_block(b, aw):
    return [Spacer(1, 10), Quote(b["text"], FRAME_W), Spacer(1, 12)]

def blocks_to_story(blocks, story, aw, mins_map=None):
    mins_map = mins_map or {}
    for idx, b in enumerate(blocks):
        t = b["t"]
        if t == "section":
            sub = b["num"].count(".") > 0
            if not sub:
                story.append(PageBreak())
                story.append(SecHeader(b["num"], b["kicker"], b["title"], sub=sub,
                                       mins=mins_map.get(b["num"])))
                if b.get("intro"):
                    story.append(Spacer(1, 5))
                    story.append(P(b["intro"], S["intro"]))
                story += essence_block(b, aw)
            else:
                story.append(Spacer(1, 8))
                story.append(SecHeader(b["num"], b["kicker"], b["title"], sub=sub))
                if b.get("intro"):
                    story.append(Spacer(1, 5))
                    story.append(P(b["intro"], S["intro"]))
                story.append(Spacer(1, 2))
        elif t == "lead":
            story.append(P(b["html"], S["lead"]))
            story.append(Spacer(1, 6))
        elif t == "p":
            story.append(P(b["html"], S["body"]))
            story.append(Spacer(1, 2))
        elif t == "quote":
            story += quote_block(b, aw)
        elif t == "kpis":
            story += kpis_block(b)
        elif t == "table":
            story += table_block(b, aw)
        elif t == "donut":
            story += donut_block(b, aw)
        elif t == "bars":
            story += bars_block(b, aw)
        elif t == "line":
            story += line_block(b, aw)
        elif t == "callout":
            story += callout_block(b, aw)
        elif t == "grid":
            story += grid_block(b, aw)
        elif t == "steps":
            story += steps_block(b, aw)
        elif t == "check":
            story += check_block(b, aw)
        elif t == "timeline":
            story += timeline_block(b, aw)
        elif t == "twocol":
            story += twocol_block(b, aw)
        elif t == "spacer":
            story.append(Spacer(1, b["pts"]))

# --------------------------------------------------------------------- página


def sp_text(c, x, y, txt, font, size, space, color, align="l"):
    """Texto con tracking (letterspacing) y alineación izquierda/derecha/centro."""
    txt = clean(txt)
    w = pdfmetrics.stringWidth(txt, font, size) + (space * max(len(txt) - 1, 0))
    if align == "r":
        x = x - w
    elif align == "c":
        x = x - w / 2
    t = c.beginText(x, y)
    t.setFont(font, size)
    if space:
        t.setCharSpace(space)
    t.setFillColor(color)
    t.textOut(txt)
    c.drawText(t)
    # resetear el tracking del stream (reportlab no lo limpia solo)
    if space:
        r = c.beginText(0, 0)
        r.setCharSpace(0)
        r.textOut("")
        c.drawText(r)

def draw_cover(canv, doc):
    canv.saveState()
    w, h = PAGE_W, PAGE_H
    canv.setFillColor(C["navy"])
    canv.rect(0, 0, w, h, stroke=0, fill=1)
    # halo decorativo
    canv.setFillColor(HexColor("#1B3A5C"))
    canv.circle(w * 0.86, h * 0.88, 210, stroke=0, fill=1)
    canv.setFillAlpha(0.5)
    canv.setFillColor(HexColor("#22476B"))
    canv.circle(w * 0.06, h * 0.10, 170, stroke=0, fill=1)
    canv.setFillAlpha(1)
    # marca de agua
    canv.setFillColor(HexColor("#C6A15B"))
    canv.setFillAlpha(0.07)
    canv.setFont(f"{SERIF}-B", 190)
    canv.drawString(w - 320, 40, "KHC")
    canv.setFillAlpha(1)
    # marco dorado
    canv.setStrokeColor(HexColor("#C6A15B"))
    canv.setStrokeAlpha(0.45)
    canv.setLineWidth(0.6)
    canv.rect(24, 24, w - 48, h - 48, stroke=1, fill=0)
    canv.setStrokeAlpha(1)
    # top
    sp_text(canv, 52, h - 66, "KHC · MARCA PROPIA", f"{FONT}-B", 7.6, 2.4, HexColor("#F1E7D4"))
    sp_text(canv, w - 52, h - 66, "OLEIROS — A CORUÑA", f"{FONT}-N", 6.8, 1.6, HexColor("#AFA99B"), align="r")
    # bloque central
    sp_text(canv, 52, h - 215, "PLAN DE NEGOCIO", f"{FONT}-B", 7.8, 3.6, C["gold"])
    canv.setFillColor(HexColor("#FBF7EE"))
    canv.setFont(f"{SERIF}-B", 42)
    canv.drawString(52, h - 268, "Una tienda de ropa")
    canv.drawString(52, h - 315, "infantil con")
    canv.setFont(f"{SERIF}-I", 42)
    canv.setFillColor(HexColor("#E9D9BB"))
    canv.drawString(52, h - 362, "marca propia")
    canv.setStrokeColor(C["gold"])
    canv.setLineWidth(2.4)
    canv.line(52, h - 398, 172, h - 398)
    canv.setFillColor(HexColor("#D9E1E8"))
    canv.setFont(f"{FONT}-N", 9.2)
    t = clean("Tienda de moda infantil 0–12 años · fabricación directa con etiqueta KHC, rotación rápida, e-commerce propio y marketing local desde el día uno.")
    lines = t.split("  ")
    if len(lines) == 1:
        from reportlab.lib.utils import simpleSplit as _ss
        lines = _ss(t, f"{FONT}-N", 9.2, 220)[:3]
    canv.setFont(f"{FONT}-N", 9.2)
    canv.setFillColor(HexColor("#D9E1E8"))
    yy = h - 428
    for ln in lines[:2]:
        canv.drawString(52, yy, ln)
        yy -= 14
    # puntos clave
    points = [("21.010 €", "INVERSIÓN TOTAL"), ("~70 %", "MARGEN BRUTO"),
              ("1.670 €/mes", "GASTOS FIJOS"), ("92 €/día", "EQUILIBRIO")]
    x = 52
    for val, lab in points:
        canv.setFillColor(C["gold"])
        canv.rect(x, h - 505, 1.6, 34, stroke=0, fill=1)
        canv.setFillColor(HexColor("#F1E7D4"))
        canv.setFont(f"{SERIF}-B", 12.5)
        canv.drawString(x + 10, h - 496, val)
        sp_text(canv, x + 10, h - 508, lab, f"{FONT}-B", 5.6, 1.0, HexColor("#AFA99B"))
        x += 128
    # pie
    canv.setStrokeColor(HexColor("#C6A15B"))
    canv.setStrokeAlpha(0.35)
    canv.setLineWidth(0.5)
    canv.line(52, 70, w - 52, 70)
    canv.setStrokeAlpha(1)
    sp_text(canv, 52, 52, "OLEIROS · A CORUÑA", f"{FONT}-N", 6.6, 1.2, HexColor("#AFA99B"))
    sp_text(canv, w / 2, 52, "SEPTIEMBRE 2026 · V1.4", f"{FONT}-N", 6.6, 1.2, HexColor("#AFA99B"), align="c")
    sp_text(canv, w - 52, 52, "DOCUMENTO DE TRABAJO", f"{FONT}-N", 6.6, 1.2, HexColor("#AFA99B"), align="r")
    canv.restoreState()

def draw_content(canv, doc):
    canv.saveState()
    w, h = PAGE_W, PAGE_H
    sp_text(canv, LM, h - 34, "KHC · PLAN DE NEGOCIO", f"{FONT}-N", 6.4, 1.4, C["gold2"])
    canv.setFillColor(C["muted"])
    canv.setFont(f"{FONT}-N", 6.4)
    canv.drawRightString(w - RM, h - 34, "Marca propia · Oleiros · A Coruña")
    canv.setStrokeColor(C["line"])
    canv.setLineWidth(0.5)
    canv.line(LM, h - 38, w - RM, h - 38)
    # pie
    canv.setFont(f"{FONT}-N", 6.4)
    canv.setFillColor(C["muted"])
    canv.drawString(LM, 30, "Documento de trabajo — verificar cifras antes de invertir")
    canv.setFillColor(C["gold2"])
    canv.setFont(f"{FONT}-B", 6.8)
    canv.drawRightString(w - RM, 30, f"{doc.page}")
    canv.restoreState()

SHORT_TITLES = {
 "01":"Resumen ejecutivo","02":"El proyecto","02.1":"Ubicación","03":"Mercado y cliente",
 "03.1":"Competencia","04":"Producto y surtido","04.1":"Qué no se trae","05":"Fabricación y suministro",
 "05.1":"Fábricas y agentes","05.2":"MOQ y plazos","05.3":"Calidad y pagos",
 "05.4":"Fabricar vs comprar","05.5":"Checklist del pedido","06":"Inversión inicial",
 "07":"Gastos fijos","08":"Márgenes y equilibrio","08.1":"Escenarios de venta",
 "08.2":"Fondo de maniobra","08.3":"¿Cuándo cobra la propietaria?","09":"Visión de crecimiento","09.1":"Las palancas","11.1":"Rentabilidad de la inversión",
 "10":"Proyección de ingresos","11":"Proyección a 5 años","12":"Plan de tesorería",
 "13":"Sensibilidad y escenarios","14":"DAFO y plan estratégico","14.1":"Objetivos medibles",
 "15":"Marketing y ventas","16":"Forma jurídica","17":"Ayudas y financiación",
 "18":"Hoja de ruta","19":"Riesgos y plan B","20":"Cuadro de mando","21":"Anexos y próximos pasos","22":"Ficha para convocatorias",
}

class PlanDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, SecHeader):
            text = f"{flowable.num} · {SHORT_TITLES.get(flowable.num, clean(flowable.title))}"
            self.notify("TOCEntry", (0, text, self.page))
            key = f"sec{flowable.num}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, 0, 0)

# ------------------------------------------------------------------- documento

def build_pdf(out_path):
    sections = [SECTION_1, SECTION_2, SECTION_3, SECTION_4, SECTION_5, SECTION_6,
                SECTION_7, SECTION_8, SECTION_9, SECTION_10, SECTION_11, SECTION_12,
                SECTION_13, SECTION_14, SECTION_15, SECTION_16, SECTION_17, SECTION_18,
                SECTION_19, SECTION_20, SECTION_21, SECTION_22]

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName=f"{FONT}-N", fontSize=8.4, leading=11.8,
                       textColor=C["ink"], leftIndent=0, spaceBefore=1.5),
        ParagraphStyle("toc1", fontName=f"{FONT}-N", fontSize=7.6, leading=10.4,
                       textColor=C["muted"], leftIndent=16, spaceBefore=2),
    ]
    toc.dotsMinLevel = 0

    # tiempo de lectura por sección
    mins_map = {}
    for secs in sections:
        mins_map.update(estimate_minutes(secs))

    story = []
    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # --- página de índice
    story.append(Spacer(1, 10))
    story.append(P("CONTENIDO", S["chartcap"]))
    story.append(Paragraph("Índice del plan", style("ind_t", fontName="Playfair-B", fontSize=17,
                                                    leading=22, textColor=C["navy"],
                                                    alignment=TA_LEFT, spaceAfter=3)))
    total_min = sum(v for k, v in mins_map.items() if k.count(".") == 0)
    story.append(Paragraph(f"<font color='#A58142'><i>22 secciones · {total_min} minutos de lectura · "
                           f"cada sección abre con su resumen de 20 segundos</i></font>",
                           style("ind_sub", fontName=f"{SERIF}-I", fontSize=8.8, leading=12,
                                 alignment=TA_LEFT, spaceAfter=12)))
    story.append(toc)
    story.append(Spacer(1, 16))

    # --- rutas de lectura
    story.append(P("CÓMO LEER ESTE PLAN", S["chartcap"]))
    paths = [
        ["Ruta", "Secciones", "Para qué sirve"],
        ["**Solo números**", "06 · 07 · 08 · 10 · 11 · 12 · 13", "Revisar cifras, decidir la inversión o preparar financiación"],
        ["**Para la solicitud de ayudas**", "02.2 · 02.3 · 05 · 17 · 22", "Lo que evalúan IGAPE, Consellería y Emigración"],
        ["**Para arrancar esta semana**", "02.1 · 17 · 18 · 19 · 21", "Local, ayudas, pedido a China y plan B"],
        ["**Lectura completa**", "01 → 22", "Todo el plan, para vosotros y como documento adjunto"],
    ]
    pt = Table([[Paragraph(clean(c).upper(), S["head"]) for c in paths[0]]] +
               [[Paragraph(rl_markup(c), S["cell"]) for c in row] for row in paths[1:]],
               colWidths=[FRAME_W * 0.20, FRAME_W * 0.30, FRAME_W * 0.50], repeatRows=1)
    pt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C["navy"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, C["line"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#FCFAF5")]),
    ]))
    story.append(pt)

    for secs in sections:
        blocks_to_story(secs, story, FRAME_W, mins_map)

    doc = PlanDoc(out_path, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM,
                  bottomMargin=BM, title="KHC · Plan de Negocio",
                  author="KHC — Tienda de ropa infantil", subject="Plan de negocio KHC, Oleiros")
    frame = Frame(LM, BM, FRAME_W, PAGE_H - TM - BM, id="content",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover",
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="Content", frames=[frame], onPage=draw_content),
    ])
    doc.multiBuild(story)
    return out_path
