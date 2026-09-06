# KHC — Tienda de Ropa Infantil (0-12 años)

Plan de negocio real para abrir **KHC**, tienda de ropa infantil con marca propia en **Oleiros (A Coruña, Galicia)**:
- Tienda física en barrio residencial de Oleiros, cerca de casa
- Fabricación directa en China con marca KHC, calidad media-alta
- **Estrategia de stock reducido y rotación rápida** (poco stock por modelo, novedades cada 3-4 semanas)
- Tienda online construida por nosotros
- Marketing continuo desde el día 1
- Empieza como autónoma; paso a SL cuando el volumen lo justifique

## Ventajas diferenciales
1. ✅ Reformas con mano de obra propia (solo pagamos materiales)
2. ✅ Fabricación directa China → márgenes ~70%
3. ✅ Web desarrollada internamente, sin coste de desarrollo
4. ✅ Alquiler contenido en Oleiros (750€/mes aprox)
5. ✅ Ingresos de reformas cubren lo personal los primeros meses (ella no necesita cobrar sueldo al principio)
6. ✅ Empieza con poco stock para rotar rápido y no quedarse con mercancía

## Números clave (escenario real KHC en Oleiros)

| Indicador | Valor |
|-----------|-------|
| **Inversión total para abrir** | **≈ 21.000 € (21.010 €)** |
| De los que: stock inicial completo | 8.690 € (~1.400 unidades) |
| De los que: fondo de maniobra (caja para primeros meses) | 4.000 € |
| Gastos fijos mensuales (marketing incluido) | **1.670 €/mes (≈ 1.700 €)** |
| Margen bruto medio marca propia China | ~70% |
| Ventas diarias para no perder dinero | ~92 €/día (2.390 €/mes) |
| Ventas para sueldo de ~1.000€/mes | ~158 €/día (≈ 4.100 €/mes) |
| Ventas para sueldo de ~2.000€/mes | ~224 €/día (≈ 5.800 €/mes) |
| Marketing mensual | 340 €/mes |
| Coste web | ~10 €/mes (dominio+hosting; desarrollo propio) |
| Tiempo hasta apertura | 3-4 meses después de tener local (contar plazo de fabricación+envío de 3 meses) |

## Documentos

**Versión premium (recomendada):**
- 🎨 `docs/KHC_Plan_Negocio_Premium.html` — Plan visual interactivo (abre en el navegador; incluye botón «Imprimir / Guardar PDF»)
- 🖨 `docs/KHC_Plan_Negocio_Premium.pdf` — Versión imprimible premium A4 (45 páginas, índice automático)

**El plan incluye el análisis completo (22 secciones, 36 subsecciones):**
- **Bloque económico-financiero:** proyección de ingresos mes a mes con estacionalidad real,
  cuenta de resultados prevista a 5 años (EBITDA, amortización, impuestos, retribución de la
  promotora), rentabilidad de la inversión (VAN +36.920 € · TIR 42 % · payback 2,6 años),
  plan de tesorería, estructura de financiación y análisis de sensibilidad con 8 escenarios.
- **Análisis estratégico:** mercado y demanda del entorno, análisis de competencia, DAFO,
  plan estratégico con objetivos medibles a 12/24/36 meses y cuadro de mando con 10 KPIs.
- **Para ayudas:** equipo y previsión de empleo, sostenibilidad/igualdad/innovación y ficha
  resumen de 1 página para convocatorias (IGAPE, Consellería, Emigración, Kit Digital).

**Leer primero (fuente en Markdown):** 📄 `docs/01_Plan_Negocio_KHC.md` — Plan completo con números ajustados

**Regenerar las versiones premium (opcional, requiere Python 3.11):**
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_plan.py   # regenera HTML + PDF
```

- 📄 `docs/02_Proveedores_Ropa_Infantil.md` — Fabricación en China, agentes, MOQ, plazos, normativa UE
- 📄 `docs/03_Ayudas_Subvenciones.md` — Ayudas emigrantes retornados, tarifa plana, cuota cero Galicia
- 📄 `docs/04_Locales_A_Corunya.md` — Zonas recomendadas (incluida Oleiros) y plantilla de seguimiento
- 📄 `docs/05_Autonoma_vs_SL.md` — Comparativa real y recomendación para KHC

Cálculos (CSV para Excel/Sheets):
- 📊 `calculos/01_inversion_inicial.csv`
- 📊 `calculos/02_gastos_fijos_mensuales.csv`
- 📊 `calculos/03_margenes_y_costes_variables.csv`
