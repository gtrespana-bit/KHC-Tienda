# -*- coding: utf-8 -*-
"""Secciones 10–14 y 20 del Plan de Negocio KHC — análisis financiero completo."""
from plan_data import (S, P, LEAD, QUOTE, KPIS, TABLE, CALLOUT, GRID, STEPS,
                       CHECKBOXES, DONUT, BARS, LINE, TIMELINE, TWOCOL,
                       PAGEBREAK, SPACER, COLORS)

# ============================================================================
# SECCIÓN 10 · PROYECCIÓN DE INGRESOS MES A MES
# ============================================================================

# Cálculo mes a mes (apertura en enero, estacionalidad moda infantil real)
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
# Año 1 ampliado a un tamaño real de tienda: 5–6 clientes/día a ~27 € + online desde el mes 3
VENTAS_BASE = [2050, 2460, 3200, 3390, 4850, 3880, 2910, 2420, 5820, 4360, 5820, 5840]
CAJA_MES = [2965, 2217, 1987, 1890, 2815, 3061, 2628, 1852, 3456, 4038, 5642, 7260]
MES_GF = 1670        # gastos fijos de la tienda
MES_SUELDO = 800     # retribución de la promotora desde el mes 1 (sección 8.3)

def _rows_mensual():
    caja = 4000
    rows = []
    for i, v in enumerate(VENTAS_BASE):
        coste = round(v * 0.30)
        margen = v - coste
        res = margen - MES_GF - MES_SUELDO
        caja += res
        rows.append([MESES[i], f"{v:,}".replace(",", ".") + " €",
                     f"{coste:,}".replace(",", ".") + " €",
                     f"{margen:,}".replace(",", ".") + " €",
                     f"{res:+,}".replace(",", ".") + " €",
                     f"{caja:,}".replace(",", ".") + " €"])
    return rows

SECTION_10 = [
    S("10", "PROYECCIÓN DE INGRESOS", "Mes a mes: el año 1 con estacionalidad real",
      "Aquí se ve cómo se comporta la tienda a lo largo de un año completo: los meses flojos, los picos de Navidad y vuelta al cole, y cómo evoluciona la caja. Los supuestos se explican para que se puedan discutir o ajustar.",
      ess=["Año 1 completo mes a mes con estacionalidad real", "Picos: vuelta al cole y Navidad · valles: rebajas y agosto", "Caja mínima 1.850 € (agosto) y cierre con 7.260 €", "Sueldo de 800 €/mes desde el mes 1 y +2.460 € antes de impuestos"]),

    P("**Supuestos de la proyección (escenario base año 1):**"),
    CHECKBOXES([
        "**Apertura en enero** y curva de aprendizaje: los 4 primeros meses venden por debajo de la media anual (la tienda aún no se conoce)",
        "**Estacionalidad de la moda infantil en España:** septiembre (vuelta al cole) y noviembre–diciembre (Navidad y Reyes) son los picos; enero–febrero y julio–agosto, rebajas y vacaciones",
        "**Margen bruto medio del 70 %** sobre el coste real puesto en tienda (sección 8)",
        "**Gastos fijos de 1.670 €/mes** (sección 7) y **sueldo de la promotora de 800 €/mes desde el mes 1** (sección 8.3)",
        "**Ticket medio de 27 €** en tienda y 5–6 clientes/día en los meses normales",
        "**Tienda online** aporta desde el mes 3–4 un 10–15 % adicional sobre la base",
    ]),

    TABLE(
        ["Mes", "Ventas", "Mercancía (30 %)", "Margen bruto", "Resultado del mes", "Caja acumulada"],
        _rows_mensual() + [["**TOTAL AÑO 1**", "**47.000 €**", "**14.100 €**", "**32.900 €**", "**+3.260 €**", "**7.260 €**"]],
        widths=[0.12, 0.18, 0.18, 0.18, 0.17, 0.17], left_cols=[0, 1, 2, 3, 4, 5], hl=[12],
    ),
    P("*La caja acumulada parte de los 4.000 € de fondo de maniobra. Los meses 1–4 y julio–agosto son los más difíciles (mínimo de 1.850 € en agosto); de mayo a junio y de septiembre a diciembre la tienda se financia sola y genera el grueso del beneficio del año.*"),

    LINE("Evolución de la caja acumulada — año 1 (€, partiendo de 4.000 €)",
         MESES,
         [("Caja acumulada", CAJA_MES)],
         unit="€",
         note="La caja nunca baja de 1.850 € en el peor mes (agosto). El colchón de 5.000 € (fondo + reserva) cubre ese momento con 3.100 € de margen; después, cada mes de temporada alta devuelve el colchón."),

    P("**Lectura honesta de la tabla.** Con el sueldo de la promotora ya incluido (800 €/mes), el punto de equilibrio sube a **3.530 €/mes**, y no se supera con regularidad hasta mayo: la tienda arranca con 6 meses difíciles, que es lo normal en un comercio nuevo. Aun así la caja nunca baja de 1.850 € gracias al colchón, y el año se cierra con **+3.260 € operativos** (antes de sueldo: +12.860 €), 7.260 € de caja y el sueldo pagado los 12 meses. **La clave del año 1 no es ganar dinero cada mes, sino pagar el sueldo, no tocar la caja y acumular en los picos.**"),
]

