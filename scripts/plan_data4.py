# -*- coding: utf-8 -*-
"""Sección 22 · Ficha resumen para solicitudes de ayudas y subvenciones."""
from plan_data import (S, P, LEAD, QUOTE, KPIS, TABLE, CALLOUT, GRID, STEPS,
                       CHECKBOXES, DONUT, BARS, LINE, TIMELINE, TWOCOL,
                       PAGEBREAK, SPACER, COLORS)

SECTION_22 = [
    S("22", "FICHA PARA CONVOCATORIAS", "Resumen de 1 página listo para formularios",
      "Esta ficha sintetiza el proyecto en el formato que piden los formularios de ayudas (IGAPE, Consellería de Emprego, Secretaría Xeral da Emigración, Ayuntamiento de A Coruña, Kit Digital). Rellena los datos, imprime esta página y adjúntala al plan completo.",
      ess=["Una página lista para formularios de ayudas", "Identificación, resumen económico y ayudas a solicitar", "Pendiente: nombre, CNAE, presupuestos y certificado de retornada", "Adjuntar al plan completo al presentar"]),

    P("**Datos identificativos del proyecto:**"),
    TABLE(
        ["Campo", "Dato"],
        [
            ["Nombre del proyecto", "KHC — Tienda de moda infantil con marca propia"],
            ["Actividad (CNAE orientativo)", "4771: Comercio al por menor de prendas de vestir · 4778: ropa y artículos de bebé · 4791: venta por internet"],
            ["Forma jurídica", "Persona física (autónoma) — la promotora; paso a SL previsto a partir de 60.000 €/año"],
            ["Persona promotora / titular", "[Nombre] — mujer emprendedora, retornada de Venezuela (ayudas a emigrantes retornados)"],
            ["Ubicación del negocio", "Oleiros (A Coruña, Galicia) — zona de Santa Cruz / Perillo / Bastiagueiro"],
            ["Forma de acceso al local", "Alquiler: ~750 €/mes, local de 40–50 m²"],
            ["N.º de empleos que se crean", "1,0 en el año 1 · 1,5 en el año 4 · 1,6 en el año 5"],
            ["Público objetivo", "Familias con niños de 0–12 años de Oleiros y área de A Coruña (+ venta online a toda España)"],
            ["Fecha prevista de inicio", "[Mes/año] — apertura prevista 4–7 meses después de la firma del local"],
            ["Fase del proyecto", "Pre-apertura: local en búsqueda, presupuesto cerrado, proveedor en selección"],
        ],
        widths=[0.30, 0.70], left_cols=[0],
    ),

    P("**Resumen económico (todas las cifras de este plan):**"),
    TABLE(
        ["Concepto", "Importe"],
        [
            ["Inversión total para abrir", "21.010 €"],
            ["— de la cual: stock inicial completo", "8.690 €"],
            ["— de la cual: fondo de maniobra", "4.000 €"],
            ["Gastos fijos mensuales", "1.670 €/mes"],
            ["Ventas previstas año 1 (escenario base)", "47.000 €"],
            ["Resultado antes de impuestos año 1 (con sueldo pagado)", "+2.460 €"],
            ["Ventas previstas año 5", "95.000 €"],
            ["Margen bruto medio", "≈ 70 %"],
            ["Punto de equilibrio", "2.390 €/mes ≈ 92 €/día"],
            ["VAN al 5 % (5 años, sueldo pagado)", "+13.710 €"],
            ["TIR", "21,1 %"],
            ["Plazo de recuperación", "3,5 años"],
            ["Retribución promotora", "800 €/mes año 1 → 1.300 → 1.550 → 1.800 → 2.100 €/mes año 5 — regla de la sección 8.3"],
        ],
        widths=[0.62, 0.38], left_cols=[0, 1],
    ),

    P("**Ayudas que se van a solicitar** (importes, órganos y plazos en la sección 17, sin repetirlos aquí):"),
    CHECKBOXES([
        "**Cuota cero de Galicia** (IGAPE) — nuevos autónomos, devolución de cuotas hasta 2 años",
        "**Tarifa plana de autónomos** (Seguridad Social) — 80 €/mes el primer año",
        "**Ayudas a personas retornadas** (Secretaría Xeral da Emigración) — autoempleo, 3.000–10.000 €",
        "**Modernización del comercio minorista** (Consellería de Economía) — 30–50 % de reforma y equipamiento",
        "**Kit Digital** (Red.es) — web, e-commerce, redes y TPV",
        "**Programas de apoyo a mujeres emprendedoras** (Instituto de la Mujer / Xunta)",
    ]),
    CALLOUT("success", "Pendiente antes de presentar la solicitud",
            "Confirmar el **nombre y NIE/DNI de la promotora**, el **CNAE definitivo** con el gestor, la **ficha catastral y referencia del local** si ya está elegido, los **presupuestos** (reforma, mobiliario, pedido a China) y el **certificado de emigrante retornado**. Con todo eso, la solicitud se presenta en 2–3 horas."),
]
