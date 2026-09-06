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
# Año 1 calibrado a la realidad del negocio: tienda (4–5 clientes/día × ~50 €)
# + canal online (150–200 €/día desde el mes 3, con 300–400 €/mes de marketing)
VENTAS_BASE = [3200, 3800, 5400, 7000, 9000, 10300, 10300, 9200, 12300, 11800, 14300, 13400]
CAJA_MES = [3070, 2560, 3170, 4900, 8030, 12070, 16110, 19380, 24820, 29910, 36750, 42960]
MES_GF = 1670        # gastos fijos de la tienda
MES_SUELDO = 1500    # retribución de la promotora desde el mes 1 (sección 8.3)

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
      ess=["Año 1: 110.000 € (tienda + online) mes a mes", "Online: ~150–200 €/día desde el mes 3 con 300–400 €/mes de marketing", "Caja mínima 2.560 € (febrero) y cierre con 42.960 €", "Sueldo de 1.500 €/mes pagado los 12 meses y +38.160 € antes de impuestos"]),

    P("**Supuestos de la proyección (escenario base año 1):**"),
    CHECKBOXES([
        "**Apertura en enero** y curva de aprendizaje: enero–febrero son los únicos meses por debajo del gasto (la tienda aún no se conoce)",
        "**Estacionalidad de la moda infantil:** septiembre (vuelta al cole) y noviembre–diciembre (Navidad y Reyes) son los picos; enero–febrero y julio–agosto, rebajas y vacaciones",
        "**Margen bruto medio del 70 %** sobre el coste real puesto en tienda (sección 8)",
        "**Gastos fijos de 1.670 €/mes** (sección 7) y **sueldo de la promotora de 1.500 €/mes desde el mes 1** (sección 8.3)",
        "**Tienda:** 4–5 clientes/día × ~50 € de ticket (una persona compra varias cosas; el regalo sube a 40–60 €)",
        "**Online:** 150–200 €/día desde el mes 3–4, sostenido con 300–400 €/mes de marketing (sección 15)",
    ]),

    TABLE(
        ["Mes", "Ventas", "Mercancía (30 %)", "Margen bruto", "Resultado del mes", "Caja acumulada"],
        _rows_mensual() + [["**TOTAL AÑO 1**", "**110.000 €**", "**33.000 €**", "**77.000 €**", "**+38.960 €**", "**42.960 €**"]],
        widths=[0.12, 0.18, 0.18, 0.18, 0.17, 0.17], left_cols=[0, 1, 2, 3, 4, 5], hl=[12],
    ),
    P("*La caja acumulada parte de los 4.000 € de fondo de maniobra. Solo enero–febrero son deficitarios (mínimo de 2.560 €); desde marzo la tienda se financia sola, con el sueldo ya pagado, y de septiembre a diciembre acumula el grueso del beneficio del año.*"),

    LINE("Evolución de la caja acumulada — año 1 (€, partiendo de 4.000 €)",
         MESES,
         [("Caja acumulada", CAJA_MES)],
         unit="€",
         note="La caja nunca baja de 2.560 € (febrero, el único mes realmente difícil). Desde marzo crece todos los meses: el negocio genera caja con el sueldo ya pagado."),

    P("**Lectura honesta de la tabla.** Con el sueldo de la promotora ya incluido (1.500 €/mes), el punto de equilibrio del año 1 es **4.530 €/mes** y se supera desde marzo. Solo enero–febrero son deficitarios (la apertura aún no se conoce), con un mínimo de caja de 2.560 € cubierto por el colchón. El año se cierra con **+38.960 € operativos** (antes de sueldo: +56.960 €), 42.960 € de caja y el sueldo pagado los 12 meses. **La clave del año 1 no es aguantar: es pagar el sueldo, no tocar la caja y acumular en los picos.**"),
]

# ============================================================================
# SECCIÓN 11 · PROYECCIÓN A 5 AÑOS Y CUENTA DE RESULTADOS
# ============================================================================