# ============================================================================
# SECCIÓN 11 · PROYECCIÓN A 5 AÑOS Y CUENTA DE RESULTADOS
# ============================================================================

SECTION_11 = [
    S("11", "PROYECCIÓN A 5 AÑOS", "Cuenta de resultados prevista y rentabilidad",
      "La proyección a 5 años responde a las preguntas que hace cualquier convocatoria de ayudas: ¿cuánto se venderá, cuánto ganará la tienda, cuánto cobrará la promotora y cuándo se recupera la inversión? Aquí la retribución de la promotora **es un coste del negocio desde el año 1** — no un residuo.",
      ess=["Ventas: 47.000 € (año 1) → 95.000 € (año 5)", "Sueldo promotora: 800 €/mes año 1 → 2.100 €/mes año 5", "Beneficio neto: 2.090 € → 9.630 € (además del sueldo)", "VAN +13.710 € · TIR 21 % · payback 3,5 años (con sueldo pagado)"]),

    P("**Escenario base quinquenal (ventas físicas + online con crecimiento por fidelización y rotación):**"),
    TABLE(
        ["Concepto", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"],
        [
            ["Ventas (a € constantes)", "47.000 €", "58.000 €", "70.000 €", "82.000 €", "95.000 €"],
            ["Margen bruto aplicado", "70 %", "71 %", "72 %", "72 %", "73 %"],
            ["Margen bruto (€)", "32.900 €", "41.180 €", "50.400 €", "59.040 €", "69.350 €"],
            ["Gastos fijos y de estructura", "20.040 €", "21.480 €", "23.400 €", "26.400 €", "29.400 €"],
            ["EBITDA", "12.860 €", "19.700 €", "27.000 €", "32.640 €", "39.950 €"],
            ["**Retribución promotora**", "**9.600 €**", "**15.600 €**", "**18.600 €**", "**21.600 €**", "**25.200 €**"],
            ["— equivalente mensual", "800 €", "1.300 €", "1.550 €", "1.800 €", "2.100 €"],
            ["Amortización (activos fijos)", "800 €", "800 €", "800 €", "800 €", "800 €"],
            ["Resultado antes de impuestos", "2.460 €", "3.300 €", "7.600 €", "10.240 €", "13.950 €"],
            ["IRPF estimado (autónoma)", "370 €", "790 €", "1.980 €", "2.970 €", "4.320 €"],
            ["**Resultado neto (además del sueldo)**", "**2.090 €**", "**2.510 €**", "**5.620 €**", "**7.270 €**", "**9.630 €**"],
            ["Beneficio retenido / reinvertido", "2.090 €", "2.510 €", "5.620 €", "7.270 €", "9.630 €"],
        ],
        widths=[0.30, 0.14, 0.14, 0.14, 0.14, 0.14], left_cols=[0, 1, 2, 3, 4, 5], hl=[5, 10],
    ),
    CALLOUT("info", "Supuestos de la cuenta de resultados (para que sea auditable)",
            "**Ventas:** año 1 = 47.000 € (proyección mensual de la sección 10, ~150 €/día con 5–6 clientes/día y canal online); crecimiento del 23 % en el año 2 por fidelización, online y calzado; después 21 %, 17 % y 16 %. **Margen:** 70 % en el año 1 y sube a 71–73 % cuando el mix se enriquece con regalo y online. **Gastos de estructura (sin sueldo):** año 1 = 1.670 €/mes; año 2 sube a 1.790 €/mes por el fin de la tarifa plana (cuota ~300 €/mes) y más marketing; año 3, 1.950 €/mes (refuerzo en temporadas); año 4, 2.200 €/mes (ayudante a media jornada, se contrata **cuando el sueldo de la promotora ya está asegurado**); año 5, 2.450 €/mes. **Retribución promotora:** coste desde el año 1, con la escalera de la sección 8.3. **Amortización:** 800 €/año de los activos fijos (~3.920 € a 5 años); el stock no se amortiza porque rota. **No se incluyen** intereses (no se prevé deuda relevante) ni IVA (se liquida aparte)."),
    CALLOUT("success", "La conclusión, en tres líneas",
            "**La propietaria cobra desde el mes 1**: 800 €/mes, con una escalera que llega a **2.100 €/mes en el año 5** (sección 8.3). **Además del sueldo, el negocio deja beneficio**: 2.090 € en el año 1 y 9.630 € en el año 5, que se reinvierten. **El local va primero**: las subidas de sueldo solo se activan cuando la caja lo aguanta sin tocar el colchón."),
    CALLOUT("warn", "Qué pasa si el año 1 no cumple (el escenario de riesgo)",
            "Si el año 1 cierra con ventas de **37.600 €** (−20 %), la tienda todavía paga la mitad del sueldo y el colchón termina el año en ~680 €. No es un escenario cómodo, pero **la regla de la sección 8.3 lo gestiona antes de llegar ahí**: el sueldo se reduce a 400 €/mes temporalmente, el pedido del año 2 se ajusta con datos reales y no hay deuda que ahogue. Este plan está diseñado para sobrevivir a un año 1 mediocre, no para triunfar solo en el papel."),

    S("11.1", "RENTABILIDAD DE LA INVERSIÓN", "VAN, TIR y plazo de recuperación"),
    P("**Análisis de la inversión como proyecto (los 4 indicadores que piden los análisis financieros):**"),
    TABLE(
        ["Indicador", "Valor", "Interpretación"],
        [
            ["Inversión inicial", "21.010 €", "Todo el desembolso para abrir (sección 6)"],
            ["Flujos de caja de la operación", "3.260 € · 4.100 € · 8.400 € · 11.040 € · 14.750 €", "Caja que deja la tienda en los años 1–5 **después de pagar el sueldo de la promotora** y antes de impuestos"],
            ["VAN al 5 %", "**+13.710 €**", "El proyecto crea 13.710 € de valor sobre el coste del dinero (5 %) con el sueldo ya pagado: es rentable de verdad"],
            ["TIR", "**21,1 %**", "Rentabilidad anual del proyecto con el sueldo incluido: muy por encima de cualquier alternativa de ahorro o deuda"],
            ["Plazo de recuperación (payback)", "**3,5 años**", "La inversión se recupera a mitad del año 4 con los flujos acumulados"],
            ["Payback descontado (al 5 %)", "≈ 3,8 años", "Considerando el coste del dinero, la recuperación se produce casi al final del año 4"],
        ],
        widths=[0.28, 0.34, 0.38], left_cols=[0, 1], hl=[2, 3],
    ),
    P("**Lectura honesta.** A diferencia de los análisis que maquillan resultados, estos flujos **ya descuentan el sueldo de la promotora**: no se valora un negocio que no paga a quien lo trabaja. Aun así, el proyecto sigue siendo claramente rentable (TIR del 21 %), porque la inversión es contenida (reformas y web a coste propio, stock rotativo) y los flujos crecen al doble entre el año 1 y el 5. El escenario del año 1 en números rojos si las ventas no acompañan está analizado en la sección 13."),
    CALLOUT("tip", "Cómo se trata esta inversión en la solicitud de ayudas",
            "La inversión subvencionable habitual en comercio minorista incluye: reforma y adecuación del local (materiales y obra), mobiliario y equipamiento, marca e imagen (rótulo, etiquetas, packaging), digitalización (web, TPV, cámaras) y stock inicial en algunos programas. Las ayudas suelen cubrir el **30–50 %** del gasto elegible: es la palanca que convierte los 21.010 € en una inversión neta de ~15.000 €. Se detalla en la sección 17."),
]

# ============================================================================
# SECCIÓN 12 · PLAN DE TESORERÍA Y FINANCIACIÓN
# ============================================================================

SECTION_12 = [
    S("12", "PLAN DE TESORERÍA", "De dónde sale el dinero, cuándo se gasta y cuándo vuelve",
      "Una tienda no muere por no ser rentable: muere por quedarse sin liquidez. Este plan de tesorería muestra la necesidad de financiación, el calendario de desembolsos y el colchón de seguridad.",
      ess=["Necesidad 21.010 €, desembolsada en 4 meses", "Financiación: 15.000 € ahorro + 3.000 € ayudas + 3.010 € banco", "Colchón de caja: 5.000 € = 3 meses de gastos", "Revisión semanal: caja real, cobros, stock y pagos"]),

    P("**De dónde sale el dinero** (el detalle de en qué se gasta cada euro está en la sección 06, no se repite aquí):"),
    TABLE(
        ["Fuente", "Importe", "Cuándo entra", "Notas"],
        [
            ["Aportación de los promotores (ahorros)", "15.000 €", "Meses −4 a 0, escalonado", "Capital propio; sin intereses ni devolución"],
            ["Ayudas y subvenciones (parte más probable de recuperar)", "3.000 €", "Primer año (cuotas y devoluciones)", "Cuota cero Galicia, tarifa plana, retornadas y modernización — sección 17"],
            ["Financiación bancaria (MicroBank / ICO / SGR AFIGAL)", "3.010 €", "Mes 0, solo si procede", "Línea emprendedores hasta 25.000 € sin aval; si las ayudas se confirman, esta partida desaparece y el excedente engorda el colchón"],
            ["**Total**", "**21.010 €**", "**—**", "**Desembolso escalonado en ~4 meses**"],
        ],
        widths=[0.36, 0.14, 0.18, 0.32], left_cols=[0, 1, 2], hl=[3],
    ),
    P("**Cómo se gasta:** local y reforma entre los meses −4 y −2, marca/mobiliario/legal en el −3 al 0, stock a la llegada (mes 0) y 5.000 € (reserva + fondo de maniobra) siempre disponibles en cuenta."),
    CALLOUT("success", "Colchón de liquidez tras la apertura",
            "La caja inicial es de 4.000 € (fondo de maniobra) + 1.000 € (reserva de imprevistos). La sección 10 muestra que el mes más bajo de caja es ~1.850 € (agosto), y el colchón completo (5.000 €) cubre **2 meses de gastos** (2.470 €/mes con sueldo) en el peor momento. Es un colchón razonable para un negocio sin deuda y con stock rotativo: el riesgo real de quedarse sin caja es bajo."),

    P("**Seguimiento de tesorería (qué se revisa cada mes):**"),
    CHECKBOXES([
        "Caja real vs. caja prevista del plan (desviación > 500 € → revisar)",
        "Cobros: pagos con tarjeta al día; online liquidado semanalmente",
        "Pagos: alquiler, cuota, proveedores China (30/70 %), gestoría",
        "Stock: valor de mercancía en tienda y rotación por modelo",
        "Reposiciones: pedido por avión (300–500 €) si un modelo se agota",
        "Impuestos: IVA trimestral y retenciones, reservar el 15–20 % de cada mes",
    ]),
]

# ============================================================================
# SECCIÓN 13 · ANÁLISIS DE SENSIBILIDAD Y ESCENARIOS
# ============================================================================

SECTION_13 = [
    S("13", "SENSIBILIDAD Y ESCENARIOS", "Qué pasa si las cosas van distintas a lo previsto",
      "El plan base es una hipótesis; el valor del plan está en saber qué ocurre si esa hipótesis falla. Este análisis somete la cuenta de resultados del año 1 a variaciones realistas y define cuándo se activa cada plan de contingencia.",
      ess=["Resiste −20 % de ventas: la caja queda en ~680 € (sueldo a 400 €/mes)", "Margen < 65 % es el límite: renegociar costes", "Umbral del colchón: 35.200 €/año con sueldo (no se toca)", "Ticket medio: la variable más controlable"]),

    P("**Sensibilidad del año 1 (sobre 47.000 € de ventas, 1.670 €/mes de gastos y 800 €/mes de sueldo): una sola tabla, sin repetir números.**"),
    TABLE(
        ["Variable", "Variación", "Ventas año 1", "Resultado antes de impuestos", "Caja a cierre", "Prob.", "Veredicto"],
        [
            ["Escenario base", "—", "47.000 €", "+2.460 €", "7.260 €", "45 %", "Viable: paga el sueldo y deja beneficio"],
            ["Ventas", "−20 %", "37.600 €", "−4.120 €", "~680 €", "40 %", "Aguanta sin vaciar el colchón; sueldo a 400 €/mes (regla 8.3)"],
            ["Ventas", "+20 % (online despega)", "56.400 €", "+9.040 €", "~13.840 €", "15 %", "Acelerar pedidos y marketing"],
            ["Margen bruto", "70 % → 65 %", "47.000 €", "+110 €", "~4.910 €", "—", "Aviso: renegociar costes o ajustar PVP"],
            ["Margen bruto", "70 % → 60 %", "47.000 €", "−2.240 €", "~2.560 €", "—", "En el límite: renegociar proveedor"],
            ["Gastos fijos", "+10 % (1.840 €/mes)", "47.000 €", "+456 €", "~5.256 €", "—", "Positivo, margen apretado"],
            ["Ticket medio", "27 € → 24 € (−11 %)", "41.800 €", "−1.160 €", "~3.640 €", "—", "La variable más controlable: mix de regalo y complementos"],
            ["Apertura", "2 meses de retraso (−10 %)", "42.300 €", "−830 €", "~3.970 €", "—", "Recuperable; ajustar pedido"],
        ],
        widths=[0.15, 0.15, 0.13, 0.16, 0.12, 0.07, 0.22], left_cols=[0, 1, 2, 3, 4, 5], hl=[0],
    ),
    CALLOUT("warn", "El dato que decide de todo: el punto de equilibrio con sueldo",
            "Con el sueldo de 800 €/mes ya incluido, la tienda **no toca el colchón de 5.000 €** mientras las ventas no bajen de **35.200 €/año** (≈ 2.930 €/mes ≈ 98 €/día): ese es el nivel en que la pérdida acumulada iguala el colchón. Por debajo, la regla de la sección 8.3 reduce el sueldo antes de tocar la caja. Y para que la tienda **pague el sueldo entero y se mantenga sola** hacen falta 42.300 €/año (≈ 3.530 €/mes ≈ 118 €/día), que es lo que el plan prevé superar con regularidad a partir de mayo del año 1."),
    P("**Conclusión del análisis.** El resultado es robusto en un rango de ±20 % de ventas: el escenario base paga el sueldo y deja beneficio; el pesimista obliga a reducir el sueldo a la mitad (la regla de la sección 8.3 lo hace automáticamente) pero no rompe el negocio; el optimista permite acelerar pedidos y contratar ayuda antes. La variable más delicada es el **margen bruto** (si bajara del 65 % hay que renegociar costes) y el ticket medio: **bajar el ticket de 27 € a 24 € equivale a vender un 11 % menos**, por eso el mix de regalo y complementos, que sube el ticket sin gastar más en publicidad, es la palanca más barata de todas."),
]

# ============================================================================
# SECCIÓN 14 · DAFO Y PLAN ESTRATÉGICO
# ============================================================================

SECTION_14 = [
    S("14", "DAFO Y PLAN ESTRATÉGICO", "Diagnóstico completo y objetivos a 12, 24 y 36 meses",
      "El DAFO recoge todo lo analizado en las secciones anteriores en una sola vista: las fortalezas que se explotan, las debilidades que se corrigen, las oportunidades que se aprovechan y las amenazas que se vigilan. Después, el plan estratégico lo convierte en objetivos medibles.",
      ess=["Margen 70 % + obra y web propias: fortalezas estructurales", "Marca desconocida: se corrige con presencia semanal", "Ayudas 4.000–12.000 €: la oportunidad clave", "Importación y estacionalidad: las amenazas a vigilar"]),

    TWOCOL(
        "💪 Fortalezas (internas)",
        [
            "**Margen del 70 %** por fabricación directa con marca propia (la ventaja estructural)",
            "**Reforma y web a coste casi cero** (mano de obra y desarrollo propios)",
            "**Stock reducido y rotación cada 3–4 semanas**: poco capital atrapado",
            "**Equipo con capacidad industrial**: la empresa de reformas cubre lo personal los primeros meses (sin nómina inicial)",
            "**Ubicación elegida a propósito**: Oleiros = familias jóvenes, nivel medio-alto, poca competencia",
            "**Producto de regalo con packaging propio**: ticket medio más alto que una tienda genérica",
        ],
        "⚠️ Debilidades (internas)",
        [
            "**Marca desconocida** al inicio: el reconocimiento se construye en 12–18 meses",
            "**Dependencia de un único proveedor** en China al principio",
            "**Experiencia limitada en retail** (primera tienda): curva de aprendizaje en compras y surtido",
            "**Cash flow estacional**: 4–5 meses al año generan la mayor parte del beneficio",
            "**Sueldo inicial ajustado (800 €/mes)**: la familia se completa con los ingresos externos de la promotora mientras la tienda crece",
        ],
    ),
    TWOCOL(
        "🔵 Oportunidades (externas)",
        [
            "**Ayudas muy relevantes**: cuota cero Galicia, tarifa plana, ayudas a retornadas, modernización del comercio (4.000–12.000 € potenciales)",
            "**Canal online**: convierte una tienda de barrio en una marca nacional sin coste fijo",
            "**Calzado y marcas españolas/portuguesas** como segunda línea de producto a partir del mes 6",
            "**Colaboraciones locales** (guarderías, colegios, fotógrafas, madres influencers) con coste casi nulo",
            "**Fondos Next Generation** para digitalización del comercio minorista",
        ],
        "🔴 Amenazas (externas)",
        [
            "**Competencia de volumen** (multinacionales y online low-cost) con precios más bajos",
            "**Riesgo de importación**: aranceles, normativa UE (REACH, seguridad infantil), retrasos por Año Nuevo Chino",
            "**Cambio de hábitos**: más compra online, menos tráfico en tiendas de barrio",
            "**Costes del local**: subidas de alquiler o comunidad en renovación",
            "**Estacionalidad extrema**: un mal noviembre–diciembre desequilibra el año entero",
        ],
    ),
    CALLOUT("success", "Estrategia que se desprende del DAFO (la «apuesta KHC»)",
            "**Explotar la fortaleza de margen para ser competitivo sin ser barato**: precio medio, calidad alta, regalo bonito. **Corregir la debilidad de marca** con presencia semanal en redes, escaparate renovado cada 2 semanas y colaboraciones locales. **Aprovechar la oportunidad de las ayudas** tramitándolas antes del alta de actividad. **Vigilar la amenaza logística** con 2–3 fábricas candidatas, muestras previas e inspección de calidad. **Protegerse de la estacionalidad** con un plan de compras inverso (Navidad se pide en julio-agosto)."),

    S("14.1", "OBJETIVOS MEDIBLES", "Hacia dónde va KHC, con plazos y métricas"),
    TIMELINE([
        ("Mes 0", "Abrir y aprender", "Apertura con stock completo, campaña de apertura y medición desde el día 1. Objetivo: 5–6 clientes/día y caja que no baje de 1.850 €. Sueldo de 800 €/mes desde el mes 1."),
        ("Mes 3", "Primera revisión real", "Análisis de rotación por modelo: se elimina lo que no vende, se refuerza lo que sí. Primer pedido de reposición con datos. Objetivo: ticket medio ≥ 27 €."),
        ("Mes 6", "Estabilizar y añadir", "Canal online funcionando, primeras colaboraciones locales, valoración del calzado. Objetivo: ventas ≥ 3.400 €/mes y 30 % de clientes recurrentes."),
        ("Mes 12", "Cerrar un año con datos", "Facturación 44.000–50.000 €, caja > 7.000 €, sueldo pagado los 12 meses, surtido depurado (los 10 mejores modelos = 50 % ventas). Decidir calzado."),
        ("Mes 24", "Consolidar y cobrar", "Facturación 58.000 €, sueldo de 1.300 €/mes para la promotora (primera subida real, con la regla de la sección 8.3), online al 20 % de ventas. Evaluar SL."),
        ("Mes 36", "Crecer o escalar", "Facturación 70.000 €, sueldo de 1.550 €/mes, refuerzo en temporadas. Decisión SL con datos y evaluación de ayudante a media jornada."),
    ]),
]

# ============================================================================
# SECCIÓN 20 · CUADRO DE MANDO Y KPIs
# ============================================================================

SECTION_20 = [
    S("20", "CUADRO DE MANDO", "Los 10 indicadores que se vigilan cada semana",
      "Un plan sin medición es una opinión. Estos son los indicadores que la promotora revisa cada semana (30 minutos) y mensualmente (1 hora), con su fórmula y su objetivo.",
      ess=["10 KPIs con fórmula, objetivo y acción si fallan", "Rutina: lunes 10 minutos, mes 1 hora", "Ventas/día ≥ 92 €: el termómetro semanal", "Dos reglas de oro: margen ≥ 70 % y caja ≥ 4.000 €"]),

    TABLE(
        ["Indicador", "Fórmula", "Objetivo año 1", "Frecuencia", "Si falla…"],
        [
            ["Ventas/día", "Facturación ÷ días abiertos", "≥ 92 €/día (equilibrio tienda); ≥ 150 €/día (objetivo año 1)", "Semanal", "Menos de 98 €/día durante 3 semanas → activar plan B (sección 19)"],
            ["Ticket medio", "Ventas ÷ nº tickets", "≥ 27 €", "Semanal", "Bajo 24 € → mejorar mix de regalo y complementos"],
            ["Clientes/día", "Tickets emitidos ÷ días", "5–6 clientes", "Semanal", "Bajo 4 → revisar tráfico, escaparate y pauta"],
            ["Conversión", "Clientes ÷ visitantes que entran", "25–35 %", "Quincenal", "Baja → revisar escaparate y precio percibido"],
            ["Margen bruto", "(Ventas − coste mercancía) ÷ Ventas", "≥ 70 % (media)", "Mensual", "Bajo 65 % → renegociar costes o subir PVP"],
            ["Rotación de stock", "Coste vendido ÷ stock medio (anual)", "≥ 4 veces/año", "Mensual", "Baja → liquidar en rebajas y recortar reposición"],
            ["Gastos fijos", "Suma de todos los fijos", "≤ 1.700 €/mes", "Mensual", "Suben > 5 % → revisar partidas"],
            ["Caja", "Saldo real de la cuenta del negocio", "≥ 4.000 € (colchón: fondo + reserva)", "Semanal", "Bajo 3.000 € → congelar reposición no urgente; revisar sueldo (sección 8.3)"],
            ["Margen de seguridad", "(Ventas − punto equilibrio con sueldo) ÷ Ventas", "≥ 4 % año 1; ≥ 10 % año 2; ≥ 15 % año 4", "Mensual", "Negativo → riesgo de no poder pagar el sueldo"],
            ["Coste de adquisición", "Marketing ÷ ventas atribuidas (últimos 60 días)", "≤ 10 % de las ventas", "Mensual", "Alto → ajustar audiencia y mensaje"],
        ],
        widths=[0.22, 0.28, 0.20, 0.10, 0.20], left_cols=[0, 1],
    ),
    CALLOUT("tip", "La rutina de los 30 minutos",
            "Cada lunes: ventas/día, ticket medio, clientes/día y caja (4 números, 10 minutos). Cada mes: margen, rotación, gastos y coste de adquisición (20 minutos). Con eso se sabe si el negocio va bien, regular o mal. **No hace falta un ERP: una hoja de cálculo con 10 columnas basta.**"),
]
