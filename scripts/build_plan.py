# -*- coding: utf-8 -*-
"""
Genera las dos versiones del Plan de Negocio KHC:
  docs/KHC_Plan_Negocio_Premium.html  (versión visual para pantalla, autocontenida)
  docs/KHC_Plan_Negocio_Premium.pdf   (versión imprimible premium A4)

Uso:
  python3 scripts/build_plan.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import html_render
import pdf_render


def main():
    out_html = os.path.join(ROOT, "docs", "KHC_Plan_Negocio_Premium.html")
    out_pdf = os.path.join(ROOT, "docs", "KHC_Plan_Negocio_Premium.pdf")

    doc = html_render.build_html()
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(doc)
    size = os.path.getsize(out_html)
    print(f"HTML  -> {out_html} ({size/1024:.0f} KB)")

    pdf_render.build_pdf(out_pdf)
    size = os.path.getsize(out_pdf)
    print(f"PDF   -> {out_pdf} ({size/1024:.0f} KB)")
    print("Listo ✦")


if __name__ == "__main__":
    main()
