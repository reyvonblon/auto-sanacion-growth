# Sistema de Seguimiento Semanal de KPIs y Analítica — *Auto Sanación*

**Libro:** *AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar*  
**Autora:** Francis Jaramillo (`ISBN-13 Paperback: 979-8403609579`)  
**Marketplaces prioritarios:** `Amazon.com (US Hispanic)`, `Amazon.es`, `Amazon.com.mx`  
**Parámetros de referencia (`config/book_profile.json`):**
- **ACoS objetivo:** `35.0%`
- **ACoS de equilibrio (break-even):** `55.0%`
- **Presupuesto diario base de Ads:** `$15.00 USD/día` (`$105.00 USD/semana` de referencia)
- **ASINs registrados:** Kindle `PENDIENTE_COMPLETAR` | Paperback `PENDIENTE_COMPLETAR` | Audible `PENDIENTE_COMPLETAR`
- **Estado KDP Select / A+ / Author Central:** `null` (verificar antes del Ciclo 01 para habilitar lectura KENP y módulos A+)

---

## 1. Metodología Semanal de Seguimiento

El ciclo analítico corre de **lunes a domingo** (corte semanal los **lunes por la mañana**, consolidando los 7 días previos cerrados: lunes–domingo) para alinear la limpieza de pujas en Amazon Ads con la lectura orgánica y de ventas en KDP.

### Cadencia Operativa
| Día | Responsable | Acción Analítica Clave | Entregable / Salida |
| :--- | :--- | :--- | :--- |
| **Lunes** | `analytics-agent` / Operador | Exportar CSVs de KDP (7 días cerrados) y Search Term Report de Amazon Ads; ejecutar `ads_analyzer.py` y `kdp_sales_tracker.py`. | `ads_analysis_report.md`, `bulk_negatives.csv`, `resumen_kdp.md` |
| **Martes** | `amazon-ads-agent` | Subir `bulk_negatives.csv` en Bulk Operations de Amazon Ads; promover términos ganadores (`Scale`) a `SP_Exact_Core`. | Campañas depuradas |
| **Miércoles–Viernes** | `content-funnel-agent` | Registrar clics y ventas atribuidas en panel de **Amazon Attribution** por cada pieza de video corto o email publicado. | Registro de atribución externa |
| **Domingo** | `analytics-agent` | Capturar snapshot semanal de **BSR** (Kindle, Paperback, Audible), conteo de reseñas/rating, unidades Audible (ACX) y actualizar la bitácora `experimentos_ab.csv`. | Tablero semanal actualizado y decisión A/B |

### Reglas de Rigor de Datos
1. **Cero datos inventados:** Toda celda sin lectura confirmada debe permanecer como `PENDIENTE_OBSERVAR` o `N/A`.
2. **Separación de ventanas:** Amazon Ads atribuye ventas a 7 o 14 días desde el clic; KDP registra regalías cuando el pedido se factura/envía (Paperback puede desfasarse 24–72 h). Comparar tendencias móviles de **14 y 28 días** además del corte semanal.
3. **Control por formato y tienda:** Registrar por separado **Kindle**, **Tapa blanda (Paperback)**, **KENP (Kindle Unlimited)** y **Audible**, y vigilar la mezcla de monedas (`USD`, `EUR`, `MXN`) al leer totales agregados de `kdp_sales_tracker.py`.

---

## 2. Plantilla de Tablero Semanal de KPIs

> **Nota:** Completar cada lunes/domingo con cifras reales exportadas. No estimar ni interpolar valores faltantes.

