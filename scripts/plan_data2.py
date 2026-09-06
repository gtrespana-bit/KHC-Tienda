# -*- coding: utf-8 -*-
"""Secciones 6–17 del Plan de Negocio KHC."""
from plan_data import (S, P, LEAD, QUOTE, KPIS, TABLE, CALLOUT, GRID, STEPS,
                       CHECKBOXES, DONUT, BARS, LINE, TIMELINE, TWOCOL,
                       PAGEBREAK, SPACER, COLORS)

# ----------------------------------------------------------------------------
# SECCIÓN 6 · INVERSIÓN INICIAL
# ----------------------------------------------------------------------------

SECTION_6 = [
    S("06", "PLAN ECONÓMICO", "Inversión inicial: línea por línea, sin inflar",
      "La inversión total para abrir KHC en Oleiros con el surtido completo es de **21.010 €**, todo incluido: local, reforma con mano de obra propia, imagen de marca, mobiliario, equipamiento, stock completo, legal, web, marketing de apertura y caja para los primeros meses.",
      ess=["21.010 € línea por línea, sin inflar", "Stock 8.690 € + fondo de maniobra 4.000 € + resto 8.320 €", "Reforma a coste de materiales (1.900 €) y web propia (120 €)", "Desembolso escalonado en ~4 meses"]),

    DONUT("Composición de la inversión inicial — 21.010 €",
          "21.010 €", "inversión total para abrir",
          [
              ("Stock inicial completo", 8690, COLORS["navy"]),
              ("Fondo de maniobra", 4000, COLORS["gold"]),
              ("Local (fianza + 1er mes)", 2250, COLORS["navy2"]),
              ("Reformas (solo materiales)", 1900, COLORS["sage"]),
              ("Mobiliario", 950, COLORS["terracotta"]),
              ("Imagen de marca", 770, COLORS["blush"]),
              ("Legal y seguro", 650, COLORS["blue"]),
              ("Equipamiento", 300, COLORS["amber"]),
              ("Marketing de apertura", 200, COLORS["green"]),
              ("Suministros", 180, COLORS["muted"]),
              ("Web (1 año)", 120, COLORS["red"]),
              ("Reserva de imprevistos", 1000, COLORS["cream"]),
          ],),
    P("**Datos clave de la distribución:** el stock representa el 41 % de la inversión (8.690 €) y el fondo de maniobra el 19 % (4.000 €). Local, reforma, marca, mobiliario, equipamiento, legal, web, suministros y marketing suman 8.320 € (el 40 % restante). No hay traspaso: se busca local vacío, y la reforma se hace a coste de materiales (1.900 €) gracias a la mano de obra propia."),

    TABLE(
        ["Categoría", "Partida", "Importe", "Justificación"],
        [
            ["LOCAL", "Fianza (2 meses) + 1er mes de alquiler a 750 €", "2.250 €", "Alquiler comercial en Oleiros 650–900 €/mes; fianza legal de 2 meses en Galicia"],
            ["REFORMAS", "Solo materiales: pintura, suelo vinílico LVT, focos LED, probador, reparaciones", "1.900 €", "Mano de obra propia: se ahorran 4.000–6.000 € frente a reforma contratada"],
            ["IMAGEN", "Rótulo fachada, vinilo escaparate, logo, etiquetas colgantes, bolsas papel", "770 €", "Imprenta local + diseño en Canva; sin luminoso al principio"],
            ["MOBILIARIO", "Percheros, mostrador, estanterías, 2 maniquíes 2ª mano, espejos, perchas, expositores", "950 €", "Segunda mano y construcción propia; el expositor de bebé junto a caja multiplica el impulso"],
            ["EQUIPAMIENTO", "TPV (lector Revolut/Square + móvil), cajón, etiquetadora, 2 cámaras WiFi, extintor", "300 €", "Sin TPV caro ni impresora de tickets al inicio (envío por SMS/email)"],
            ["STOCK", "Ropa KHC China (825 prendas, 30 modelos)", "5.500 €", "≈ 3.550 € FOB × 1,55 puesto en Oleiros"],
            ["STOCK", "Bebé/regalo marca KHC (sets, muselinas, baberos, mantas, chupeteros…)", "2.000 €", "≈ 435 unidades; márgenes 75–85 % y sube el ticket medio"],
            ["STOCK", "Artículos bebé marca España (Suavinex, Nuk, Avent)", "530 €", "≈ 180 uds; el cliente busca la marca concreta"],
            ["STOCK", "Juguete pequeño (madera, libros de tela, peluche)", "310 €", "≈ 90 uds; regalo, alta rotación, poco espacio"],
            ["STOCK", "Complementos KHC (calcetines, diademas, gorros, baberos)", "350 €", "≈ 530 uds; margen 80–90 %, impulso puro"],
            ["LEGAL", "Alta autónoma, licencia de apertura, seguro primer trimestre, revisión contrato", "650 €", "Local < 50 m² con obra menor: licencia más económica; registro de marca más adelante"],
            ["WEB", "Dominio + hosting 1 año (desarrollo propio)", "120 €", "Dominio 12 € + hosting WooCommerce ~9 €/mes"],
            ["MARKETING", "Campaña pre-apertura + día de apertura", "200 €", "Segmentación local en redes 2 semanas antes; el marketing continuo va en gastos fijos"],
            ["SUMINISTROS", "Altas de luz y agua (fibra sin coste con contrato)", "180 €", "Fianzas y acometidas"],
            ["RESERVA", "Imprevistos", "1.000 €", "Las reformas siempre tienen sorpresas; se rebaja de 2.000 a 1.000 € por obra propia"],
            ["MANIOBRA", "Fondo de maniobra (caja de los primeros meses)", "4.000 €", "Explicado en detalle en la sección 8"],
            ["", "**INVERSIÓN TOTAL PARA ABRIR**", "**21.010 €**", "**≈ 21.000 € con margen**"],
        ],
        widths=[0.14, 0.38, 0.12, 0.36], left_cols=[0, 1, 2], hl=[16],
    ),

    CALLOUT("success", "Qué incluyen los 21.010 € y qué no",
            "Incluye todo lo necesario para abrir y aguantar los primeros meses con stock completo de ropa + bebé + regalo + juguete pequeño. **No incluye** bañeras, carritos, tronas, sillas de coche, calzado ni ropa de embarazada (excluidos a propósito en la sección 4), ni la nómina de ella los primeros meses (los ingresos de reformas cubren lo personal)."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 7 · GASTOS FIJOS MENSUALES
# ----------------------------------------------------------------------------

SECTION_7 = [
    S("07", "GASTOS FIJOS MENSUALES", "1.670 €/mes y cada euro explicado",
      "Los gastos fijos incluyen TODO lo que hay que pagar cada mes funcione o no la tienda: alquiler, cuota de autónoma, suministros, gestoría, seguro, web y marketing continuo. No incluyen sueldo durante los primeros meses ni el coste de la mercancía (que es variable: solo se paga si se vende).",
      ess=["1.670 €/mes con TODO incluido", "Alquiler y comunidad: 800 €/mes · Marketing: 340 €/mes", "Cuota autónoma 80 € (tarifa plana) y cuota cero en Galicia", "Sin sueldo al inicio: el punto de equilibrio baja a 92 €/día"]),

    BARS("Desglose mensual de los 1.670 €", "€/mes", [
        ("Alquiler + comunidad", 800, COLORS["navy"]),
        ("Marketing continuo", 340, COLORS["gold"]),
        ("Suministros (luz, agua, fibra)", 195, COLORS["sage"]),
        ("Gestión (autónoma + gestoría)", 150, COLORS["terracotta"]),
        ("Otros corrientes (consumibles, mantenimiento, banca, imprevistos)", 140, COLORS["blue"]),
        ("Seguro", 35, COLORS["blush"]),
        ("Web (hosting prorrateado)", 10, COLORS["amber"]),
    ]),

    TABLE(
        ["Partida", "€/mes", "Comentario"],
        [
            ["Alquiler local (40–50 m², Oleiros)", "750", "Zonas residenciales: 650–900 €/mes"],
            ["Comunidad", "50", "Edificio con local comercial"],
            ["Cuota autónoma (tarifa plana 1er año)", "80", "80 €/mes los 12 primeros meses; con la cuota cero de Galicia puede ser 0 € en periodos (sujeto a requisitos). Se presupuesta conservador"],
            ["Electricidad (LED, local pequeño)", "130", "Iluminación eficiente; media de negocio similar"],
            ["Agua", "20", "Uso básico"],
            ["Fibra internet", "45", "Necesaria para TPV, cámaras y web"],
            ["Gestoría", "70", "Contabilidad de autónoma; sube al doble si se pasa a SL"],
            ["Seguro multirriesgo + RC", "35", "≈ 380–480 €/año prorrateado"],
            ["Web (hosting + dominio)", "10", "Desarrollo propio; sin coste de programación"],
            ["Marketing continuo", "340", "250 € pauta social + 50 € colaboraciones locales + 40 € consumibles/embalaje"],
            ["Consumibles, mantenimiento, banca, imprevistos", "140", "Etiquetas, limpieza, arreglos, comisiones, reserva mensual"],
            ["**TOTAL GASTOS FIJOS**", "**1.670 €**", "**Redondeando: ≈ 1.700 €/mes**"],
        ],
        widths=[0.46, 0.14, 0.40], left_cols=[0, 1], hl=[11],
    ),

    CALLOUT("info", "La clave del marketing continuo",
            "KHC no puede permitirse dejar de estar visible: el presupuesto de **340 €/mes** (≈ 11 €/día) se invierte en pauta local segmentada a padres y madres en un radio de 15 km, colaboraciones con perfiles locales y material para la web/escaparate. Es el gasto que convierte una tienda de barrio en la tienda de referencia de su zona; si las ventas lo permiten, es lo primero que se escala."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 8 · MÁRGENES, EQUILIBRIO Y FONDO DE MANIOBRA
# ----------------------------------------------------------------------------

SECTION_8 = [
    S("08", "MÁRGENES Y PUNTO DE EQUILIBRIO", "Cuánto hay que vender para no perder dinero (y para vivir)",
      "Esta es la sección que convierte el plan en números útiles: margen bruto del ~70 % sobre el coste real puesto en tienda, punto de equilibrio diario, escenarios de sueldo y la justificación del fondo de maniobra de 4.000 €.",
      ess=["Margen medio ~70 %; complementos y regalo hasta el 90 %", "Equilibrio: 2.390 €/mes ≈ 92 €/día (3–4 clientes de 25 €)", "Sueldo 1.000 € → 158 €/día · 2.000 € → 224 €/día", "Fondo de 4.000 € = 2,4 meses de gastos de colchón"]),

    P("**El margen bruto.** Cada prenda se compra a su coste real (fábrica + importación: factor 1,55 × FOB) y se vende a 3,4–3,9 × ese coste. Resultado: un margen bruto medio del **70 %** (68–75 % en ropa, 75–90 % en complementos y regalo, 55–60 % en marca española). Esto significa que **por cada 100 € vendidos, quedan 70 € para pagar gastos fijos y generar beneficio**; la mercancía cuesta 30 €."),

    TABLE(
        ["Categoría", "Coste real (puesto en tienda)", "PVP orientativo", "Margen bruto", "Markup"],
        [
            ["Body algodón peinado OEKO-TEX", "2,10–3,20 €", "9,90–15,90 €", "73–80 %", "≈ 3,9×"],
            ["Conjunto bebé 3 piezas (regalo estrella)", "6,20–8,90 €", "29,90–48,90 €", "70–76 %", "≈ 3,7×"],
            ["Sudadera con capucha", "5,20–7,70 €", "21,90–34,90 €", "70–76 %", "≈ 3,4×"],
            ["Pantalón jogger / vaquero", "3,70–8,40 €", "18,90–38,90 €", "69–78 %", "≈ 3,4–3,7×"],
            ["Abrigo / plumífero", "10,10–15,50 €", "39,90–69,90 €", "68–75 %", "≈ 3,2×"],
            ["Calcetines (par)", "0,50–0,80 €", "3,50–7,50 €", "80–88 %", "≈ 5,8×"],
            ["Diadema / lazo", "0,30–1,10 €", "3,90–9,90 €", "82–90 %", "≈ 6,8×"],
            ["Set regalo caja KHC (montado en tienda)", "6,40–10,50 €", "29,90–54,90 €", "75–81 %", "≈ 4,3×"],
            ["Vestido/traje de comunión (temporada)", "17–30 €", "69,90–139,90 €", "72–79 %", "≈ 4,0×"],
            ["**Media ponderada KHC**", "—", "—", "**68–75 %**", "**≈ 3,8×**"],
        ],
        widths=[0.30, 0.24, 0.20, 0.14, 0.12], left_cols=[0], hl=[9],
    ),
    P("*Para los cálculos globales se usa un **70 % conservador** (el mix real con regalos y complementos tiende a ser mejor). Además hay que descontar 0,4–0,8 % de comisión TPV, 3–5 % de devoluciones (muchas son cambios de talla) y 2–3 % de mermas/rebajas: todo ya contemplado en el margen conservador.*"),

    S("08.1", "¿CUÁNTO HAY QUE VENDER?", "Los tres escenarios que importan"),
    TABLE(
        ["Escenario", "Fórmula", "Ventas/mes", "Ventas/día (26 días)", "Qué significa"],
        [
            ["Cubrir gastos", "1.670 € ÷ 0,70", "2.386 € → 2.390 €", "≈ 92 €/día", "3–4 clientes/día de 25 € de ticket medio: la tienda ya no pierde dinero"],
            ["Sueldo 1.000 €/mes (neto)", "(1.670 + 1.200) ÷ 0,70", "≈ 4.100 €", "≈ 158 €/día", "≈ 6–7 clientes/día; objetivo del año 1–2 con online"],
            ["Sueldo 2.000 €/mes (neto)", "(1.670 + 2.400) ÷ 0,70", "≈ 5.814 € → 5.800 €", "≈ 224 €/día", "≈ 9–10 clientes/día; objetivo del año 2–3"],
        ],
        widths=[0.18, 0.20, 0.18, 0.18, 0.26], left_cols=[0, 1, 2, 3],
    ),
    CALLOUT("info", "El cálculo en una línea",
            "Por cada euro vendido, 0,70 € van a pagar la tienda. Por eso ventas = gastos fijos ÷ 0,70. Con sueldo se trata igual: se suma el coste bruto del sueldo (neto + ~20 % de cotizaciones) a los gastos fijos y se divide entre 0,70. **Este es el termómetro que se vigila cada semana.**"),

    S("08.2", "FONDO DE MANIOBRA", "Por qué 4.000 € y no 0 € ni 8.000 €"),
    P("El fondo de maniobra **no es un gasto**: es dinero en la cuenta de la tienda para pagar facturas cuando las ventas todavía no cubren los gastos. Antes se habían puesto 8.000 € contando sueldo desde el mes 1; al no haber sueldo los primeros meses (los ingresos de reformas cubren lo personal), el fondo se reduce a la mitad: **4.000 €**, algo más de 2 meses de gastos completos como colchón."),
    P("Proyección realista de los 6 primeros meses (ventas de apertura con su curva post-apertura, mercancía 30 % del importe vendido, gastos 1.670 €/mes):"),
    LINE("Caja al final de cada mes (€) · partiendo de 4.000 €",
         ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"],
         [("Caja acumulada", [4290, 3880, 3750, 3900, 4330, 4900])],
         unit="€"),
    TABLE(
        ["Mes", "Facturación", "Coste mercancía (30 %)", "Gastos fijos", "Resultado del mes", "Caja al final"],
        [
            ["Mes 1 (apertura)", "2.800 €", "840 €", "1.670 €", "+290 €", "4.290 €"],
            ["Mes 2 (bajada normal)", "1.800 €", "540 €", "1.670 €", "−410 €", "3.880 €"],
            ["Mes 3", "2.200 €", "660 €", "1.670 €", "−130 €", "3.750 €"],
            ["Mes 4", "2.600 €", "780 €", "1.670 €", "+150 €", "3.900 €"],
            ["Mes 5", "3.000 €", "900 €", "1.670 €", "+430 €", "4.330 €"],
            ["Mes 6", "3.200 €", "960 €", "1.670 €", "+570 €", "4.900 €"],
        ],
        widths=[0.22, 0.16, 0.22, 0.14, 0.14, 0.12], left_cols=[0],
    ),
    P("**Conclusión:** la pérdida máxima acumulada esperada es de ~410 € en el mes 2 y se recupera en el mes 4. Con 4.000 € de fondo hay 2,4 meses de gastos completos de margen de seguridad. **Y si las ventas fueran la mitad de lo previsto** (por ejemplo 1.200 €/mes los primeros 4 meses), se perderían ~500 €/mes y el fondo aguantaría 8 meses: tiempo más que suficiente para reaccionar (reforzar marketing, ajustar pedidos, añadir online, abrir horarios)."),
    P("**Regla de decisión:** si al mes 6 la caja está por debajo de 3.500 €, se activa el plan B (sección 19): menos reposición, más pauta local, promociones de temporada y revisión del alquiler. El fondo de maniobra existe precisamente para que esas decisiones se tomen con calma y no con urgencia."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 9 · PROYECCIÓN A 12 MESES Y ESCALADO
# ----------------------------------------------------------------------------

SECTION_9 = [
    S("09", "VISIÓN DE CRECIMIENTO", "Cómo crece KHC: de tienda de barrio a marca",
      "La proyección financiera detallada está en las secciones 10–13 (mes a mes, 5 años, tesorería y sensibilidad). Aquí, la lógica de crecimiento: en qué orden se invierte cada euro de beneficio y qué palanca se activa en cada fase.",
      ess=["Año 1 demostrar · año 2 consolidar · año 3 rentabilizar · año 4 escalar · año 5 marca", "Palanca 1: rotación de stock · palanca 2: online · palanca 3: calzado", "El beneficio se reinvierte en stock ganador, no en extras"]),

    TABLE(
        ["Fase", "Facturación objetivo", "Palanca principal", "Qué se consigue"],
        [
            ["Año 1 — Demostrar", "33.000 €", "Rotación de stock + marketing local", "Surtido depurado, 3–4 clientes/día, caja > 6.000 €, primer año con datos reales"],
            ["Año 2 — Consolidar", "45.000 €", "Canal online + fidelización", "Online al 20 % de ventas, retribución de 6.000 € para la promotora, calzado incorporado"],
            ["Año 3 — Rentabilizar", "55.000 €", "Mix premium (regalo + eventos) + colaboraciones", "Retribución de 9.000 €, beneficio retenido para crecimiento, evaluación de SL"],
            ["Año 4 — Escalar", "62.000 €", "Personal auxiliar + mayor rotación", "La dueña pasa a dirección; más horas de tienda; segundo ciclo de compras optimizado"],
            ["Año 5 — Marca", "70.000 €", "Posible segunda ubicación o franquicia ligera", "Facturación > 60.000 €: momento de decidir SL y estructura de crecimiento"],
        ],
        widths=[0.16, 0.16, 0.30, 0.38], left_cols=[0, 1],
    ),

    S("09.1", "LAS PALANCAS", "En qué orden se invierte el beneficio"),
    STEPS([
        ("Stock y rotación (primera palanca)", "Cuando se sabe qué modelos venden, se suben los pedidos de los ganadores y se recorta a los que no. Más rotación = más margen con menos metros."),
        ("Canal online", "La web propia convierte a KHC en una marca con alcance nacional: envíos con ticket medio 35–55 € y coste marginal casi nulo. El objetivo es que el online sea el 20–30 % de la facturación en el año 2."),
        ("Calzado (mes 6 en adelante)", "Sin calzado en la apertura; a partir del segundo semestre, si la rotación de ropa lo justifica, calzado portugués de marca propia: margen alto y cercanía logística con Galicia."),
        ("Eventos y colaboraciones", "Colecciones de comunión/temporada alta, colaboraciones con guarderías y colegios de la zona, y presencia en ferias locales: cada evento es un pico de facturación planificable."),
        ("Equipo y segunda tienda (año 4–5)", "Con facturación estable > 60.000 € y beneficio > 15.000 €/año, la SL tiene sentido fiscal y se abre la puerta a ampliar, incorporar socios o una segunda ubicación."),
    ]),
    CALLOUT("info", "La regla de inversión del beneficio",
            "Cada 1.000 € de stock extra que rota a 3,5× genera ~2.500 € de margen bruto anual. Por eso el beneficio del año 1 se reinvierte en **stock ganador y marketing**, no en equipamiento ni en retribución: el dinero que produce crecimiento es el que está en la mercancía que se vende."),
    GRID([
        ("📈", "Indicadores que se vigilan", "Ventas/día, ticket medio, unidades por categoría, % de stock rotado, coste de adquisición por cliente, caja. Definición completa en la sección 20."),
        ("🧭", "Regla del 70 %", "Mientras el margen bruto se mantenga ≥ 70 % y la caja suba mes a mes, se puede acelerar; si baja de 65 %, se para la expansión y se revisa el surtido."),
        ("🎯", "Regla del 20–30 %", "Mantener el marketing entre el 20–30 % del gasto de estructura (340 € sobre ~1.670 €/mes): es el gasto que convierte una tienda de barrio en la referencia de su zona."),
    ]),
]

# ----------------------------------------------------------------------------
# SECCIÓN 10 · MARKETING Y VENTAS
# ----------------------------------------------------------------------------

SECTION_15 = [
    S("15", "MARKETING Y VENTAS", "El plan 360º: abrir con ruido y no desaparecer",
      "Una tienda de barrio no se llena sola: se llena con un sistema simple y constante. Este es el plan de marketing completo, presupuestado y realista: 200 € de apertura + 340 €/mes de continuidad.",
      ess=["200 € de apertura + 340 €/mes de marketing continuo", "Pauta local 8–9 €/día en un radio de 15 km", "Escaparate cada 2 semanas y 3 publicaciones por semana", "Google Maps y reseñas: la compra de barrio empieza online"]),

    TABLE(
        ["Fase", "Acción", "Coste", "Objetivo"],
        [
            ["Pre-apertura (2 semanas antes)", "Campaña en Instagram/Facebook/TikTok segmentada a padres/madres de Oleiros y área (radio 15 km): «KHC abre en tu barrio», teasers del local, sorteo de apertura", "150 €", "Que toda familia con niños de la zona sepa que KHC abre"],
            ["Día de apertura", "Evento: globos, pequeños detalles para niños, foto con mascota, presencia de micro-influencers locales", "50 €", "Boca a boca + contenido para redes"],
            ["Continuo (mes a mes)", "Pauta 8–9 €/día en redes sociales segmentada local + contenido de novedades 3 veces/semana", "250 €/mes", "Que la marca aparezca cuando la familia busca ropa infantil o regalo"],
            ["Continuo", "Colaboraciones con perfiles locales (madres influencers de A Coruña/Oleiros), entregas de producto para regalos", "50 €/mes", "Prueba social; el 40 % de la clientela de barrio llega por recomendación"],
            ["Continuo", "Consumibles de marca: bolsas, tarjetas, embalaje de la web", "40 €/mes", "Que el packaging recuerde a KHC y se comparta"],
            ["Web y e-commerce", "WooCommerce propio: SEO local, catálogo, envíos a toda España, captación de email/WhatsApp", "≈ 10 €/mes", "Facturación adicional sin coste fijo"],
            ["Retención", "WhatsApp Business + lista de email + programa de puntos + recordatorios de cambio de talla y novedades", "0 €", "Que la clientela vuelva: el 50 % del objetivo son 3–4 clientes/día recurrentes"],
        ],
        widths=[0.18, 0.46, 0.12, 0.24], left_cols=[0, 2],
    ),

    GRID([
        ("🏪", "Escaparate = escaparate de novedades", "Cambiar cada 2 semanas. Un escaparate que se mueve hace que la gente pare; uno estático hace que dejen de mirar."),
        ("📍", "Google Maps + reseñas", "Ficha de negocio optimizada, fotos del producto y del interior, responder cada reseña. El 70 % de las compras de barrio empiezan buscando «tienda ropa infantil cerca de mí»."),
        ("🤝", "Alianzas locales", "Guarderías, colegios, academias y fotógrafas de recién nacidos de la zona: descuentos cruzados y presencia en sus recomendaciones."),
        ("🎯", "Medición", "Cada 100 € de pauta tienen que traer visitas y ventas medibles. Si una campaña no convierte en 4 semanas, se cambia el mensaje o la audiencia."),
    ]),
    CALLOUT("tip", "El hábito que sostiene todo el plan",
            "Publicar **3 novedades por semana en Instagram/TikTok** (producto, detalle, «hoy en tienda», reels de outfits) cuesta tiempo de ella, no dinero, y es la mitad del efecto del marketing. La tienda pequeña que funciona es la que se ve cada semana, no la que se vio una vez."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 11 · FORMA JURÍDICA
# ----------------------------------------------------------------------------

SECTION_16 = [
    S("16", "FORMA JURÍDICA", "Autónoma ahora, SL cuando toque",
      "La decisión fiscal más importante del proyecto tiene una respuesta clara y sin mitos: **empezar como autónoma** los primeros 18–24 meses y pasar a SL cuando la facturación estable supere 60.000 €/año con planes de crecimiento confirmados.",
      ess=["Autónoma 18–24 meses; SL a partir de 60.000 €/año", "Tarifa plana 80 € + cuota cero de Galicia", "La SL cuesta +2.200 a +3.500 € el primer año", "Pasar luego cuesta ~1.000 € y 2–3 semanas"]),

    TABLE(
        ["Mito", "Realidad"],
        [
            ["«La SL da más imagen de seriedad»", "A los clientes de una tienda de barrio y a los proveedores chinos les da igual; los bancos piden aval personal en ambos casos los primeros años"],
            ["«La SL protege el patrimonio»", "Al principio no: casero, banco y proveedores exigen aval personal. La protección real llega con 3–4 años de solvencia"],
            ["«La SL paga menos impuestos»", "Por debajo de ~50.000 € de beneficio, la autónoma paga menos"],
            ["«Cambiar luego es un problema»", "Pasar de autónomo a SL cuesta ~1.000 € y 2–3 semanas: trámite rutinario"],
            ["«Con SL se deducen más gastos»", "Los gastos de actividad se deducen prácticamente igual en ambos regímenes"],
        ],
        widths=[0.28, 0.72], left_cols=[0],
    ),
    TABLE(
        ["Concepto", "Autónoma", "SL"],
        [
            ["Constitución", "0–150 €", "1.200–1.800 € (+3.000 € capital social que se queda en la empresa, no es gasto)"],
            ["Cuota Seguridad Social", "80 €/mes tarifa plana; luego 230–300 €", "La misma cuota exacta: la administradora también se da de alta en autónomos"],
            ["Gestoría", "60–130 €/mes", "120–200 €/mes (doble: más contabilidad)"],
            ["Obligaciones", "Libro de ingresos/gastos sencillo", "Balances, actas, depósito anual de cuentas en el Registro Mercantil (públicas)"],
            ["Disposición del dinero", "La cuenta es tuya", "El dinero es de la empresa: sacarlo requiere nómina o dividendos con impuestos"],
            ["Cierre", "~50 € y 1 semana", "800–1.500 € y 3–6 meses"],
            ["**Coste extra el primer año**", "—", "**+2.200 a +3.500 €**"],
        ],
        widths=[0.26, 0.36, 0.38], left_cols=[0], hl=[6],
    ),
    TABLE(
        ["Beneficio anual", "Impuestos autónoma (IRPF)", "Impuestos SL (Sociedades + dividendos)", "Mejor opción"],
        [
            ["12.000 €", "1.500 € (12,5 %)", "4.700 €", "Autónoma ✅"],
            ["20.000 €", "3.900 € (19,5 %)", "7.375 €", "Autónoma ✅"],
            ["30.000 €", "7.350 € (24,5 %)", "10.500 €", "Autónoma ✅"],
            ["40.000 €", "11.000 € (27,5 %)", "13.500 €", "Autónoma (diferencia pequeña)"],
            ["50.000 €", "15.000 € (30 %)", "16.500 €", "Prácticamente igual"],
            ["60.000 €", "19.200 € (32 %)", "19.500 €", "Empate"],
            ["70.000 €", "23.800 € (34 %)", "22.500 €", "SL ✅"],
            ["100.000 €+", "37 %+ marginal", "25 % si se reinvierte; ~44 % si todo en dividendos", "SL ✅ (si se reinvierte)"],
        ],
        widths=[0.20, 0.27, 0.33, 0.20], left_cols=[0, 1, 2],
    ),
    CALLOUT("info", "El matiz clave de la SL",
            "El 25 % de Sociedades solo aplica al dinero que **se queda en la empresa** para reinvertir. Si el beneficio se saca como dividendos, hay que pagar además un 19–26 %, y la ventaja fiscal desaparece hasta beneficios muy altos. Por eso la SL solo tiene sentido cuando hay reinversión de verdad (más stock, personal, segunda tienda)."),
    P("**Plan de ruta:** mes 0 → alta de autónoma para ella con tarifa plana (tú mantienes tu empresa de reformas separada); meses 18–24 → revisión con números reales: si la facturación es estable < 60 k, se sigue de autónoma sin prisa; si es > 60 k con planes de crecimiento, se pasa a SL en ese momento. Y aunque la tienda sea autónoma, **tú puedes facturar legalmente la reforma del local** desde tu empresa a precio de mercado: la tienda se lo deduce como gasto de apertura."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 12 · AYUDAS Y FINANCIACIÓN
# ----------------------------------------------------------------------------

SECTION_17 = [
    S("17", "AYUDAS, SUBVENCIONES Y FINANCIACIÓN", "El dinero que se puede recuperar (y cómo pedirlo)",
      "Hay ayudas muy relevantes para este proyecto concreto, especialmente por tres motivos: es una mujer emprendedora, es un retorno de emigración (Venezuela) y se implanta en Galicia. **La regla de oro: muchas ayudas se solicitan ANTES del alta de actividad, no después.**",
      ess=["Potencial de 4.000–12.000 € entre ayudas y ahorro", "Cuota cero, tarifa plana, retornadas y modernización", "Regla de oro: solicitar ANTES del alta de actividad", "La inversión neta puede quedar por debajo de 15.000 €"]),

    TABLE(
        ["Ayuda / programa", "Importe potencial", "Para qué", "Estado / cómo se tramita"],
        [
            ["Tarifa plana estatal", "Ahorro ~1.800–2.600 € en el primer año", "Cuota autónoma a 80 €/mes (en vez de 230–300 €)", "Alta en Hacienda + Seguridad Social; no haber sido autónomo en 2 años"],
            ["Cuota cero Xunta de Galicia", "Devolución de cuotas hasta 2 años (hasta ~5.000–6.000 €)", "Nuevos autónomos en Galicia", "Oficina do Emprendedor / IGAPE; requisitos y convocatoria vigente"],
            ["Ayudas a personas retornadas", "3.000–10.000 € (según convocatoria)", "Autoempleo de gallegos retornados del exterior", "Secretaría Xeral da Emigración de la Xunta; certificado de emigrante retornado"],
            ["IGAPE / Consellería de Emprego", "5.000–10.000 € en subvenciones directas", "Mujeres, menores de 35, retornadas; modernización del comercio", "Convocatorias anuales; solicitar antes del alta"],
            ["Ayudas a la modernización del comercio", "30–50 % de reforma y equipamiento", "Reforma, digitalización, TPV, eficiencia energética", "Consellería de Economía, Empresa e Innovación / fondos Next Generation"],
            ["Kit Digital", "2.000–12.000 € en bono", "Web, e-commerce, gestión de redes, TPV, ciberseguridad", "acelerapyme.es; convocatorias continuas"],
            ["Ayuntamiento de A Coruña", "Microcréditos y programas locales", "A Coruña Emprende, oficina municipal de emprendimiento", "Concellaría de Emprego e Economía Social"],
            ["Financiación (si hiciera falta)", "MicroBank hasta 25.000 € sin aval · ENISA 25.000–1.500.000 € · ICO", "Complementar la inversión inicial u operativa", "Bancos/ENISA; requieren plan de negocio (este documento)"],
        ],
        widths=[0.22, 0.18, 0.28, 0.32], left_cols=[0, 1],
    ),
    CALLOUT("success", "Estimación conservadora de ayudas/ahorros potenciales",
            "Entre tarifa plana, cuota cero, ayudas a retornadas y modernización, el **potencial razonable ronda los 4.000–12.000 €** entre ahorro directo y subvenciones (sujeto a requisitos y convocatorias, siempre verificando en las webs oficiales). Con eso, la inversión neta real puede quedar por debajo de 15.000 €."),
    P("**Orden de actuación recomendado (antes de firmar nada):** 1) cita en la Oficina do Emprendedor de la Xunta (también en A Coruña); 2) servicio de emprendimiento del Ayuntamiento; 3) Secretaría Xeral da Emigración (por el retorno); 4) cita en IGAPE con los programas vigentes; 5) solicitar ayudas ANTES del alta de actividad y de firmar el alquiler. Documentación que se llevará: DNI/NIE, empadronamiento, plan de negocio (este documento), presupuestos de reforma/stock/equipamiento, certificado de emigrante retornado y vida laboral."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 13 · PREPARACIÓN DE APERTURA (CRONOGRAMA)
# ----------------------------------------------------------------------------

SECTION_18 = [
    S("18", "HOJA DE RUTA", "Los 12 pasos desde hoy hasta la apertura (4–7 meses)",
      "El plazo total depende del local y de la licencia, pero la secuencia es fija. La clave: **el pedido a China se hace en paralelo a la reforma**, porque es lo que más tarda (3–4 meses).",
      ess=["4–7 meses desde hoy hasta la apertura", "Pedido a China en paralelo a la reforma (es lo que más tarda)", "12 pasos secuenciados semana a semana", "Semanas 8–12: el momento crítico (pedido + obra)"]),

    TIMELINE([
        ("Semana 1–2", "Contactar oficinas de apoyo y ayudas", "Oficina do Emprendedor, Ayuntamiento y Secretaría Xeral da Emigración. Nada de firmar alquiler antes de saber qué ayudas existen."),
        ("Semana 2–6", "Empadronamiento, NIE y documentación", "Todo en regla, vida laboral, certificado de emigrante retornado."),
        ("Semana 2–8", "Búsqueda y visitas de locales", "Oleiros (Santa Cruz, Perillo, Bastiagueiro) según checklist de la sección 2. Cuadro de seguimiento con 12 criterios por local."),
        ("Semana 6–8", "Números definitivos con el local real", "Se sustituyen las cifras estimadas de este plan por alquiler y metros reales y se recalcula todo."),
        ("Semana 6–8", "Solicitud de ayudas", "Antes del alta de actividad. Este documento + presupuestos son la base de la solicitud."),
        ("Semana 8", "Negociar contrato y licencia", "Contrato con opción a obra, fianza de 2 meses; solicitud de licencia de apertura (obra menor, local < 50 m²)."),
        ("Semana 8–12", "Pedido a China (¡ya!) + reforma en paralelo", "Contactar agente/fábricas, muestras, pedido inicial ~6.000 € FOB. La producción y el marítimo ocupan 3–4 meses."),
        ("Semana 8–14", "Reforma del local", "Con mano de obra propia: pintura, suelo vinílico, iluminación, probador. Solo materiales: 1.900 €."),
        ("Semana 10–12", "Desarrollo de la web y redes", "WooCommerce, catálogo, perfiles sociales, ficha de Google Maps. Ella empieza el contenido."),
        ("Semana 12–16", "Montaje y recepción de mercancía", "Mobiliario, cámaras, TPV, implantación del stock, etiquetado y preparación."),
        ("Semana 14–16", "Campaña pre-apertura", "2 semanas de pauta local + evento del día de apertura (200 € de presupuesto)."),
        ("Semana 16+", "Apertura 🎉", "Y desde el día 1: novedades cada 3–4 semanas, medición semanal y disciplina de marketing."),
    ]),
    CALLOUT("warn", "El error que hay que evitar",
            "Esperar a tener el local para pedir la mercancía: el primer pedido tarda 3–4 meses desde la aprobación de muestras. El plan correcto es **local + reforma + pedido a China en paralelo**, y por eso el plazo total es de 4–7 meses y no de 8–10."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 14 · RIESGOS Y MITIGACIÓN
# ----------------------------------------------------------------------------

SECTION_19 = [
    S("19", "RIESGOS Y PLAN B", "Los 8 riesgos reales y cómo se gestionan",
      "Un plan de negocio honesto lista los riesgos antes de que ocurran y deja escrito el plan B para cada uno. Estos son los riesgos concretos de KHC y su mitigación.",
      ess=["8 riesgos identificados, cada uno con su mitigación", "Retrasos en China: el más probable → pedir con antelación", "Plan B (mes 6): si la caja baja de 3.500 €, 5 acciones claras", "El fondo de maniobra existe para decidir con calma"]),

    TABLE(
        ["Riesgo", "Impacto", "Mitigación"],
        [
            ["Retrasos en China (Año Nuevo Chino, Golden Week, producción)", "Alto — puede retrasar la apertura", "Pedidos con 3–4 meses de antelación; 2–3 fábricas/agente; refuerzos por avión en 7–10 días"],
            ["Ventas por debajo de lo previsto los primeros 6 meses", "Medio-alto", "Fondo de maniobra de 4.000 € (2,4 meses de gastos); sin sueldo inicial; stock reducido; plan B del mes 6: más pauta, menos reposición, promociones"],
            ["Stock muerto / tallas que no rotan", "Medio", "Pocas unidades por modelo; tallas medias cargadas; novedades cada 3–4 semanas; liquidación en rebajas de enero y julio"],
            ["Aranceles, aduanas y normativa UE (REACH, seguridad infantil)", "Medio", "Agente/despachante; certificaciones OEKO-TEX y especificaciones firmadas con la fábrica; inspección de calidad antes del envío"],
            ["Dependencia de un único proveedor", "Medio", "2–3 fábricas candidatas; muestras comparadas; Trade Assurance; stock de seguridad en los modelos básicos"],
            ["Local sin licencia o contrato desfavorable", "Alto", "Local con licencia comercial previa; revisión del contrato (100 €); cláusulas de obra y de salida"],
            ["Competencia o cambio de hábitos del consumidor", "Medio", "Marca propia y regalo (no precio); servicio y cercanía; canal online; diferenciación por calidad percibida"],
            ["Costes que se disparan (alquiler, suministros, cuotas)", "Medio", "Presupuesto con reserva mensual de 50 €; revisión anual del alquiler; eficiencia energética LED"],
        ],
        widths=[0.28, 0.16, 0.56], left_cols=[0],
    ),
    CALLOUT("info", "El plan B del mes 6 (se activa si la caja cae de 3.500 €)",
            "1) Congelar reposición de modelos que no venden y reforzar 3–4 modelos ganadores. 2) Subir la pauta local a 15 €/día durante 6 semanas y lanzar una promoción de temporada. 3) Revisar horarios (tardes y sábados = oro en tiendas de barrio). 4) Adelantar la apertura del canal online y las colaboraciones. 5) Si nada remonta en 60 días, negociar con el casero y replantear la ubicación. El fondo de maniobra existe para que este plan se ejecute con calma."),
]

# ----------------------------------------------------------------------------
# SECCIÓN 15 · ANEXOS
# ----------------------------------------------------------------------------

SECTION_21 = [
    S("21", "ANEXOS Y PRÓXIMOS PASOS", "Detalle completo, fuentes y lo que viene ahora",
      "Los anexos reproducen al detalle los CSV del repositorio (inversión, gastos y márgenes), para que cualquier cifra de este plan sea auditable y actualizable.",
      ess=["Todos los detalles y CSV reproducibles", "Anexos: inversión, márgenes por producto y fuentes", "Próximo paso: actualizar cifras cuando haya local", "Checklist de esta semana para arrancar"]),

    P("**Anexo A — Inversión por bloques** (la línea por línea completa está en la sección 06 y en `calculos/01_inversion_inicial.csv`):"),
    TABLE(
        ["Bloque", "Importe", "Partidas incluidas"],
        [
            ["Local", "2.250 €", "Fianza (2 meses) + primer mes de alquiler a 750 €"],
            ["Obra e imagen", "2.670 €", "Reforma a coste de materiales (1.900 €) + rótulo, vinilos, logo, etiquetas y bolsas (770 €)"],
            ["Mobiliario y equipamiento", "1.250 €", "Percheros, mostrador, estanterías, maniquíes, espejos (950 €) + TPV, cajón, etiquetadora, cámaras, extintor (300 €)"],
            ["Stock inicial completo", "8.690 €", "Ropa KHC (5.500) + bebé/regalo KHC (2.000) + marca España (530) + juguete (310) + complementos (350)"],
            ["Legal, web, marketing y suministros", "1.150 €", "Licencia y seguro (650) + dominio y hosting (120) + apertura (200) + altas de suministros (180)"],
            ["Reserva y fondo de maniobra", "5.000 €", "Imprevistos (1.000) + caja de los primeros meses (4.000)"],
            ["**INVERSIÓN TOTAL**", "**21.010 €**", "**Todas las partidas del desglose de la sección 06**"],
        ],
        widths=[0.24, 0.16, 0.60], left_cols=[0, 1], hl=[6],
    ),
    PAGEBREAK(),
    P("**Anexo B — Márgenes por producto (resumen del CSV):**"),
    TABLE(
        ["Producto", "Coste real", "PVP", "Margen", "Comentario"],
        [
            ["Body algodón peinado", "2,10–3,20 €", "9,90–15,90 €", "73–80 %", "El básico que más repite"],
            ["Body pack de 3", "5,30–7,60 €", "24,90–39,90 €", "69–75 %", "El pack sube el ticket"],
            ["Conjunto 2 piezas", "4,00–6,00 €", "19,90–32,90 €", "70–77 %", "El caballo de batalla"],
            ["Conjunto 3 piezas", "6,20–8,90 €", "29,90–48,90 €", "70–76 %", "Regalo estrella"],
            ["Mameluco/pelele", "3,20–4,90 €", "17,90–28,90 €", "73–78 %", "Muy vendido"],
            ["Camiseta manga corta", "2,50–4,10 €", "11,90–19,90 €", "72–79 %", "Volumen"],
            ["Sudadera capucha", "5,20–7,70 €", "21,90–34,90 €", "70–76 %", "Temporada media"],
            ["Vaquero/jogger", "3,70–8,40 €", "18,90–38,90 €", "69–78 %", "Depende del modelo"],
            ["Abrigo/plumífero", "10,10–15,50 €", "39,90–69,90 €", "68–75 %", "Mayor ticket invierno"],
            ["Pijama", "3,50–5,40 €", "14,90–24,90 €", "72–78 %", "Recurrencia"],
            ["Calcetines", "0,50–0,80 €", "3,50–7,50 €", "80–88 %", "Impulso puro"],
            ["Diadema/lazo", "0,30–1,10 €", "3,90–9,90 €", "82–90 %", "Máximo margen"],
            ["Set regalo KHC", "6,40–10,50 €", "29,90–54,90 €", "75–81 %", "Producto estrella"],
            ["Traje de comunión", "17,00–30,00 €", "69,90–139,90 €", "72–79 %", "Temporada abril–mayo"],
        ],
        widths=[0.24, 0.16, 0.16, 0.12, 0.32], left_cols=[0, 1, 2, 3],
    ),

    P("**Fuentes y herramientas del documento:**"),
    GRID([
        ("📄", "Documentos de partida", "docs/01 Plan de negocio (v1.3) · docs/02 Proveedores China · docs/03 Ayudas · docs/04 Locales · docs/05 Autónoma vs SL"),
        ("📊", "Cálculos auditables", "calculos/01_inversion_inicial.csv · calculos/02_gastos_fijos_mensuales.csv · calculos/03_margenes_y_costes_variables.csv"),
        ("⚙️", "Generación automática", "scripts/plan_data.py + scripts/build_plan.py → HTML interactivo y PDF imprimible"),
        ("⚠️", "Nota de responsabilidad", "Cifras orientativas basadas en datos de mercado de 2025–2026 y en los valores validados con los promotores. Verificar convocatorias, normativa y precios antes de cada decisión de inversión"),
    ]),

    P("**Próximos pasos inmediatos (esta semana):**"),
    CHECKBOXES([
        "Pedir cita en la **Oficina do Emprendedor** y en la **Secretaría Xeral da Emigración** (ayudas antes que nada)",
        "Definir el **logo y etiquetas KHC** en formato vectorial (lo necesitan las fábricas para las muestras)",
        "Empezar a listar **5–8 locales** en Oleiros con la plantilla de evaluación de la sección 2",
        "Contactar **2–3 agentes de compra** hispanohablantes o fábricas de Alibaba con Trade Assurance",
        "Confirmar **presupuesto disponible** (ahorros + posible ayuda/Financiación) y fecha objetivo de apertura",
        "Cuando haya local concreto: **actualizar este plan** con alquiler y metros reales (los cálculos se regeneran automáticamente)",
    ]),
]
