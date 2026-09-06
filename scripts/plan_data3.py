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
VENTAS_BASE = [1430, 1730, 2260, 2380, 3400, 2720, 2040, 1700, 4080, 3060, 4080, 4080]
CAJA_MES = [3331, 2872, 2784, 2780, 3490, 3724, 3482, 3002, 4188, 4660, 5846, 7032]
MES_GF = 1670

def _rows_mensual():
    caja = 4000
    rows = []
    for i, v in enumerate(VENTAS_BASE):
        coste = round(v * 0.30)
        margen = v - coste
        res = margen - MES_GF
        caja += res
        rows.append([MESES[i], f"{v:,}".replace(",", ".") + " €",
                     f"{coste:,}".replace(",", ".") + " €",
                     f"{margen:,}".replace(",", ".") + " €",
                     f"{res:+,}".replace(",", ".") + " €",
                     f"{caja:,}".replace(",", ".") + " €"])
    return rows

SECTION_10 = [
    S("10", "PROYECCIÓN DE INGRESOS", "Mes a mes: el año 1 con estacionalidad real",
      "Aquí se ve cómo se comporta la tienda a lo largo de un año completo: los meses flojos, los picos de Navidad y vuelta al cole, y cómo evoluciona la caja. Los supuestos son conservadores y se explican para que se puedan discutir o ajustar."),

    P("**Supuestos de la proyección (escenario base año 1):**"),
    CHECKBOXES([
        "**Apertura en enero** y curva de aprendizaje: los 4 primeros meses venden por debajo de la media anual (la tienda aún no se conoce)",
        "**Estacionalidad de la moda infantil en España:** septiembre (vuelta al cole) y noviembre–diciembre (Navidad y Reyes) son los picos; enero–febrero y julio–agosto, rebajas y vacaciones",
        "**Margen bruto medio del 70 %** sobre el coste real puesto en tienda (sección 8)",
        "**Gastos fijos de 1.670 €/mes** (sección 7) y sin sueldo de la promotora los primeros meses",
        "**Ticket medio de 25 €** en tienda y 3–4 clientes/día en los meses normales",
        "**Tienda online** aporta desde el mes 3–4 un 10–15 % adicional sobre la base",
    ]),

    BARS("Facturación mensual año 1 (€) — escenario base",
         "€/mes",
         [(MESES[i], VENTAS_BASE[i], COLORS["gold"] if VENTAS_BASE[i] >= 3000 else COLORS["navy"]) for i in range(12)],
         note="Picos: vuelta al cole (septiembre) y Navidad (noviembre–diciembre). Valles: rebajas y vacaciones (enero, febrero, julio, agosto)."),

    TABLE(
        ["Mes", "Ventas", "Mercancía (30 %)", "Margen bruto", "Resultado", "Caja acumulada"],
        _rows_mensual() + [["**TOTAL AÑO 1**", "**32.960 €**", "**9.888 €**", "**23.072 €**", "**+3.032 €**", "**7.032 €**"]],
        widths=[0.12, 0.18, 0.18, 0.18, 0.17, 0.17], left_cols=[0, 1, 2, 3, 4, 5], hl=[12],
    ),
    P("*La caja acumulada parte de los 4.000 € de fondo de maniobra. Los meses 1–4 son los más difíciles (mínimo de 2.780 € a finales de abril); a partir de mayo la tienda se financia sola y en septiembre–diciembre genera el grueso del beneficio del año.*"),

    LINE("Evolución de la caja acumulada — año 1 (€, partiendo de 4.000 €)",
         MESES,
         [("Caja acumulada", CAJA_MES)],
         unit="€",
         note="La caja nunca baja de 2.780 € en el peor mes. El mínimo se toca en el mes 4; después, cada mes de temporada alta devuelve el colchón."),

    P("**Lectura honesta de la tabla.** La tienda no es rentable en el mes 1 ni en el 2, y el punto de equilibrio mensual (2.390 €/mes) no se supera con regularidad hasta mayo. Sin embargo, en ningún momento la caja baja de 2.780 € gracias al fondo de maniobra, y el año se cierra con +3.032 € antes de impuestos y 7.032 € de caja. **El éxito del año 1 no depende de ganar dinero cada mes, sino de no tocarse la caja y acumular en los picos.**"),
]

# ============================================================================
# SECCIÓN 11 · PROYECCIÓN A 5 AÑOS Y CUENTA DE RESULTADOS
# ============================================================================