| Categoría | KPI | Semana 0 (Línea Base) | Semana 1 | Semana 2 | Semana 3 | Semana 4 | Semana 5 | Semana 6 | Meta / Referencia |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Ranking** | BSR Tienda Principal (`Amazon.com` Kindle) | `PENDIENTE_OBSERVAR` | | | | | | | Tendencia descendente sostenida |
| **Ranking** | BSR Tienda Principal (`Amazon.com` Paperback) | `PENDIENTE_OBSERVAR` | | | | | | | Tendencia descendente sostenida |
| **Ranking** | BSR `Amazon.es` / `Amazon.com.mx` | `PENDIENTE_OBSERVAR` | | | | | | | Top 20 en subcategoría nicho |
| **Ventas** | Unidades netas Kindle | `PENDIENTE_OBSERVAR` | | | | | | | Crecimiento WoW >= 10% |
| **Ventas** | Unidades netas Paperback | `PENDIENTE_OBSERVAR` | | | | | | | Sostener margen unitario |
| **KU** | Páginas leídas KENP (si `kdp_select_enrolled=true`) | `PENDIENTE_OBSERVAR` | | | | | | | N/A si no está en KDP Select |
| **Audio** | Unidades Audible (ACX / Audible) | `PENDIENTE_OBSERVAR` | | | | | | | Seguimiento mensual/semanal ACX |
| **Ingresos** | Regalías brutas totales KDP (`total_royalty`) | `PENDIENTE_OBSERVAR` | | | | | | | Superar gasto semanal de Ads |
| **Ads PPC** | Impresiones Ads | `PENDIENTE_OBSERVAR` | | | | | | | Suficiente volumen para testear CTR |
| **Ads PPC** | Clics Ads | `PENDIENTE_OBSERVAR` | | | | | | | Mín. 100 clics/sem para significancia |
| **Ads PPC** | CTR (`clicks / impressions * 100`) | `PENDIENTE_OBSERVAR` | | | | | | | >= 0.40% (ideal >= 0.60%) |
| **Ads PPC** | CPC promedio (`spend / clicks`) | `PENDIENTE_OBSERVAR` | | | | | | | <= $0.35 USD |
| **Ads PPC** | CVR (`orders / clicks * 100`) | `PENDIENTE_OBSERVAR` | | | | | | | >= 8.0% – 10.0% en búsqueda exacta |
| **Ads PPC** | Gasto total Ads (`ad_spend`) | `PENDIENTE_OBSERVAR` | | | | | | | Ref. `$105.00 USD/sem` (`$15/día`) |
| **Ads PPC** | Ventas atribuidas Ads (`sales`) | `PENDIENTE_OBSERVAR` | | | | | | | Creciente con ACoS controlado |
| **Rentabilidad** | ACoS (`spend / sales * 100`) | `PENDIENTE_OBSERVAR` | | | | | | | **<= 35.0%** (Break-even: **55.0%**) |
| **Rentabilidad** | TACoS sobre Regalías (`ad_spend / total_royalty * 100`) | `PENDIENTE_OBSERVAR` | | | | | | | **<= 25.0% – 30.0%** en fase de escala |
| **Rentabilidad** | Utilidad neta después de Ads (`total_royalty - ad_spend`) | `PENDIENTE_OBSERVAR` | | | | | | | > $0.00 tras fase de lanzamiento |
| **Prueba Social** | Reseñas totales / Calificación promedio | `PENDIENTE_OBSERVAR` | | | | | | | >= 4.5 estrellas |

---

## 3. Diccionario de Métricas

