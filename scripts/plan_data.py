# -*- coding: utf-8 -*-
"""
Contenido estructurado del Plan de Negocio KHC.
Fuente: docs/01..05 + calculos/*.csv del repositorio.
Toda cifra está alineada con los CSV (inversión 21.010 €, gastos 1.670 €/mes).
"""

META = {
    "brand": "KHC",
    "document": "Plan de Negocio",
    "subtitle": "Tienda de moda infantil 0–12 años · Marca propia",
    "location": "Oleiros · A Coruña · Galicia",
    "edition": "Edición Septiembre 2026 · v1.5",
    "confidential": "Documento de trabajo — cifras orientativas, en revisión continua",
}

COLORS = {
    "navy": "#10233A",
    "navy2": "#1B3A5C",
    "gold": "#C6A15B",
    "gold2": "#A58142",
    "cream": "#F6F1E7",
    "paper": "#FBF9F4",
    "ink": "#1D2733",
    "muted": "#5B6875",
    "line": "#E3DACB",
    "sage": "#7C9A8C",
    "terracotta": "#C97B5A",
    "blush": "#D9A79B",
    "blue": "#7FA8C9",
    "green": "#4E8A6E",
    "red": "#B4502E",
    "amber": "#C88A2E",
}

def S(num, kicker, title, intro="", ess=None):
    return {"t": "section", "num": num, "kicker": kicker, "title": title, "intro": intro, "ess": ess}


def estimate_minutes(secs_list):
    """Tiempo de lectura estimado por sección (para chips de lectura)."""
    import re as _re
    mins = {}
    for si, b in enumerate(secs_list):
        if b["t"] != "section" or b["num"].count("."):
            continue
        ws = 0
        def add(t):
            nonlocal ws
            if isinstance(t, str):
                ws += len(_re.sub(r"[*`#\[\]<>/]", "", t).split())
        add(b.get("kicker", "")); add(b.get("title", "")); add(b.get("intro", ""))
        if b.get("ess"):
            ws += sum(len(x.split()) for x in b["ess"])
        for bb in secs_list[si + 1:]:
            if bb["t"] == "section" and bb["num"].count(".") == 0:
                break
            for v in bb.values():
                if isinstance(v, str):
                    add(v)
                elif isinstance(v, (list, tuple)):
                    for x in v:
                        if isinstance(x, str):
                            add(x)
                        elif isinstance(x, (list, tuple)):
                            for y in x:
                                if isinstance(y, str):
                                    add(y)
                                elif isinstance(y, (list, tuple)):
                                    for z in y:
                                        if isinstance(z, str):
                                            add(z)
        mins[b["num"]] = max(1, round(ws / 170))
    return mins

def P(html):
    return {"t": "p", "html": html}

def LEAD(html):
    return {"t": "lead", "html": html}

def QUOTE(text):
    return {"t": "quote", "text": text}

def KPIS(items):
    # items: (valor, etiqueta, detalle)
    return {"t": "kpis", "items": items}

def TABLE(cols, rows, widths=None, note=None, left_cols=None, hl=None):
    return {"t": "table", "cols": cols, "rows": rows, "widths": widths,
            "note": note, "left": left_cols or [], "hl": hl or []}

def CALLOUT(tone, title, html):
    return {"t": "callout", "tone": tone, "title": title, "html": html}

def GRID(items):
    # items: (titulo, texto)
    return {"t": "grid", "items": items}

def STEPS(items):
    # items: (titulo, texto|"")
    return {"t": "steps", "items": items}

def CHECKBOXES(items):
    return {"t": "check", "items": items}

def DONUT(title, center_value, center_label, data, note=None):
    return {"t": "donut", "title": title, "cv": center_value, "cl": center_label,
            "data": data, "note": note}

def BARS(title, unit, data, note=None):
    # data: (label, valor, color)
    return {"t": "bars", "title": title, "unit": unit, "data": data, "note": note}

def LINE(title, labels, series, unit="€", colors=None, note=None):
    # series: (nombre, valores)
    return {"t": "line", "title": title, "labels": labels, "series": series,
            "unit": unit, "colors": colors or [], "note": note}

def TIMELINE(items):
    # items: (periodo, titulo, texto)
    return {"t": "timeline", "items": items}

def TWOCOL(ltitle, litems, rtitle, ritems, tones=None):
    return {"t": "twocol", "lt": ltitle, "li": litems, "rt": rtitle, "ri": ritems}

def PAGEBREAK():
    return {"t": "pagebreak"}

def SPACER(pts=10):
    return {"t": "spacer", "pts": pts}

# ----------------------------------------------------------------------------
# SECCIÓN 1 · RESUMEN EJECUTIVO
# ----------------------------------------------------------------------------