SECTION_11 = [
    S("11", "PROYECCIÓN A 5 AÑOS", "Cuenta de resultados prevista y rentabilidad",
      "La proyección a 5 años responde a las preguntas que hace cualquier convocatoria de ayudas: ¿cuánto se venderá, cuánto se ganará, cuánto se puede retribuir la promotora y cuándo se recupera la inversión?"),

    P("**Escenario base quinquenal (ventas físicas + online con crecimiento por fidelización y rotación):**"),
    TABLE(
        ["Concepto", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"],
        [
            ["Ventas (a € constantes)", "33.000 €", "45.000 €", "55.000 €", "62.000 €", "70.000 €"],
            ["Margen bruto aplicado", "70 %", "70 %", "71 %", "72 %", "72 %"],
            ["Margen bruto (€)", "23.100 €", "31.500 €", "39.050 €", "44.640 €", "50.400 €"],
            ["Gastos fijos y de estructura", "20.040 €", "21.000 €", "24.000 €", "26.000 €", "28.500 €"],
            ["EBITDA", "3.060 €", "10.500 €", "15.050 €", "18.640 €", "21.900 €"],
            ["Amortización (activos fijos)", "800 €", "800 €", "800 €", "800 €", "800 €"],
            ["Resultado antes de impuestos", "2.260 €", "9.700 €", "14.250 €", "17.840 €", "21.100 €"],
            ["IRPF estimado (autónoma)", "340 €", "1.840 €", "3.490 €", "4.820 €", "6.330 €"],
            ["**Resultado neto**", "1.920 €", "7.860 €", "10.760 €", "13.020 €", "14.770 €"],
            ["Retribución promotora (objetivo)", "0 €", "6.000 €", "9.000 €", "11.000 €", "12.500 €"],
            ["Beneficio retenido / reinvertido", "1.920 €", "1.860 €", "1.760 €", "2.020 €", "2.270 €"],
        ],
        widths=[0.30, 0.14, 0.14, 0.14, 0.14, 0.14], left_cols=[0, 1, 2, 3, 4, 5], hl=[8],
    ),
    CALLOUT("info", "Supuestos de la cuenta de resultados (para que sea auditables)",
            "**Ventas:** año 1 = 32.960 € (proyección mensual de la sección 10); crecimiento del 36 % en el año 2 por fidelización, online y calzado; después 22 %, 13 % y 13 %. **Margen:** 70 % estable, sube a 71–72 % cuando el mix se enriquece con regalo y online. **Gastos de estructura:** año 1 = 1.670 €/mes; año 2 suben por el fin de la tarifa plana (cuota autónoma ~300 €/mes) y más marketing; año 3 se incorpora una ayuda a media jornada; años 4–5 crecen por marketing y segunda tienda en estudio. **Amortización:** 800 €/año de los activos fijos (~3.920 € a 5 años: reformas, mobiliario, equipamiento, imagen); el stock no se amortiza porque rota. **No se incluyen** intereses (no se prevé deuda relevante) ni IVA (se liquida aparte)."),
    P("**La rentabilidad en 3 preguntas:**"),
    GRID([
        ("🧮", "¿Cuándo se recupera la inversión de 21.010 €?",
         "El EBITDA acumulado supera la inversión a mediados del **año 3** (28.610 € acumulados a cierre del año 3). Payback estimado: **2,6 años**."),
        ("💶", "¿Cuánto puede cobrar la promotora?",
         "Nada el año 1 (los ingresos de la empresa de reformas cubren lo personal); **6.000 €/año en el año 2** y ~1.000 €/mes en el año 3, subiendo hasta 12.500 €/año en el año 5. El resto de beneficio se reinvierte en stock y rotación."),
        ("📈", "¿Se llega a la SL?",
         "La facturación supera los 60.000 € en el año 5. El cambio a SL se estudia a partir del año 3–4 con beneficio estable > 15.000 €/año (sección 16)."),
    ]),
    CALLOUT("warn", "Qué pasa si el año 1 no cumple (el escenario más probable)",
            "Si el año 1 cierra con ventas de **26.400 €** (−20 %), el resultado antes de impuestos es de **−1.580 €** y el fondo de maniobra termina el año en ~2.400 €. La tienda sigue siendo viable: no hay deuda, no hay sueldo comprometido, el stock es rotativo y se puede ajustar el pedido del año 2 con datos reales. Este plan está diseñado para sobrevivir a un año 1 mediocre, no para triunfar solo en el papel."),

    S("11.1", "RENTABILIDAD DE LA INVERSIÓN", "VAN, TIR y plazo de recuperación"),
    P("**Análisis de la inversión como proyecto (los 4 indicadores que piden los análisis financieros):**"),
    TABLE(
        ["Indicador", "Valor", "Interpretación"],
        [
            ["Inversión inicial", "21.010 €", "Todo el desembolso para abrir (sección 6)"],
            ["Flujos de caja de la operación (EBITDA)", "3.060 € · 10.500 € · 15.050 € · 18.640 € · 21.900 €", "Caja generada por la tienda en los años 1–5, antes de impuestos y sin considerar la retribución de la promotora"],
            ["VAN al 5 %", "**+36.920 €**", "El proyecto crea 36.920 € de valor sobre el coste del dinero (5 %): es claramente rentable"],
            ["TIR", "**42,0 %**", "Rentabilidad anual del proyecto: muy por encima de cualquier alternativa de ahorro o deuda"],
            ["Plazo de recuperación (payback)", "**2,6 años**", "La inversión se recupera a mediados del año 3 con los flujos acumulados"],
            ["Payback descontado (al 5 %)", "≈ 3,1 años", "Considerando el coste del dinero, la recuperación se produce durante el año 3"],
        ],
        widths=[0.28, 0.34, 0.38], left_cols=[0, 1], hl=[2, 3],
    ),
    P("**Lectura honesta.** El VAN y la TIR son tan altos porque el modelo no paga nóminas los primeros años y porque la inversión es contenida (reformas y web a coste propio, stock rotativo). Es exactamente lo que un inversor o una convocatoria quieren ver: **una inversión moderada con flujos crecientes y recuperación en menos de 3 años**, y al mismo tiempo el plan reconoce que el año 1 puede cerrar en números rojos si las ventas no acompañan (escenario de la sección 13)."),
    CALLOUT("tip", "Cómo se trata esta inversión en la solicitud de ayudas",
            "La inversión subvencionable habitual en comercio minorista incluye: reforma y adecuación del local (materiais y obra), mobiliario y equipamiento, marca e imagen (rótulo, etiquetas, packaging), digitalización (web, TPV, cámaras) y stock inicial en algunos programas. Las ayudas suelen cubrir el **30–50 %** del gasto elegible: es la palanca que convierte los 21.010 € en una inversión neta de ~15.000 €. Se detalla en la sección 17."),
]

# ============================================================================
# SECCIÓN 12 · PLAN DE TESORERÍA Y FINANCIACIÓN
# ============================================================================

SECTION_12 = [
    S("12", "PLAN DE TESORERÍA", "De dónde sale el dinero, cuándo se gasta y cuándo vuelve",
      "Una tienda no muere por no ser rentable: muere por quedarse sin liquidez. Este plan de tesorería muestra la necesidad de financiación, el calendario de desembolsos y el colchón de seguridad."),

    P("**Necesidad de financiación (la inversión de la sección 6, vista como dinero):**"),
    TABLE(
        ["Concepto", "Importe", "Cuándo se desembolsa"],
        [
            ["Local: fianza 2 meses + 1er mes", "2.250 €", "En la firma del contrato (mes −4)"],
            ["Reformas (materiales)", "1.900 €", "Meses −4 a −2 (durante la obra)"],
            ["Imagen de marca + mobiliario + equipamiento", "2.020 €", "Meses −3 a −2"],
            ["Legal, suministros, web, marketing apertura", "1.150 €", "Meses −3 a 0"],
            ["Stock inicial completo (pedido China)", "8.690 €", "Mes 0 (cuando llega la mercancía)"],
            ["Reserva de imprevistos", "1.000 €", "Reservada; se usa solo si hace falta"],
            ["Fondo de maniobra", "4.000 €", "Mes 0; disponible en cuenta"],
            ["**TOTAL**", "**21.010 €**", "**Desembolso escalonado en ~4 meses**"],
        ],
        widths=[0.44, 0.16, 0.40], left_cols=[0, 1], hl=[7],
    ),
    P("**De dónde sale (estructura de financiación propuesta):**"),
    TABLE(
        ["Fuente", "Importe", "Notas"],
        [
            ["Aportación de los promotores (ahorros)", "15.000 €", "Capital propio; sin intereses ni devolución"],
            ["Ayudas y subvenciones estimadas (potencial 4.000–12.000 €)", "3.000 €", "Cuota cero Galicia, tarifa plana, ayudas a retornadas, modernización (sección 17). Se presupuesta solo el tramo más probable de devoluciones/ahorro directo"],
            ["Financiación bancaria (MicroBank / ICO / SGR AFIGAL)", "3.010 €", "Solo si las ayudas no se confirman; línea emprendedores hasta 25.000 € sin aval; interés bajo"],
            ["**Total**", "**21.010 €**", "**Con ayudas confirmadas, la financiación bancaria se reduce o desaparece y el excedente engorda el fondo de maniobra**"],
        ],
        widths=[0.44, 0.16, 0.40], left_cols=[0, 1], hl=[3],
    ),
    CALLOUT("success", "Colchón de liquidez tras la apertura",
            "La caja inicial es de 4.000 € (fondo de maniobra) + 1.000 € (reserva de imprevistos). La sección 10 muestra que el mes más bajo de caja es ~2.780 €, es decir, **1,7 veces los gastos fijos mensuales** en el peor momento. Con el colchón completo (5.000 €), el margen sube a 3 meses de gastos. Es un colchón razonable para un negocio sin deuda y con stock rotativo: el riesgo real de quedarse sin caja es bajo."),

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
      "El plan base es una hipótesis; el valor del plan está en saber qué ocurre si esa hipótesis falla. Este análisis somete la cuenta de resultados del año 1 a variaciones realistas y define cuándo se activa cada plan de contingencia."),

    P("**Sensibilidad del resultado del año 1 (sobre 32.960 € de ventas y 1.670 €/mes de gastos):**"),
    TABLE(
        ["Variable", "Variación", "Ventas año 1", "Resultado antes de impuestos", "Caja a cierre", "Veredicto"],
        [
            ["Escenario base", "—", "32.960 €", "+2.260 €", "7.032 €", "Viable con holgura"],
            ["Ventas", "−20 %", "26.400 €", "−1.580 €", "~2.440 €", "Aguanta; aplicar plan B (sección 19)"],
            ["Ventas", "+20 % (online despega)", "39.550 €", "+6.900 €", "~11.645 €", "Acelerar pedidos y marketing"],
            ["Margen bruto", "70 % → 65 %", "32.960 €", "+1.410 €", "~5.384 €", "Positivo, pero revisar costes"],
            ["Margen bruto", "70 % → 60 %", "32.960 €", "−240 €", "~3.736 €", "En el límite; renegociar proveedor"],
            ["Gastos fijos", "+10 % (1.840 €/mes)", "32.960 €", "+930 €", "~5.028 €", "Positivo, margen apretado"],
            ["Ticket medio", "25 € → 20 €", "26.400 €", "−1.580 €", "~2.440 €", "Revisar precios y mix de regalo"],
            ["Apertura", "2 meses de retraso", "29.000 €", "+470 €", "~7.600 €", "Recuperable; ajustar pedido"],
        ],
        widths=[0.16, 0.14, 0.16, 0.20, 0.14, 0.20], left_cols=[0, 1, 2, 3, 4],
    ),
    CALLOUT("warn", "El dato que decide de todo: el punto de equilibrio de caja",
            "La tienda **no pierde el colchón** mientras las ventas anuales no bajen de **22.900 €** (≈ 1.900 €/mes ≈ 73 €/día): ese es el nivel en que la pérdida acumulada iguala el fondo de maniobra de 4.000 €. Por debajo de esa cifra hay que tomar decisiones (renegociar alquiler, recortar marketing, buscar otro formato). El escenario pesimista de este plan (−20 %) queda por encima de ese umbral."),

    P("**Los 3 escenarios del plan, en resumen:**"),
    TABLE(
        ["Escenario", "Probabilidad razonada", "Ventas año 1", "Resultado", "Decisión asociada"],
        [
            ["Conservador — «que no falle nada»", "40 %", "26.400 €", "−1.580 €", "Aguantar con fondo, ajustar pedido año 2, mantener marketing en 340 €/mes (es lo que trae clientes)"],
            ["Base — «el plan tal cual»", "45 %", "32.960 €", "+2.260 €", "Ejecutar el plan, medir, repetir lo que funciona"],
            ["Optimista — «online + regalo despegan»", "15 %", "39.550 €", "+6.900 €", "Reinvertir en stock ganador, subir marketing a 450 €/mes, adelantar el calzado"],
        ],
        widths=[0.22, 0.14, 0.14, 0.14, 0.36], left_cols=[0, 1, 2, 3],
    ),
    P("**Conclusión del análisis.** El resultado es robusto en un rango de ±20 % de ventas: el escenario base cubre gastos y deja caja; el pesimista consume parte del fondo pero no rompe el negocio; el optimista permite acelerar. La variable más delicada es el **margen bruto** (si bajara del 65 % hay que renegociar costes) y la más controlable es el **ticket medio** (el mix de regalo y complementos lo sube, y eso es decisión de la tienda, no del mercado)."),
]

