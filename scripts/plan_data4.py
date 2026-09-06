# -*- coding: utf-8 -*-
"""Sección 22 · Ficha resumen para solicitudes de ayudas y subvenciones."""
from plan_data import (S, P, LEAD, QUOTE, KPIS, TABLE, CALLOUT, GRID, STEPS,
                       CHECKBOXES, DONUT, BARS, LINE, TIMELINE, TWOCOL,
                       PAGEBREAK, SPACER, COLORS)

SECTION_22 = [
    S("22", "FICHA PARA CONVOCATORIAS", "Resumen de 1 página listo para formularios",
      "Esta ficha sintetiza el proyecto en el formato que piden los formularios de ayudas (IGAPE, Consellería de Emprego, Secretaría Xeral da Emigración, Ayuntamiento de A Coruña, Kit Digital). Rellena los datos, imprime esta página y adjúntala al plan completo."),

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
            ["N° de empleos que se crean", "1,0 en el año 1 · 1,5 en el año 3 · 2,0 en el año 5"],
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
            ["Ventas previstas año 1 (escenario base)", "32.960 €"],
            ["Resultado antes de impuestos año 1", "+2.260 €"],
            ["Ventas previstas año 5", "70.000 €"],
            ["Margen bruto medio", "≈ 70 %"],
            ["Punto de equilibrio", "2.390 €/mes ≈ 92 €/día"],
            ["VAN al 5 % (5 años)", "+36.920 €"],
            ["TIR", "42,0 %"],
            ["Plazo de recuperación", "2,6 años"],
        ],
        widths=[0.62, 0.38], left_cols=[0, 1],
    ),

    P("**Ayudas y subvenciones que se van a solicitar (por orden de prioridad):**"),
    TABLE(
        ["Ayuda", "Órgano", "Importe estimado", "Estado"],
        [
            ["Cuota cero de Galicia (nuevos autónomos)", "IGAPE / Xunta de Galicia", "Devolución de cuotas hasta 2 años", "A solicitar antes del alta"],
            ["Tarifa plana de autónomos", "Seguridad Social", "Ahorro ~1.800–2.600 € primer año", "Automática al darse de alta"],
            ["Ayudas a personas retornadas (autoempleo)", "Secretaría Xeral da Emigración", "3.000–10.000 €", "A solicitar al llegar / antes del alta"],
            ["Subvención a la modernización del comercio", "Consellería de Economía, Empresa e Innovación", "30–50 % de reforma y equipamiento", "Convocatoria anual"],
            ["Kit Digital (web, e-commerce, redes, TPV)", "Red.es / acelerapyme", "Bono 2.000–12.000 €", "Convocatorias continuas"],
            ["Programas de apoyo a mujeres emprendedoras", "Instituto de la Mujer / Xunta", "Microcréditos o subvenciones", "Según convocatoria"],
        ],
        widths=[0.34, 0.24, 0.24, 0.18], left_cols=[0],
    ),
    CALLOUT("success", "Pendiente antes de presentar la solicitud",
            "Confirmar el **nombre y NIE/DNI de la promotora**, el **CNAE definitivo** con el gestor, la **ficha catastral y referencia del local** si ya está elegido, los **presupuestos** (reforma, mobiliario, pedido a China) y el **certificado de emigrante retornado**. Con todo eso, la solicitud se presenta en 2–3 horas."),
]