| Métrica | Definición y Fórmula Exacta | Fuente de Datos | Umbrales / Regla de Decisión |
| :--- | :--- | :--- | :--- |
| **BSR (Best Sellers Rank)** | Posición relativa de ventas por hora/día dentro de una tienda y formato específico (`Kindle`, `Paperback`, `Audible`). Menor número = mayor volumen de ventas recientes. | Página del producto en Amazon (`Amazon.com`, `Amazon.es`, `Amazon.com.mx`). | Observar tendencia de 7 días (evitar sobre-reaccionar a picos de 1 hora). Si sube de golpe tras pausar Ads, revisar caída de velocidad de ventas. |
| **Unidades Kindle / Paperback** | Unidades netas vendidas (brutas menos devoluciones/cancelaciones) por formato y marketplace. | Reporte CSV de KDP (`Net Units Sold` / `Unidades netas vendidas`). | Desglosar por formato para validar elasticidad de precio y qué formato responde mejor a cada campaña. |
| **KENP (Kindle Edition Normalized Pages)** | Páginas normalizadas leídas por suscriptores de Kindle Unlimited. Aplica **únicamente** si `kdp_select_enrolled` es `true`. | Reporte CSV de KDP (`KENP Read` / `Páginas leídas de KENP`). | El ingreso estimado depende de la tarifa mensual del fondo KDP Select. Sumar al total de regalías en el reporte de KDP. |
| **Audible (Unidades / Regalías Audio)** | Copias vendidas (compra directa, crédito de membresía o Whispersync) del audiolibro. | Panel **ACX** / **Audible** (no aparece en el CSV estándar de regalías KDP). | Registrar manualmente cada semana en el tablero; no mezclar en el CSV que lee `kdp_sales_tracker.py`. |
| **CTR (Click-Through Rate)** | $\text{CTR (\%)} = \frac{\text{Clics}}{\text{Impresiones}} \times 100$. Calculado por `ads_analyzer.py` (`ctr_percent`). | Search Term Report CSV de Amazon Ads. | `< 0.25%`: portada, título/subtítulo o segmentación poco relevante. `>= 0.50%`: alta relevancia de anuncio frente al término. |
| **CVR (Conversion Rate en Ads)** | $\text{CVR (\%)} = \frac{\text{Pedidos atribuidos}}{\text{Clics}} \times 100$. Calculado por `ads_analyzer.py` (`cvr_percent`). | Search Term Report CSV de Amazon Ads (`7 Day Total Orders (#)` / `Clicks`). | `< 5%`: fricción en ficha (descripción HTML, Contenido A+, precio o pocas reseñas) antes de escalar pujas. `>= 10%`: ficha sana lista para escalar. |
| **ACoS (Advertising Cost of Sales)** | $\text{ACoS (\%)} = \frac{\text{Gasto Ads}}{\text{Ventas atribuidas por Ads}} \times 100$. Calculado por `ads_analyzer.py` (`acos_percent`). | Search Term Report CSV de Amazon Ads. | **<= 35.0%** (`target_acos_percent`): escalar puja/presupuesto. **35.1% – 55.0%**: optimizar pujas. **> 55.0%** (`break_even_acos_percent`): reducir puja o negativizar si persiste sin ventas. |
| **TACoS (Total Advertising Cost of Sales)** | En este proyecto (`scripts/kdp_sales_tracker.py`), se mide sobre **regalías totales brutas**: $\text{TACoS (\%)} = \frac{\text{ad\_spend}}{\text{total\_royalty}} \times 100$ (`tacos_on_royalty_percent`). | Cruce entre `ad_spend` (Amazon Ads) y `total_royalty` (CSV de KDP). | **<= 35%**: Ads impulsan crecimiento orgánico sano. **> 55%**: el gasto publicitario excede la rentabilidad de regalías; auditar términos `bleeder` y conversión de ficha. |
| **Utilidad Neta post-Ads** | $\text{Net Profit} = \text{total\_royalty} - \text{ad\_spend}$ (`net_profit_after_ads` en `kdp_sales_tracker.py`). | Salida de `scripts/kdp_sales_tracker.py`. | Debe mantenerse positiva después de la fase inicial de prueba de palabras clave (semanas 1–3). |

---

## 4. Flujo Paso a Paso: Exportación de CSVs y Ejecución de Scripts

### Paso 1 — Exportar el Reporte de Ventas y Regalías desde KDP
1. Ingresar a **KDP (kdp.amazon.com)** → pestaña **Informes (Reports)** → **Regalías de meses anteriores / Estimador de regalías (Royalties Estimator)** o **Pedidos (Orders)**.
2. Seleccionar el rango exacto de **7 días cerrados** (lunes a domingo de la semana evaluada) y filtrar por el título *AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar* (o verificar todos los formatos: Kindle y Tapa blanda).
3. Hacer clic en **Descargar informe (.csv)** y guardarlo en una ruta ordenada, por ejemplo:
   `data/semanal/semana_01/kdp_royalties.csv`
4. **Columnas compatibles con `scripts/kdp_sales_tracker.py`:** el script detecta automáticamente encabezados en inglés o español:
   - `Title` / `Título`
   - `Marketplace` / `Tienda`
   - `Transaction Type` / `Tipo de transacción` / `Format` / `Formato`
   - `Net Units Sold` / `Units Sold` / `Unidades netas vendidas` / `Unidades vendidas`
   - `KENP Read` / `Páginas leídas de KENP`
   - `Royalty` / `Regalías` / `Estimated Earnings` / `Ganancias estimadas`
   - `Currency` / `Moneda`

> [!WARNING]
> **Control de monedas múltiples:** `kdp_sales_tracker.py` suma numéricamente la columna `Royalty` sin conversión cambiaria. Si el CSV mezcla `USD` (`Amazon.com`), `EUR` (`Amazon.es`) y `MXN` (`Amazon.com.mx`), revisar primero el desglose por tienda o exportar/filtrar reportes por moneda homogénea antes de calcular el TACoS global.

---

### Paso 2 — Exportar el *Search Term Report* desde Amazon Ads
1. Ingresar a **Amazon Ads Console** (para cada marketplace activo: `.com`, `.es`, `.com.mx`) → **Medición e informes (Measurement & Reporting)** → **Informes de productos patrocinados (Sponsored Products Reports)**.
2. Crear/descargar un informe con esta configuración:
   - **Tipo de informe:** *Término de búsqueda (Search term)*
   - **Unidad de tiempo:** *Resumen (Summary)*
   - **Periodo:** mismos 7 días cerrados (o ventana móvil de 14 días para detectar términos sin ventas con mayor muestra).
   - **Formato:** `.csv` (si Amazon Ads descarga `.xlsx`, abrir y guardar como **CSV UTF-8**).