# ============================================================================
# SECCIÓN 14 · DAFO Y PLAN ESTRATÉGICO
# ============================================================================

SECTION_14 = [
    S("14", "DAFO Y PLAN ESTRATÉGICO", "Diagnóstico completo y objetivos a 12, 24 y 36 meses",
      "El DAFO recoge todo lo analizado en las secciones anteriores en una sola vista: las fortalezas que se explotan, las debilidades que se corrigen, las oportunidades que se aprovechan y las amenazas que se vigilan. Después, el plan estratégico lo convierte en objetivos medibles."),

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
            "**Sin sueldo el año 1**: el modelo depende de los ingresos externos de la promotora",
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
        ("Mes 0", "Abrir y aprender", "Apertura con stock completo, campaña de apertura y medición desde el día 1. Objetivo: 3–4 clientes/día y caja que no baje de 2.500 €."),
        ("Mes 3", "Primera revisión real", "Análisis de rotación por modelo: se elimina lo que no vende, se refuerza lo que sí. Primer pedido de reposición con datos. Objetivo: ticket medio ≥ 25 €."),
        ("Mes 6", "Estabilizar y añadir", "Canal online funcionando, primeras colaboraciones locales, valoración del calzado. Objetivo: ventas ≥ 2.700 €/mes y 30 % de clientes recurrentes."),
        ("Mes 12", "Cerrar un año con datos", "Facturación 30.000–36.000 €, caja > 6.000 €, surtido depurado (los 10 mejores modelos = 50 % ventas). Decidir calzado y segunda tienda."),
        ("Mes 24", "Consolidar y cobrar", "Facturación 45.000 €, retribución de 6.000 €/año para la promotora, online al 20 % de ventas. Evaluar SL."),
        ("Mes 36", "Crecer o escalar", "Facturación 55.000 €, retribución 9.000 €/año, posible segunda ubicación o personal auxiliar. Decisión SL con datos."),
    ]),
]

