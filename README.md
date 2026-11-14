# Auto Sanación — Sistema Multiagente de Crecimiento en Amazon

Sistema orquestado para escalar las ventas de ***AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar*** de **Francis Jaramillo** en Amazon (Kindle, Tapa blanda y Audible).

## Arquitectura de Agentes
- **Orquestador Principal:** Coordina prioridades, consolida entregables y ejecuta ciclos semanales de optimización.
- **`amazon-seo-agent`:** Auditoría de ficha KDP, HTML de descripción, 7 casillas de keywords (máx. 50 bytes UTF-8), categorías y Contenido A+.
- **`amazon-ads-agent`:** Arquitectura de campañas Sponsored Products, archivos Bulk Operations CSV y limpieza automática de términos sin ventas.
- **`content-funnel-agent`:** Guiones de Reels/TikTok/Shorts, carruseles y secuencias de email con enlaces de Amazon Attribution.
- **`reviews-pr-agent`:** Flujo ético post-lectura para reseñas, kit de prensa y prospección de podcasts/medios.
- **`analytics-agent`:** Seguimiento semanal de unidades, páginas KENP, TACoS y registro de experimentos A/B.

## Herramientas Automatizadas (`scripts/`)
- `scripts/kdp_seo_optimizer.py`: Empaquetado y validación estricta en bytes UTF-8 de las 7 casillas KDP y validación del HTML de descripción (<= 4000 caracteres).
- `scripts/ads_analyzer.py`: Análisis de *Search Term Reports* (inglés/español), exportación automática de `bulk_negatives.csv` y generación de campañas Bulk iniciales.
- `scripts/kdp_sales_tracker.py`: Consolidación de regalías, unidades, KENP y TACoS a partir de reportes CSV de KDP.

## Cómo Ejecutar Pruebas y Scripts
```bash
# Ejecutar pruebas unitarias
python3 -m unittest discover -s tests -v

# Validar descripción y empaquetar 7 casillas de keywords KDP
python3 scripts/kdp_seo_optimizer.py --keywords-json outputs/ciclo_01/kdp_keywords_input.json --description-html outputs/ciclo_01/kdp_description.html

# Generar archivo Bulk inicial de Amazon Ads
python3 scripts/ads_analyzer.py --starter-spec-json outputs/ciclo_01/ads_starter_spec.json --out-dir outputs/ciclo_01/ads

# Analizar un Search Term Report semanal exportado de Amazon Ads
python3 scripts/ads_analyzer.py --search-terms-csv path/to/search_term_report.csv --target-acos 35 --out-dir outputs/semanal

# Consolidar ventas KDP + gasto Ads
python3 scripts/kdp_sales_tracker.py --kdp-csv path/to/kdp_royalties.csv --ad-spend 120.0 --out-md outputs/semanal/resumen_kdp.md
```