3. Guardar el archivo en:
   `data/semanal/semana_01/search_term_report.csv`
4. **Columnas compatibles con `scripts/ads_analyzer.py`:** soporta encabezados en inglés o español (`Campaign Name` / `Nombre de la campaña`, `Ad Group Name`, `Match Type`, `Customer Search Term` / `Término de búsqueda del cliente`, `Impressions`, `Clicks`, `Spend` / `Gasto`, `7 Day Total Sales` / `14 Day Total Sales` / `Ventas totales de 7 días`, `7 Day Total Orders (#)` / `Pedidos totales de 7 días (#)`).

---

### Paso 3 — Procesar Amazon Ads con `scripts/ads_analyzer.py`
Ejecutar desde la raíz del proyecto (`/Users/raymondvonblon/.gemini/antigravity/scratch/auto-sanacion-growth`):

```bash
python3 scripts/ads_analyzer.py \
  --search-terms-csv data/semanal/semana_01/search_term_report.csv \
  --target-acos 35 \
  --min-bleeder-clicks 8 \
  --max-bleeder-spend 5.0 \
  --out-dir outputs/semanal/semana_01/ads
```

**Qué hace el script automáticamente:**
- Clasifica cada término de búsqueda en:
  - **Scale:** `orders >= 2` y `ACoS <= 35.0%` (candidatos a promover a `SP_Exact_Core`).
  - **Optimize:** `orders >= 1` con ACoS mayor al objetivo (ajustar puja).
  - **Negative Exact (bleeders):** `orders == 0` y (`clicks >= 8` o `spend >= $5.00`).
  - **Watch:** resto de términos con poca data.
- Genera dos archivos en `--out-dir`:
  1. `outputs/semanal/semana_01/ads/ads_analysis_report.md` (resumen con CTR, CPC, CVR, ACoS, gasto desperdiciado y tablas accionables).
  2. `outputs/semanal/semana_01/ads/bulk_negatives.csv` (listo para subir a Amazon Ads → *Bulk Operations* con `negativeExact` o `Negative Product Targeting` por ASIN).
- Imprime en consola un JSON con `summary.spend` (gasto total de Ads del periodo).

---

### Paso 4 — Cruzar Ventas KDP + Gasto Ads con `scripts/kdp_sales_tracker.py`
Tomar el valor exacto de `summary.spend` devuelto en el Paso 3 (por ejemplo, si fue `105.00`) y pasarlo al argumento `--ad-spend`:

```bash
python3 scripts/kdp_sales_tracker.py \
  --kdp-csv data/semanal/semana_01/kdp_royalties.csv \
  --ad-spend 105.00 \
  --out-md outputs/semanal/semana_01/resumen_kdp.md
```

**Qué produce:**
- Genera `outputs/semanal/semana_01/resumen_kdp.md` con:
  - **Unidades netas vendidas** (`total_units`)
  - **Páginas leídas KENP** (`total_kenp`)
  - **Regalías totales brutas** (`total_royalty`)
  - **Inversión en Amazon Ads** (`ad_spend`)
  - **TACoS sobre Regalías** (`tacos_on_royalty_percent`)
  - **Utilidad neta después de Ads** (`net_profit_after_ads`)
  - **Tabla de desglose por Tienda (Marketplace)** (`by_marketplace`).

---

### Paso 5 — Consolidación Manual Complementaria y Cierre Semanal
1. **BSR y Reseñas:** Anotar manualmente en el tablero el BSR de cada formato/tienda y el número total de reseñas + calificación promedio.
2. **Audible (ACX):** Consultar el panel de ACX y registrar las unidades de audiolibro de la semana.
3. **Amazon Attribution:** Si se publicaron Reels/TikToks/Shorts o correos con etiquetas de atribución (`amazon_attribution_tags` en `config/book_profile.json`), registrar clics, vistas de página de detalle (DPV), carritos (ATC) y compras atribuidas.
4. **Bitácora A/B (`outputs/ciclo_01/experimentos_ab.csv`):** Actualizar el estado, resultado observado y decisión (`Escalar`, `Iterar`, `Descartar`) del experimento activo de la semana.

---

### Verificación Técnica de los Scripts
Antes o después de modificar los scripts del proyecto, validar la suite de pruebas unitarias:

```bash
python3 -m unittest discover -s tests -v
```