SECTION_1 = [
    S("01", "RESUMEN EJECUTIVO",
      "La oportunidad, en dos frases",
      "KHC es una tienda de ropa infantil (0–12 años) con marca propia en un barrio residencial de Oleiros (A Coruña): fabricación directa en China con la etiqueta KHC, tienda física, online propia y marketing local desde el primer día.",
      ess=["Inversión: 21.010 € con todo incluido para abrir",
           "Margen ~70 % por marca propia → equilibrio a 92 €/día",
           "Año 1: 32.960 € de ventas y caja que no baja de 2.700 €",
           "VAN +36.920 € · TIR 42 % · recuperación en 2,6 años"]),
    LEAD("**La idea en una frase:** ropa infantil de calidad media-alta con marca propia, vendida en una tienda cercana donde los padres vuelven cada mes a ver novedades."),

    KPIS([
        ("≈ 21.010 €", "INVERSIÓN TOTAL", "Todo incluido: local, reformas, stock, marca, legal y caja"),
        ("8.690 €", "STOCK INICIAL", "≈ 1.400 uds · 37–39 refs · ropa KHC + bebé/regalo + juguete"),
        ("1.670 €/mes", "GASTOS FIJOS", "Alquiler, cuota, suministros, gestoría, seguro, web y marketing"),
        ("≈ 70 %", "MARGEN BRUTO", "Marca propia China; complementos hasta 85 %"),
        ("≈ 92 €/día", "PUNTO DE EQUILIBRIO", "2.390 €/mes de venta cubren todos los gastos fijos"),
        ("4–7 meses", "TIEMPO HASTA ABRIR", "Desde hoy hasta apertura: local → reformas → primer pedido China"),
    ]),

    P("**El modelo, en cuatro piezas:**"),
    GRID([
        ("🧵", "Marca propia", "Fábricas chinas producen con la etiqueta KHC: margen ~70 % frente al 55–60 % de la reventa."),
        ("📍", "Tienda de barrio", "Oleiros: familias jóvenes, nivel adquisitivo medio-alto y poca competencia infantil."),
        ("🌐", "Online + redes", "Web propia y marketing local de 340 €/mes: la tienda se ve cada semana, no solo el día de apertura."),
        ("🔄", "Stock corto", "Novedades cada 3–4 semanas: poco capital atrapado y clientela que vuelve."),
    ]),

    P("**Por qué funciona.** No compite por precio con las multinacionales ni por volumen con el online: compite por **proximidad, marca y novedad**. Con gastos fijos de 1.670 €/mes y margen del 70 %, bastan **~92 € al día** —3–4 clientes de 25 €— para no perder dinero. Y hay dos ventajas que pocos proyectos tienen: la reforma la hace vuestra empresa (solo se paga material) y los ingresos de esa actividad cubren lo personal los primeros meses, lo que baja la inversión en ~4.000 €."),

    P("**Las 6 ventajas diferenciales, en una lista:**"),
    CHECKBOXES([
        "**Reformas con mano de obra propia:** solo se paga material (1.900 € en vez de 6.000–8.000 €).",
        "**Fabricación directa China → márgenes ~70 %** (8–12 puntos más que un multimarca).",
        "**Web desarrollada internamente:** sin coste de desarrollo, ~10 €/mes.",
        "**Alquiler contenido en Oleiros:** 750 €/mes por un local de 40–50 m².",
        "**Ingresos de la empresa de reformas** cubren lo personal: la tienda no paga sueldo al inicio.",
        "**Stock reducido + rotación rápida:** cero mercancía vieja y capital siempre líquido.",
    ]),

    TABLE(
        ["El plan, en cifras", "Valor", "Dónde se detalla"],
        [
            ["Inversión total (todo incluido)", "21.010 €", "Sección 06"],
            ["Gastos fijos mensuales", "1.670 €/mes", "Sección 07"],
            ["Punto de equilibrio", "92 €/día · 2.390 €/mes", "Sección 08"],
            ["Ventas año 1 (escenario base)", "32.960 €", "Sección 10"],
            ["Beneficio neto año 5", "14.770 €", "Sección 11"],
            ["VAN · TIR · recuperación", "+36.920 € · 42 % · 2,6 años", "Sección 11"],
        ],
        widths=[0.40, 0.30, 0.30], left_cols=[0, 1], hl=[0],
    ),

    CALLOUT("tip", "Cómo leer este plan (para no perderse)",
            "Tres rutas según lo que necesites: **solo números** → secciones 06, 07, 08, 10, 11, 12 y 13 (inversión, gastos, márgenes, proyecciones, tesorería y sensibilidad). **Para la solicitud de ayudas** → 02.2 (equipo y empleo), 02.3 (sostenibilidad e igualdad), 17 (ayudas) y 22 (ficha de 1 página). **Para arrancar esta semana** → 02.1 (local), 17, 18 (hoja de ruta) y 21 (próximos pasos). Cada sección abre con un recuadro «Lo esencial»: si solo tienes 2 minutos, léelos y ya tienes el plan."),
]

# SECCIÓN 2 · EL PROYECTO Y EL MODELO DE NEGOCIO
# ----------------------------------------------------------------------------