# ============================================================================
# SECCIÓN 20 · CUADRO DE MANDO Y KPIs
# ============================================================================

SECTION_20 = [
    S("20", "CUADRO DE MANDO", "Los 10 indicadores que se vigilan cada semana",
      "Un plan sin medición es una opinión. Estos son los indicadores que la promotora revisa cada semana (30 minutos) y mensualmente (1 hora), con su fórmula y su objetivo."),

    TABLE(
        ["Indicador", "Fórmula", "Objetivo año 1", "Frecuencia", "Si falla…"],
        [
            ["Ventas/día", "Facturación ÷ días abiertos", "≥ 92 €/día (equilibrio); 126 €/día (objetivo)", "Semanal", "Menos de 60 €/día durante 3 semanas → activar plan B"],
            ["Ticket medio", "Ventas ÷ nº tickets", "≥ 25 €", "Semanal", "Bajo 20 € → mejorar mix de regalo y complementos"],
            ["Clientes/día", "Tickets emitidos ÷ días", "3–4 clientes", "Semanal", "Bajo 2 → revisar tráfico, escaparate y pauta"],
            ["Conversión", "Clientes ÷ visitantes que entran", "25–35 %", "Quincenal", "Baja → revisar escaparate y precio percibido"],
            ["Margen bruto", "(Ventas − coste mercancía) ÷ Ventas", "≥ 70 % (media)", "Mensual", "Bajo 65 % → renegociar costes o subir PVP"],
            ["Rotación de stock", "Coste vendido ÷ stock medio (anual)", "≥ 4 veces/año", "Mensual", "Baja → liquidar en rebajas y recortar reposición"],
            ["Gastos fijos", "Suma de todos los fijos", "≤ 1.700 €/mes", "Mensual", "Suben > 5 % → revisar partidas"],
            ["Caja", "Saldo real de la cuenta del negocio", "≥ 4.000 € (colchón)", "Semanal", "Bajo 3.000 € → congelar reposición no urgente"],
            ["Margen de seguridad", "(Ventas − punto equilibrio) ÷ Ventas", "≥ 13 % año 1; ≥ 33 % año 2", "Mensual", "Negativo → riesgo real de pérdidas"],
            ["Coste de adquisición", "Marketing ÷ ventas atribuidas (últimos 60 días)", "≤ 10 % de las ventas", "Mensual", "Alto → ajustar audiencia y mensaje"],
        ],
        widths=[0.22, 0.28, 0.20, 0.10, 0.20], left_cols=[0, 1],
    ),
    CALLOUT("tip", "La rutina de los 30 minutos",
            "Cada lunes: ventas/día, ticket medio, clientes/día y caja (4 números, 10 minutos). Cada mes: margen, rotación, gastos y coste de adquisición (20 minutos). Con eso se sabe si el negocio va bien, regular o mal. **No hace falta un ERP: una hoja de cálculo con 10 columnas basta.**"),
]