SECTION_11 = [
    S("11", "PROYECCIÓN A 5 AÑOS", "Cuenta de resultados prevista y rentabilidad",
      "La proyección a 5 años responde a las preguntas que hace cualquier convocatoria de ayudas: ¿cuánto se venderá, cuánto ganará la tienda, cuánto cobrará la promotora y cuándo se recupera la inversión? Aquí la retribución de la promotora **es un coste del negocio desde el año 1** — no un residuo.",
      ess=["Ventas: 110.000 € (año 1) → 195.000 € (año 5)", "Sueldo promotora: 1.500 €/mes año 1 → 2.800 €/mes año 5", "Beneficio neto: ~29.000 € → ~47.500 € (además del sueldo)", "La inversión se recupera dentro del año 1 (≈ 7 meses)"]),

    P("**Escenario base quinquenal (ventas físicas + online con crecimiento por fidelización y rotación):**"),
    TABLE(
        ["Concepto", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"],
        [
            ["Ventas (a € constantes)", "110.000 €", "135.000 €", "160.000 €", "180.000 €", "195.000 €"],
            ["Margen bruto aplicado", "70 %", "71 %", "72 %", "72 %", "73 %"],
            ["Margen bruto (€)", "77.000 €", "95.850 €", "115.200 €", "129.600 €", "142.350 €"],
            ["Gastos fijos y de estructura", "20.040 €", "22.800 €", "27.600 €", "31.800 €", "36.000 €"],
            ["EBITDA", "56.960 €", "73.050 €", "87.600 €", "97.800 €", "106.350 €"],
            ["**Retribución promotora**", "**18.000 €**", "**21.600 €**", "**25.200 €**", "**28.800 €**", "**33.600 €**"],
            ["— equivalente mensual", "1.500 €", "1.800 €", "2.100 €", "2.400 €", "2.800 €"],
            ["Amortización (activos fijos)", "800 €", "800 €", "800 €", "800 €", "800 €"],
            ["Resultado antes de impuestos", "38.160 €", "50.650 €", "61.600 €", "68.200 €", "71.950 €"],
            ["IRPF estimado (autónoma)", "9.160 €", "14.690 €", "19.710 €", "22.510 €", "24.460 €"],
            ["**Resultado neto (además del sueldo)**", "**29.000 €**", "**35.960 €**", "**41.890 €**", "**45.690 €**", "**47.490 €**"],
            ["Beneficio retenido / reinvertido", "29.000 €", "35.960 €", "41.890 €", "45.690 €", "47.490 €"],
        ],
        widths=[0.30, 0.14, 0.14, 0.14, 0.14, 0.14], left_cols=[0, 1, 2, 3, 4, 5], hl=[5, 10],
    ),
    CALLOUT("info", "Supuestos de la cuenta de resultados (para que sea auditable)",
            "**Ventas:** año 1 = 110.000 € (sección 10; tienda 4–5 clientes/día × ~50 € + online 150–200 €/día); año 2 +23 % por fidelización, calzado y online; después +18 %, +13 % y +8 %. **Margen:** 70 % en el año 1 y sube a 71–73 % con el mix de regalo y online. **Gastos de estructura (sin sueldo):** año 1 = 1.670 €/mes; año 2 sube a 1.900 €/mes (fin de la tarifa plana + más marketing); año 3, 2.300 €/mes (ayudante en temporadas); año 4, 2.650 €/mes (ayudante a media jornada estable); año 5, 3.000 €/mes (ayudante estable + marketing). **Retribución promotora:** coste desde el mes 1, con la escalera de la sección 8.3. **Amortización:** 800 €/año de los activos fijos; el stock no se amortiza porque rota. **No se incluyen** intereses (no hay deuda relevante) ni IVA (se liquida aparte)."),
    CALLOUT("success", "La conclusión, en tres líneas",
            "**La propietaria cobra desde el mes 1**: 1.500 €/mes, con una escalera que llega a **2.800 €/mes en el año 5** (sección 8.3). **Además del sueldo, el negocio deja beneficio**: ~29.000 € en el año 1 y ~47.500 € en el año 5, que se reinvierten. **El local va primero**: las subidas de sueldo solo se activan cuando la caja lo aguanta sin tocar el colchón."),
    CALLOUT("warn", "Qué pasa si el año 1 no cumple (el escenario de riesgo)",
            "Si el año 1 cierre con ventas de **88.000 €** (−20 %), el resultado antes de impuestos seguiría siendo **+22.760 €** y la caja terminaría en ~27.560 €: el sueldo se paga íntegro y el proyecto sigue siendo fuerte. El plan está calculado para que **ni el caso malo quite el sueldo ni toque el colchón**."),

    S("11.1", "RENTABILIDAD DE LA INVERSIÓN", "VAN, TIR y plazo de recuperación"),
    P("**Análisis de la inversión como proyecto (los 4 indicadores que piden los análisis financieros):**"),
    TABLE(
        ["Indicador", "Valor", "Interpretación"],
        [
            ["Inversión inicial", "21.010 €", "Todo el desembolso para abrir (sección 6)"],
            ["Flujos de caja de la operación", "38.960 € · 51.450 € · 62.400 € · 69.000 € · 72.750 €", "Caja que deja la tienda en los años 1–5 **después de pagar el sueldo de la promotora** y antes de impuestos"],
            ["VAN al 5 %", "**+230.000 €**", "El proyecto crea ~230.000 € de valor sobre el coste del dinero (5 %) con el sueldo ya pagado"],
            ["TIR", "**> 100 %**", "La inversión es pequeña frente a la capacidad de caja del negocio: se recupera en el primer año"],
            ["Plazo de recuperación (payback)", "**≈ 7 meses**", "La inversión de 21.010 € se recupera dentro del año 1 con los flujos de la operación"],
            ["Payback descontado (al 5 %)", "**≈ 8 meses**", "Incluso descontando el coste del dinero, la recuperación es del primer año"],
        ],
        widths=[0.28, 0.34, 0.38], left_cols=[0, 1], hl=[2, 3],
    ),
    P("**Lectura honesta.** Estos flujos **ya descuentan el sueldo de la promotora**: no se valora un negocio que no paga a quien lo trabaja. Y aun así la inversión se recupera en el primer año porque el negocio, con el margen del 70 % y los costes contenidos, genera caja desde marzo. Eso no significa que no haya riesgo: el riesgo real está en **la caja de los dos primeros meses** y en la estacionalidad, no en recuperar el dinero. Por eso el plan insiste en la regla de la sección 8.3 y en el fondo de maniobra: el proyecto no depende de la suerte, depende de no tocar la caja mientras arranca."),
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
            "La caja inicial es de 4.000 € (fondo de maniobra) + 1.000 € (reserva de imprevistos). La sección 10 muestra que el mes más bajo de caja es ~2.560 € (febrero, el único deficitario) y que desde marzo la tienda genera caja todos los meses. El colchón completo (5.000 €) cubre **1,6 meses de gastos** (3.170 €/mes con sueldo): es la protección justa para los dos meses de arranque, y el negocio se financia solo a partir de ahí."),

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

    P("**Sensibilidad del año 1 (sobre 110.000 € de ventas, 1.670 €/mes de gastos y 1.500 €/mes de sueldo): una sola tabla, sin repetir números.**"),
    TABLE(
        ["Variable", "Variación", "Ventas año 1", "Resultado antes de impuestos", "Caja a cierre", "Prob.", "Veredicto"],
        [
            ["Escenario base", "—", "110.000 €", "+38.160 €", "42.960 €", "45 %", "Paga el sueldo y deja 29.000 € de beneficio"],
            ["Ventas", "−20 %", "88.000 €", "+22.760 €", "~27.560 €", "40 %", "Sigue pagando el sueldo entero y sin tocar el colchón"],
            ["Ventas", "+20 % (online despega)", "132.000 €", "+53.560 €", "~58.360 €", "15 %", "Acelerar pedidos, marketing y contratar antes"],
            ["Margen bruto", "70 % → 65 %", "110.000 €", "+32.660 €", "~37.460 €", "—", "Aviso: renegociar costes o ajustar PVP"],
            ["Margen bruto", "70 % → 60 %", "110.000 €", "+27.160 €", "~31.960 €", "—", "Sigue siendo positivo: renegociar proveedor"],
            ["Gastos fijos", "+10 % (1.840 €/mes)", "110.000 €", "+36.156 €", "~40.956 €", "—", "Positivo, margen algo más apretado"],
            ["Ticket medio", "50 € → 45 € (−10 %)", "99.000 €", "+30.460 €", "~35.260 €", "—", "La variable más controlable: mix de regalo"],
            ["Apertura", "2 meses de retraso (−6 %)", "103.000 €", "+33.260 €", "~38.060 €", "—", "Recuperable; ajustar pedido"],
        ],
        widths=[0.15, 0.15, 0.13, 0.16, 0.12, 0.07, 0.22], left_cols=[0, 1, 2, 3, 4, 5], hl=[0],
    ),
    CALLOUT("warn", "El dato que decide de todo: el punto de equilibrio con sueldo",
            "Con el sueldo de 1.500 €/mes ya incluido, la tienda **no toca el colchón de 5.000 €** mientras las ventas no bajen de **47.200 €/año** (≈ 3.930 €/mes ≈ 151 €/día), y **paga todo el sueldo y todos los gastos** a partir de **54.300 €/año** (≈ 4.530 €/mes ≈ 174 €/día). El plan del año 1 (110.000 €) está un 100 % por encima de ese umbral: el margen de seguridad es enorme, y el escenario pesimista (−20 %) sigue pagando el sueldo entero."),
    P("**Conclusión del análisis.** El negocio es robusto en todo el rango razonable: incluso con un −20 % de ventas se paga el sueldo entero y sobra beneficio. Las dos variables que hay que vigilar son el **margen bruto** (si cae al 65 % hay que renegociar costes) y el **ticket medio**: bajar el ticket de 50 € a 45 € equivale a vender un 10 % menos, por eso el mix de regalo y complementos —que sube el ticket sin gastar más en publicidad— es la palanca más barata de todas."),
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
            "**El arranque depende de los dos primeros meses**: si enero–febrero se quedan a la mitad, el colchón se toca (aunque la regla 8.3 lo limita)",
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
        ("Mes 0", "Abrir y aprender", "Apertura con stock completo, campaña de apertura y medición desde el día 1. Objetivo: 4–5 clientes/día en tienda + online arrancando, y caja que no baje de 2.500 €. Sueldo de 1.500 €/mes desde el mes 1."),
        ("Mes 3", "Primera revisión real", "Análisis de rotación por modelo: se elimina lo que no vende, se refuerza lo que sí. Primer pedido de reposición con datos. Objetivo: ticket medio ≥ 45 € y online ≥ 100 €/día."),
        ("Mes 6", "Estabilizar y añadir", "Canal online consolidado (~150 €/día), primeras colaboraciones locales, valoración del calzado. Objetivo: ventas ≥ 9.000 €/mes y 30 % de clientes recurrentes."),
        ("Mes 12", "Cerrar un año con datos", "Facturación 100.000–120.000 €, caja > 35.000 €, sueldo pagado los 12 meses, surtido depurado (los 10 mejores modelos = 50 % ventas). Decidir calzado y refuerzo."),
        ("Mes 24", "Consolidar y cobrar", "Facturación 135.000 €, sueldo de 1.800 €/mes para la promotora (subida con la regla de la sección 8.3), online al 40 % de ventas. Evaluar SL con 35.000 € de beneficio."),
        ("Mes 36", "Crecer o escalar", "Facturación 160.000 €, sueldo de 2.100 €/mes, ayudante en temporadas. Decisión SL con datos y evaluación de ayudante a media jornada."),
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
            ["Ventas/día", "Facturación ÷ días abiertos", "≥ 92 €/día (equilibrio tienda); ≥ 300 €/día (objetivo año 1)", "Semanal", "Menos de 174 €/día durante 3 semanas → revisar pauta y escaparate (sección 19)"],
            ["Ticket medio", "Ventas ÷ nº tickets", "≥ 45 € (mix tienda + online)", "Semanal", "Bajo 40 € → mejorar mix de regalo y complementos"],
            ["Clientes/día", "Tickets emitidos ÷ días", "4–5 en tienda + 3–5 pedidos online", "Semanal", "Bajo 3 en tienda → revisar tráfico, escaparate y pauta"],
            ["Conversión", "Clientes ÷ visitantes que entran", "25–35 %", "Quincenal", "Baja → revisar escaparate y precio percibido"],
            ["Margen bruto", "(Ventas − coste mercancía) ÷ Ventas", "≥ 70 % (media)", "Mensual", "Bajo 65 % → renegociar costes o subir PVP"],
            ["Rotación de stock", "Coste vendido ÷ stock medio (anual)", "≥ 3,5 veces/año (el plan del año 1: 3,8)", "Mensual", "Baja → liquidar en rebajas y recortar reposición"],
            ["Gastos fijos", "Suma de todos los fijos", "≤ 1.700 €/mes", "Mensual", "Suben > 5 % → revisar partidas"],
            ["Caja", "Saldo real de la cuenta del negocio", "≥ 4.000 € (colchón: fondo + reserva)", "Semanal", "Bajo 3.000 € → congelar reposición no urgente; revisar sueldo (sección 8.3)"],
            ["Margen de seguridad", "(Ventas − punto equilibrio con sueldo) ÷ Ventas", "≥ 40 % año 1 (≈ 50 % real)", "Mensual", "Bajo 25 % → revisar precios y costes"],
            ["Coste de adquisición", "Marketing ÷ ventas atribuidas (últimos 60 días)", "≤ 10 % de las ventas", "Mensual", "Alto → ajustar audiencia y mensaje"],
        ],
        widths=[0.22, 0.28, 0.20, 0.10, 0.20], left_cols=[0, 1],
    ),
    CALLOUT("tip", "La rutina de los 30 minutos",
            "Cada lunes: ventas/día, ticket medio, clientes/día y caja (4 números, 10 minutos). Cada mes: margen, rotación, gastos y coste de adquisición (20 minutos). Con eso se sabe si el negocio va bien, regular o mal. **No hace falta un ERP: una hoja de cálculo con 10 columnas basta.**"),
]