SECTION_2 = [
    S("02", "EL PROYECTO", "El modelo de negocio, explicado sin adornos",
      "Cómo funciona KHC por dentro: qué se vende, dónde se vende, quién lo hace y por qué la estrategia de stock reducido es la clave del negocio.",
      ess=["Tienda de barrio + online propia + marketing local desde el día 1", "Clave: stock corto y novedades cada 3–4 semanas", "Ella en tienda, él en reformas y web; empezar como autónoma", "Ayudas a retornadas, mujeres y cuota cero: 4.000–12.000 € de potencial"]),

    P("**Qué es KHC.** Una tienda de ropa infantil de 0 a 12 años con **marca propia**: los diseños, tejidos, colores y etiquetas los elige KHC, y las fábricas chinas los producen con su logo. Ese es el modelo que más margen deja en ropa infantil: el precio de coste solo incluye fábrica + importación, sin intermediarios ni margen de marca ajena."),

    GRID([
        ("🧵", "Producto — Ropa 0–12 años",
         "Bodies, conjuntos bebé, pijamas, camisetas, sudaderas, pantalones, vestidos y abrigos de calidad media-alta (algodón peinado 180–220 g/m², costuras dobles, planchado de etiquetas KHC)."),
        ("🎁", "Motores de ticket — Bebé y regalo",
         "Sets regalo recién nacido, muselinas, baberos, mantas, chupeteros, peluches y juguete sensorial de madera. Suben el ticket medio de 25 € a 40–60 € y son el motivo de compra por impulso junto a caja."),
        ("📍", "Canal 1 — Tienda física de barrio",
         "Local de 40–50 m² en zona residencial de Oleiros, cerca de colegios y parques. El negocio de proximidad: la gente ve, toca, prueba y regala."),
        ("🌐", "Canal 2 — Tienda online propia",
         "WooCommerce desarrollado internamente. Vende en toda España, capta clientes que ya conocen la marca por Instagram y suma facturación sin coste fijo."),
        ("📱", "Canal 3 — Instagram, Facebook y TikTok",
         "Marketing continuo de 340 €/mes: pauta local segmentada a padres/madres en un radio de 15 km, colaboraciones con perfiles locales y contenido de novedades."),
        ("🔄", "Estrategia — Stock corto, rotación rápida",
         "~30 modelos en tienda, pocas unidades por modelo y novedades cada 3–4 semanas. La clientela vuelve a menudo, no queda mercancía vieja y el capital está siempre líquido."),
    ]),

    QUOTE("«No hay que llenar la tienda de stock: hay que llenarla de novedad. Un niño crece cada mes, y su familia tiene un motivo para volver cada mes.»"),

    P("**Quién hace qué.**"),
    TABLE(
        ["Rol", "Quién", "Qué aporta"],
        [
            ["Dirección y venta", "Ella", "Gestión diaria, atención al cliente, compras, redes sociales y operativa de la tienda"],
            ["Acondicionamiento del local", "Tú (empresa de reformas)", "Reforma completa a coste de materiales (1.900 €): pintura, suelo vinílico, iluminación y probador"],
            ["Web y tecnología", "Tú", "Tienda online, dominio/hosting (≈10 €/mes), TPV, cámaras y soporte"],
            ["Estrategia y números", "Ambos", "Plan de negocio, pedidos a China, análisis de rotación y finanzas"],
        ],
        widths=[0.22, 0.33, 0.45], left_cols=[0],
    ),

    CALLOUT("info", "Forma jurídica inicial: autónoma",
            "Se empieza como **autónoma** con tarifa plana (80 €/mes el primer año) y, en Galicia, con la **cuota cero** para nuevos autónomos (devolución de cuotas durante hasta 2 años sujeto a requisitos). El cambio a **SL** se valora cuando la facturación estable supere **60.000 €/año**. Detalle completo en la sección 16."),

    S("02.1", "LA UBICACIÓN", "Por qué Oleiros y no el centro de A Coruña",
      "La ubicación no es un detalle: es la mitad del negocio. KHC es una tienda de proximidad, y la proximidad en ropa infantil significa familias jóvenes con niños pequeños a menos de 10 minutos andando."),

    TABLE(
        ["Factor", "Oleiros (Santa Cruz · Perillo · Bastiagueiro)", "Centro de A Coruña"],
        [
            ["Perfil de cliente", "Familias jóvenes, nivel adquisitivo medio-alto, segundo hijo frecuente", "Paso masivo pero heterogéneo; más turista y moda adulta"],
            ["Competencia directa", "Muy baja: casi no hay tienda infantil de regalo/marca propia", "Alta: grandes cadenas y multimarca"],
            ["Alquiler 40–60 m²", "650–900 €/mes", "1.200–2.500 €/mes"],
            ["Clientela recurrente", "Alta: la zona es residencial, la gente vive y repite", "Media: mucha compra de paso, poco vínculo"],
            ["Aparcamiento y paseo", "Bueno, con colegios, parques y guarderías cerca", "Dificultades de parking"],
            ["Distancia de casa", "A minutos, sin perder tiempo en desplazamientos", "20–30 minutos"],
        ],
        widths=[0.24, 0.38, 0.38], left_cols=[0],
    ),

    P("**Criterios del local ideal (checklist para no equivocarse):**"),
    CHECKBOXES([
        "Calle con **paso de peatones** real de familias (no solo tráfico de coches)",
        "Radio de 500 m con **colegio, guardería o parque** (las madres pasan a diario)",
        "**Aparcamiento** a menos de 100 m (regalos y carritos = cliente con coche)",
        "**Escaparate de 3 m o más** y buena luz natural (la ropa infantil se vende visualmente)",
        "Local vacío o con obra menor: **sin traspaso** y sin reforma estructural",
        "**Licencia de actividad comercial** concedida anteriormente en el local",
        "Comercio complementario cerca: moda, juguetería, cafeterías, panadería",
        "Planta baja, sin escaleras y con acceso para carritos de bebé",
    ]),
    CALLOUT("warn", "Zonas a descartar al principio",
            "Centros comerciales grandes (Marineda): alquileres de 1.800–3.500 €/mes y competencia directa con H&M, Zara Kids y multinacionales. Calles de paso nocturno/fiesta. Locales estrechos con escaparate pequeño (la venta en infantil es visual) y locales que exijan reforma estructural."),

    S("02.2", "EQUIPO Y ORGANIZACIÓN", "Quién hace cada cosa, cuántas horas y qué empleo se crea",
      "Un negocio pequeño se organiza por roles, no por organigramas. Este es el reparto real de tareas, el tiempo de dedicación y la previsión de empleo para los próximos 5 años (dato que piden la mayoría de convocatorias)."),
    TABLE(
        ["Rol", "Quién", "Dedicación inicial", "Tareas principales"],
        [
            ["Dirección, compras y venta", "Ella (promotora, autónoma)", "Jornada completa (física en tienda)", "Atención al cliente, compras y pedidos a China, gestión de caja, redes sociales, análisis semanal de ventas"],
            ["Acondicionamiento del local", "Él (empresa de reformas)", "Proyecto puntual (meses −4 a 0)", "Reforma a coste de materiales (1.900 €); factura a KHC como gasto de apertura"],
            ["Web, tecnología y soporte", "Él (empresa de reformas)", "2–4 h/semana los primeros meses", "Tienda online, dominio/hosting, TPV, cámaras, mantenimiento"],
            ["Estrategia y finanzas", "Ambos", "1 h/semana", "Revisión de KPIs, decisiones de stock, seguimiento de tesorería"],
            ["Gestoría y asesoría fiscal", "Gestor externo", "70 €/mes", "Contabilidad, impuestos, nóminas futuras, ayudas"],
            ["Agente de compras en China", "Externo", "Comisión 5–8 % del pedido", "Negociación con fábricas, inspección de calidad, logística y aduanas"],
            ["Ayuda en tienda (temporada alta)", "Contratación a media jornada", "Desde el año 3 (1.000 €/mes de coste)", "Refuerzo en Navidad, vuelta al cole y comuniones; libera a la promotora para compras"],
        ],
        widths=[0.22, 0.22, 0.24, 0.32], left_cols=[0],
    ),
    P("**Previsión de empleo (en puestos equivalentes a jornada completa):**"),
    TABLE(
        ["Periodo", "Empleo ETC", "Detalle"],
        [
            ["Año 1", "1,0", "Promotora a jornada completa (autónoma). Sin nóminas: los ingresos externos cubren lo personal"],
            ["Año 2", "1,0", "Promotora a jornada completa; se valora una ayuda a media jornada en Navidad"],
            ["Año 3", "1,5", "Promotora + ayuda a media jornada contratada (coste ~1.000 €/mes en picos)"],
            ["Año 4", "1,75", "Promotora en dirección + empleada a media jornada estable"],
            ["Año 5", "2,0", "Promotora en dirección + 1 empleada a jornada completa; posible segunda tienda"],
        ],
        widths=[0.14, 0.16, 0.70], left_cols=[0],
    ),
    CALLOUT("info", "Por qué el modelo es casi «sin nómina» al principio",
            "La estructura deliberadamente evita costes fijos de personal durante los primeros 18 meses: la promotora trabaja como autónoma (su retribución sale del beneficio, no de una nómina) y los ingresos de la empresa de reformas cubren lo personal. Eso permite que la inversión inicial baje a 21.010 € y que el punto de equilibrio sea de 92 €/día en lugar de 145 €/día. El empleo se crea cuando la caja lo sostiene: año 3."),

    S("02.3", "SOSTENIBILIDAD, IGUALDAD E INNOVACIÓN", "Los tres ejes que valoran las convocatorias",
      "Las ayudas al comercio (IGAPE, Consellería, fondos Next Generation) puntúan explícitamente estos tres ejes. Este proyecto los cumple de forma natural, no forzada."),
    GRID([
        ("🌱", "Sostenibilidad",
         "Comercio de proximidad (reduce desplazamientos y apoya el tejido local); iluminación LED y eficiencia energética; packaging de papel reciclado con el logo KHC; tejidos con certificación OEKO-TEX; stock reducido = menos excedentes y menos residuo textil; compras consolidadas en contenedor compartido (menos emisiones por prenda)."),
        ("⚖️", "Igualdad",
         "Proyecto **liderado por una mujer** como promotora y autónoma; empresa familiar con conciliación (tienda a minutos de casa); horarios adaptados a la vida del barrio; compras a proveedores que cumplen normativa laboral (auditoría y Trade Assurance)."),
        ("💡", "Innovación",
         "**Marca propia** (no reventa): diseño y etiqueta KHC; **rotación cada 3–4 semanas** con reposiciones por avión; **e-commerce propio** y marketing digital segmentado (Instagram, TikTok, SEO local); datos de venta por modelo para decidir compras; TPV y WhatsApp Business; modelo de negocio difícil de replicar por la competencia de barrio."),
    ]),
]

