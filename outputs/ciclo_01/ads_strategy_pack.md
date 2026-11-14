# Plan Ultra-Optimizado de Amazon Ads — Presupuesto Máximo $100 USD/mes

Diseñado específicamente para proteger un presupuesto acotado (**máximo $100 USD totales** / **$20–$30 USD por formato**) y maximizar ventas reales sin desperdiciar clics.

## 1. Regla de Oro para Micro-Presupuesto ($100 USD)
1. **No dividir demasiado los formatos:** Amazon Ads (Sponsored Products dentro de KDP) funciona para **Kindle** y **Tapa blanda** (Audible no se anuncia por Sponsored Products de KDP, sino que recibe tráfico cruzado desde la misma página del libro en Amazon).
   - **Recomendación:** Si quieres repartir **$20–$30 USD por formato**, concentra **$2.00/día en Tapa blanda** (mejor regalía por unidad) y **$1.00/día en Kindle** (o **$3.00/día** en un solo formato ganador = **$90 USD/mes**, por debajo de tu tope de $100).
2. **Pujas bajas ("Sniper Low-Bid"):** En vez de pagar $0.40–$0.60 por clic, pujamos entre **$0.13 y $0.22 USD**. Así **$100 USD compran ~450–700 clics reales** de personas buscando exactamente temas de autosanación en español.
3. **Cero campañas Broad abiertas al inicio:** La campaña `SP_Broad_Research_Paused` queda **pausada** por defecto para evitar clics curiosos que queman el presupuesto.

## 2. Estructura de Campañas en `starter_bulk_campaigns.csv` (27 filas)
| Campaña | Estado | Presupuesto/día | Puja | Objetivo |
| :--- | :--- | ---: | ---: | :--- |
| `SP_Exact_Sniper_100USD` | Activa | `$1.75` | `$0.14–$0.22` | 15 palabras clave **Exactas** de altísima intención de compra en español. |
| `SP_Auto_LowBid_Lottery` | Activa | `$1.25` | `$0.13` | Captura impresiones muy baratas en páginas de libros similares y búsquedas automáticas. |
| `SP_Broad_Research_Paused` | Pausada | `$1.00` | `$0.14–$0.15` | Solo activar cuando las 2 primeras ya estén dando ventas rentables. |

## 3. Pasos Antes de Subir (2 minutos)
1. Abre [starter_bulk_campaigns.csv](file:///Users/raymondvonblon/.gemini/antigravity/scratch/auto-sanacion-growth/outputs/ciclo_01/ads/starter_bulk_campaigns.csv) y reemplaza `REEMPLAZAR_CON_ASIN_REAL` por el **ASIN real** de Amazon (ej. `B0...`, el código que sale en la URL normal de compra `amazon.com/dp/B0...`).
2. En **Amazon Advertising → Portfolios**, crea un portafolio llamado `Auto Sanacion` y ponle **Budget Cap = $100.00 USD** (límite duro de gasto mensual).
3. Sube el archivo en **Sponsored Ads → Bulk Operations**.

## 4. Regla Semanal de Corte Rápido (Cada Lunes)
Con $100 USD no podemos esperar 15 clics sin venta. Ejecuta:
```bash
python3 scripts/ads_analyzer.py --search-terms-csv reporte.csv --target-acos 30 --min-bleeder-clicks 6 --max-bleeder-spend 2.50 --out-dir outputs/semanal
```
Esto bloquea automáticamente cualquier término que alcance **6 clics o $2.50 USD sin ventas** y te entrega el archivo `bulk_negatives.csv` listo para subir.