# ----------------------------------------------------------------------------
# SECCIÓN 3 · MERCADO Y CLIENTE
# ----------------------------------------------------------------------------

SECTION_3 = [
    S("03", "MERCADO Y CLIENTE", "Quién compra, cuánto gasta y cuándo",
      "Una tienda de barrio no necesita captar al 1 % de un mercado enorme: necesita que el 5 % de las familias de su entorno la conozcan y repitan. Estas son las claves del comportamiento de compra.",
      ess=["~8.000 niños de 0–12 años en el entorno ≈ 1,6 M€/año de gasto", "Solo hace falta captar el 2–3 %: 3–4 clientes al día", "Cadenas y online no dan lo que da una tienda de barrio", "Diferenciación: tacto, asesoramiento, regalo y packaging KHC"]),

    P("**El cliente tipo de KHC** es una madre (o padre) de 28–45 años, de nivel medio-alto, que vive a menos de 10 minutos de la tienda y que compra para: (1) necesidades básicas del bebé, (2) regalo de nacimiento, bautizo o cumpleaños, y (3) caprichos de calidad para sus hijos. Valora el **tacto y la cercanía** por encima del precio: sabe lo que es el algodón peinado, busca algo bonito que no haya en el supermercado y paga 12–15 € por un body de calidad si lo puede tocar y se lo aconsejan."),

    TABLE(
        ["Concepto de compra", "Cuándo", "Ticket medio", "Por qué es clave"],
        [
            ["Regalo de nacimiento", "Todo el año — pico otoño", "30–60 €", "El cliente no compara precio: compra el conjunto bonito y la caja regalo"],
            ["Bautizo / Comunión", "Abril–junio", "50–140 €", "Tickets altísimos y compra planificada: hay que tener colección"],
            ["Ropa de temporada", "Sept–Oct y Feb–Mar", "25–45 €", "Recurrencia real: los niños cambian de talla cada 4–6 meses"],
            ["Complementos e impulso", "Cualquier día", "4–12 €", "Margen 80–85 % y rotación instantánea junto a caja"],
            ["Navidad", "Nov–Dic (50 % del año en 2 meses para tiendas infantiles)", "35–70 €", "La temporada más importante; hay que planear stock desde agosto"],
            ["Online (toda España)", "Continuo", "35–55 €", "Incrementa facturación sin coste fijo; el envío lo paga el cliente"],
        ],
        widths=[0.24, 0.24, 0.16, 0.36], left_cols=[0],
    ),

    P("**Tamaño del mercado y demanda potencial (método bottom-up del «barrio»).** El mercado objetivo se estima a partir del entorno real, no de cifras macro: en el entorno de Oleiros (Santa Cruz, Perillo, Bastiagueiro, Dorneda) viven, de forma conservadora, **más de 8.000 niños de 0–12 años** (una población de ~40.000 habitantes en el entorno con una estructura de edad joven, superior a la media gallega). Con un gasto medio de ~200 €/año por niño en ropa, el gasto anual en ropa infantil del entorno ronda los **1,6 millones de €**. KHC solo necesita captar el **2–3 %** de ese gasto (32.000–48.000 €/año) para alcanzar el objetivo del primer año. Es un objetivo alcanzable con 3–4 clientes al día."),
    TABLE(
        ["Parámetro de demanda", "Valor conservador", "Fuente / hipótesis"],
        [
            ["Población del entorno de Oleiros (área de influencia 3–5 km)", "≈ 40.000 habitantes", "Cifras de población municipal del entorno; zonas residenciales consolidadas"],
            ["Niños de 0–12 años estimados", "≈ 8.000 (20 %)", "Estructura de edad joven del área, superior a la media gallega"],
            ["Gasto medio anual en ropa infantil por niño", "≈ 200 €", "Gasto medio en moda infantil España; rango 150–250 € según nivel adquisitivo"],
            ["Gasto total en ropa infantil del entorno", "≈ 1,6 M€/año", "8.000 niños × 200 €"],
            ["Cuota necesaria para el objetivo del año 1 (32.000–36.000 €)", "2,0–2,3 %", "Facturación objetivo ÷ gasto total del entorno"],
            ["Clientes necesarios para ese objetivo", "≈ 104 compras/mes", "3–4 clientes/día de 25 € de ticket medio"],
        ],
        widths=[0.34, 0.26, 0.40], left_cols=[0],
    ),
    CALLOUT("info", "Por qué la cuota del 2–3 % es realista (y no una promesa)",
            "Una tienda de barrio no compite por el 100 % del mercado: compite por el porcentaje que sus clientes le dan por **proximidad, marca y novedad**. Con 8.000 niños en el entorno, alcanzar 3–4 clientes al día (104 al mes) es captar una parte mínima del gasto que ya existe. Además, la tienda online añade un mercado nacional sin coste fijo adicional, y los artículos de regalo/impulso elevan el ticket medio por encima de los 25 € usados en el cálculo — el escenario es prudente."),

    S("03.1", "COMPETENCIA Y DIFERENCIACIÓN", "Con quién compite KHC y dónde está su hueco",
      "KHC no compite de frente con nadie: compite por el mismo presupuesto familiar desde un posicionamiento distinto. Este análisis identifica los competidores reales del entorno y las ventajas con las que KHC se diferencia."),
    TABLE(
        ["Competidor / alternativa", "Tipo", "Fortaleza", "Debilidad frente a KHC"],
        [
            ["Multinacionales y cadenas (H&M Kids, Zara Kids, Primark, Lefties)", "Moda de volumen", "Precio, stock masivo, marca conocida", "Sin marca propia, sin asesoramiento, ropa «de colección» que se repite; no hacen regalo personalizado"],
            ["Tiendas multimarca de bebé (boutiques de A Coruña)", "Especializadas", "Surtido amplio de marcas", "Márgenes bajos (son intermediarios), precios altos; pocas con tienda online propia"],
            ["Puericultura y farmacias", "Bebé funcional", "Marca de confianza, tráfico alto", "No venden ropa de moda ni regalo; compra funcional, no emocional"],
            ["Online (Amazon, Shein, Temu, Zalando)", "Precio y comodidad", "Precio, catálogo infinito", "Cliente de barrio valora tocar la tela, tallar en persona y el regalo con envase bonito; sin trato humano ni urgencia"],
            ["Jugueterías y supermercados", "Regalo genérico", "Volumen, conocido", "No especializadas en bebé; regalo sin personalización KHC"],
            ["Segunda mano (Vinted, Wallapop)", "Precio", "Muy barato", "Sin garantía de calidad, sin marca, sin experiencia de compra; no compite por el mismo cliente de regalo"],
        ],
        widths=[0.28, 0.16, 0.26, 0.30], left_cols=[0],
    ),
    P("**La conclusión competitiva es clara:** el hueco de KHC está entre la moda de volumen (que no personaliza ni asesora) y la tienda funcional de puericultura (que no hace moda ni regalo). KHC cubre ese espacio con **marca propia a precio medio, asesoramiento real, producto de regalo con packaging propio y proximidad**."),
    CALLOUT("success", "La barrera de entrada que KHC construye (y por qué no es fácil de copiar)",
            "El modelo se apoya en 4 ventajas difíciles de replicar por la competencia: (1) **margen del 70 %** por fabricación directa con marca propia — un multimarca no puede bajar precios sin perder margen; (2) **relación de barrio**: la clientela repite porque la conocen, es la ventaja de la tienda física frente al online; (3) **rotación cada 3–4 semanas**: la competencia trabaja con temporada larga y no renueva el escaparate; (4) **canal propio online y WhatsApp** con la marca KHC, que convierte la tienda en una marca, no en un punto de venta."),

    CALLOUT("tip", "Estacionalidad: la curva que hay que respetar",
            "La ropa infantil es extraordinariamente estacional: **Navidad, reyes, comuniones y vuelta al cole** concentran la facturación. El plan de pedidos a China tiene que trabajar al revés: el stock de Navidad se pide en julio–agosto, el de comuniones en enero–febrero y el de primavera en noviembre–diciembre. La estrategia de rotación rápida (pedidos pequeños + refuerzos por avión en 7–10 días) es el seguro contra los picos imprevistos."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 4 · MARCA, PRODUCTO Y SURTIDO
# ----------------------------------------------------------------------------

SECTION_4 = [
    S("04", "MARCA, PRODUCTO Y SURTIDO", "El mix completo: qué se vende, cuánto de cada cosa y qué NO se vende",
      "El surtido inicial de 8.690 € cubre la tienda completa y deja margen para rotar. Aquí está el detalle de cada categoría, el porqué de cada decisión y la lista explícita de lo que se excluye para no tirar el dinero.",
      ess=["≈ 1.400 unidades · 37–39 referencias · 8.690 € de stock", "30 modelos de ropa KHC + bebé/regalo + juguete pequeño", "Complementos y regalo: margen 80–90 % e impulso junto a caja", "No se traen: carritos, bañeras, calzado ni sillas de coche"]),

    P("**Filosofía de surtido: poco, bueno, rotativo.** 30 modelos de ropa con una media de 20–35 unidades por modelo (MOQ pequeño, trabajando con fábricas pequeñas/medianas o agente), 4–5 referencias de complementos de alta rotación, una colección de bebé/regalo que dispara el ticket y una selección mínima pero rentable de juguete de madera y peluche. Todo ello con un surtido completo de marca española en lo que el cliente busca por nombre (Suavinex, Nuk, Avent, Interbaby)."),

    TABLE(
        ["Categoría", "Modelos / referencias", "Unidades", "Coste puesto en tienda", "Margen bruto"],
        [
            ["Ropa KHC (bodies, conjuntos, pijamas, camisetas, sudaderas, pantalones, vestidos, abrigos)", "30 modelos", "825 prendas", "5.500 €", "70–79 %"],
            ["Bebé/regalo marca KHC (sets regalo, muselinas, baberos, mantas, chupeteros, sonajeros, toallas, doudous, neceseres)", "9 líneas", "≈ 435 uds", "2.000 €", "75–85 %"],
            ["Artículos bebé de marca española (Suavinex, Nuk, Avent, Interbaby)", "3–4 marcas", "≈ 180 uds", "530 €", "55–60 %"],
            ["Juguete pequeño (madera sensorial, libros de tela, peluche)", "3 líneas", "≈ 90 uds", "310 €", "Alto"],
            ["Complementos KHC (calcetines, diademas, gorros, baberos básicos)", "4–5 refs.", "≈ 530 uds", "350 €", "80–90 %"],
            ["**TOTAL STOCK INICIAL**", "**37–39 refs.**", "**≈ 1.400 uds**", "**8.690 €**", "**Medio ≈ 70 %**"],
        ],
        widths=[0.38, 0.15, 0.13, 0.15, 0.19], left_cols=[0, 4],
        hl=[5],
    ),
    P("*El coste «puesto en tienda» incluye fábrica, flete, seguro, arancel del 12 %, despacho, IVA de importación (deducible) y transporte a Oleiros. El total de 5.500 € de ropa equivale a ~3.550 € FOB en China × factor 1,55.*"),

    P("**¿Basta para llenar una tienda de 45 m²?** Sí, con margen. Un local de 45 m² útiles admite 195–235 prendas colgadas, 280–380 dobladas, 4–6 en maniquíes y 300–400 de reposición en trastienda: **~800–1.000 prendas visibles + reposición**. Los 825 de ropa KHC más 435 de bebé/regalo más 530 complementos y 90 juguetes cubren de sobra, sin apelotonar (que es justo lo que da sensación de calidad)."),

    CALLOUT("success", "Las 5 reglas para que la tienda parezca llena sin gastar más",
            "<ol><li>Dejar 2–3 dedos entre percha y percha: la ropa respira, parece más cara y se ve más cantidad.</li><li>Espejos grandes en paredes: multiplican el espacio visualmente.</li><li>Complementos en el expositor de caja: baratos, y dan sensación de surtido enorme.</li><li>Cambiar el escaparate cada 2 semanas: novedad constante, la gente lo nota.</li><li>Si queda un hueco tras abrir: pedido pequeño por **avión (7–10 días)** de 300–500 € para rellenar en caliente.</li></ol>"),

    S("04.1", "QUÉ NO SE TRAE", "La lista de exclusiones (tan importante como el surtido)",
      "El dinero de una tienda pequeña no está para ocupar metros: está para rotar. Estas categorías se descartan en la apertura porque atan capital, espacio o riesgo."),
    TABLE(
        ["Producto", "Motivo de la exclusión"],
        [
            ["Bañeras", "Mucho espacio de almacenaje, compra única (una por familia) y rotación bajísima"],
            ["Carritos, sillas de paseo, tronas, hamacas, parques", "Inversión y espacio grandes; el cliente los compra en tiendas especializadas con garantía y reparto"],
            ["Sillas de coche", "Normativa de seguridad estricta, homologaciones y marcas concretas; riesgo alto de devolución"],
            ["Juguetes grandes y electrónicos", "Competencia directa de jugueterías, espacio y márgenes menores"],
            ["Calzado", "Gran problema de tallas y stock muerto; se incorpora a los 6 meses si la tienda funciona (o calzado portugués con marca propia)"],
            ["Ropa de embarazada", "No es el público objetivo del arranque"],
            ["Pañales y toallitas a granel", "Margen bajo y compra ya resuelta en supermercado"],
        ],
        widths=[0.28, 0.72], left_cols=[0],
    ),
    P("**Y por qué la estrategia de poco stock es la mejor decisión del plan:** menos capital atrapado en mercancía; si un modelo no vende se liquidan pocas unidades y se pasa página; novedades cada 3–4 semanas que hacen volver a la clientela; menos riesgo de tallas muertas a fin de temporada; se puede probar qué funciona en Oleiros y repetir solo lo que vende; y se liberan 3.000 € de caja para reforzar marketing o reponer lo que rueda. A los 3–4 meses, con datos reales, se hacen pedidos mayores de los modelos ganadores."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 5 · FABRICACIÓN EN CHINA Y CADENA DE SUMINISTRO
# ----------------------------------------------------------------------------

SECTION_5 = [
    S("05", "FABRICACIÓN Y SUMINISTRO", "Marca propia desde China: el proceso completo",
      "El 62 % de la inversión son productos con marca propia fabricados en China. Este es el proceso real: cómo se fabrica, cuánto cuesta puesto en la tienda, cuánto tarda y cómo se hace sin arriesgar el dinero.",
      ess=["Factor 1,55× FOB: cómo se calcula el coste real puesto en tienda", "MOQ bajo con fábricas pequeñas: 100–300 uds por modelo", "3–4 meses desde muestras a tienda → pedir con antelación", "30 % depósito + 70 % contra envío y control de calidad antes de pagar"]),

    P("**Qué es fabricar con marca propia (OEM/ODM).** Las fábricas chinas producen las prendas según las especificaciones de KHC (modelo, tejido, colores, tallas) y las etiquetan con el logo KHC. No hace falta diseñar desde cero: la mayoría de fábricas dejan elegir modelos de su catálogo y cambiar colores, detalles y etiquetas. Ese es el modelo de mayor margen: **el coste es fábrica + importación, sin margen de marca ajena ni distribuidores**."),

    CALLOUT("info", "El número que lo explica todo: factor 1,55 × FOB",
            "Cuando la fábrica cotiza un precio FOB (por ejemplo 3,00 € por una camiseta), el coste real **puesto en la trastienda de Oleiros** es ~1,55 × ese precio (≈ 4,65 €). La regla rápida: **precio de venta ≈ 3,5–3,9 × coste puesto**, lo que da un margen bruto del 68–75 % en ropa y del 75–90 % en complementos."),

    TABLE(
        ["Concepto de importación", "% sobre FOB", "Notas"],
        [
            ["Precio FOB fábrica", "100 %", "Lo que cotiza la fábrica en China"],
            ["Flete marítimo LCL (carga compartida)", "8–12 %", "Contenedor compartido; barato para pedidos de 1.500–3.000 prendas"],
            ["Seguro marítimo", "≈ 1 %", "Cubre el valor de la mercancía en tránsito"],
            ["Arancel UE textil", "12 %", "Sobre CIF (coste + flete + seguro)"],
            ["Despachante de aduanas", "2–3 % (mín. 150–250 € por envío)", "Gestión documental y de aranceles"],
            ["IVA de importación", "21 % (deducible)", "Se paga al llegar y se recupera en las liquidaciones trimestrales"],
            ["Transporte puerto → Oleiros", "≈ 2 %", "Puertos habituales: Vigo, Algeciras o Valencia"],
            ["**Factor total puesto en tienda**", "**≈ 1,50–1,60 × FOB**", "**Regla práctica: 1,55 ×**"],
        ],
        widths=[0.32, 0.20, 0.48], left_cols=[0, 1], hl=[7],
    ),

    S("05.1", "DÓNDE Y CON QUIÉN", "Fábricas, zonas y agentes de compras"),
    TABLE(
        ["Plataforma / zona", "Qué es", "Uso recomendado"],
        [
            ["Alibaba.com", "La mayor plataforma B2B mundial de fábricas", "Búsqueda inicial: filtrar «Verified Supplier» y «Trade Assurance»"],
            ["1688.com", "Mercado interno chino: precios más bajos, en chino", "Con agente; no todas las fábricas exportan solas"],
            ["Made-in-China / Global Sources", "Alternativas con fábricas medianas-grandes", "Segunda ronda de contactos"],
            ["Guangzhou · Foshan · Dongguan (Guangdong)", "La mayor zona textil de China: ropa infantil competitiva", "Zona principal para el primer pedido"],
            ["Zhejiang (Hangzhou · Yiwu · Ningbo)", "Ropa básica, calcetines y complementos", "Complementos y packs"],
            ["Qingdao (Shandong)", "Ropa de bebé de buena calidad", "Bodies y puericultura textil"],
        ],
        widths=[0.30, 0.40, 0.30], left_cols=[0],
    ),
    P("**Agente de compras: la inversión más rentable del primer pedido.** Un agente que hable chino y español negocia en tu nombre, verifica calidad antes de enviar, consolida pedidos de varias fábricas y gestiona envío y aduanas. Su comisión habitual es del **5–8 % del valor del pedido (300–500 € en el primer pedido)** y evita errores que cuestan miles. Nada de pagar el 100 % por adelantado: **30 % depósito + 70 % contra envío** (Trade Assurance o T/T) y, si se puede, inspección de calidad de terceros (QIMA/SGS, 150–300 €) antes de liberar el pago final."),

    S("05.2", "MOQ Y PLAZOS", "Cuánto piden de mínimo y cuánto tarda"),
    TABLE(
        ["Tipo de proveedor", "MOQ por modelo", "MOQ por talla/color", "¿Vale para KHC?"],
        [
            ["Fábrica grande", "500–1.000 uds", "100–200", "No para el primer pedido"],
            ["Fábrica mediana", "300–500 uds", "50–100", "Solo para modelos ganadores"],
            ["Fábrica pequeña / taller", "100–300 uds", "20–50", "Sí: la opción inteligente para empezar"],
            ["Agente con relaciones", "100–200 uds", "Negociable", "Sí: suele bajar el MOQ"],
            ["Stock/overstock", "50–100 uds", "Mezcla", "Para complementar, no para la marca"],
            ["Mercados Yiwu", "5–20 uds", "Sueltas", "Muy flexible pero difícil etiquetar"],
        ],
        widths=[0.26, 0.20, 0.22, 0.32], left_cols=[0],
    ),
    P("**Plan del primer pedido:** ~6.000 € FOB en 20–25 modelos con 80–100 unidades por modelo (2–3 colores, tallas surtidas de 0-6m a 6-7a; la talla 8–12 se compra en menor cantidad porque rota menos). Es perfectamente factible con fábricas pequeñas/medianas de Guangzhou o Zhejiang."),
    TABLE(
        ["Paso", "Plazo"],
        [
            ["Contactar fábricas/agente + negociar muestras", "3–6 semanas"],
            ["Fabricar y aprobar muestras físicas", "2–4 semanas"],
            ["Producción en masa", "30–60 días"],
            ["Control de calidad + preparación del envío", "1 semana"],
            ["Flete marítimo China → puerto España", "28–40 días"],
            ["Aduanas + transporte a Oleiros", "1 semana"],
            ["**Total desde la aprobación de muestras**", "**3–4 meses**"],
        ],
        widths=[0.70, 0.30], left_cols=[0], hl=[6],
    ),
    CALLOUT("warn", "Dos paradas que hay que respetar",
            "**Año Nuevo Chino** (enero–febrero, fecha variable): las fábricas paran 2–4 semanas, con retrasos en cadena. **Golden Week** (principios de octubre): una semana de parón. Los pedidos se planifican con estas paradas en el calendario: el stock de Navidad se pide en julio–agosto como muy tarde."),

    S("05.3", "CALIDAD, NORMATIVA Y PAGOS", "Lo que no se puede negociar"),
    TABLE(
        ["Elemento", "Especificación recomendada"],
        [
            ["Tejido bebé", "Algodón peinado (combed cotton) 180–220 g/m²; nada de cardado, que es más áspero y barato"],
            ["Certificaciones", "OEKO-TEX Standard 100 (clase I para bebé); proveedor conforme a REACH"],
            ["Costuras y cremalleras", "Doble costura en cuello y sisas; cremalleras YKK o equivalente"],
            ["Botones y cordones", "Resistencia a tracción según EN 12586; sin cordones largos (normativa infantil UE)"],
            ["Tintes", "Sin azo-dyes; conformidad REACH"],
            ["Etiquetas", "Etiqueta tejida con logo KHC cosida (calidad percibida superior); composición y tallaje en español según normativa UE"],
            ["Packaging", "Bolsa individual con logo KHC; cajas por modelo y talla"],
        ],
        widths=[0.24, 0.76], left_cols=[0],
    ),
    TABLE(
        ["Método de pago", "Seguridad", "Cuándo usarlo"],
        [
            ["Trade Assurance (Alibaba)", "Alta — escrow", "Opción recomendada para el primer pedido"],
            ["T/T 30 % + 70 % contra B/L", "Media-alta", "El más habitual; nunca 100 % por adelantado"],
            ["Carta de crédito (L/C)", "Alta", "Pedidos grandes; innecesaria al empezar"],
            ["PayPal", "Media", "Muestras y pedidos muy pequeños"],
            ["Western Union / MoneyGram", "Muy baja", "Nunca"],
        ],
        widths=[0.32, 0.22, 0.46], left_cols=[0],
    ),

    S("05.4", "FABRICAR PROPIO VS. COMPRAR EN ESPAÑA", "El mix de origen óptimo"),
    TWOCOL(
        "🧵 Fabricar en China (marca KHC, margen 70–90 %)",
        [
            "Ropa de todas las categorías: bodies, conjuntos, pijamas, camisetas, pantalones, sudaderas, vestidos, abrigos",
            "Complementos textiles: calcetines, diademas, gorros, bufandas, baberos, muselinas, mantas",
            "Sets regalo con packaging KHC (el producto estrella de la tienda)",
            "Artículos de regalo: chupeteros, sonajeros, doudous, toallas de capucha",
        ],
        "🟡 Comprar a distribuidores españoles (margen 55–60 %)",
        [
            "Chupetes, biberones y puericultura de marca (Suavinex, Nuk, Avent): el cliente los busca por nombre",
            "Pedido inicial pequeño de 300–500 € para tener la referencia y medir demanda",
            "Calzado portugués (Felgueiras, Oliveira de Azeméis): calidad excelente a 2–3 h de A Coruña, con MOQ bajos — candidato para el segundo año",
            "Medias y calcetines Cóndor: referencia buscada en Galicia",
        ],
    ),

    S("05.5", "CHECKLIST DEL PRIMER PEDIDO", "Los 13 pasos, en orden"),
    STEPS([
        ("Logo y etiquetas en vectorial", "Preparar logo KHC, etiquetas tejidas, colgantes y diseño de bolsas antes de contactar fábricas."),
        ("Elegir agente o 3–5 fábricas", "Agente hispanohablante de confianza o proveedores de Alibaba con Trade Assurance."),
        ("Definir la lista de modelos", "20–25 modelos para ~6.000 € FOB; tallas cargadas en las medias (1-3m a 6-9m; 2-3a a 5-6a)."),
        ("Pedir muestras", "2–3 fábricas por modelo; presupuesto 300–600 € + 100–250 € de envío."),
        ("Comparar muestras", "Tacto, caída, costuras, etiquetas, tallaje real (medir, no fiarse del tallaje chino)."),
        ("Elegir fábrica y negociar", "Precio, MOQ, plazo, condiciones de pago y penalizaciones por retraso."),
        ("Aprobar muestras y firmar especificaciones", "Tejido, gramaje, colores Pantone, medidas, costuras, etiquetas, packaging."),
        ("Pagar 30 % de depósito", "Por Trade Assurance o T/T; nunca el 100 %."),
        ("Control de calidad en fábrica", "Inspector externo (QIMA/SGS) o tu agente: revisar 50–100 prendas al azar antes del envío."),
        ("Coordinar envío marítimo LCL", "Con despachante de aduanas; documentos: factura, packing list, B/L, certificados."),
        ("Pagar aranceles + IVA de importación", "A la llegada a puerto; el IVA se deduce en la liquidación trimestral."),
        ("Transporte a Oleiros y verificación", "Recontar, revisar calidad, etiquetar/preparar y pasar la ropa por la plancha si hace falta."),
        ("Modelo de un pedido completo", "~3–4 meses con muestras y producción; planear el segundo pedido con datos de venta reales."),
    ]),

    TABLE(
        ["Costes del proceso del primer pedido", "Estimación"],
        [
            ["Muestras de varias fábricas (20–40 uds)", "300–600 €"],
            ["Envío de muestras DHL/FedEx", "100–250 €"],
            ["Inspección de calidad en fábrica", "150–300 €"],
            ["Comisión de agente (5–8 % del pedido)", "300–500 €"],
            ["**Total del proceso**", "**850–1.650 €**"],
        ],
        widths=[0.70, 0.30], left_cols=[0], hl=[4],
    ),
    P("*Estos costes ya están parcialmente incluidos en la línea de stock de la inversión (dentro del factor 1,55 × FOB), pero conviene tenerlos identificados por separado para negociar y controlar.*"),
]
